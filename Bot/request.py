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
        raise RuntimeError

    return next_lesson


async def schedule_task(task, planned_date: datetime) -> None:
    # if datetime.datetime.now() > planned_date:
    #     # TODO - faire des vrais classes d'erreur
    #     raise RuntimeError("Planned date is already passed")

    current_time: Datetime = Datetime.now()
    sleep_time: timedelta = planned_date - current_time
    logging.info(f"Scheduled to run {task} at {planned_date}")
    await asyncio.sleep(sleep_time.total_seconds())

    if iscoroutinefunction(task):
        return await task()
    else:
        return task()
