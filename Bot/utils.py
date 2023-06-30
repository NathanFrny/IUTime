"""This module contains all the functions that are used in the bot."""
# TODO - rename this file, utils.py is too generic
from datetime import timedelta, datetime
import asyncio
import logging
import json
from inspect import iscoroutinefunction


from discord import Embed, Colour
from constants import LOGOPATH, AUTHORS, DATASOURCES, TP
from homework import Homework


def embed_schedule_construct(
    title: str,
    color: int | Colour,
    schedule: list[tuple],
    description: str | None,
    sign: bool = True,
) -> Embed:
    """Create a discord Embed object representing a student's shedule

    Args:
        title (str): title of the embed
        color (int | Colour): color of the embed
        schedule (list): schedule of student, use sorting function for a good structure
        description (str | None): description of the embed
        sign (bool): signed by CSquare on demand, default True

    Returns:
        Embed: discord Embed object, ready to be sent
    """
    # TODO - Create a real lesson class
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
        embed.set_footer(text=f"Écris par : {AUTHORS}")

    return embed


def notification_parameter_change(
    user_id: str, parameter: bool, notification: str, path: str = DATASOURCES
) -> bool:
    """Change the notification's parameter for the user

    Args:
        user_id (str): user's discord id
        parameter (bool): true if notification accepted, false else
        notification (str): which notification need a modification
        path (str, optional): path to json Defaults to DATASOURCES.

    Returns:
        bool: true if modification is done, false if any error happened
    """
    with open(path, "r+", encoding="utf-8") as file:
        try:
            j_s: dict = json.load(file)
        except json.JSONDecodeError:
            j_s: dict = {}
    try:
        if user_id in j_s.keys():
            j_s[user_id][notification] = parameter
        else:
            print(1)
            j_s[user_id] = {notification: parameter}

        with open(path, "w+", encoding="utf-8") as file:
            json.dump(j_s, file)
        return True
    except RuntimeError:
        return False


def get_notified_users(notify: str, sources: str = DATASOURCES) -> list:
    """Return all IDs found in json in parameters where schedule's notification are activated

    Args:
        notify (str) : type of notification seached
        sources (str, optional): Path to json. Defaults to DATASOURCES.

    Returns:
        list: All IDs found
    """
    try:
        with open(sources, "r", encoding="utf-8") as file:
            j_s: dict = json.load(file)
    except FileNotFoundError:
        return []
    logging.debug("path = %s", sources)
    liste_id = [user_ for user_, user_params in j_s.items() if user_params[notify]]
    try:
        logging.debug("Type des ID renvoyés : %s", type(liste_id[0]))
    except IndexError:
        logging.debug("liste_id is empty")
    return liste_id


async def schedule_task(task, planned_date: datetime) -> None:
    """Schedule a task to run at a specific time.

    Args:
        task (callable | coroutine): task to run
        planned_date (datetime): time to run the task

    Returns:
        None
    """

    # if datetime.datetime.now() > planned_date:
    #     # TODO - faire des vrais classes d'erreur
    #     raise RuntimeError("Planned date is already passed")

    current_time: datetime = datetime.now()
    sleep_time: timedelta = planned_date - current_time
    logging.info("Scheduled to run %s at %s", task.__name__, planned_date)
    await asyncio.sleep(sleep_time.total_seconds())

    if iscoroutinefunction(task):
        return await task()

    return task()


def sorting_schedule(cours_dict: dict) -> list[tuple]:
    """Sorts the dictionary keys time order.

    Args:
        cours_dict (dict): Representation of lessons.

    Returns:
        list[tuple]: List of tuples containing the string of an hour in index 0 and
        a dictionary of the lesson in index 1.
    """
    logging.debug("cours_dict = %s", cours_dict)

    sorted_items = sorted(cours_dict.items(), key=lambda x: x[0])
    logging.debug("sorted_items = %s", sorted_items)

    return list[sorted_items]


def add_homework_for_tp(homework: Homework, t_p: str, path: str = DATASOURCES) -> bool:
    """Add an homework in json file

    Args:
        homework (Homework): homework need to be added
        tp (str): tp group concerned
        path (str, optional): path to json file. Defaults to DATASOURCES.

    Returns:
        bool: true if adding complete, false if error happened
    """
    with open(path, "r+", encoding="utf-8") as file:
        try:
            j_s: dict = json.load(file)
        except json.JSONDecodeError:
            j_s: dict = {}
    try:
        if "homework" not in j_s:
            j_s["homework"] = {}

        if t_p not in j_s["homework"]:
            j_s["homework"][t_p] = []

        j_s["homework"][t_p].append(homework.tojson())

        with open(path, "w+", encoding="utf-8") as file:
            json.dump(j_s, file)
        return True

    except RuntimeError:
        return False


def del_homework_for_tp(placement: int, t_p: str, path=DATASOURCES) -> int:
    """Remove an homework in json file

    Args:
        placement (int): index of the homework
        tp (str): tp group concerned
        path (str, optional): path to json file. Defaults to DATASOURCES.

    Returns:
        int: 1 if deletion is successful, 0 if an error occurs during execution,
            2 if user gave a miss-argument
    """
    try:
        with open(path, "r+", encoding="utf-8") as file:
            j_s: dict = json.load(file)

        homework_list: dict = j_s["homework"][t_p]
        if placement < 0:
            raise IndexError
        del homework_list[placement]

        with open(path, "w+", encoding="utf-8") as file:
            json.dump(j_s, file)

        return 1

    except (json.JSONDecodeError, KeyError, IndexError):
        # if user gave a miss-argument, because no any homework registered in his tp
        return 2
    except FileNotFoundError:
        return 0


def homework_for_tp(t_p: str, path: str = DATASOURCES) -> list[Homework]:
    """Return a list of object Homework

    Args:
        tp (str): tp group concerned
        path (str, optional): path to json file. Defaults to DATASOURCES.

    Returns:
        list[Homework]: list of Homework for the tp asked
    """
    with open(path, "r+", encoding="utf-8") as file:
        try:
            j_s: dict = json.load(file)
        except json.JSONDecodeError:
            j_s: dict = {}

    list_dict_homework: list[Homework] = []
    try:
        list_dict_homework: list[dict] = j_s["homework"][t_p]
    except KeyError:
        pass
    list_homework: list[Homework] = []
    for homework_dict in list_dict_homework:
        list_homework.append(Homework.fromjson(json.dumps(homework_dict)))

    return list_homework


def homework_auto_remove(path: str = DATASOURCES):
    """Remove out-dated homewoks from json file

    Args:
        path (str, optional): path to json file. Defaults to DATASOURCES.
    """
    all_homeworks_dict: dict = {}
    current_date: datetime = datetime.now()
    for t_p in TP.values():
        logging.debug("TP = %s", t_p)

        homeworks_temp: list[Homework] = homework_for_tp(t_p=t_p, path=path)
        logging.debug("homeworks_temp = %s", homeworks_temp)
        homeworks: list[Homework] = []
        for homework in homeworks_temp:
            if homework.date_rendu + timedelta(days=1) > current_date:
                logging.debug("valid homework : %s", homework)
                homeworks.append(homework.tojson())
            else:
                logging.debug("unvalid homework : %s", homework)

        all_homeworks_dict[t_p] = homeworks
        logging.debug("all_homeworks_dict = %s", all_homeworks_dict)

    with open(path, "r+", encoding="utf-8") as file:
        try:
            j_s: dict = json.load(file)
        except json.JSONDecodeError:
            j_s: dict = {}

    j_s["homework"] = all_homeworks_dict

    with open(path, "w+", encoding="utf-8") as file:
        json.dump(j_s, file)
