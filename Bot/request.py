from __future__ import annotations
from datetime import datetime, date, timedelta
from ics import Calendar
from pytz import timezone
from lesson import Lesson
import logging


def lessons_tp(t_p: str, logger_main, tomorrow: bool = False, day: int = 0) -> list[Lesson]:
    """Calcule et retourne l'emploi du temps du TP concerné

    Args:
        t_p (str): Groupe TP concerné (Ex: BUT1TD1TPA)
        tommorow (bool): Si l'on veut l'emploi du temps du lendemain.

    Returns:
        list[Lesson]: Liste de Cours 
    """
    logger_main.info(f"called | args: {t_p}, {tomorrow}")
    t_p = t_p.upper()
    logging.debug("tp's value = %s", t_p)

    ics_file: str = f"Calendars/{t_p}/{t_p}"
    logging.debug("Source's path : %s", ics_file)

    with open(ics_file, "r", encoding="utf-8") as file:
        ical_data: str = file.read()

    calendar: Calendar = Calendar(ical_data)

    lessons: list[Lesson] = []
    reference_date: date = date.today()
    reference_date += timedelta(hours=24*day)
    if tomorrow:
        reference_date += timedelta(hours=24)
    logging.debug("Reference_date = %s", reference_date)

    for event in calendar.events:
        logging.debug("event : %s", event)
        start_utc: datetime = event.begin.astimezone(timezone("Europe/Paris"))
        end_utc: datetime = event.end.astimezone(timezone("Europe/Paris"))

        if start_utc.date() == reference_date:
            logging.debug("Event date == reference_date")
            event.name = event.name.upper()

            start_hour: str = start_utc.strftime("%H:%M")
            end_hour: str = end_utc.strftime("%H:%M")

            # recover professor's name
            description: str = event.description
            lines: list[str] = description.split("\n")
            logging.debug(
                "Event name: %s | Event description: %s | start_hour: %s | end_hour: %s",
                event.name,
                description,
                start_hour,
                end_hour,
            )
            # cleaning lines
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

            if len(teacher) > 0:
                teacher: str = teacher[0]
            else:
                teacher: str = "No teachers"
            logging.debug("teacher = %s", teacher)

            lessons.append(
                Lesson(
                    start_hour=start_hour,
                    end_hour=end_hour,
                    professor=teacher,
                    room=event.location,
                    t_p=t_p,
                    cours=f"{event.name}",
                )
            )
        else:
            logging.debug(
                "Error on event date's: %s | reference_date: %s",
                start_utc.date(),
                reference_date,
            )
    return lessons


# def next_lesson_for_tp(lessons: list[Lesson], t_p: str) -> Lesson | None:
#    """Return the next lesson regardless of the date
#
#    Args:
#        cours: lessons
#        tp: TP code
#
#    Returns:
#        list[tuple]: represention of the lesson
#    """
#
#    next_lesson: Lesson = None
#
#    date_: datetime = datetime.now()
#    logging.debug("date = %s", date_)
#
#    total_minutes: int = (date_.hour * 60) + date_.minute
#    logging.debug("total_minutes = %s", total_minutes)
#
#    schedule: list[tuple] = Lesson.sorting_schedule(lessons)
#
#    for lesson in schedule:
#        logging.debug("lesson: %s", lesson)
#        lesson: Lesson
#        # Conversion in total minutes
#        minutes = lesson.start_hour.hour * 60 + lesson.start_hour.minute
#        if total_minutes < minutes:
#            return lesson
#
#    if next_lesson is None:
#        logging.error("Le TP %s n'a pas/plus de cours aujourd'hui", t_p.upper())
#        raise RuntimeError(f"Le TP {t_p.upper()} n'a pas/plus de cours aujourd'hui")
#
#    return next_lesson
#
