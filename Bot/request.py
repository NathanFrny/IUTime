"""Module contenant les fonctions permettant de récupérer les cours d'un TP"""
from __future__ import annotations
import logging
from datetime import datetime, date
from ics import Calendar
from pytz import timezone
from lesson import Lesson


def lessons_tp(t_p: str) -> list[Lesson]:
    """Return schedule for tp group concerned

    Args:
        t_p (str): tp group  concerned (like: BUT1TD1TPA)

    Returns:
        dict: dict representing the schedule
    """
    t_p = t_p.upper()
    logging.debug("tp's value = %s", t_p)

    ics_file: str = f"Calendars/{t_p}/ADECal.ics"
    logging.debug("Source's path : %s", ics_file)

    with open(ics_file, "r", encoding="utf-8") as file:
        ical_data: str = file.read()

    calendar: Calendar = Calendar(ical_data)

    lessons: list[Lesson] = []
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
            lessons.append(
                Lesson(
                    start_hour=start_hour,
                    end_hour=end_hour,
                    professor=teacher,
                    room=event.location,
                    t_p=t_p,
                    cours=event.description,
                )
            )
        else:
            logging.debug(
                "Error on event date's: %s | reference_date: %s",
                start_utc.date(),
                reference_date,
            )
    return lessons


def next_lesson_for_tp(lessons: list[Lesson], t_p: str) -> Lesson | None:
    """Return the next lesson regardless of the date

    Args:
        cours: lessons
        tp: TP code

    Returns:
        list[tuple]: represention of the lesson
    """

    next_lesson: Lesson = None

    date_: datetime = datetime.now()
    logging.debug("date = %s", date_)

    total_minutes: int = (date_.hour * 60) + date_.minute
    logging.debug("total_minutes = %s", total_minutes)

    schedule: list[tuple] = Lesson.sorting_schedule(lessons)

    for lesson in schedule:
        logging.debug("lesson: %s", lesson)
        lesson: Lesson
        # Conversion in total minutes
        minutes = lesson.start_hour.hour * 60 + lesson.start_hour.minute
        if total_minutes < minutes:
            return lesson

    if next_lesson is None:
        logging.error("Le TP %s n'a pas/plus de cours aujourd'hui", t_p.upper())
        raise RuntimeError(f"Le TP {t_p.upper()} n'a pas/plus de cours aujourd'hui")

    return next_lesson
