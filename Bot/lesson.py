from __future__ import annotations
import logging
from discord import Embed, Colour
from constants import AUTHORS, LOGOPATH


class Lesson:
    """
    Representation of a Lesson

    Args:
        start_hour (str): start hour of the lesson
        end_hour (str): end hour of the lesson
        professor (str): name of the professor
        room (str): room number
        t_p (str): TP concerned
        cours (str): name of lesson
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
        """
        Get the start hour of the lesson.

        Returns:
            str: Start hour of the lesson.
        """
        return self._start_hour

    @start_hour.setter
    def start_hour(self, hour: str):
        """
        Set the start hour of the lesson.

        Args:
            hour (str | int): Start hour to be set for the lesson.
        """
        self._start_hour = str(hour)

    @property
    def end_hour(self) -> str:
        """
        Get the end hour of the lesson.

        Returns:
            str: End hour of the lesson.
        """
        return self._end_hour

    @end_hour.setter
    def end_hour(self, hour: str):
        """
        Set the end hour of the lesson.

        Args:
            hour (str | int): End hour to be set for the lesson.
        """
        self._end_hour = str(hour)

    @property
    def professor(self) -> str:
        """
        Get the name of the professor for the lesson.

        Returns:
            str: Name of the professor.
        """
        return self._professor

    @professor.setter
    def professor(self, professor: str):
        """
        Set the name of the professor for the lesson.

        Args:
            professor (str): Name of the professor to be set.
        """
        self._professor = professor

    @property
    def room(self) -> str:
        """
        Get the room number for the lesson.

        Returns:
            str: Room number of the lesson.
        """
        return self._room

    @room.setter
    def room(self, room: str):
        """
        Set the room number for the lesson.

        Args:
            room (str): Room number to be set for the lesson.
        """
        self._room = room

    @property
    def t_p(self) -> str:
        """
        Get the TP concerned for the lesson.

        Returns:
            str: TP concerned for the lesson.
        """
        return self._t_p

    @t_p.setter
    def t_p(self, t_p: str):
        """
        Set the TP concerned for the lesson.

        Args:
            t_p (str): TP to be set for the lesson.
        """
        self._t_p = t_p

    @property
    def cours(self) -> str:
        """
        Get the name of the lesson.

        Returns:
            str: Name of the lesson.
        """
        return self._cours

    @cours.setter
    def cours(self, cours: str):
        """
        Set the name of the lesson.

        Args:
            cours (str): Name of the lesson to be set.
        """
        self._cours = cours

    def __repr__(self):
        return (
            f"Lesson: start_hour={self.start_hour}, end_hour={self.end_hour}, "
            f"professor={self.professor}, lesson={self.cours}, room={self.room}, tp={self.t_p}"
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
                value=f"Start: {debut}\nRoom: {salle}\nTeacher: {prof}\nEnd: {heure_fin}\n\n",
                inline=False,
            )
        if sign:
            embed.set_thumbnail(url=LOGOPATH)
            embed.set_footer(text=f"{AUTHORS}")

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
