import datetime
import logging
import requests
import asyncio
import os
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from functools import partial
from discord import (
    Embed,
    Intents,
    Member,
    User,
    ApplicationContext,
    Guild,
    Role,
    InteractionResponded,
    Option,
    Bot,
    File,
)
from discord.ext import tasks
from request import lessons_tp
from utils import (
    notification_parameter_change,
    get_notified_users,
    schedule_task,
    add_homework_for_tp,
    homework_for_tp,
    del_homework_for_tp,
    homework_auto_remove,
)
from constants import (
    TP_DISCORD_TO_SCHEDULE,
    DATASOURCES,
    IUTSERVID,
    ZINCEID,
    NOTIFICATION_JSON_KEYS,
    HOMEWORKSOURCES,
    TP_SCHEDULE_TO_DISCORD,
    TARGETED_HOUR_NOTIF_LESSONS,
    TARGETED_HOUR_NOTIF_HOMEWORKS,
    TP_SCHEDULE,
    HELP,
    ADMIN_LIST,
    IMPORTANT_FILES,
)
from homework import Homework
from lesson import Lesson
from _token import TOKEN

intents = Intents.default()
bot: Bot = Bot(intents=intents)


@bot.event
async def on_ready():
    """Actions effectuées à la connexion du bot"""
    if not bot.user:
        raise InterruptedError("The bot didn't connect")

    logger_main.info(
        "Logged in as %s (%s)", bot.user.name, bot.user.id
    )  # Confirmation de la connexion

    asyncio.create_task(wait_for_auto_start_notif_lessons())
    asyncio.create_task(wait_for_auto_start_notif_homeworks())
    asyncio.create_task(ical_updates.start())


@tasks.loop(hours=24)
async def plan_notif_for_tp():
    """Pour chaque groupe TP enregistré, créer une liste des notifications de cours à envoyer et programme leur envoit à l'heure adéquate"""
    logger_main.info("called")
    all_lesson: list[Lesson] = []
    for t_p in TP_SCHEDULE_TO_DISCORD.keys():
        all_lesson.extend(lessons_tp(t_p=t_p, logger_main=logger_main))
        await asyncio.sleep(1)

    all_lesson = Lesson.sorting_schedule(all_lesson)
    while all_lesson != []:
        lesson = all_lesson.pop(0)
        logger_main.debug("lesson = %s", lesson)
        asyncio.create_task(
            plan_notification(t_p=TP_SCHEDULE_TO_DISCORD[lesson.t_p], lesson=lesson)
        )


@tasks.loop(hours=24)
async def homeworks_notif():
    """Envoyer une notification de devoirs pour chaque utilisateur qui active les notifications
    et supprimer les devoirs dépassés"""
    logger_main.info("called")
    homework_auto_remove(logger_main=logger_main)
    homework_dict: dict = {}
    for t_p in TP_DISCORD_TO_SCHEDULE.keys():
        homeworks = homework_for_tp(
            t_p=TP_DISCORD_TO_SCHEDULE[t_p], logger_main=logger_main
        )
        homeworks = Homework.remembers_compare(homeworks)
        if homeworks != []:
            homework_dict[t_p] = Homework.embed_homework_construct(
                title="Notification automatique des devoirs",
                color=0x00FF00,
                homeworks=homeworks,
                description=f"Devoirs pour {TP_DISCORD_TO_SCHEDULE[t_p]}",
                sign=True,
                sorting=True,
            )

    for t_p in homework_dict.keys():
        users_list = await get_user_list_from_tp(notify="homeworks", t_p=t_p)
        await send_notification(user_list=users_list, embed=homework_dict[t_p])


@tasks.loop(hours=1)
async def ical_updates():
    """Mise à jour automatique des emplois du temps"""
    counter = 0
    for tp in TP_SCHEDULE.keys():
        try:
            response = requests.get(TP_SCHEDULE[tp], verify=False, timeout=1)
            if response.status_code == 200:
                if not os.path.exists(f"Calendars/{tp}"):
                    os.makedirs(f"Calendars/{tp}")
                with open(f"Calendars/{tp}/{tp}", "wb") as file:
                    file.write(response.content)
                logger_main.info(f"Schedule update for {tp}")
                counter += 1
            else:
                logger_main.critical(
                    f"response.status_code = {response.status_code}, tp = {tp}"
                )
        except Exception as e:
            logger_main.critical(f"erreur : {e}, tp={tp}")
        await asyncio.sleep(3)  # Laisser le temps au bot de répondre aux requêtes
    logger_main.info(f"ended : {counter}/{len(TP_SCHEDULE.keys())} icals updated")


async def get_roles_list_from_user(user: User) -> list[Role]:
    """Renvoie la liste des rôles de l'utilisateur

    Args:
        user (Utilisateur): utilisateur

    Retourne:
        list[Role]: Liste des rôles de l'utilisateur
    """

    logger_main.info(f"Called | args : {user}")
    guild: Guild = bot.get_guild(IUTSERVID)
    if guild:
        logging.debug("user_ = %s", user)
        member: Member = await guild.fetch_member(user.id)
        logging.debug("member = %s", member)
        roles = member.roles
        logging.debug("roles = %s", roles)
        return roles
    else:
        logger_main.critical("No guild found")


@bot.command(description="Demandez votre emploi du temps")
async def schedule(
    ctx: ApplicationContext,
    t_p: Option(str, description="TP group") = "",
    day: Option(int, description="Schedule for which day") = 0,
):
    """Commande pour récupérer et envoyer l'emploi du temps d'un groupe TP spécifique.
        Si l'heure est > 19, récupérer et envoyer l'emploi du temps du lendemain.

    Args:
        ctx (ApplicationContext): Le contexte de l'application.
        t_p (str): Le groupe TP pour lequel récupérer l'emploi du temps.
    """

    logger_main.info(f"called by : {ctx.author.id} | args : {t_p}, {day}")
    member: User | Member = ctx.author
    logging.debug("User value : %s", member)

    if t_p == "":
        if isinstance(member, User):
            logging.debug("User wrong type")
            roles_list: list[Role] = await get_roles_list_from_user(member)
        else:
            logging.debug("User is member")
            roles_list: list[Role] = member.roles
            logging.debug(f"Roles: {roles_list}")

        for role in roles_list:
            logging.debug(f"role: {role.name}")
            if role.name in TP_DISCORD_TO_SCHEDULE.keys():
                logging.debug("tp found")
                t_p = TP_DISCORD_TO_SCHEDULE[role.name]
                break

        if t_p == "":
            await ctx.interaction.response.send_message(
                "Vous n'avez aucun rôle TP", ephemeral=True
            )
            return

    if t_p.upper() in TP_DISCORD_TO_SCHEDULE.values():
        logging.debug("tp value : %s", t_p)
        date: datetime.datetime = datetime.datetime.now()
        logging.debug("date = %s", date)
        if date.hour >= 16:
            tomorrow: bool = True
            date += datetime.timedelta(days=1)
        else:
            tomorrow: bool = False
        await ctx.interaction.response.send_message(
            "Done!", ephemeral=True
        )
        date += datetime.timedelta(days=day)
        _schedule: list = Lesson.sorting_schedule(
            lessons_tp(t_p, tomorrow=tomorrow, logger_main=logger_main, day=day)
        )
        logging.debug("schedule value : %s", _schedule)

        embed = Lesson.embed_schedule_construct(
            title=f"Emploi du temps du {date.day}/{date.month}/{date.year}",
            description=f"{t_p}",
            color=0xFF0000,  # red
            schedule=_schedule,
            sign=True,
        )
        await send_notification(user_list=[member], embed=embed)
    else:
        logging.debug("TP not found")
        message: str = "Les arguments attendus sont :"
        for element in TP_DISCORD_TO_SCHEDULE.values():
            message += element + ", "
        message = message[:-2]  # Last 2 caracters suppression
        await ctx.interaction.response.send_message(
            message, ephemeral=True
        )  # Responding if bad argument


@bot.command(description="Besoin d'aide ?")
async def iutime(ctx: ApplicationContext):
    """Equivalent du /help"""
    await ctx.interaction.response.send_message(HELP, ephemeral=True)


@bot.command(description="""Activer/Désactiver les notifications pour les devoirs ou les leçons""")
async def notif(
    ctx: ApplicationContext,
    notification_homeworks: Option(
        bool, description="Activer/Désactiver les notifications pour les devoirs"
    ),
    notification_lessons: Option(
        bool, description="Activer/Désactiver les notifications pour les cours"
    ),
):
    """Permet aux utilisateurs de modifier leurs paramètres de notification

    Args:
        ctx (ApplicationContext): Récupération des utilisateurs Discord
        notification_homeworks (bool): Modifier le paramètre de notification des devoirs
        notification_lessons (bool): Modifier le paramètre de notification des leçons
    """

    logger_main.info(
        f"called by : {ctx.author.id} | args : {notification_homeworks}, {notification_lessons}"
    )
    author_id: str = str(ctx.author.id)
    notification_parameter_change(
        user_id=author_id,
        parameter=notification_lessons,
        notification="next_lessons",
        path=DATASOURCES,
        logger_main=logger_main,
    )
    notification_parameter_change(
        user_id=author_id,
        parameter=notification_homeworks,
        notification="homeworks",
        path=DATASOURCES,
        logger_main=logger_main,
    )
    await ctx.interaction.response.send_message("Done!", ephemeral=True)


@bot.command(description="Demander les devoirs enregistrer pour votre TP")
async def homework(ctx: ApplicationContext):
    """Commande pour récupérer et envoyer les devoirs à l'utilisateur.

    Args:
        ctx (ApplicationContext): Le contexte de l'application.
    """

    logger_main.info(f"called by : {ctx.author.id}")

    user: User | Member = ctx.author
    if isinstance(user, User):
        roles: list[Role] = await get_roles_list_from_user(user=user)
    else:
        roles: list[Role] = user.roles

    homeworks: list = None
    logging.debug("User value : %s", user)

    for role in roles:
        logging.debug("role value : %s", role)
        if role.name in TP_DISCORD_TO_SCHEDULE.keys():
            logging.debug("role.name value : %s", role.name)
            homeworks: list[Homework] = homework_for_tp(
                TP_DISCORD_TO_SCHEDULE[role.name],
                path=HOMEWORKSOURCES,
                logger_main=logger_main,
            )
            logging.debug("homeworks_temp value : %s", homeworks)
            logging.debug(
                "homeworks_temp's elem type : %s",
                {type(homeworks[0]) if homeworks else "homeworks_temp is empty"},
            )
            # Sending homeworks or another message if not homeworks
            if homeworks:
                homeworks = Homework.sorting_homeworks(homeworks)
                embed: Embed = Homework.embed_homework_construct(
                    title=role.name,
                    color=0x00FF00,
                    homeworks=homeworks,
                    description="Devoirs",
                )
                await send_notification(user_list=[user], embed=embed)
                await ctx.interaction.response.send_message("Done!", ephemeral=True)
            else:
                await send_notification(
                    user_list=[user], message="Pas de devoirs enregistrés pour votre TP"
                )
                await ctx.interaction.response.send_message("Done!", ephemeral=True)
            break

    # If user has not any TP group
    try:
        await ctx.interaction.response.send_message(
            "Vous n'étes assigné à aucun groupe TP", ephemeral=True
        )
    except InteractionResponded:
        pass

@bot.command(description="AJoutez un devoir pour votre TP")
async def add_homework(
    ctx: ApplicationContext,
    ressource: Option(str, description="Ressource du devoir"),
    prof: Option(str, description="Proffesseur ayant donné le devoir"),
    remember: Option(
        str,
        description="To be notified some days before the deadline : 'ONEDAY', 'THREEDAY', 'ONEWEEK', 'ALWAYS",
    ),
    date_rendue: Option(
        str, description="Date de rendu, format: 'AAAA-MM-DD-HH-MM', exemple '2023-07-03-02-40"
    ),
    description: Option(str, description="Description simple du devoir"),
    note: Option(bool, description="Ce devoir est-il noté ?") = False,
):
    """Commande pour ajouter un devoir au TP.

    Args:
        ctx (ApplicationContext): Le contexte de l'application.
        ressource (str): La ressource du devoir.
        prof (str): Le professeur du devoir.
        remember (str): L'importance/criticité du devoir.
        date_rendu (str): La date limite du devoir au format 'AAAA-MM-JJ-HH-MM'.
        description (str): La description du devoir.
        note (bool, facultatif): Indique si le devoir doit être noté. Par défaut, False.
    """

    logger_main.info(
        f"called by : {ctx.author.id} | args: {ressource}, {prof}, {remember}, {date_rendue}, {description}, {note}"
    )

    user: User | Member = ctx.author
    if isinstance(user, User):
        roles: list[Role] = await get_roles_list_from_user(user=user)
    else:
        roles: list[Role] = user.roles

    logging.debug(f"roles = {roles}")

    for role in roles:
        if role.name in TP_DISCORD_TO_SCHEDULE.keys() and (
            "délégué" in [role.name for role in roles]
            or "devoirs" in [role.name for role in roles]
        ):
            logging.debug("TP and role 'délégué' or 'devoirs' found")
            try:
                date_rendu_obj: datetime.datetime = datetime.datetime.strptime(
                    date_rendue, "%Y-%m-%d-%H-%M"
                )
            except ValueError:
                await ctx.interaction.response.send_message(
                    "Format de date invalide, utilisez le format 'YYYY-MM-DD-HH-MM'",
                    ephemeral=True,
                )
                return

            homework_ = Homework(
                ressource, prof, remember, date_rendu_obj, description, note
            )
            logging.debug("homework = %s", homework_)
            result: bool = add_homework_for_tp(
                homework=homework_,
                t_p=TP_DISCORD_TO_SCHEDULE[role.name],
                path=HOMEWORKSOURCES,
                logger_main=logger_main,
            )
            if result:
                await ctx.interaction.response.send_message(
                    "Devoir ajouté !", ephemeral=True
                )
                return
            else:
                # Never supposed to appear
                logger_main.critical(
                    f"Error in add_homework_for_tp function : {result}"
                )
                zince: User = await bot.fetch_user(ZINCEID)
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                await zince.send(
                    f"({date}) Error in add_homework function (main.py)\
for user {ctx.author}, tp = {role.name}, homework = {homework_}"
                )
                await ctx.interaction.response.send_message(
                    "An error happened, my creators have been notified", ephemeral=True
                )
            break
    logger_main.debug("TP or role 'délégué'|'devoirs' not found")
    await ctx.interaction.response.send_message(
        "Seul les délégués des TP ou les étudiants ayant le rôle 'devoirs' sont autorisés à modifier les devoirs enregistrés pour leur TP",
        ephemeral=True,
    )


@bot.command(description="Supprimez un devoirs enregistré pour votre TP")
async def del_homework(
    ctx: ApplicationContext,
    emplacement: Option(
        int,
        description="Placement de la liste des devoirs, départ à 1, laisser vide pour obtenir la liste des devoirs"
    ) = None,
):
    """Commande pour supprimer un devoir du TP.

    Args:
        ctx (ApplicationContext): Le contexte de l'application.
        emplacement (int, facultatif): L'emplacement du devoir à supprimer. Par défaut, None.
    """

    logger_main.info(f"called by : {ctx.author.id} | args: {emplacement}")

    user: User | Member = ctx.author
    if isinstance(user, User):
        roles: list[Role] = await get_roles_list_from_user(user=user)
    else:
        roles: list[Role] = user.roles

    logging.debug(f"roles = {roles}")

    for role in roles:
        if role.name in TP_DISCORD_TO_SCHEDULE.keys() and (
            "délégué" in [role.name for role in roles]
            or "devoirs" in [role.name for role in roles]
        ):
            # 0 = not
            if not emplacement:
                logging.debug("not placement")

                homeworks: list[Homework] = homework_for_tp(
                    t_p=TP_DISCORD_TO_SCHEDULE[role.name],
                    path=HOMEWORKSOURCES,
                    logger_main=logger_main,
                )
                logging.debug("homeworks = %s", homeworks)
                embed: Embed = Homework.embed_homework_construct(
                    title="Liste des devoirs enregistrés",
                    description=""""Utilisez la commande /del_homework en indiquant le numéro du devoir que vous souhaitez supprimer""",
                    color=0x00FF00,
                    homeworks=homeworks,
                    sorting=False,
                )
                await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                logging.debug("placement")
                result: int = del_homework_for_tp(
                    placement=emplacement - 1,
                    t_p=TP_DISCORD_TO_SCHEDULE[role.name],
                    path=HOMEWORKSOURCES,
                    logger_main=logger_main,
                )
                match result:
                    case 1:
                        await ctx.interaction.response.send_message(
                            "Done!", ephemeral=True
                        )
                    case 0:
                        logging.critical(
                            f"Error on del_homework_for_tp function : {result}"
                        )
                        # Never supposed to appear
                        zince: User = await bot.fetch_user(ZINCEID)
                        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        await zince.send(
                            f"({date}) Error in del_homework function (main.py) for\
user {ctx.author}, tp = {role.name}, placement = {emplacement}"
                        )
                        await ctx.interaction.response.send_message(
                            "An error happened, my creators have been notified",
                            ephemeral=True,
                        )
                    case 2:
                        await ctx.interaction.response.send_message(
                            "Seems like this homework doesn't exist", ephemeral=True
                        )
                break
    try:
        await ctx.interaction.response.send_message(
            "Seul les délégués des TP ou les étudiants ayant le rôle 'devoirs' sont autorisés à modifier les devoirs enregistrés pour leur TP",
            ephemeral=True,
        )
    except InteractionResponded:
        pass


async def plan_notification(t_p: str, lesson: Lesson) -> None:
    """Envoyer une notification 5 minutes avant la prochaine leçon

    Args:
        tp (str): code du groupe TP
        lesson (Leçon): objet leçon à envoyer
    """

    logger_main.info("Plan lesson for TP %s : %s", t_p, lesson)

    embed: Embed = Lesson.embed_schedule_construct(
        title="Prochain cours:",
        description=None,
        color=0x9370DB,
        schedule=[lesson],
        sign=True,
    )
    lesson_time: datetime.datetime = datetime.datetime.strptime(
        lesson.start_hour, "%H:%M"
    ).time()
    lesson_time: datetime.datetime = datetime.datetime.combine(
        datetime.date.today(), lesson_time
    )
    # if lesson_time < datetime.datetime.now() - datetime.timedelta(hours=0, minutes=20):
    #    logger_main.info("Lesson time to far in the past, %s", lesson_time)
    #    return

    notification_time: datetime.datetime = datetime.datetime.now()
    notification_time = notification_time.replace(
        hour=lesson_time.hour, minute=lesson_time.minute
    )
    # notification sent 5 min before lesson
    notification_time -= datetime.timedelta(minutes=5)
    logger_main.info(f"waiting for : {notification_time}")
    task = partial(
        send_notification,
        await get_user_list_from_tp(notify="next_lessons", t_p=t_p),
        embed=embed,
    )

    asyncio.ensure_future(
        schedule_task(task, logger_main=logger_main, planned_date=notification_time)
    )


async def send_notification(
    user_list: list[User], embed: Embed = None, message: str = None, file: File = None
):
    """Envoie une notification avec un message privé à tous les utilisateurs de la liste d'utilisateurs

    Args:
        user_list (list[Utilisateur]): La liste des utilisateurs à notifier
        embed (Embed | None): L'incrustation qui sera envoyée
        message (str | None): Le message qui sera envoyé
    """

    for user in user_list:
        if message:
            await user.send(message)
        if embed:
            await user.send(embed=embed)
        if file:
            await user.send(file=file)
    logger_main.info("notification sent to users : %s", user_list)


async def get_user_list_from_tp(notify: str, t_p: str, serv_id=IUTSERVID) -> list:
    """Renvoie une liste d'identifiants d'utilisateurs qui ont activé la notification recherchée

    Args:
        notify (str): Notification recherchée
        tp (str): Groupe TP (exemple : BUT1-TPA)
        serv_id (int): Serveur ciblé. PAR DÉFAUT IUTSERVID

    Returns:
        list: Identifiants des utilisateurs Discord
    """

    logger_main.info(f"called | args : {notify}, {t_p}, {serv_id}")
    res = []
    user_list: list[str] = get_notified_users(notify=notify, logger_main=logger_main)
    guild: Guild = bot.get_guild(serv_id)
    logging.debug("Discord server found: %s", guild.name)
    if guild:
        for user_ in user_list:
            logging.debug("user_ = %s", user_)
            member: Member = await guild.fetch_member(user_)
            logging.debug("member = %s", member)
            roles = member.roles
            logging.debug("roles = %s", roles)
            for role in roles:
                if t_p == role.name:
                    res.append(member)
    else:
        raise RuntimeError("Discord server not found")

    return res


async def wait_for_auto_start_notif_lessons():
    """Attendre jusqu'à l'heure indiqué pour lancer la fonction
    Args:
        """
    current_time: datetime.datetime = datetime.datetime.now()
    target_time: datetime.datetime = datetime.datetime(
        current_time.year,
        current_time.month,
        current_time.day,
        TARGETED_HOUR_NOTIF_LESSONS[0],
        TARGETED_HOUR_NOTIF_LESSONS[1],
    )
    logger_main.info(f"called")
    # Calculate delay before target time
    if current_time < target_time:
        wait_time: datetime = target_time - current_time
        logging.debug("wait time = %s", wait_time)
    else:
        next_day: datetime.datetime = current_time + datetime.timedelta(days=1)
        target_time = datetime.datetime(
            next_day.year,
            next_day.month,
            next_day.day,
            TARGETED_HOUR_NOTIF_LESSONS[0],
            TARGETED_HOUR_NOTIF_LESSONS[1],
        )
        wait_time: datetime.timedelta = target_time - current_time

    # waiting until target time
    logging.info("waiting %s seconds", wait_time.total_seconds())
    await asyncio.sleep(wait_time.total_seconds())

    asyncio.create_task(plan_notif_for_tp.start())



@bot.command(description="Recovery a file from root (ADMIN ONLY)")
async def recovery_files(
    ctx: ApplicationContext,
    path: Option(str, description="Send in DMs files from this path") = "",
    all: Option(bool, description="All important files") = False,
):
    """
    Send asked files if you are in ADMIN_LIST

    Args:
        ctx (ApplicationContext): The application context.
        path (str, optionnal): Path of asked file DEFAULT: ""
        all (bool, optionnal): If you want logs and jsons files DEFAULT: False
    """
    if ctx.author.id in ADMIN_LIST:
        if all:
            await ctx.interaction.response.send_message("Done!", ephemeral=True)

            for path in IMPORTANT_FILES:
                with open(path, "r") as file:
                    await send_notification([ctx.author], file=File(file))
        else:
            try:
                with open(path, "r") as file:
                    await send_notification([ctx.author], file=File(file))
                    await ctx.interaction.response.send_message("Done!", ephemeral=True)

            except FileNotFoundError:
                await ctx.interaction.response.send_message(
                    "FileNotFoundError", ephemeral=True
                )
    else:
        await ctx.interaction.response.send_message(
            "Vous n'étes pas enregistré en tant qu'administateur", ephemeral=True
        )


if __name__ == "__main__":
    disable_warnings(
        InsecureRequestWarning
    )  # Désactive des messages de prévention du module requests
    log_format = (
        "%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s : %(message)s"
    )
    log_level = logging.DEBUG

    logging.basicConfig(
        level=log_level,
        format=log_format,
    )

    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    if not os.path.exists("Calendars"):
        os.makedirs("Calendars")
    # Retranscription des logs du script main
    logger_main = logging.getLogger(f"main.py")
    file_handler_main = logging.FileHandler("Logs/main_logs.txt")
    file_handler_main.setLevel(log_level)
    file_handler_main.setFormatter(logging.Formatter(log_format))
    logger_main.addHandler(file_handler_main)

    # Retranscription des logs du module discord
    logger_discord = logging.getLogger("discord")
    file_handler_discord = logging.FileHandler("Logs/discord_logs.txt")
    file_handler_discord.setLevel(log_level)
    file_handler_discord.setFormatter(logging.Formatter(log_format))
    logger_discord.addHandler(file_handler_discord)

    bot.run(TOKEN)
