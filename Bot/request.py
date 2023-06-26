import logging
from ics import Calendar
from pytz import timezone
from datetime import datetime as Datetime, date
from utils import sorting_schedule


# Renvoies les cours de la journée pour le TP mis en paramètre
def lessons_TP(tp: str) -> dict:
    print("lessons_TP")
    tp = tp.upper()
    logging.debug(
        f"({Datetime.now()}) | request.py lessons_TP function : tp's value = {tp} | {type(tp)}"
    )

    ics_file: str = f"Calendars/{tp}/ADECal.ics"
    logging.debug(
        f"({Datetime.now()}) | request.py lessons_TP function : Source's path : {ics_file} | {type(ics_file)}"
    )

    with open(ics_file, "r", encoding="utf-8") as file:
        ical_data: str = file.read()

    calendar: Calendar = Calendar(ical_data)

    lessons: dict[str:dict] = {}
    reference_date: date = date.today()
    logging.debug(
        f"({Datetime.now()}) request.py lessons_TP function : Reference_date = {reference_date} | {type(reference_date)}"
    )

    for event in calendar.events:
        logging.debug(
            f"({Datetime.now()}) request.py lessons_TP function : event : {event} | {type(event)}"
        )
        start_utc: Datetime = event.begin.astimezone(timezone("Europe/Paris"))
        end_utc: Datetime = event.end.astimezone(timezone("Europe/Paris"))

        # Si l'évênement est aujourd'hui
        if start_utc.date() == reference_date:
            logging.debug(
                f"({Datetime.now()}) request.py lessons_TP function : Event is today"
            )
            event.name = event.name.upper()

            start_hour: str = start_utc.strftime("%H:%M")
            end_hour: str = end_utc.strftime("%H:%M")

            # On récupère les profs du cours
            description: str = event.description
            lines: list[str] = description.split("\n")
            logging.debug(
                f"({Datetime.now()}) request.py lessons_TP function : event_name = {event.name} | {type(event.name)}\n\
({Datetime.now()}) request.py lessons_TP function : start_hour = {start_hour} | {type(start_hour)}\n\
({Datetime.now()}) request.py lessons_TP function : end_hour = {end_hour} | {type(end_hour)}\n\
({Datetime.now()}) request.py lessons_TP function : description = {description} | {type(description)}"
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
            logging.debug(
                f"({Datetime.now()}) request.py lessons_TP function : teacher = {teacher} | {type(teacher)}"
            )

            # Si il y a un profs alors on récupère uniquement le teacheren string sinon on indique qu'il n'y a aucun prof
            if len(teacher) > 0:
                teacher: str = teacher[0]
            else:
                teacher: str = "Aucun prof"
            logging.debug(
                f"({Datetime.now()}) request.py lessons_TP function : teacher = {teacher} | {type(teacher)}"
            )

            # On crée la valeur du dictionnaire contenant le cours (la clé est l'heure de début du cours)
            lessons[start_hour]: dict[str] = {
                # TODO - Créer un objet "cours"
                "Cours": event.name[:-3],
                "Salle": event.location,
                "Prof": teacher,
                "Heure de début": start_hour,
                "Heure de fin": end_hour,
            }
        else:
            logging.debug(
                f"({Datetime.now()}) request.py lessons_TP function : Error on event date's : {str(start_utc.date())} | {type(start_utc.date())}"
            )
    return lessons


def next_lesson_for_tp(cours_dict: dict[str], tp: str) -> list[tuple] | None:
    print(next_lesson_for_tp)
    """Return the next lesson regardless of the date

    Args:
        cours: lessons
        tp: TP code

    Returns:
        list[tuple]: represention of the lesson
    """

    next_lesson: list[tuple] = None

    date_: Datetime = Datetime.now()
    logging.debug(
        f"({Datetime.now()}) request.py next_lesson_for_tp function : date = {date_} | {type(date_)}"
    )

    total_minutes: int = (date_.hour * 60) + date_.minute
    logging.debug(
        f"({Datetime.now()}) request.py next_lesson_for_tp function : total_minutes = {total_minutes} | {type(total_minutes)}"
    )

    cours: list[tuple] = sorting_schedule(cours_dict)

    for key in cours:
        logging.debug(
            f"({Datetime.now()}) request.py next_lesson_for_tp function : value of key: {key} | {type(key)}"
        )
        # Conversion in total minutes
        key: tuple[str]
        minutes = int(key[0].split(":")[0]) * 60 + int(key[0].split(":")[1])
        if total_minutes < minutes:
            return [key]
        else:
            pass

    if next_lesson is None:
        logging.error(
            f"({Datetime.now()}) request.py next_lesson_for_tp function : Le TP {tp} n'a pas/plus de cours aujourd'hui"
        )
        raise RuntimeError

    return next_lesson
