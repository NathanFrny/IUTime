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
        embed.set_footer(text=f"Écris par : {AUTHORS}")

    return embed


def embed_homework_construct(
    title: str,
    color: int | Colour,
    homeworks: list[Homework],
    description: str | None,
    sign: bool = True,
    sorting: bool = True,
) -> Embed:
    """Create a discord Embed object representing a student's homeworks

    Args:
        title (str): title of the embed
        color (int | Colour): color of the embed
        homeworks (list[Homework]): homeworks of student
        description (str | None): description of the embed
        sign (bool, optional): signed by CSquare on demand, default True
        sorting (bool, optional): sorting of homework to position them with outdated on top, default True
    Returns:
        Embed: discord Embed object, ready to be sent
    """
    if sorting:
        sorting_homeworks(homeworks)
    embed: Embed = Embed(
        title=title, description=description if description else "", color=color
    )
    for homework in homeworks:
        if homework.criticite_compare:
            ressource: str = homework.ressource
            prof: str = homework.prof
            date_rendu: datetime = homework.date_rendu
            description: str = homework.description
            note: bool = homework.note
            outdated: bool = homework.outdated

            embed.add_field(
                name=f"{ressource} {'DEADLINE DEPASSÉ' if outdated else ''}",
                value=f"Prof: {prof}\nPour le: {date_rendu.day}/{date_rendu.month if len(str(date_rendu.month)) > 1 else '0'+str(date_rendu.month)}/{date_rendu.year} {date_rendu.hour}H{date_rendu.minute if len(str(date_rendu.minute)) > 1 else '0'+str(date_rendu.minute)}\nDescription: {description}\n{'Devoir noté' if note else ''}",
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
    print(type(user_id))
    with open(path, "r+", encoding="utf-8") as file:
        try:
            js: dict = json.load(file)
        except json.JSONDecodeError:
            js: dict = {}
    try:
        if user_id in js.keys():
            js[user_id][notification] = parameter
        else:
            print(1)
            js[user_id] = {notification: parameter}

        with open(path, "w+", encoding="utf-8") as file:
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
    with open(sources, "r", encoding="utf-8") as f:
        js: dict = json.load(f)
    # TODO - try/except
    logging.debug("path = %s", sources)
    liste_id = [user_ for user_, user_params in js.items() if user_params["notify"]]
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
    else:
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

    return [(hour, lesson) for hour, lesson in sorted_items]


def sorting_homeworks(homework_list: list[Homework]) -> list[Homework]:
    return sorted(homework_list, key=lambda hw: hw.is_outdated(), reverse=False)


def add_homework_for_tp(homework: Homework, tp: str, path: str = DATASOURCES) -> bool:
    """Add an homework in json file

    Args:
        homework (Homework): homework need to be added
        tp (str): tp group concerned
        path (str, optional): path to json file. Defaults to DATASOURCES.

    Returns:
        bool: true if adding complete, false if error happened
    """
    with open(path, "r+") as file:
        try:
            js: dict = json.load(file)
        except json.JSONDecodeError:
            js: dict = {}
    try:
        if "homework" not in js:
            js["homework"] = {}

        if tp not in js["homework"]:
            js["homework"][tp] = []

        js["homework"][tp].append(homework.tojson())

        with open(path, "w+") as file:
            json.dump(js, file)
        return True

    except RuntimeError:
        return False


def del_homework_for_tp(placement: int, tp: str, path=DATASOURCES) -> int:
    """Remove an homework in json file

    Args:
        placement (int): index of the homework
        tp (str): tp group concerned
        path (str, optional): path to json file. Defaults to DATASOURCES.

    Returns:
        int: 1 if deletion is successful, 0 if an error occurs during execution, 2 if user gave a miss-argument
    """
    try:
        with open(path, "r+") as file:
            js: dict = json.load(file)

        homework_list: dict = js["homework"][tp]
        if placement < 0:
            raise IndexError
        del homework_list[placement]

        with open(path, "w+") as file:
            json.dump(js, file)

        return 1

    except (json.JSONDecodeError, KeyError, IndexError):
        # if user gave a miss-argument, because no any homework registered in his tp or not even in all others tp
        return 2
    except FileNotFoundError:
        return 0


def homework_for_tp(tp: str, path: str = DATASOURCES) -> list[Homework]:
    """Return a list of object Homework

    Args:
        tp (str): tp group concerned
        path (str, optional): path to json file. Defaults to DATASOURCES.

    Returns:
        list[Homework]: list of Homework for the tp asked
    """
    with open(path, "r+") as file:
        try:
            js: dict = json.load(file)
        except json.JSONDecodeError:
            js: dict = {}

    list_dict_homework: list[Homework] = []
    try:
        list_dict_homework: list[dict] = js["homework"][tp]
    except KeyError:
        pass
    list_homework: list[Homework] = []
    for homework_dict in list_dict_homework:
        list_homework.append(Homework.fromjson(json.dumps(homework_dict)))

    return list_homework


def homework_auto_remove(path: str = DATASOURCES):
    all_homeworks_dict: dict = {}
    current_date: datetime = datetime.now()
    for tp in TP.values():
        logging.debug(f"TP = {tp}")

        homeworks_temp: list[Homework] = homework_for_tp(tp=tp, path=path)
        logging.debug(f"homeworks_temp = {homeworks_temp}")
        homeworks: list[Homework] = []
        for homework in homeworks_temp:
            if homework.date_rendu + timedelta(days=1) > current_date:
                logging.debug(f"valid homework : {homework}")
                homeworks.append(homework.tojson())
            else:
                logging.debug(f"unvalid homework : {homework}")

        all_homeworks_dict[tp] = homeworks
        logging.debug(f"all_homeworks_dict = {all_homeworks_dict}")

    with open(path, "r+") as file:
        try:
            js: dict = json.load(file)
        except json.JSONDecodeError:
            js: dict = {}

    js["homework"] = all_homeworks_dict

    with open(path, "w+") as file:
        json.dump(js, file)
