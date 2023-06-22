import logging


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

    sorted_items = sorted(cours_dict.items(), key=lambda x: x[0])
    logging.debug(f"sorted_items = {sorted_items}")

    return [(hour, lesson) for hour, lesson in sorted_items]
