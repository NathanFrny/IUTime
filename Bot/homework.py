from __future__ import annotations
import json
from datetime import datetime, timedelta
from remember import Remember
from discord import Embed, Colour
from constants import AUTHORS, LOGOPATH


class Homework:
    """
    Classe représentant un devoir.

    Attr:
        ressource (str): Ressource associé au devoir.
        prof (str): Nom du Professeur ayant demandé ce devoir.
        importance (enum): Nombre de jour à l'avance auquel ce devoir sera envoyé en notification.
        date_rendu (datetime): Date de rendu du devoir.
        description (str): Description du devoir.
        note (bool, optional): Indique si le devoir est noté.
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
                self._remember: Remember = Remember.ONEDAY
            case "THREEDAY":
                self._remember: Remember = Remember.TREEDAY
            case "ALWAYS":
                self._remember: Remember = Remember.ALWAYS
            case "ONEWEEK":
                self._remember: Remember = Remember.ONEWEEK
            case 1:
                self._remember: Remember = Remember.ONEDAY
            case 3:
                self._remember: Remember = Remember.THREEDAY
            case 7:
                self._remember: Remember = Remember.ONEWEEK
            case _:
                self._remember: Remember = Remember.ALWAYS

        self._date_rendu: datetime = date_rendu
        self._description: str = description
        self._note: bool = note

    @property
    def ressource(self) -> str:
        return self._ressource

    @ressource.setter
    def ressource(self, value: str):
        self._ressource = value

    @property
    def prof(self) -> str:
        return self._prof

    @prof.setter
    def prof(self, value: str):
        self._prof = value

    @property
    def remember(self) -> Remember:
        return self._remember

    @remember.setter
    def remember(self, value: Remember):
        self._remember = value

    @property
    def date_rendu(self) -> datetime:
        return self._date_rendu

    @date_rendu.setter
    def date_rendu(self, value: datetime):
        self._date_rendu = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def note(self) -> bool:
        return self._note

    @note.setter
    def note(self, value: bool):
        self._note = value

    def __repr__(self):
        return f"Homework(ressource={self._ressource}, prof={self._prof}, \
remember={self._remember}, date_rendu={self._date_rendu}, \
description={self._description}, note={self._note}"

    def is_outdated(self) -> bool:
        """
        Regarde si la date de rendu du devoir est déjà passée.

        Returns:
            bool: True si la date est déjà passée, False sinon.
        """
        current_date: datetime = datetime.now()
        return current_date > self._date_rendu

    def tojson(self) -> dict:
        """
        Convertit l'objet en un format JSON

        Returns:
            dict: Dictionnaire compatible JSON
        """
        homework_dict = {
            "ressource": self._ressource,
            "prof": self._prof,
            "remember": self._remember.value,
            "date_rendu": self._date_rendu.isoformat(),
            "description": self._description,
            "note": self._note,
        }
        return homework_dict

    def remember_compare(self) -> bool:
        """Compare la date de rendu du devoir avec la date actuel ainsi que l'importante attribué au devoir.

        Returns:
            bool: True si la date actuelle + importance (en jour) est supérieur à la date de rendue du devoir, False sinon.
        """
        current_date = datetime.now()
        delta = timedelta(days=self._remember.value)
        return (current_date + delta) >= self._date_rendu

    @staticmethod
    def remembers_compare(list_homeworks: list[Homework]) -> list[Homework]:
        """Retourne la liste de voir avec uniquement les devoirs à rappeller en notification.

        Return:
            list[homework]: Liste de devoirs.
        """
        sorted_homeworks: list[Homework] = []
        for homework in list_homeworks:
            if homework.remember_compare():
                sorted_homeworks.append(homework)
        return sorted_homeworks

    @staticmethod
    def fromjson(json_str: str) -> Homework:
        """Crée un devoir à partir d'une chaîne de caractére (dictionnaire) au format JSON.

        Args:
            json_str (str): Chaîne de caractére au format JSON.

        Returns:
            Homework: Objet devoir créé.
        """
        homework_dict: dict = json.loads(json_str)
        ressource = homework_dict.get("ressource")
        prof = homework_dict.get("prof")
        Remember = homework_dict.get("remember")
        date_rendu = datetime.fromisoformat(homework_dict.get("date_rendu"))
        description = homework_dict.get("description")
        note = homework_dict.get("note", False)

        return Homework(ressource, prof, Remember, date_rendu, description, note)

    @staticmethod
    def sorting_homeworks(homework_list: list[Homework]) -> list[Homework]:
        """Trie une liste de devoir en plaçant en premiers les devoirs dont la date de rendue est dépassée.

        Args:
            homework_list (list[Homework]): Liste de devoirs.

        Returns:
            list[Homework]: Liste de devoirs triés.
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
        """Crée un Embed discord représentant plusieurs devoirs.
        Args:
            title (str): Titre de l'Embed.
            color (int | Colour): Couleur de l'Embed.
            homeworks (list[Homework]): Liste de devoirs.
            description (str | None): Description de l'Embed.
            sign (bool, optional): Signature par CSquare (Default: True).
            sorting (bool, optional): Trie des devoirs afin de placer les devoirs dont la date de rendue est dépassée en premiéres positions. (Default True).
        Returns:
            Embed: Embed Discord prêt à être envoyé.
        """
        if sorting:
            Homework.sorting_homeworks(homeworks)

        embed: Embed = Embed(
            title=title, description=description if description else "", color=color
        )
        for homework in homeworks:
            ressource: str = homework.ressource
            prof: str = homework.prof
            date_rendu: datetime = homework.date_rendu
            description: str = homework.description
            note: bool = homework.note

            embed.add_field(
                name=f"{ressource} {'DEADLINE PDEPASSE' if homework.is_outdated() else ''}",
                value=f"Prof: {prof}\Pour le: {date_rendu.day}/\
{date_rendu.month if len(str(date_rendu.month)) > 1 else '0'+str(date_rendu.month)}\
/{date_rendu.year} {date_rendu.hour}H{date_rendu.minute if len(str(date_rendu.minute)) > 1 else '0'+str(date_rendu.minute)}\
\nDescription: {description}\n{'Noté ? ' if note else ''}",
            )
        if sign:
            embed.set_thumbnail(url=LOGOPATH)
            embed.set_footer(text=f"{AUTHORS}")

        return embed
