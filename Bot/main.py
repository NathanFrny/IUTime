import datetime
import logging
from discord import *
from functools import partial
from request import lessons_TP, next_lesson_for_tp
from utils import (
    sorting,
    embed_schedule_construct,
    notification_parameter_change,
    get_notified_users,
    schedule_task,
    add_homework_for_tp,
)
from rich import print
from constants import TOKEN, TP, DATASOURCES, IUTSERVID, ZINCEID, NOTIFICATION_JSON_KEYS
from homework import Homework

intents = Intents.default()
bot: Bot = Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    if not bot.user:
        raise InterruptedError("The bot didn't connect")

    logging.info(
        f"Logged in as {bot.user.name} ({bot.user.id})"
    )  # Bot connection confirmation

    # plan all asks
    for tp in TP.keys():
        await plan_notification(tp)


@bot.command(description="Ask your schedule")
async def schedule(ctx: ApplicationContext, tp: str):
    """Main Feature:
    Using /schedule on discord channel or bot's DMs
    return in DMs the choiced TP shedule's for the day

    Update soon : return schedule for tommorrow if hour >= 7pm"""
    # TODO - writte error reporting
    user: User | Member = ctx.author
    logging.debug(
        f"({datetime.datetime.now()}) | main.py schedule function :  User value : {user}"
    )
    if tp.upper() in TP.values():
        logging.debug(
            f"({datetime.datetime.now()}) | main.py schedule function : tp value : {tp}"
        )
        date: datetime.date = datetime.date.today()
        schedule: list = sorting(lessons_TP(tp))
        logging.debug(
            f"({datetime.datetime.now()}) | main.py schedule function : schedule value : {schedule}"
        )

        embed = embed_schedule_construct(
            title=f"Emploi du temps du {date}",
            description=f"{tp}",
            color=0xFF0000,  # red
            schedule=schedule,
            sign=True,
        )

        await send_notification(user_list=[user], embed=embed)
        await ctx.interaction.response.send_message("Done!")  # Responding to user
    else:
        logging.debug(
            f"({datetime.datetime.now()}) | main.py schedule function : TP not found"
        )
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
        id: str = str(ctx.author.id)
        result = notification_parameter_change(
            user_id=id, parameter=boolean, notification=notification, path=DATASOURCES
        )
        if result:
            await ctx.interaction.response.send_message("Done!")
        else:
            # Never supposed to appear
            zince: User = await bot.fetch_user(ZINCEID)
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            await zince.send(
                f"({date}) Error in notif function (main.py) for user {ctx.author}, notification = {notification}, boolean = {boolean}"
            )
            await ctx.interaction.response.send_message(
                "An error happened, my creators have been notified"
            )
    else:
        logging.debug(
            f"({datetime.datetime.now()}) | main.py notif function : notification not found"
        )
        message: str = "Les arguments attendus sont :"
        for element in NOTIFICATION_JSON_KEYS:
            message += element + ", "
        message = message[:-2]  # Last 2 caracters suppression
        await ctx.interaction.response.send_message(
            message
        )  # Responding if bad argument


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

    print(roles_name)
    for name in roles_name:
        print(name)
        if name in TP.keys() and "délégué" in roles_name:
            print(date_rendu)
            try:
                date_rendu_obj: datetime.datetime = datetime.datetime.strptime(
                    date_rendu, f"%Y-%m-%d-%H-%M"
                )
            except ValueError:
                await ctx.interaction.response.send_message(
                    "Format de date invalide. Utilisez le format 'AAAA-MM-JJ-HH-MM'"
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


async def plan_notification(tp: str) -> None:
    print("plan_notification")
    """Send a notification 5 minutes before the next lesson

    Args:
        tp (str): code of the TP group
    """

    # Get the next lesson hour
    try:
        next_lesson: list[tuple] = next_lesson_for_tp(lessons_TP(TP[tp]), tp)
    except RuntimeError as e:
        # If the TP doesn't have any lessons, stop the automatic planing
        logging.error(
            f"({datetime.datetime.now()}) | main.py plan_notification function : The TP {tp} doesn't have any more lesson, shuttig down the automatic planning"
        )
        return
    logging.info(
        f"({datetime.datetime.now()}) | main.py plan_notification function : Send lesson for TP {tp} : {next_lesson}"
    )

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
    print("send_notification")
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
        logging.debug(
            f"({datetime.datetime.now()}) | main.py send_notification function : notification sent"
        )


async def get_user_list_from_tp(tp: str, serv_ID=IUTSERVID) -> list:
    print("get_user_list_from_tp")
    """Renvoie l'ID des utilisateurs faisant partie du TP

    Args:
        tp (str): TP cible (rôle discord)

    Returns:
        list: liste d'identifiants discord
    """
    res = []
    user_list: list[str] = get_notified_users()
    guild: Guild = bot.get_guild(serv_ID)
    logging.debug(
        f"({datetime.datetime.now()}) | main.py get_user_list_from_tp function : Discord server found: {guild.name} | {type(guild.name)}"
    )
    if guild:
        for user_ in user_list:
            logging.debug(
                f"({datetime.datetime.now()}) | main.py get_user_list_from_tp function : user_ = {user_} | {type(user_)}"
            )
            member: Member = await guild.fetch_member(user_)
            logging.debug(
                f"({datetime.datetime.now()}) | main.py get_user_list_from_tp function : member = {member} | {type(member)}"
            )
            roles = member.roles
            logging.debug(
                f"({datetime.datetime.now()}) | main.py get_user_list_from_tp function : roles = {roles} | {type(roles)}"
            )
            for role in roles:
                if tp == role.name:
                    res.append(member)
    else:
        raise RuntimeError("Discord server not found")

    return res


if __name__ == "__main__":
    logging.basicConfig(level=logging.CRITICAL)
    bot.run(TOKEN)
