# IUTime
A Discord bot that can read a schedule and respond to user queries.

---
Made by Artu Florient, Bonnel Noah, Fourny Nathan

---------------------------------------------------------------------
To tests functions: 
Copy/paste the following code to got some tests on functions then execute testing.py

For main.py:
    if __name__ == "main":
        from rich import print

        SEPARATOR = (
            "-----------------------------------------------------------------------"
        )
        logging.basicConfig(level=logging.DEBUG)
        PATH_TO_JSON: str = "TestingSources/index.json"
        SERVERID = 1092412416811343872

        print(f"PATH_TO_JSON : str = {PATH_TO_JSON}")
        print(SEPARATOR)

        print(
            "get_notified_users testing function:\n\
Args: \n\
    PATH_TO_JSON :     str = 'TestingSources/index.json'\n\
Expected return:\n\
    ['363011509564997642', '479649694033641502', '534827724183699476']\n\
Take care of : nothing\n\
    "
    )
        print(
            f"RESULT FOR FUNCTION : get_notified_users: \n\
{get_notified_users(PATH_TO_JSON)}"
    )

-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
For request.py
    if __name__ == "request":
        from utils import *
        from rich import print

        SEPARATOR = (
            "-----------------------------------------------------------------------"
        )
        logging.basicConfig(level=logging.DEBUG)

        DEBUGTP = "testing"
        COURS = testing_lessons_generation()

        print(
            f"DEBUGTP = {DEBUGTP}\n\
COURS = {COURS}"
    )
        print(SEPARATOR)
        print(
            "lessons_TP testing function:\n\
Args: \n\
    DEBUGTP :     str = 'testing'\n\
Expected return:\n\
    lessons : dict = { \n\
'08:00': { \n\
    'Cours': 'Mathematics', \n\
    'Salle': 'A101', \n\
    'Prof': 'Mr. Dupont', \n\
    'Heure de début': '08:00', \n\
    'Heure de fin': '09:30' }, \n\
'09:30': { \n\
    'Cours': 'Physics', \n\
    'Salle': 'B202', \n\
    'Prof': 'Mrs. Martin', \n\
    'Heure de début': '09:30', \n\
    'Heure de fin': '11:00' }, \n\
'12:00': { \n\
    'Cours': 'Computer Science', \n\
    'Salle': 'C303', \n\
    'Prof': 'Mr. Smith', \n\
    'Heure de début': '12:00', \n\
    'Heure de fin': '13:00' }, \n\
'14:00': { \n\
    'Cours': 'Chemistry', \n\
    'Salle': 'D404', \n\
    'Prof': 'Ms. Johnson', \n\
    'Heure de début': '14:00', \n\
    'Heure de fin': '15:30' } \n\
}\n\
Take care of: The test dates may not correspond to the dates indicated in the events in the Calendars/TESTING/ADECal.ics file."
    )
        print(
            f"RESULT FOR FONCTION : lesson_TP: \n\
{lessons_TP(DEBUGTP)}"
    )
        print(SEPARATOR)
        print(
            "next_lesson_for_tp testing function:\n\
Args :\n\
    COURS : dict = testing_lessons_generation()\n\
    DEBUGTP : str = 'testing'\n\
Expected return : next_lesson : dict =\n\
{'00:00': {\n\
    'Cours': 'Cours 1',\n\
    'Salle': 'Salle 1',\n\
    'Prof': 'Prof 1',\n\
    'Heure de début': '00:00',\n\
    'Heure de fin': '01:00'\n\
}}\n\
Take care of: Result of the function depend of actual hour"
    )
        print(
            f"RESULT FOR FUNCTION : next_lesson_for_tp: \n\
{next_lesson_for_tp(COURS, DEBUGTP)}"
    )

-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------

For utils.py
    if __name__ == "utils":
        from rich import print

        SEPARATOR = (
            "-----------------------------------------------------------------------"
        )
        logging.basicConfig(level=logging.DEBUG)

        COURS = {
            "16:49": {
                "Cours": "Cours 1",
                "Salle": "Salle 1",
                "Prof": "Prof 1",
                "Heure de début": "16:49",
                "Heure de fin": "17:14",
            },
            "05:22": {
                "Cours": "Cours 1",
                "Salle": "Salle 1",
                "Prof": "Prof 1",
                "Heure de début": "5:22",
                "Heure de fin": "14:37",
            },
            "14:00": {
                "Cours": "Cours 1",
                "Salle": "Salle 1",
                "Prof": "Prof 1",
                "Heure de début": "14:00",
                "Heure de fin": "15:01",
            },
        }
        print(f"COURS = {COURS}")
        print(SEPARATOR)
        print(
            "sorting testing function:\n\
Args: \n\
    COURS :     dict = COURS\n\
Expected return:\n\
    sorted_dict : list = [('05:22', {'Cours': 'Cours 1',\n\
'Salle': 'Salle 1',\n\
'Prof': 'Prof 1',\n\
'Heure de début': '5:22',\n\
'Heure de fin': '14:37'}), \n\
    ('14:00', {'Cours': 'Cours 1',\n\
'Salle': 'Salle 1',\n\
'Prof': 'Prof 1',\n\
'Heure de début': '14:00',\n\
'Heure de fin': '15:01'}), \n\
('16:49', {'Cours': 'Cours 1',\n\
'Salle': 'Salle 1',\n\
'Prof': 'Prof 1',\n\
'Heure de début': '16:49',\n\
'Heure de fin': '17:14'})] \n\
        "
    )
        print(
            f"RESULT FOR FONCTION : sorting: \n\
{sorting(COURS)}"
    )

