"""Main file of the bot, contains all the commands and the main loop"""
import datetime
import logging
import asyncio
from functools import partial
from discord import (
    Embed,
    Intents,
    Member,
    User,
    Bot,
    ApplicationContext,
    Guild,
    Role,
    InteractionResponded,
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
    TOKEN,
    TP_DISCORD_TO_SCHEDULE,
    DATASOURCES,
    IUTSERVID,
    ZINCEID,
    NOTIFICATION_JSON_KEYS,
    HOMEWORKSOURCES,
    TP_SCHEDULE_TO_DISCORD,
    TARGETED_HOUR,
)
from homework import Homework
from lesson import Lesson

intents = Intents.default()
bot: Bot = Bot(intents=intents)


@bot.event
async def on_ready():
    """Actions to do when the bot is ready to use"""
    if not bot.user:
        raise InterruptedError("The bot didn't connect")

    logging.info(
        "Logged in as %s (%s)", bot.user.name, bot.user.id
    )  # Bot connection confirmation
    await wait_for_start_time()


@tasks.loop(hours=24)
async def plan_notif_for_tp():
    """Recover all lesson for each TP group to send it to plan_notification function"""
    all_lesson: list = []
    for (
        t_p
    ) in TP_DISCORD_TO_SCHEDULE.keys():  # pylint: disable=consider-iterating-dictionary
        schedule_: list[Lesson] = lessons_tp(t_p=TP_DISCORD_TO_SCHEDULE[t_p])
        for lesson in schedule_:
            all_lesson.append(lesson)

    all_lesson = Lesson.sorting_schedule(all_lesson)
    while all_lesson != []:
        lesson = all_lesson.pop(0)
        logging.debug("lesson = %s", lesson)
        await plan_notification(t_p=TP_SCHEDULE_TO_DISCORD[lesson.t_p], lesson=lesson)


@tasks.loop(hours=24)
async def homeworks_notif():
    homework_dict: dict = {}
    for t_p in TP_DISCORD_TO_SCHEDULE.keys():
        homeworks = homework_for_tp(TP_DISCORD_TO_SCHEDULE[t_p])
        homework_dict[t_p] = Homework.embed_homework_construct(
            title="teste",
            color=0x00FF00,
            homeworks=homeworks,
            description="teste",
            sign=True,
            sorting=True,
        )
    for t_p in homework_dict.keys():
        users_list = await get_user_list_from_tp(notify="homeworks", t_p=t_p)
        await send_notification(user_list=users_list, embed=homework_dict[t_p])


@bot.command(description="Ask your schedule")
async def schedule(ctx: ApplicationContext, t_p: str):
    """Command to retrieve and send the schedule for a specific TP group.

    Args:
        ctx (ApplicationContext): The application context.
        t_p (str): The TP group for which to retrieve the schedule.
    """
    # TODO - if 7pm past, return tomorrow's schedule
    user: User | Member = ctx.author
    logging.debug("User value : %s", user)
    if t_p.upper() in TP_DISCORD_TO_SCHEDULE.values():
        logging.debug("tp value : %s", t_p)
        date: datetime.date = datetime.date.today()
        _schedule: list = Lesson.sorting_schedule(lessons_tp(t_p))
        logging.debug("() | main.py schedule function : schedule value : %s", _schedule)

        embed = Lesson.embed_schedule_construct(
            title=f"Emploi du temps du {date}",
            description=f"{t_p}",
            color=0xFF0000,  # red
            schedule=_schedule,
            sign=True,
        )

        await send_notification(user_list=[user], embed=embed)
        await ctx.interaction.response.send_message("Done!")  # Responding to user
    else:
        logging.debug("TP not found")
        message: str = "Les arguments attendus sont :"
        for element in TP_DISCORD_TO_SCHEDULE.values():
            message += element + ", "
        message = message[:-2]  # Last 2 caracters suppression
        await ctx.interaction.response.send_message(
            message
        )  # Responding if bad argument


@bot.command(description="Activer ou non les notifications des cours")
async def notif(ctx: ApplicationContext, notification: str, boolean: bool):
    """Permet aux utilisateurs d'activer ou désactiver les notifications de prochains cours"""
    if notification in NOTIFICATION_JSON_KEYS:
        author_id: str = str(ctx.author.id)
        result = notification_parameter_change(
            user_id=author_id,
            parameter=boolean,
            notification=notification,
            path=DATASOURCES,
        )
        if result:
            await ctx.interaction.response.send_message("Done!")
        else:
            # Never supposed to appear
            zince: User = await bot.fetch_user(ZINCEID)
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            await zince.send(
                f"({date}) Error in notif function (main.py) for user\
                    {ctx.author}, notification = {notification}, boolean = {boolean}"
            )
            await ctx.interaction.response.send_message(
                "An error happened, my creators have been notified"
            )
    else:
        logging.debug("Notification not found")
        message: str = "Les arguments attendus sont: "
        for element in NOTIFICATION_JSON_KEYS:
            message += element + ", "
        message = message[:-2]  # Last 2 caracters suppression
        await ctx.interaction.response.send_message(
            message
        )  # Responding if bad argument


@bot.command(description="Demandez les devoirs enregistrés liés à son TP")
async def homework(ctx: ApplicationContext):
    """Command to retrieve and send homeworks to the user.

    Args:
        ctx (ApplicationContext): The application context.
    """
    # TODO - checker la génération d'une erreur azec add_homework si l'utilisateur n'est relié a aucun groupe de tp
    user: User | Member = ctx.author
    logging.debug("User value : %s", user)
    # Récupération du TP de l'utilisateur
    roles: list[Role] = user.roles
    for role in roles:
        logging.debug("role value : %s", role)
        if (
            role.name in TP_DISCORD_TO_SCHEDULE.keys()
        ):  # pylint: disable=consider-iterating-dictionary
            logging.debug("role.name value : %s", role.name)
            homeworks_temp: list[Homework] = homework_for_tp(
                TP_DISCORD_TO_SCHEDULE[role.name], path=HOMEWORKSOURCES
            )
            logging.debug("homeworks_temp value : %s", homeworks_temp)
            logging.debug(
                "homeworks_temp's elem type : %s",
                {
                    type(homeworks_temp[0])
                    if homeworks_temp
                    else "homeworks_temp is empty"
                },
            )
            homeworks: list[Homework] = []
            # DO NOT use remove method here
            for homework_ in homeworks_temp:
                if homework_.criticite_compare():
                    homeworks.append(homework_)
            break
    # Envois des devoirs ou d'un message si aucun devoir
    if homeworks:
        embed: Embed = Homework.embed_homework_construct(
            title=role.name,  # pylint: disable=undefined-loop-variable
            color=0x00FF00,
            homeworks=homeworks,
            description="Devoir",
        )
        await send_notification(user_list=[user], embed=embed)
        await ctx.interaction.response.send_message("Done!")
    else:
        await send_notification(user_list=[user], message="Aucun devoirs enregistrés")
        await ctx.interaction.response.send_message("Done!")

    # Si aucun groupe TP n'a été trouvé
    try:
        await ctx.interaction.response.send_message(
            "Aucun groupe TP ne vous est attribué sur ce serveur discord"
        )
    except InteractionResponded:
        pass


@bot.command(description="Ajouter un devoir à son TP")
async def add_homework(
    ctx: ApplicationContext,
    ressource: str,
    prof: str,
    criticite: str,
    date_rendu: str,
    description: str,
    note: bool = False,
):
    """Command to add a homework to the TP.

    Args:
        ctx (ApplicationContext): The application context.
        ressource (str): The resource of the homework.
        prof (str): The professor of the homework.
        criticite (str): The importance/criticality of the homework.
        date_rendu (str): The deadline of the homework in the format 'YYYY-MM-DD-HH-MM'.
        description (str): The description of the homework.
        note (bool, optional): Whether the homework needs to be noted. Defaults to False.
    """
    # TODO - ajouter des descriptions aux arguments visible sur discord ( format de la date notemment)

    user: User | Member = ctx.author
    roles: list[Role] = user.roles
    roles_name: list[str] = []
    for role in roles:
        roles_name.append(role.name)

    logging.debug("roles_name = %s", roles_name)

    for name in roles_name:
        if (
            name
            in TP_DISCORD_TO_SCHEDULE.keys()  # pylint: disable=consider-iterating-dictionary
            and "délégué" in roles_name
        ):
            logging.debug("TP and role 'délégué' found")
            try:
                date_rendu_obj: datetime.datetime = datetime.datetime.strptime(
                    date_rendu, "%Y-%m-%d-%H-%M"
                )
            except ValueError:
                await ctx.interaction.response.send_message(
                    "Format de date invalide. Utilisez le format 'AAAA-MM-JJ-HH-MM'"
                )
                return

            homework_ = Homework(
                ressource, prof, criticite, date_rendu_obj, description, note
            )
            logging.debug("homework = %s", homework_)
            result: bool = add_homework_for_tp(
                homework=homework_,
                t_p=TP_DISCORD_TO_SCHEDULE[name],
                path=HOMEWORKSOURCES,
            )
            if result:
                await ctx.interaction.response.send_message("Devoir ajouté avec succès")
            else:
                # Never supposed to appear
                zince: User = await bot.fetch_user(ZINCEID)
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                await zince.send(
                    f"({date}) Error in add_homework function (main.py)\
for user {ctx.author}, tp = {name}, homework = {homework_}"
                )
                await ctx.interaction.response.send_message(
                    "An error happened, my creators have been notified"
                )
            break
    try:
        logging.debug("TP or role 'délégué' not found")
        await ctx.interaction.response.send_message(
            "Seul les délégués des TP ont le droit de modifier les devoirs enregistrés"
        )
    except InteractionResponded:
        pass


@bot.command(description="Supprimer un devoir à son TP")
async def del_homework(ctx: ApplicationContext, emplacement: int = None):
    """Command to delete a homework from the TP.

    Args:
        ctx (ApplicationContext): The application context.
        emplacement (int, optional): The placement of the homework to be deleted. Defaults to None.
    """
    user: User | Member = ctx.author
    roles: list[Role] = user.roles
    roles_name: list[str] = []
    for role in roles:
        roles_name.append(role.name)

    logging.debug("roles_name = %s", roles_name)

    for name in roles_name:
        if (
            name
            in TP_DISCORD_TO_SCHEDULE.keys()  # pylint: disable=consider-iterating-dictionary
            and "délégué" in roles_name
        ):
            # 0 = not
            if not emplacement:
                logging.debug("not placement")

                homeworks: list[Homework] = homework_for_tp(
                    t_p=TP_DISCORD_TO_SCHEDULE[name], path=HOMEWORKSOURCES
                )
                logging.debug("homeworks = %s", homeworks)
                embed: Embed = Homework.embed_homework_construct(
                    title="Liste des devoirs enregistrés",
                    description="Utilisez la commande /del_homework en indiquant\
le numéro du devoir que vous voulez supprimer",
                    color=0x00FF00,
                    homeworks=homeworks,
                    sorting=False,
                )
                await ctx.interaction.response.send_message(embed=embed)
            else:
                logging.debug("placement")
                result: int = del_homework_for_tp(
                    placement=emplacement - 1,
                    t_p=TP_DISCORD_TO_SCHEDULE[name],
                    path=HOMEWORKSOURCES,
                )
                match result:
                    case 1:
                        await ctx.interaction.response.send_message("Done!")
                    case 0:
                        # Never supposed to appear
                        zince: User = await bot.fetch_user(ZINCEID)
                        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        await zince.send(
                            f"({date}) Error in del_homework function (main.py) for\
user {ctx.author}, tp = {name}, placement = {emplacement}"
                        )
                        await ctx.interaction.response.send_message(
                            "An error happened, my creators have been notified"
                        )
                    case 2:
                        await ctx.interaction.response.send_message(
                            "Il semblerai que le devoir dont vous avez\
 demandé la suppression n'existe pas"
                        )
                break
    try:
        await ctx.interaction.response.send_message(
            "Seul les délégués des TP ont le droit de modifier les devoirs enregistrés"
        )
    except InteractionResponded:
        pass


async def plan_notification(t_p: str, lesson: Lesson) -> None:
    """Send a notification 5 minutes before the next lesson

    Args:
        tp (str): code of the TP group
        lesson (lesson): lesson object that should be sent
    """
    logging.debug("(Send lesson for TP %s : %s", t_p, lesson)

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
    if lesson_time < datetime.datetime.now() - datetime.timedelta(hours=1, minutes=30):
        logging.info("Lesson time to far in the past, %s", lesson_time)
        return

    notification_time: datetime.datetime = datetime.datetime.now()
    notification_time = notification_time.replace(
        hour=lesson_time.hour, minute=lesson_time.minute
    )
    # notification sent 5 min before lesson
    notification_time -= datetime.timedelta(minutes=5)

    task = partial(
        send_notification,
        await get_user_list_from_tp(notify="next_lesson", t_p=t_p),
        embed=embed,
    )

    await schedule_task(
        task,
        notification_time,
    )


async def send_notification(
    user_list: list[User], embed: Embed = None, message: str = None
):
    """Sends a notification with a private message to all the users in user_list

    Args:
        user_list (list[User]): The list of users to be notified
        embed (Embed | None): The embed that will be sent
        message (str | None): The message that will be sent
    """

    for user in user_list:
        if message:
            await user.send(message)
        if embed:
            await user.send(embed=embed)
    logging.debug("notification sent to users : %s", user_list)


async def get_user_list_from_tp(notify: str, t_p: str, serv_id=IUTSERVID) -> list:
    """Renvoie l'ID des utilisateurs faisant partie du TP

    Args:
        notify (str): notification recherché
        tp (str): TP cible (rôle discord) (like: BUT1-TPA)
        serv_id (int): targeted server. DEFAULT IUTSERVID

    Returns:
        list: liste d'identifiants discord
    """
    logging.debug("t_p =  %s", t_p)
    res = []
    user_list: list[str] = get_notified_users(notify=notify)
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


async def wait_for_start_time():
    current_time: datetime.datetime = datetime.datetime.now()
    target_time: datetime.datetime = datetime.datetime(
        current_time.year,
        current_time.month,
        current_time.day,
        TARGETED_HOUR[0],
        TARGETED_HOUR[1],
    )
    logging.debug("target time = %s", target_time)
    # Calculer le délai avant l'heure cible
    if current_time < target_time:
        wait_time: datetime = target_time - current_time
        logging.debug("wait time = %s", wait_time)
    else:
        next_day: datetime.datetime = current_time + datetime.timedelta(days=1)
        target_time = datetime.datetime(
            next_day.year,
            next_day.month,
            next_day.day,
            TARGETED_HOUR[0],
            TARGETED_HOUR[1],
        )
        wait_time: datetime.timedelta = target_time - current_time

    # Attendre jusqu'à l'heure cible
    logging.info("waiting %s seconds", wait_time.total_seconds())
    await asyncio.sleep(wait_time.total_seconds())

    asyncio.ensure_future(plan_notif_for_tp.start())

    await asyncio.sleep(58200)  # 16h10min
    asyncio.ensure_future(homeworks_notif.start())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s : %(message)s",
    )
    homework_auto_remove()
    bot.run(TOKEN)
