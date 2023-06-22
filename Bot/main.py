import datetime
import json
import logging
from discord import *
from functools import partial
from request import lessons_TP, next_lesson_for_tp, schedule_task
from utils import sorting
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


@bot.command(description="Ask your schedule")
async def schedule(ctx: ApplicationContext, tp: str):
    """Main Feature:
    Using /schedule on discord channel or bot's DMs
    return in DMs the choiced TP shedule's for the day

    Update soon : return schedule for tommorrow if hour >= 7pm"""

    user: User | Member = ctx.author
    if tp.upper() in TP.values():
        date: datetime.date = datetime.date.today()
        schedule: list = sorting(lessons_TP(tp))
        embed: Embed = Embed(
            title=f"Schedule {date}",
            description=f"Voici l'emploi du temps du {tp}",
            color=0x9370DB,  # Purple
        )
        embed.set_thumbnail(url=LOGOPATH)
        embed.set_footer(text=f"Ecris par : {AUTHORS}")

        for heures in schedule:
            debut: dict = heures[1]["Heure de début"]
            cours: str = schedule[heures][1]["Cours"]
            salle: str = schedule[heures][1]["Salle"]
            prof: str = schedule[heures][1]["Prof"]
            heure_fin: str = schedule[heures][1]["Heure de fin"]

            embed.add_field(
                name=cours,
                value=f"Début: {debut}\nSalle: {salle}\nProf: {prof}\nHeure de fin: {heure_fin}\n\n",
                inline=False,
            )

        await user.send(embed=embed)  # Send schedule in DM's
        await ctx.interaction.response.send_message("Done!")  # Responding to user
    else:
        message: str = "Les arguments attendus sont :"
        for element in TP.values():
            message += element + ", "
        message = message[:-2]  # Last 2 caracters suppression
        await ctx.interaction.response.send_message(
            message
        )  # Responding if bad argument


@bot.command(description="Activer ou non les notifications des cours")
async def notif(ctx: ApplicationContext, boolean: bool, path=DATASOURCES):
    """Permet aux utilisateurs d'activer ou désactiver les notifications de prochains cours"""
    id: int = ctx.author.id
    with open(path, "r+") as f:
        try:
            js = json.load(f)
        except json.JSONDecodeError:
            js = {}
    if id in js.keys():
        js[id]["notify"] = boolean
    else:
        js[id] = {"notify": boolean}

    with open(path, "w+") as f:
        json.dump(js, f)
    await ctx.interaction.response.send_message("Done!")


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


async def get_user_list_from_tp(tp: str, serv_ID=IUTSERVID) -> list:
    # TODO - je sais pas comment mais va falloir trouver comment tester cette fonction
    """Renvoie l'ID des utilisateurs faisant partie du TP

    Args:
        tp (str): TP cible (rôle discord)

    Returns:
        list: liste d'identifiants discord
    """
    res = []
    user_list = get_notified_users()
    guild = bot.get_guild(serv_ID)
    logging.debug(f"Discord server found: {guild.name}")
    if guild:
        for user_ in user_list:
            logging.debug(f"user_ = {user_}")
            member = await guild.fetch_member(user_)
            logging.debug(f"member = {member}")
            roles = member.roles
            logging.debug(f"roles = {roles}")
            if tp in roles:
                res.append(user_)
    else:
        raise RuntimeError("Discord server not found")

    return res


def get_notified_users(sources: str = DATASOURCES) -> list:
    """Return all IDs found in json in parameters where schedule's notification are activated

    Args:
        sources (str, optional): Path to json. Defaults to DATASOURCES.

    Returns:
        list: All IDs found
    """
    with open(sources, "r") as f:
        js: dict = json.load(f)
    # TODO - try/except
    logging.debug(f"path = {sources}")
    liste_id = [
        user_ for user_, user_params in js.items() if user_params["notify"] == True
    ]
    logging.debug(f"Type des ID renvoyés : {type(liste_id[0])}")
    return liste_id


if __name__ == "__main__":
    bot.run(TOKEN)
