from __future__ import annotations
import json
from datetime import datetime, timedelta
from remember import Remember
from discord import Embed, Colour
from constants import AUTHORS, LOGOPATH


class Homework:
    """
    Class representing a homework.

    Args:
        ressource (str): Resource associated with the homework.
        prof (str): Professor in charge of the homework.
        importance (str | int): Importance of the homework,
                                can be a string ("BANALE", "NORMAL", "CRITIQUE")
                                or an integer (1, 3).
        date_rendu (datetime): Due date of the homework.
        description (str): Description of the homework.
        note (bool, optional): Indicates if the homework has been noted. Defaults to False.
    """

    def __init__(
        self: Homework,
        ressource: str,
        prof: str,
        importance: str | int,
        date_rendu: datetime,
        description: str,
        note: bool = False,
    ):
        if isinstance(importance, str):
            importance = importance.upper()
        self._ressource: str = ressource
        self._prof: str = prof
        match importance:
            case "ONEDAY":
                self._criticite: Remember = Remember.ONEDAY
            case "TREEDAY":
                self._criticite: Remember = Remember.TREEDAY
            case "ALWAYS":
                self._criticite: Remember = Remember.ALWAYS
            case "ONEWEEK":
                self._criticite: Remember = Remember.ONEWEEK
            case 1:
                self._criticite: Remember = Remember.ONEDAY
            case 3:
                self._criticite: Remember = Remember.TREEDAY
            case 7:
                self._criticite: Remember = Remember.ONEWEEK
            case _:
                self._criticite: Remember = Remember.ALWAYS

        self._date_rendu: datetime = date_rendu
        self._description: str = description
        self._note: bool = note

    @property
    def ressource(self) -> str:
        """
        Get the resource associated with the homework.

        Returns:
            str: Resource associated with the homework.
        """
        return self._ressource

    @ressource.setter
    def ressource(self, value: str):
        """
        Set the resource associated with the homework.

        Args:
            value (str): Resource to be associated with the homework.
        """
        self._ressource = value

    @property
    def prof(self) -> str:
        """
        Get the professor in charge of the homework.

        Returns:
            str: Professor in charge of the homework.
        """
        return self._prof

    @prof.setter
    def prof(self, value: str):
        """
        Set the professor in charge of the homework.

        Args:
            value (str): Professor to be set in charge of the homework.
        """
        self._prof = value

    @property
    def criticite(self) -> Remember:
        """
        Get the importance of the homework.

        Returns:
            Critical: Importance of the homework.
        """
        return self._criticite

    @criticite.setter
    def criticite(self, value: Remember):
        """
        Set the importance of the homework.

        Args:
            value (Critical): Importance to be set for the homework.
        """
        self._criticite = value

    @property
    def date_rendu(self) -> datetime:
        """
        Get the due date of the homework.

        Returns:
            datetime: Due date of the homework.
        """
        return self._date_rendu

    @date_rendu.setter
    def date_rendu(self, value: datetime):
        """
        Set the due date of the homework.

        Args:
            value (datetime): Due date to be set for the homework.
        """
        self._date_rendu = value

    @property
    def description(self) -> str:
        """
        Get the description of the homework.

        Returns:
            str: Description of the homework.
        """
        return self._description

    @description.setter
    def description(self, value: str):
        """
        Set the description of the homework.

        Args:
            value (str): Description to be set for the homework.
        """
        self._description = value

    @property
    def note(self) -> bool:
        """
        Get the note status of the homework.

        Returns:
            bool: True if the homework has been noted, False otherwise.
        """
        return self._note

    @note.setter
    def note(self, value: bool):
        """
        Set the note status of the homework.

        Args:
            value (bool): Note status to be set for the homework.
        """
        self._note = value

    def __repr__(self):
        return f"Homework(ressource={self._ressource}, prof={self._prof}, \
criticite={self._criticite}, date_rendu={self._date_rendu}, \
description={self._description}, note={self._note}"

    def is_outdated(self) -> bool:
        """
        Check if the homework is outdated.

        Returns:
            bool: True if the homework is outdated, False otherwise.
        """
        current_date: datetime = datetime.now()
        return current_date > self._date_rendu

    def tojson(self) -> dict:
        """
        Convert the homework object to a JSON-compatible dictionary.

        Returns:
            dict: JSON-compatible dictionary representing the homework object.
        """
        homework_dict = {
            "ressource": self._ressource,
            "prof": self._prof,
            "criticite": self._criticite.value,
            "date_rendu": self._date_rendu.isoformat(),
            "description": self._description,
            "note": self._note,
        }
        return homework_dict

    def criticite_compare(self) -> bool:
        """Compare the due date of the homework with current date and importance.

        Returns:
            bool: True if current date and importance (in days) > due date, False otherwise.
        """
        current_date = datetime.now()
        delta = timedelta(days=self._criticite.value, hours=12)
        return (current_date + delta) >= self._date_rendu

    @staticmethod
    def fromjson(json_str: str) -> Homework:
        """
        Create a Homework object from a JSON string.

        Args:
            json_str (str): JSON string representing the Homework object.

        Returns:
            Homework: Homework object created from the JSON string.
        """
        homework_dict: dict = json.loads(json_str)
        ressource = homework_dict.get("ressource")
        prof = homework_dict.get("prof")
        criticite = homework_dict.get("criticite")
        date_rendu = datetime.fromisoformat(homework_dict.get("date_rendu"))
        description = homework_dict.get("description")
        note = homework_dict.get("note", False)

        return Homework(ressource, prof, criticite, date_rendu, description, note)

    @staticmethod
    def sorting_homeworks(homework_list: list[Homework]) -> list[Homework]:
        """Sort a list of homeworks based on their outdated status.

        Args:
            homework_list (list[Homework]): List of Homework objects.

        Returns:
            list[Homework]: Sorted list of Homework objects
        """
        return sorted(homework_list, key=lambda hw: hw.is_outdated(), reverse=False)

    @staticmethod
    def embed_homework_construct(
        title: str,
        color: int | Colour,
        homeworks: list[Homework],
        description: str | None,
        sign: bool = True,
        sorting: bool = True,
    ) -> Embed:
        """Create a discord Embed object representing a student's homeworks

        Args:
            title (str): title of the embed
            color (int | Colour): color of the embed
            homeworks (list[Homework]): homeworks of student
            description (str | None): description of the embed
            sign (bool, optional): signed by CSquare on demand, default True
            sorting (bool, optional): sorting of homework to position them with outdated on top,
                                    default True
        Returns:
            Embed: discord Embed object, ready to be sent
        """
        if sorting:
            Homework.sorting_homeworks(homeworks)
        embed: Embed = Embed(
            title=title, description=description if description else "", color=color
        )
        for homework in homeworks:
            if homework.criticite_compare:
                ressource: str = homework.ressource
                prof: str = homework.prof
                date_rendu: datetime = homework.date_rendu
                description: str = homework.description
                note: bool = homework.note

                embed.add_field(
                    name=f"{ressource} {'DEADLINE PASSED' if homework.is_outdated() else ''}",
                    value=f"Teacher: {prof}\nFor: {date_rendu.day}/\
{date_rendu.month if len(str(date_rendu.month)) > 1 else '0'+str(date_rendu.month)}\
/{date_rendu.year} {date_rendu.hour}H{date_rendu.minute if len(str(date_rendu.minute)) > 1 else '0'+str(date_rendu.minute)}\
\nDescription: {description}\n{'Graded homework' if note else ''}",
                )
        if sign:
            embed.set_thumbnail(url=LOGOPATH)
            embed.set_footer(text=f"{AUTHORS}")

        return embed


