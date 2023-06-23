import logging
import json
from datetime import datetime
from discord import Embed, Colour
from datetime import timedelta
import asyncio
from inspect import iscoroutinefunction
from constants import LOGOPATH, AUTHORS, DATASOURCES


def embed_schedule_construct(
    title: str,
    color: int | Colour,
    schedule: list[tuple],
    description: str | None,
    sign: bool = True,
) -> Embed:
    """Create a discord embed object representing a student's shedule

    Args:
        title (str): title of the embed
        color (int | Colour): color of the embed
        schedule (list): schedule fo the student, use sorting function for a good structure
        description (str | None): description of the embed
        sign (bool): signed by CSquare on demand, default True

    Returns:
        Embed: discord Embed object, ready to be sended
    """
    # TODO - Create a real lesson class
    print(schedule)
    embed: Embed = Embed(title=title, description=description, color=color)
    for heures in schedule:
        debut: str = heures[1]["Heure de début"]
        cours: str = heures[1]["Cours"]
        salle: str = heures[1]["Salle"]
        prof: str = heures[1]["Prof"]
        heure_fin: str = heures[1]["Heure de fin"]
        embed.add_field(
            name=cours,
            value=f"Début: {debut}\nSalle: {salle}\nProf: {prof}\nHeure de fin: {heure_fin}\n\n",
            inline=False,
        )
    if sign:
        embed.set_thumbnail(url=LOGOPATH)
        embed.set_footer(text=f"Ecris par : {AUTHORS}")

    return embed


def lesson_notification_parameter_change(
    user_id: str, parameter: bool, path: str = DATASOURCES
) -> bool:
    """Change the notification's parameter for the user

    Args:
        user_id (str): user's discord id
        parameter (bool): true if notification accepted, false else
        path (str, optional): path to json Defaults to DATASOURCES.

    Returns:
        bool: true if modification is done, false if any error happened
    """
    with open(path, "r+") as file:
        try:
            js: dict = json.load(file)
        except json.JSONDecodeError:
            js: dict = {}
    try:
        if user_id in js.keys():
            js[user_id]["notify"] = parameter
        else:
            js[user_id] = {"notify": parameter}

        with open(path, "w+") as file:
            json.dump(js, file)
        return True
    except RuntimeError:
        return False


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
    logging.debug(
        f"({datetime.now()}) | utils.py get_notified_users function : path = {sources}"
    )
    liste_id = [
        user_ for user_, user_params in js.items() if user_params["notify"] == True
    ]
    try:
        logging.debug(
            f"({datetime.now()}) | utils.py get_notified_users function : Type des ID renvoyés : {type(liste_id[0])}"
        )
    except IndexError:
        logging.debug(
            f"({datetime.now()}) | utils.py get_notified_users function : liste_id is empty"
        )
    return liste_id


async def schedule_task(task, planned_date: datetime) -> None:
    print("schedule_task")
    # if datetime.datetime.now() > planned_date:
    #     # TODO - faire des vrais classes d'erreur
    #     raise RuntimeError("Planned date is already passed")

    current_time: datetime = datetime.now()
    sleep_time: timedelta = planned_date - current_time
    logging.info(
        f"({datetime.now()}) request.py schedule_task function : Scheduled to run {task} at {planned_date}"
    )
    await asyncio.sleep(sleep_time.total_seconds())

    if iscoroutinefunction(task):
        return await task()
    else:
        return task()


def sorting(cours_dict: dict) -> list[tuple]:
    """Sorts the dictionary keys time order.

    Args:
        cours_dict (dict): Representation of lessons.

    Returns:
        list[tuple]: List of tuples containing the string of an hour in index 0 and a dictionary of the lesson in index 1.
    """
    logging.debug(
        f"({datetime.now()}) | utils.py sorting function : cours_dict = {cours_dict}"
    )

    sorted_items = sorted(cours_dict.items(), key=lambda x: x[0])
    logging.debug(
        f"({datetime.now()}) | utils.py sorting function : sorted_items = {sorted_items}"
    )

    return [(hour, lesson) for hour, lesson in sorted_items]
