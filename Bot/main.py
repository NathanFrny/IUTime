"""Main file of the bot, contains all the commands and the main loop"""
import datetime
import logging
from functools import partial
from discord import Embed, Intents, Member, User, Bot, ApplicationContext, Guild
from request import lessons_tp, next_lesson_for_tp
from utils import (
    sorting_schedule,
    embed_schedule_construct,
    notification_parameter_change,
    get_notified_users,
    schedule_task,
    add_homework_for_tp,
    homework_for_tp,
    embed_homework_construct,
    del_homework_for_tp,
    homework_auto_remove,
)
from rich import print  # pylint: disable=redefined-builtin
from constants import TOKEN, TP, DATASOURCES, IUTSERVID, ZINCEID, NOTIFICATION_JSON_KEYS
from homework import Homework

intents = Intents.default()
bot: Bot = Bot(intents=intents)

# logging style: "31/01/2023 12:00:00 | DEBUG | main.py | function : message"
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s : %(message)s",
    level=logging.DEBUG,
)


@bot.event
async def on_ready():
    """Actions to do when the bot is ready to use"""
    if not bot.user:
        raise InterruptedError("The bot didn't connect")

    logging.info(
        "Logged in as %s (%s)", bot.user.name, bot.user.id
    )  # Bot connection confirmation

    # plan all asks
    for tp in TP:
        await plan_notification(tp)


@bot.command(description="Ask your schedule")
async def schedule(ctx: ApplicationContext, tp: str):
    """Main Feature:
    Using /schedule on discord channel or bot's DMs
    return in DMs the choiced TP shedule's for the day

    Update soon : return schedule for tommorrow if hour >= 7pm"""
    # TODO - writte error reporting
    user: User | Member = ctx.author
    logging.debug("User value : %s", user)
    if tp.upper() in TP.values():
        logging.debug("tp value : %s", tp)
        date: datetime.date = datetime.date.today()
        _schedule: list = sorting(lessons_tp(tp))
        logging.debug("() | main.py schedule function : schedule value : %s", _schedule)

        embed = embed_schedule_construct(
            title=f"Emploi du temps du {date}",
            description=f"{tp}",
            color=0xFF0000,  # red
            schedule=_schedule,
            sign=True,
        )

        await send_notification(user_list=[user], embed=embed)
        await ctx.interaction.response.send_message("Done!")  # Responding to user
    else:
        logging.debug("TP not found")
        message: str = "Les arguments attendus sont :"
        for element in TP.values():
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
        message: str = "Les arguments attendus sont :"
        for element in NOTIFICATION_JSON_KEYS:
            message += element + ", "
        message = message[:-2]  # Last 2 caracters suppression
        await ctx.interaction.response.send_message(
            message
        )  # Responding if bad argument


@bot.command(description="Demandez les devoirs enregistrés liés à son TP")
async def homework(ctx: ApplicationContext):
    # TODO - checker la génération d'une erreur azec add_homework si l'utilisateur n'est relié a aucun groupe de tp
    user: User | Member = ctx.author
    logging.debug(f"User value : {user}")
    # Récupération du TP de l'utilisateur
    roles: list[Role] = user.roles
    for role in roles:
        logging.debug(f"role value : {role}")
        if role.name in TP.keys():
            logging.debug(f"role.name value : {role.name}")
            homeworks_temp: list[Homework] = homework_for_tp(TP[role.name])
            logging.debug(f"homeworks_temp value : {homeworks_temp}")
            logging.debug(
                f"homeworks_temp's elem type : {type(homeworks_temp[0]) if homeworks_temp != [] else 'homeworks_temp is empty'}"
            )
            homeworks: list[Homework] = []
            # DO NOT use remove method here
            for homework in homeworks_temp:
                if homework.criticite_compare():
                    homeworks.append(homework)
            break
    # Envois des devoirs ou d'un message si aucun devoir
    if homeworks:
        embed: Embed = embed_homework_construct(
            title=role.name, color=0x00FF00, homeworks=homeworks, description="Devoir"
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
    # TODO - ajouter des descriptions aux arguments visible sur discord ( format de la date notemment)
    # TODO - ajouter les logging.debug | Colin technology waiting room

    user: User | Member = ctx.author
    roles: list[Role] = user.roles
    roles_name: list[str] = []
    for role in roles:
        roles_name.append(role.name)

    for name in roles_name:
        if name in TP.keys() and "délégué" in roles_name:
            try:
                # TODO - revoir l'écriture de la date dans la commande
                date_rendu_obj: datetime.datetime = datetime.datetime.strptime(
                    date_rendu, f"%Y-%m-%d-%H-%M"
                )
            except ValueError:
                await ctx.interaction.response.send_message(
                    "Format de date invalide. Utilisez le format 'AAAA-JJ-MM-HH-MM'"
                )
                return

            homework = Homework(
                ressource, prof, criticite, date_rendu_obj, description, note
            )
            result: bool = add_homework_for_tp(
                homework,
                TP[name],
            )
            if result:
                await ctx.interaction.response.send_message("Devoir ajouté avec succès")
            else:
                # Never supposed to appear
                zince: User = await bot.fetch_user(ZINCEID)
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                await zince.send(
                    f"({date}) Error in add_homework function (main.py) for user {ctx.author}, tp = {name}, homework = {homework}"
                )
                await ctx.interaction.response.send_message(
                    "An error happened, my creators have been notified"
                )
            break
    try:
        await ctx.interaction.response.send_message(
            "Seul les délégués des TP ont le droit de modifier les devoirs enregistrés"
        )
    except InteractionResponded:
        pass


@bot.command(description="Supprimer un devoir à son TP")
async def del_homework(ctx: ApplicationContext, emplacement: int = None):
    user: User | Member = ctx.author
    roles: list[Role] = user.roles
    roles_name: list[str] = []
    for role in roles:
        roles_name.append(role.name)

    for name in roles_name:
        if name in TP.keys() and "délégué" in roles_name:
            # 0 = not
            if not emplacement:
                homeworks: list[Homework] = homework_for_tp(TP[name])
                embed: Embed = embed_homework_construct(
                    title="Liste des devoirs enregistrés",
                    description="Utilisez la commande /del_homework en indiquant le numéro du devoir que vous voulez supprimer",
                    # TODO - Sondage pour savoir si il faut préciser les numéros dans l'embed ou pas
                    color=0x00FF00,
                    homeworks=homeworks,
                    sorting=False,
                )
                await ctx.interaction.response.send_message(embed=embed)
            else:
                result: int = del_homework_for_tp(
                    placement=emplacement - 1, tp=TP[name]
                )
                match result:
                    case 1:
                        await ctx.interaction.response.send_message("Done!")
                    case 0:
                        # Never supposed to appear
                        zince: User = await bot.fetch_user(ZINCEID)
                        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                        await zince.send(
                            f"({date}) Error in del_homework function (main.py) for user {ctx.author}, tp = {name}, placement = {emplacement}"
                        )
                        await ctx.interaction.response.send_message(
                            "An error happened, my creators have been notified"
                        )
                    case 2:
                        await ctx.interaction.response.send_message(
                            "Il semblerai que le devoir dont vous avez demandé la suppression n'existe pas"
                        )
                break
    try:
        await ctx.interaction.response.send_message(
            "Seul les délégués des TP ont le droit de modifier les devoirs enregistrés"
        )
    except InteractionResponded:
        pass


async def plan_notification(tp: str) -> None:
    """Send a notification 5 minutes before the next lesson

    Args:
        tp (str): code of the TP group
    """

    # Get the next lesson hour
    try:
        next_lesson: list[tuple] = next_lesson_for_tp(lessons_tp(TP[tp]), tp)
    except RuntimeError:
        # If the TP doesn't have any lessons, stop the automatic planing
        logging.error(
            "The TP %s doesn't have any more lesson, shuttig down the automatic planning",
            tp,
        )
        return
    logging.info("(Send lesson for TP %s : %s", tp, next_lesson)

    embed: Embed = embed_schedule_construct(
        title="Prochain cours:",
        description=None,
        color=0x9370DB,
        schedule=next_lesson,
        sign=True,
    )
    print(f"next lesson : {next_lesson}")
    lesson_time: datetime.datetime = datetime.datetime.strptime(
        next_lesson[0][1]["Heure de début"], "%H:%M"
    )

    notification_time: datetime.datetime = datetime.datetime.now()
    notification_time.replace(hour=lesson_time.hour, minute=lesson_time.minute)
    # notification sent 5 min before lesson
    notification_time -= datetime.timedelta(minutes=5)

    task = partial(send_notification, await get_user_list_from_tp(tp), embed=embed)

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


async def get_user_list_from_tp(tp: str, serv_id=IUTSERVID) -> list:
    """Renvoie l'ID des utilisateurs faisant partie du TP

    Args:
        tp (str): TP cible (rôle discord)

    Returns:
        list: liste d'identifiants discord
    """
    res = []
    user_list: list[str] = get_notified_users()
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
                if tp == role.name:
                    res.append(member)
    else:
        raise RuntimeError("Discord server not found")

    return res


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s : %(message)s",
    )
    homework_auto_remove()
    bot.run(TOKEN)
