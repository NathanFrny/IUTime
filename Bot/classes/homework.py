from __future__ import annotations
from datetime import datetime
from critical import Critical


class Homework:
    def __init__(
        self: Homework,
        ressource: str,
        prof: str,
        criticite: Critical,
        date_rendu: datetime,
        description: str,
        note: bool = False,
    ):
        self._ressource: str = ressource
        self._prof: str = prof
        self._criticite: Critical = criticite
        self._date_rendu: datetime = date_rendu
        self._description: str = description
        self._note: bool = note
        self._outdated: bool = False

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
    def criticite(self) -> Critical:
        return self._criticite

    @criticite.setter
    def criticite(self, value: Critical):
        self._criticite = value

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

    @property
    def outdated(self) -> bool:
        return self._outdated

    @outdated.setter
    def outdated(self, value: bool):
        self._outdated = value

    def __repr__(self):
        return f"Devoir(ressource={self._ressource}, prof={self._prof}, criticite={self._criticite}, date_rendu={self._date_rendu}, description={self._description}, note={self._note}, outdated={self._outdated})"

    def is_outdated(self) -> bool:
        current_date = datetime.now().date()
        return current_date > self._date_rendu

    def mark_outdated(self):
        self._outdated = True

    def tojson(self) -> dict:
        homework_dict = {
            "ressource": self._ressource,
            "prof": self._prof,
            "criticite": self._criticite.value,
            "date_rendu": self._date_rendu.isoformat(),
            "description": self._description,
            "note": self._note,
            "outdated": self._outdated,
        }
        return homework_dict
