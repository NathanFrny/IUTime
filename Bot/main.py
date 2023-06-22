import datetime
import json
import logging
from discord import *
from discord.ext import tasks
from functools import partial
from request import lessons_TP, next_lesson_for_tp, schedule_task
from rich import print
from constants import (
    TOKEN,
    TP,
    LOGOPATH,
    AUTHORS,
    DATASOURCES,
    IUTSERVID,
)

logging.basicConfig(level=logging.INFO)


intents = Intents.default()
bot: Bot = Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    if not bot.user:
        raise InterruptedError("The bot didn't connect")

    print(
        f"Logged in as {bot.user.name} ({bot.user.id})"
    )  # Bot connection confirmation
    # await wait_for_start_time()

    # plan all asks
    for tp in TP.keys():
        await plan_notification(tp)


async def plan_notification(tp: str) -> None:
    """Send a notification 5 minutes before the next lesson

    Args:
        tp (str): code of the TP group
    """

    # Get the next lesson hour
    try:
        next_lesson = next_lesson_for_tp(lessons_TP(TP[tp]), tp)
    except RuntimeError as e:
        # If the TP doesn't have any lessons, stop the automatic planing
        logging.error(
            f"The TP {tp} doesn't have any more lesson, shuttig down the automatic planning"
        )
        return
    logging.info(f"Send lesson for TP {tp} : {next_lesson}")
    embed: Embed = Embed(title="Prochain cours :", color=0x9370DB)  # Purple
    embed.set_thumbnail(url=LOGOPATH)
    embed.set_footer(text=f"Ecris par : {AUTHORS}")
    embed.add_field(
        name=next_lesson["Cours"],
        value=f"Salle: {next_lesson['Salle']}\n\
            Prof: {next_lesson['Prof']}\n\
            Heure de fin: {next_lesson['Heure de fin']}\n\n",
        inline=False,
    )

    lesson_time = datetime.datetime.strptime(next_lesson["Heure de début"], "%H:%M")

    notification_time = datetime.datetime.now()
    notification_time.replace(hour=lesson_time.hour, minute=lesson_time.minute)
    notification_time -= datetime.timedelta(minutes=5)

    task = partial(send_notification, await get_user_list_from_tp(tp), embed=embed)

    await schedule_task(
        task,
        notification_time,
    )


async def send_notification(user_list: list[User], embed: Embed):
    """Sends a notification with a private message to all the users in user_list

    Args:
        user_list (list[User]): The list of users to be notified
        embed (Embed): The embed that will be sent
    """

    for user in user_list:
        await user.send(embed=embed)


async def get_user_list_from_tp(tp: str) -> list[int]:
    """Renvoie l'ID des utilisateurs faisant partie du TP

    Args:
        tp (str): TP cible (rôle discord)

    Returns:
        list[int]: liste d'identifiants discord
    """
    res = []
    user_list = await get_notified_users()
    guild = bot.get_guild(IUTSERVID)
    for user_ in user_list:
        member = await guild.fetch_member(user_)
        roles = member.roles
        if tp in roles:
            res.append(user_)

    return res


async def get_notified_users() -> list[int]:
    with open("index.json", "r") as f:
        js: dict = json.load(f)
    # TODO - try/except
    return [user_ for user_, user_params in js.items() if user_params["notify"] == True]


if __name__ == "__main__":
    bot.run(TOKEN)

if __name__ == "main":
    pass
