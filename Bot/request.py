import logging
from ics import Calendar
from pytz import timezone
import datetime
from datetime import timedelta, datetime as Datetime, date
import asyncio
from inspect import iscoroutinefunction
from utils import sorting


# Renvoies les cours de la journée pour le TP mis en paramètre
def lessons_TP(tp: str) -> dict:
    tp = tp.upper()
    logging.debug(f"tp's value = {tp}")

    ics_file: str = f"Calendars/{tp}/ADECal.ics"
    logging.debug(f"Source's path : {ics_file}")

    with open(ics_file, "r", encoding="utf-8") as file:
        ical_data: str = file.read()

    calendar: Calendar = Calendar(ical_data)

    lessons: dict[str:dict] = {}
    reference_date: date = date.today()
    logging.debug(f"Reference_date = {reference_date}")

    for event in calendar.events:
        logging.debug(f"event : {event}")
        start_utc: datetime = event.begin.astimezone(timezone("Europe/Paris"))
        end_utc: datetime = event.end.astimezone(timezone("Europe/Paris"))

        # Si l'évênement est aujourd'hui
        if start_utc.date() == reference_date:
            logging.debug("Event is today")
            event.name = event.name.upper()

            start_hour: str = start_utc.strftime("%H:%M")
            end_hour: str = end_utc.strftime("%H:%M")

            # On récupère les profs du cours
            description: str = event.description
            lines: list[str] = description.split("\n")
            logging.debug(
                f"event_name = {event.name}\n\
start_hour = {start_hour}\n\
end_hour = {end_hour}\n\
description = {description}"
            )
            # Suppression des lines contenant "BUT" ou des parenthèses
            teacher: list[str] = [
                ligne
                for ligne in lines
                if "BUT" not in ligne
                and "DUT" not in ligne
                and "(" not in ligne
                and ")" not in ligne
                and ligne.strip() != ""
            ]
            logging.debug(f"teacher = {teacher}")

            # Si il y a un profs alors on récupère uniquement le teacheren string sinon on indique qu'il n'y a aucun prof
            if len(teacher) > 0:
                teacher: str = teacher[0]
            else:
                teacher: str = "Aucun prof"
            logging.debug(f"teacher = {teacher}")

            # On crée la valeur du dictionnaire contenant le cours (la clé est l'heure de début du cours)
            lessons[start_hour]: dict[str:str, str:str, str:str, str:str, str:str] = {
                # TODO - Créer un objet "cours"
                "Cours": event.name[:-3],
                "Salle": event.location,
                "Prof": teacher,
                "Heure de début": start_hour,
                "Heure de fin": end_hour,
            }
        else:
            logging.debug(f"Error on event date's : {str(start_utc.date())}")
    return lessons


def next_lesson_for_tp(cours_dict: dict[str], tp: str) -> tuple | None:
    """Return the next lesson regardless of the date

    Args:
        cours: lessons
        tp: TP code

    Returns:
        dict: dictionnary representing the lesson
    """

    next_lesson: dict = None

    date_: Datetime = Datetime.now()
    logging.debug(f"date = {date_}")

    total_minutes: int = (date_.hour * 60) + date_.minute
    logging.debug(f"total_minutes = {total_minutes}")

    cours: list[tuple] = sorting(cours_dict)

    for key in cours:
        logging.debug(f"type of key: {type(key)}")
        logging.debug(f"value of key: {key}")
        # Conversion in total minutes
        key: tuple[str, dict]
        # NOTE - Annotation un peu bizarre, à vérifier
        minutes = int(key[0].split(":")[0]) * 60 + int(key[0].split(":")[1])
        if total_minutes < minutes:
            return key
        else:
            pass

    if next_lesson is None:
        logging.error(f"Le TP {tp} n'a pas/plus de cours aujourd'hui")

    return next_lesson


async def schedule_task(task, planned_date: datetime) -> None:
    # if datetime.datetime.now() > planned_date:
    #     # TODO - faire des vrais classes d'erreur
    #     raise RuntimeError("Planned date is already passed")

    current_time: datetime = datetime.now()
    sleep_time: timedelta = planned_date - current_time
    logging.info(f"Scheduled to run {task} at {planned_date}")
    await asyncio.sleep(sleep_time.total_seconds())

    if iscoroutinefunction(task):
        return await task()
    else:
        return task()


if __name__ == "request":
    from utils import *
    from rich import print

    SEPARATOR = (
        "-----------------------------------------------------------------------"
    )
    logging.basicConfig(level=logging.DEBUG)

    DEBUGTP = "testing"
    COURS = testing_lessons_generation()

    print(
        f"DEBUGTP = {DEBUGTP}\n\
COURS = {COURS}"
    )
    print(SEPARATOR)
    print(
        "lessons_TP testing function:\n\
Args: \n\
    DEBUGTP :     str = 'testing'\n\
Expected return:\n\
    lessons : dict = { \n\
'08:00': { \n\
    'Cours': 'Mathematics', \n\
    'Salle': 'A101', \n\
    'Prof': 'Mr. Dupont', \n\
    'Heure de début': '08:00', \n\
    'Heure de fin': '09:30' }, \n\
'09:30': { \n\
    'Cours': 'Physics', \n\
    'Salle': 'B202', \n\
    'Prof': 'Mrs. Martin', \n\
    'Heure de début': '09:30', \n\
    'Heure de fin': '11:00' }, \n\
'12:00': { \n\
    'Cours': 'Computer Science', \n\
    'Salle': 'C303', \n\
    'Prof': 'Mr. Smith', \n\
    'Heure de début': '12:00', \n\
    'Heure de fin': '13:00' }, \n\
'14:00': { \n\
    'Cours': 'Chemistry', \n\
    'Salle': 'D404', \n\
    'Prof': 'Ms. Johnson', \n\
    'Heure de début': '14:00', \n\
    'Heure de fin': '15:30' } \n\
}\n\
Take care of: The test dates may not correspond to the dates indicated in the events in the Calendars/TESTING/ADECal.ics file."
    )
    print(
        f"RESULT FOR FONCTION : lesson_TP: \n\
{lessons_TP(DEBUGTP)}"
    )
    print(SEPARATOR)
    print(
        "next_lesson_for_tp testing function:\n\
Args :\n\
    COURS : dict = testing_lessons_generation()\n\
    DEBUGTP : str = 'testing'\n\
Expected return : next_lesson : dict =\n\
{'00:00': {\n\
    'Cours': 'Cours 1',\n\
    'Salle': 'Salle 1',\n\
    'Prof': 'Prof 1',\n\
    'Heure de début': '00:00',\n\
    'Heure de fin': '01:00'\n\
}}\n\
Take care of: Result of the function depend of actual hour"
    )
    print(
        f"RESULT FOR FUNCTION : next_lesson_for_tp: \n\
{next_lesson_for_tp(COURS, DEBUGTP)}"
    )
