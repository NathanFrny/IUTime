"""Module contenant les fonctions permettant de récupérer les cours d'un TP"""
import logging
from datetime import datetime, date
from ics import Calendar
from pytz import timezone
from datetime import datetime, date
from utils import sorting_schedule


def lessons_tp(tp: str) -> dict:
    """Renvoies les cours de la journée pour le TP mis en paramètre"""
    tp = tp.upper()
    logging.debug("tp's value = %s", tp)

    ics_file: str = f"Calendars/{tp}/ADECal.ics"
    logging.debug("Source's path : %s", ics_file)

    with open(ics_file, "r", encoding="utf-8") as file:
        ical_data: str = file.read()

    calendar: Calendar = Calendar(ical_data)

    lessons: dict[str:dict] = {}
    reference_date: date = date.today()
    logging.debug("Reference_date = %s", reference_date)

    for event in calendar.events:
        logging.debug("event : %s", event)
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
                "Event name: %s | Event description: %s | start_hour: %s | end_hour: %s",
                event.name,
                description,
                start_hour,
                end_hour,
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
            logging.debug("teacher = %s", teacher)

            # Si il y a un profs alors on récupère uniquement le teacheren string sinon on indique qu'il n'y a aucun prof
            if len(teacher) > 0:
                teacher: str = teacher[0]
            else:
                teacher: str = "Aucun prof"
            logging.debug("teacher = %s", teacher)

            # On crée la valeur du dictionnaire contenant le cours (la clé est l'heure de début du cours)
            lessons[start_hour]: dict[str] = {
                "Cours": event.name[:-3],
                "Salle": event.location,
                "Prof": teacher,
                "Heure de début": start_hour,
                "Heure de fin": end_hour,
            }
        else:
            logging.debug(
                "Error on event date's: %s | reference_date: %s",
                start_utc.date(),
                reference_date,
            )
    return lessons


def next_lesson_for_tp(cours_dict: dict[str], tp: str) -> list[tuple] | None:
    """Return the next lesson regardless of the date

    Args:
        cours: lessons
        tp: TP code

    Returns:
        list[tuple]: represention of the lesson
    """

    next_lesson: list[tuple] = None

    date_: datetime = datetime.now()
    logging.debug("date = %s", date_)

    total_minutes: int = (date_.hour * 60) + date_.minute
    logging.debug("total_minutes = %s", total_minutes)

    cours: list[tuple] = sorting_schedule(cours_dict)

    for key in cours:
        logging.debug("value of key: %s", key)
        # Conversion in total minutes
        key: tuple[str]
        minutes = int(key[0].split(":")[0]) * 60 + int(key[0].split(":")[1])
        if total_minutes < minutes:
            return [key]

    if next_lesson is None:
        logging.error("Le TP %s n'a pas/plus de cours aujourd'hui", tp.upper())
        raise RuntimeError(f"Le TP {tp.upper()} n'a pas/plus de cours aujourd'hui")

    return next_lesson
