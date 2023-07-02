from __future__ import annotations
import logging
from datetime import datetime, timedelta
from discord import Embed, Colour
from constants import AUTHORS, LOGOPATH


class Lesson:
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
    def start_hour(self, hour: str | int):
        self._start_hour = str(hour)

    @property
    def end_hour(self) -> str:
        return self._end_hour

    @end_hour.setter
    def end_hour(self, hour: str | int):
        self._end_time = str(hour)

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
            f"Lesson: start_date={self.start_hour}, end_date={self.end_hour}, "
            f"professor={self.professor}, cours={self.cours}, room={self.room}, tp={self.t_p}"
        )

    @staticmethod
    def embed_schedule_construct(
        title: str,
        color: int | Colour,
        schedule: list[Lesson],
        description: str | None,
        sign: bool = True,
    ) -> Embed:
        """Create a discord Embed object representing a student's shedule

        Args:
            title (str): title of the embed
            color (int | Colour): color of the embed
            schedule (list[Lesson]): schedule of student
            description (str | None): description of the embed
            sign (bool): signed by CSquare on demand, default True

        Returns:
            Embed: discord Embed object, ready to be sent
        """
        embed: Embed = Embed(title=title, description=description, color=color)
        for lesson in schedule:
            logging.debug("lesson = %s", lesson)
            debut: str = lesson.start_hour
            cours: str = lesson.cours
            salle: str = lesson.room
            prof: str = lesson.professor
            heure_fin: str = lesson.end_hour
            embed.add_field(
                name=cours,
                value=f"Début: {debut}\nSalle: {salle}\nProf: {prof}\nHeure de fin: {heure_fin}\n\n",
                inline=False,
            )
        if sign:
            embed.set_thumbnail(url=LOGOPATH)
            embed.set_footer(text=f"Écris par : {AUTHORS}")

        return embed

    @staticmethod
    def sorting_schedule(schedule: list[Lesson]) -> list[Lesson]:
        """Sorts the lessons list by start time order.

        Args:
            schedule (list[Lesson]): Representation of schedule.

        Returns:
            list[Lesson]: List of lessons sorted
        """
        sorted_items = sorted(schedule, key=lambda x: x.start_hour)
        logging.debug("sorted_items = %s", sorted_items)

        return sorted_items
