from __future__ import annotations
from datetime import datetime, timedelta
from critical import Critical
import json


class Homework:
    def __init__(
        self: Homework,
        ressource: str,
        prof: str,
        importance: str | int,
        date_rendu: datetime,
        description: str,
        note: bool = False,
    ):
        if type(importance) == str:
            importance = importance.upper()
        self._ressource: str = ressource
        self._prof: str = prof
        match importance:
            case "BANALE":
                self._criticite: Critical = Critical.BANALE
            case "NORMAL":
                self._criticite: Critical = Critical.NORMAL
            case "CRITIQUE":
                self._criticite: Critical = Critical.CRITIQUE
            case 1:
                self._criticite: Critical = Critical.BANALE
            case 3:
                self._criticite: Critical = Critical.NORMAL
            case _:
                self._criticite: Critical = Critical.CRITIQUE

        self._date_rendu: datetime = date_rendu
        self._description: str = description
        self._note: bool = note
        self._outdated: bool = self.is_outdated()

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
        return f"Devoir(ressource={self._ressource}, prof={self._prof}, importance={self._criticite}, date_rendu={self._date_rendu}, description={self._description}, note={self._note}, outdated={self._outdated})"

    def is_outdated(self) -> bool:
        current_date: datetime = datetime.now()
        if current_date > self._date_rendu:
            self._outdated = True
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

    def criticite_compare(self) -> bool:
        """Compare the due date of the homework with current date and importance

        Returns:
            bool: True if current date and importance (in days) > due date, False otherwise
        """
        current_date = datetime.now()
        delta = timedelta(days=self.criticite.value)
        return (current_date + delta) >= self.date_rendu

    @staticmethod
    def fromjson(json_str: str) -> Homework:
        homework_dict: dict = json.loads(json_str)
        ressource = homework_dict.get("ressource")
        prof = homework_dict.get("prof")
        criticite = homework_dict.get("criticite")
        date_rendu = datetime.fromisoformat(homework_dict.get("date_rendu"))
        description = homework_dict.get("description")
        note = homework_dict.get("note", False)

        return Homework(ressource, prof, criticite, date_rendu, description, note)


if __name__ == "__main__":
    # Création d'un devoir
    homework1: Homework = Homework(
        "Mathématiques",
        "M. Dupont",
        "normal",
        datetime(2023, 6, 30, 15, 00),
        "Faire les exercices 1 à 5",
        note=True,
    )

    # Vérification des valeurs des attributs
    assert homework1.ressource == "Mathématiques"
    assert homework1.prof == "M. Dupont"
    assert homework1.criticite == Critical.NORMAL
    assert homework1.date_rendu == datetime(2023, 6, 30, 15, 00)
    assert homework1.description == "Faire les exercices 1 à 5"
    assert homework1.note == True
    assert homework1.outdated == False

    # Modification des attributs
    homework1.criticite = Critical.BANALE
    homework1.description = "Faire les exercices 1 à 10"
    homework1.outdated = True

    # Vérification des valeurs modifiées
    assert homework1.criticite == Critical.BANALE
    assert homework1.description == "Faire les exercices 1 à 10"
    assert homework1.outdated == True

    # Conversion en JSON
    json_data: str = json.dumps(homework1.tojson())

    # Création d'un nouvel objet Homework à partir du JSON
    homework2: Homework = Homework.fromjson(json_data)

    # Vérification que les deux objets sont identiques
    assert homework1.ressource == homework2.ressource
    assert homework1.prof == homework2.prof
    assert homework1.criticite == homework2.criticite
    assert homework1.date_rendu == homework2.date_rendu
    assert homework1.description == homework2.description
    assert homework1.note == homework2.note

    print("Tous les tests ont réussi avec succès.")
