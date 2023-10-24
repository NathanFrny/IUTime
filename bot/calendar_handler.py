"""This module handles the calendar events and the calendar file."""

import sqlite3
import asyncio

import requests


class CalendarHandler:
    """Class that handles the read and write of calendar events to the database.
    Also ensures the downloading of the calendar file from the APIs."""

    # --------------------------#
    #     Class constants      #
    # --------------------------#
    ICAL_URLS = {
        "BUT1TD1TPA": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc38732002143ffcc28a30e8c25ae0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT1TD1TPB": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214633da5846189fc9de0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT1TD2TPC": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214cb97491b201409c5e0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT1TD2TPD": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214b4c69b21f41db101e0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT1TD3TPE": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc38732002142edc9a35a1d5436ee0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT2TD1TPA": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214afa61ee6300d9346e0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT2TD1TPB": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc387320021454fe9d42b6752ce5e0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT2TD2TPC": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc387320021459430e2aefb27d40e0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT2TD2TPD": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214eba1f059caa03d5ae0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT2TD3TPAAPP": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214097a0191464d3295324cfcf2e9e6b435e05b7ab2457e00b4571f857a52dc5aa230f492d81d4f1a0fa96c4fad30084a42",
        "BUT2TD3TPBAPP": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc38732002145a3f91796c885729e0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT3AAPP": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214a86890e163ca034ee0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT3ATP1FI": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214a2f73a72523cc44be0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT3ATP2FI": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214a9bb6791dfafa87ee0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
        "BUT3BAPP": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc387320021412405c8e744f3509e0fa50826f0818af2370d544632bbb83906f45af276f59aec18424f8595af9f973866adc6bb17503",
    }

    TIMEOUT_SECONDS = 5  # Timeout for the requests to the API

    def __init__(self, db_conn: sqlite3.Connection):
        self.db_conn = db_conn
        self.db_cursor = db_conn.cursor()

        self.check_database()

    def check_database(self):
        """Ensures that the database contains the correct tables. If not, inits it."""
        self.db_cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='calendar'"
        )
        if self.db_cursor.fetchone() is None:
            self.init_database()

    def init_database(self):
        """Initializes the database by creating the calendar table."""
        self.db_cursor.execute(
            "CREATE TABLE IF NOT EXISTS calendar (tp TEXT PRIMARY KEY, calendar TEXT)"
        )
        self.db_conn.commit()

    async def update_calendars(self):
        """Updates the calendars by downloading the ical files from the API."""

        # Create asyncio tasks
        tasks = []
        for tp in self.ICAL_URLS:
            tasks.append(asyncio.create_task(self.download_calendar(tp)))

        # Wait for all tasks to finish
        await asyncio.wait(tasks)

    async def download_calendar(self, tp: str):
        """Downloads the calendar file from the API and writes it to the database."""

        # Get the calendar file from the API
        response = requests.get(
            self.ICAL_URLS[tp], timeout=self.TIMEOUT_SECONDS, verify=False
        )

        # Write the calendar file to the database
        self.db_cursor.execute(
            "UPDATE calendar SET calendar = ? WHERE tp = ?", (response.text, tp)
        )
        self.db_conn.commit()


if __name__ == "__main__":
    cal = CalendarHandler(sqlite3.connect("database.db"))
    asyncio.run(cal.update_calendars())
