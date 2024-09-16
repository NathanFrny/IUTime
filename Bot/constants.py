LOGOPATH = "https://i.imgur.com/VVhr2OF.png"
DATASOURCES = "JSON/index.json"
HOMEWORKSOURCES = "JSON/homeworks.json"
IUTSERVID = 690169359490089059
LESSONS_HOUR = {
    8: "08:30",
    9: "10:00",
    11: "11:30",
    12: "13:00",
    14: "14:30",
    15: "16:00",
    16: "10:00",
    17: "17:30",
    18: "10:00",
}
TP_DISCORD_TO_SCHEDULE = {
    "BUT1-TPA": "BUT1TPA",
    "BUT1-TPB": "BUT1TPB",
    "BUT1-TPC": "BUT1TPC",
    "BUT1-TPD": "BUT1TPD",
    "BUT1-TPE": "BUT1TPE",
    "BUT2-TPA": "BUT2TPA",
    "BUT2-TPB": "BUT2TPB",
    "BUT2-TPC": "BUT2TPC",
    "BUT2-TPD": "BUT2TPD",
    "BUT2-APPA": "BUT2APPA",
    "BUT2-APPB": "BUT2APPB",
    "BUT3-TPA": "BUT3TPA",
    "BUT3-TPB": "BUT3TPB",
    "BUT3-AAPA": "BUT3APPA",
    "BUT3-AAPB": "BUT3APPB",
}
TP_SCHEDULE_TO_DISCORD = {
    "BUT1TPA": "BUT1-TPA",
    "BUT1TPB": "BUT1-TPB",
    "BUT1TPC": "BUT1-TPC",
    "BUT1TPD": "BUT1-TPD",
    "BUT1TPE": "BUT1-TPE",
    "BUT2TPA": "BUT2-TPA",
    "BUT2TPB": "BUT2-TPB",
    "BUT2TPC": "BUT2-TPC",
    "BUT2TPD": "BUT2-TPD",
    "BUT2APPA": "BUT2-APPA",
    "BUT2APPB": "BUT2-APPB",
    "BUT3TPA": "BUT3-TPA",
    "BUT3TPB": "BUT3-TPB",
    "BUT3APPA": "BUT3-AAPA",
    "BUT3APPB": "BUT3-AAPB",
}
DEFAULT_STRING_NO_LESSON = "Pas de cours prévu dans l'heure suivante"
NOTIFICATION_JSON_KEYS = [
    "next_lessons",  # Value for notification of the next lesson
    "homeworks",  # Value for notification of homeworks
]

TP_SCHEDULE = {
    "BUT1TPA": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214f10aa373cf877d6dea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT1TPB": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc38732002142879514c891f9d04ea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT1TPC": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc387320021403bb3cac7f4dce14ea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT1TPD": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214a4af781f8c47d1eaea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT1TPE": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214c55eb78c10620f88ea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT2TPA": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214c59041f6a31990f5ea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT2TPB": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc387320021476db9e7a9f83e128ea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT2TPC": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc38732002149f438338bd606a64ea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT2TPD": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214ae2f302cdcaacc0aea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT2APPA": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc38732002147c182b59da8ee9beea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT2APPB": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214d0925e84aaf5f6a4ea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT3TPA": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc38732002140e5b28b25d1fd66bea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT3TPB": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214d41d5d036c2ce769ea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT3APPA": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc3873200214b2dabd805fa66974ea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
    "BUT3APPB": "https://edt.univ-littoral.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?data=8241fc38732002144d408f0d671f0efbea8ccab428c89e097070b31f8deeace8c5fe00e25987de25e0fa50826f0818af42f6b661317fa297",
}
AUTHORS = "C Square : Artu Florient, Bois Thimote, Bonnel Noah, Fourny Nathan, Prokopowicz Colin"

TARGETED_HOUR_NOTIF_LESSONS = (3, 0)  # 3,0
TARGETED_HOUR_NOTIF_HOMEWORKS = (18, 10)  # 18,10


HELP = f"```\ 
Commandes:\n\ 
schedule: Donne l'emploi du temps d'aujourd'hui pour le TP donné ou récupéré automatiquement, après 19h donne l'emploi du temps du lendemain\n\ 
    Args: (TP: str = '') | (day: int = 0)\n\ 
    TP (OPTIONNEL): TP dont vous voulez l'emploi du temps\n\ 
    day (OPTIONNEL): Si vous voulez l'emploi du temps dans x jours\n\ 
    Exemple: /schedule BUT2TD2TPD 4\n\ 
    Si vous ne donnez aucun argument, votre TP est récupéré directement via vos rôles discord\n\ 
\n\ 
homework: Donne la liste des devoirs en fonction de votre rôle TP\n\ 
\n\ 
notif: Pour modifier vos préférences de notifications\n\ 
\n\ 
add_homework (Représentant de classe ou rôle 'devoir' UNIQUEMENT): Ajouter un nouveau devoir pour votre TP\n\ 
    Args: (ressource: str) | (prof: str) | (importance: str | int) | (date_rendue: date) | (description: str) | (note: bool = False)\n\ 
    ressource: module du devoir\n\ 
    prof: professeur\n\ 
    importance: chaîne de caractères qui représente l'importance du devoir\n\ 
    date_rendue: date de remise\n\ 
    description: une petite description du devoir\n\ 
    note (OPTIONNEL): True si c'est un devoir noté, False sinon\n\ 
    Exemple: /add_homework ressource: SAE prof: Synave importance: critique date_rendue: 2023-09-29-15-45 description: SAE jeu vidéo note: true\n\ 
\n\ 
del_homework (Représentant de classe ou rôle 'devoir' UNIQUEMENT): Supprimer un devoir à un emplacement donné\n\ 
    Args: (emplacement: int)\n\ 
    emplacement (OPTIONNEL): emplacement du devoir dans la liste (écrit de gauche à droite puis de haut en bas)\n\ 
    Exemple: /del_homework 2\n\ 
    Si votre emplacement = 0 OU si vous n'avez pas donné d'emplacement, affichez vos devoirs enregistrés\n\ 
```"


ADMIN_LIST = [363011509564997642, 238995072740229121, 534827724183699476]
IMPORTANT_FILES = [
    "JSON/homeworks.json",
    "JSON/index.json",
    "Logs/main_logs.txt",
    "Logs/discord_logs.txt",
]
