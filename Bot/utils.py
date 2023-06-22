import logging


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
