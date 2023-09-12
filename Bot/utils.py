from datetime import timedelta, datetime
import asyncio
import logging
import json
from inspect import iscoroutinefunction
from constants import (
    DATASOURCES,
    TP_DISCORD_TO_SCHEDULE,
    HOMEWORKSOURCES,
)
from homework import Homework


def notification_parameter_change(
    user_id: str, parameter: bool, notification: str, logger_main, path: str = DATASOURCES
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
    logger_main.info(f"called | args: {user_id}, {parameter}, {notification} {path}")
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


def get_notified_users(notify: str, logger_main, sources: str = DATASOURCES) -> list:
    """Return all IDs found in json in parameters where schedule's notification are activated

    Args:
        notify (str) : type of notification seached
        sources (str, optional): Path to json. Defaults to DATASOURCES.

    Returns:
        list: All IDs found
    """
    logger_main.info(f"called | args: {notify}, {sources}")
    try:
        with open(sources, "r", encoding="utf-8") as file:
            j_s: dict = json.load(file)
    except FileNotFoundError:
        return []
    logging.debug("path = %s", sources)
    liste_id = [
        user_ for user_, user_params in j_s.items() if user_params.get(notify, False)
    ]
    try:
        logging.debug("ID types returned : %s", type(liste_id[0]))
    except IndexError:
        logging.debug("liste_id is empty")
    return liste_id


async def schedule_task(task, logger_main, planned_date: datetime = datetime.now()) -> None:
    """Schedule a task to run at a specific time.

    Args:
        task (callable | coroutine): task to run
        planned_date (datetime): time to run the task

    Returns:
        None
    """
    #logger_main.info(f"called | args: {task}, {planned_date}")
    current_time: datetime = datetime.now()
    sleep_time: timedelta = planned_date - current_time
    await asyncio.sleep(sleep_time.total_seconds())

    if iscoroutinefunction(task):
        return await task()

    return task()


def add_homework_for_tp(
    homework: Homework, t_p: str, logger_main, path: str = HOMEWORKSOURCES
) -> bool:
    """Add an homework in json file

    Args:
        homework (Homework): homework need to be added
        tp (str): tp group concerned
        path (str, optional): path to json file. Defaults to HOMEWORKSOURCES.

    Returns:
        bool: true if adding complete, false if error happened
    """
    logger_main.info(f"called | {homework}, {t_p}, {path}")
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


def del_homework_for_tp(placement: int, t_p: str, logger_main, path=HOMEWORKSOURCES) -> int:
    """Remove an homework in json file

    Args:
        placement (int): index of the homework
        tp (str): tp group concerned
        path (str, optional): path to json file. Defaults to HOMEWORKSOURCES.

    Returns:
        int: 1 if deletion is successful, 0 if an error occurs during execution,
            2 if user gave a miss-argument
    """
    logger_main.info(f"called | args: {placement}, {t_p}, {path}")
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
        # if user gave a miss-argument or because no any homework registered in his tp
        return 2
    except FileNotFoundError:
        return 0


def homework_for_tp(t_p: str, logger_main, path: str = HOMEWORKSOURCES) -> list[Homework]:
    """Return a list of object Homework

    Args:
        tp (str): tp group concerned
        path (str, optional): path to json file. Defaults to HOMEWOKSOURCES.

    Returns:
        list[Homework]: list of Homework for the tp asked
    """
    logger_main.info(f"called | args: {t_p}, {path}")
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


def homework_auto_remove(logger_main, path: str = HOMEWORKSOURCES):
    """Remove out-dated homewoks from json file

    Args:
        path (str, optional): path to json file. Defaults to HOMEWORKSOURCES.
    """
    logger_main.info(f"called | args: {path}")
    all_homeworks_dict: dict = {}
    current_date: datetime = datetime.now()
    for t_p in TP_DISCORD_TO_SCHEDULE.values():
        logging.debug("TP = %s", t_p)

        homeworks_temp: list[Homework] = homework_for_tp(t_p=t_p, path=path, logger_main=logger_main)
        logging.debug("homeworks_temp = %s", homeworks_temp)
        homeworks: list[Homework] = []
        for homework in homeworks_temp:
            if homework.date_rendu + timedelta(days=1, hours=12) > current_date:
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

