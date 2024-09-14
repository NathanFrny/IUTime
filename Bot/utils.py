from datetime import timedelta, datetime
import asyncio
import logging
import json
from inspect import iscoroutinefunction
from constants import DATASOURCES, TP_DISCORD_TO_SCHEDULE, HOMEWORKSOURCES, ADMIN_LIST
from homework import Homework


def notification_parameter_change(
    user_id: str,
    parameter: bool,
    notification: str,
    logger_main,
    path: str = DATASOURCES,
) -> bool:
    """Modifie les paramétres de notifications de l'utilisateur.

    Args:
        user_id (str): ID Discord de l'utilisateur.
        parameter (bool): True si la notifcation est accepté par l'utilisateur, False sinon.
        notification (str): Nom de la notification à modifier.
        path (str, optional): Chemin vers le fichier de sauvegarde. Defaults to DATASOURCES.

    Returns:
        bool: True si la modification à bien été effectué, False si une erreur est survenue.
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


def get_notified_users(
    notify: str, logger_main, sources: str = DATASOURCES
) -> list[str]:
    """Retourne tous les ID Discord dans la fichier JSON source pour lequel la notification est bien activé

    Args:
        notify (str) : Nom de la notification recherchée.
        sources (str, optional): Chemin vers le fichier source. Defaults to DATASOURCES.

    Returns:
        list[str]: Liste de tous les ID Discord trouvés.
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


async def schedule_task(
    task: callable, logger_main, planned_date: datetime = datetime.now()
) -> None:
    """Prévoit une tâche à effectuer à la date et l'heure indiquée.

    Args:
        task (callable | coroutine): Tâche à effectuer.
        planned_date (datetime): Date et heure à laquelle la tâche doit être effectuée.

    Returns:
        None
    """
    logger_main.info(f"called | args: {task}, {planned_date}")
    current_time: datetime = datetime.now()
    sleep_time: timedelta = planned_date - current_time
    await asyncio.sleep(sleep_time.total_seconds() - 3600)

    if iscoroutinefunction(task):
        return await task()

    return task()


def add_homework_for_tp(
    homework: Homework, t_p: str, logger_main, path: str = HOMEWORKSOURCES
) -> bool:
    """Ajoute un nouveau devoir dans un fichier JSON adapté.

    Args:
        homework (Homework): Devoir à ajouter.
        tp (str): Groupe TP concerné.
        path (str, optional): Chemin vers le fichier de sauvegarde. Defaults to HOMEWORKSOURCES.

    Returns:
        bool: True si l'ajout à été effectué, false si une erreur est survenue
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


def del_homework_for_tp(
    placement: int, t_p: str, logger_main, path=HOMEWORKSOURCES
) -> int:
    """Suppression d'un devoir dans un fichier JSON adapté.

    Args:
        placement (int): Index du devoir dans la liste de devoir du groupe TP concerné.
        tp (str): Groupe TP concerné.
        path (str, optional): Chemin vers le fichier source. Defaults to HOMEWORKSOURCES.

    Returns:
        int: 1 si le devoir à bien été supprimé,
             0 si une erreur d'exécution est survenue,
             2 si l'utilisateur a donné un argument invalide.
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

    except (KeyError, IndexError):
        return 2
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def homework_for_tp(
    t_p: str, logger_main, path: str = HOMEWORKSOURCES
) -> list[Homework]:
    """Retourne la liste des devoirs enregistré pour le TP concerné.

    Args:
        tp (str): Groupe TP concerné.
        path (str, optional): Chemin vers le fichier source. Defaults to HOMEWOKSOURCES.

    Returns:
        list[Homework]: Liste de devoirs.
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
    """Supprime les devoirs dont la date de rendue est dépassée.

    Args:
        path (str, optional): Chemin vers le fichier source. Defaults to HOMEWORKSOURCES.
    """
    logger_main.info(f"called | args: {path}")
    all_homeworks_dict: dict = {}
    current_date: datetime = datetime.now()
    for t_p in TP_DISCORD_TO_SCHEDULE.values():
        logging.debug("TP = %s", t_p)

        homeworks_temp: list[Homework] = homework_for_tp(
            t_p=t_p, path=path, logger_main=logger_main
        )
        logging.debug("homeworks_temp = %s", homeworks_temp)
        homeworks: list[Homework] = []
        for homework in homeworks_temp:
            if homework.date_rendu + timedelta(hours=12) > current_date:
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


# def is_dst(date):
#    """Détermine si une date donnée est en heure d'été (DST) pour la France."""
#    dernier_dimanche_mars = max(semaine for semaine in range(25, 32) if datetime(date.year, 3, semaine).weekday() == 6)
#    dernier_dimanche_octobre = max(semaine for semaine in range(25, 32) if datetime(date.year, 10, semaine).weekday() == 6)
#
#    debut_dst = datetime(date.year, 3, dernier_dimanche_mars, 2, 0, 0)  # L'heure d'été commence à 2h du matin le dernier dimanche de mars
#    fin_dst = datetime(date.year, 10, dernier_dimanche_octobre, 3, 0, 0)  # L'heure d'été se termine à 3h du matin le dernier dimanche d'octobre
#
#    return debut_dst <= date < fin_dst
#
# def convert_to_utc(heure, minute):
#    """Convertit l'heure locale française en UTC en tenant compte de l'heure d'été."""
#    maintenant = datetime.now()
#    heure_locale = datetime(maintenant.year, maintenant.month, maintenant.day, heure, minute)
#
#    # Détermine le décalage en fonction de l'activation de l'heure d'été
#    decalage = 2 if is_dst(heure_locale) else 1
#    # Conversion en UTC
#    heure_utc = heure_locale - timedelta(hours=decalage)
#    return heure_utc.hour, heure_utc.minute
