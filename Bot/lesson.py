from __future__ import annotations
import logging
from discord import Embed, Colour
from constants import AUTHORS, LOGOPATH


class Lesson:
    """
    Représente un cours.

    Attr:
        start_hour (str): Heure de début du cours.
        end_hour (str): Heure de fin du cours.
        professor (str): Nom du professeur.
        room (str): Salle.
        t_p (str): Groupe TP concerné.
        cours (str): Nom du cours.
    """

    def __init__(
        self: Lesson,
        start_hour: str,
        end_hour: str,
        professor: str,
        room: str,
        t_p: str,
        cours: str,
    ):
        self._start_hour: str = start_hour
        self._end_hour: str = end_hour
        self._professor: str = professor
        self._room: str = room
        self._t_p: str = t_p
        self._cours: str = cours

    @property
    def start_hour(self) -> str:
        return self._start_hour

    @start_hour.setter
    def start_hour(self, hour: str):
        self._start_hour = str(hour)

    @property
    def end_hour(self) -> str:
        return self._end_hour

    @end_hour.setter
    def end_hour(self, hour: str):
        self._end_hour = str(hour)

    @property
    def professor(self) -> str:
        return self._professor

    @professor.setter
    def professor(self, professor: str):
        self._professor = professor

    @property
    def room(self) -> str:
        return self._room

    @room.setter
    def room(self, room: str):
        self._room = room

    @property
    def t_p(self) -> str:
        return self._t_p

    @t_p.setter
    def t_p(self, t_p: str):
        self._t_p = t_p

    @property
    def cours(self) -> str:
        return self._cours

    @cours.setter
    def cours(self, cours: str):
        self._cours = cours

    def __repr__(self):
        return (
            f"Cours: Début={self.start_hour}, Fin={self.end_hour}, "
            f"Prof={self.professor}, Cours={self.cours}, Salle={self.room}, TP={self.t_p}"
        )

    @staticmethod
    def embed_schedule_construct(
        title: str,
        color: int | Colour,
        schedule: list[Lesson],
        description: str | None,
        sign: bool = True,
    ) -> Embed:
        """Crée un Embed Discord représentant l'emplois du temps d'un étudiant.

        Args:
            title (str): Titre de l'Embed.
            color (int | Colour): Couleur de l'Embed.
            schedule (list[Lesson]): Liste de Cours.
            description (str | None): Description de l'Embed.
            sign (bool): Signature par CSquare (Default: True).

        Returns:
            Embed: Embed discord prêt à être envoyé.
        """
        embed: Embed = Embed(title=title, description=description, color=color)
        for lesson in schedule:
            logging.debug("lesson = %s", lesson)
            embed.add_field(
                name=lesson.cours,
                value=f"Début: {lesson.start_hour}\nSalle: {lesson.room}\nProfesseur: {lesson.professor}\nFin: {lesson.end_hour}\n\n",
                inline=False,
            )
        if sign:
            embed.set_thumbnail(url=LOGOPATH)
            embed.set_footer(text=f"{AUTHORS}")

        return embed

    @staticmethod
    def sorting_schedule(schedule: list[Lesson]) -> list[Lesson]:
        """Trie une liste de cours par ordre chronologique dans la journée.

        Args:
            schedule (list[Lesson]): Liste de cours.

        Returns:
            list[Lesson]: Liste de cours trié.
        """
        sorted_items = sorted(schedule, key=lambda x: x.start_hour)
        logging.debug("sorted_items = %s", sorted_items)

        return sorted_items
