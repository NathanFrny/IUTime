import logging
import datetime


def testing_lessons_generation() -> dict:
    """to tests others functions ONLY (useless to test this function)

    Returns:
        dict: Representation of a lesson for each hour of the day
    """
    cours: dict = {}
    for heure in range(0, 24):
        heure_debut = f"{heure:02d}:00"
        heure_fin = f"{heure+1:02d}:00"
        cours[heure_debut] = {
            "Cours": f"Cours {heure+1}",
            "Salle": f"Salle {heure+1}",
            "Prof": f"Prof {heure+1}",
            "Heure de début": heure_debut,
            "Heure de fin": heure_fin,
        }
    return cours


def sorting(cours_dict: dict) -> list[tuple]:
    """Sorts the dictionary keys time order.

    Args:
        cours_dict (dict): Representation of lessons.

    Returns:
        list[tuple]: List of tuples containing the string of an hour in index 0 and a dictionary of the lesson in index 1.
    """
    logging.debug(f"cours_dict = {cours_dict}")

    sorted_items = sorted(cours_dict.keys(), key=lambda x: x[0])
    logging.debug(f"sorted_items = {sorted_items}")
    teste = [(hour, lesson) for hour, lesson in sorted_items]
    for elt in teste:
        elt[0] = datetime()


if __name__ == "utils":
    from utils import *
    from rich import print

    SEPARATOR = (
        "-----------------------------------------------------------------------"
    )
    logging.basicConfig(level=logging.DEBUG)

    COURS = {
        "16:49": {
            "Cours": "Cours 1",
            "Salle": "Salle 1",
            "Prof": "Prof 1",
            "Heure de début": "16:49",
            "Heure de fin": "17:14",
        },
        "5:22": {
            "Cours": "Cours 1",
            "Salle": "Salle 1",
            "Prof": "Prof 1",
            "Heure de début": "5:22",
            "Heure de fin": "14:37",
        },
        "14:00": {
            "Cours": "Cours 1",
            "Salle": "Salle 1",
            "Prof": "Prof 1",
            "Heure de début": "14:00",
            "Heure de fin": "15:01",
        },
    }
    print(f"COURS = {COURS}")
    print(SEPARATOR)
    print(
        "sorting testing function:\n\
Args: \n\
    COURS :     dict = COURS\n\
Expected return:\n\
    sorted_dict : list = [('5:22', {'Cours': 'Cours 1',\n\
'Salle': 'Salle 1',\n\
'Prof': 'Prof 1',\n\
'Heure de début': '5:22',\n\
'Heure de fin': '14:37'}), \n\
    ('14:00', {'Cours': 'Cours 1',\n\
'Salle': 'Salle 1',\n\
'Prof': 'Prof 1',\n\
'Heure de début': '14:00',\n\
'Heure de fin': '15:01'}), \n\
('16:49', {'Cours': 'Cours 1',\n\
'Salle': 'Salle 1',\n\
'Prof': 'Prof 1',\n\
'Heure de début': '16:49',\n\
'Heure de fin': '17:14'})] \n\
        "
    )
    print(
        f"RESULT FOR FONCTION : sorting: \n\
{sorting(COURS)}"
    )
