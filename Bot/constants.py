LOGOPATH = "https://i.imgur.com/VVhr2OF.png"
DATASOURCES = "JSON/index.json"
HOMEWORKSOURCES = "JSON/homeworks.json"
IUTSERVID = 1092412416811343872
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
    "BUT1-TPA": "BUT1TD1TPA",
    "BUT1-TPB": "BUT1TD1TPB",
    "BUT1-TPC": "BUT1TD2TPC",
    "BUT1-TPD": "BUT1TD2TPD",
    "BUT1-TPE": "BUT1TD3TPE",
    "BUT2-TPA": "BUT2TD1TPA",
    "BUT2-TPB": "BUT2TD1TPB",
    "BUT2-TPC": "BUT2TD2TPC",
    "BUT2-TPD": "BUT2TD2TPD",
    "BUT2-APP": "BUT2TD3TPAAPP",
    "BUT3-TPA": "BUT3ATP1FI",
    "BUT3-TPB": "BUT3ATP2FI",
    "BUT3-TPC": "BUT3AAPP",
    "BUT3-TPD": "BUT3BAPP",
}
TP_SCHEDULE_TO_DISCORD = {
    "BUT1TD1TPA": "BUT1-TPA",
    "BUT1TD1TPB": "BUT1-TPB",
    "BUT1TD2TPC": "BUT1-TPC",
    "BUT1TD2TPD": "BUT1-TPD",
    "BUT1TD3TPE": "BUT1-TPE",
    "BUT2TD1TPA": "BUT2-TPA",
    "BUT2TD1TPB": "BUT2-TPB",
    "BUT2TD2TPC": "BUT2-TPC",
    "BUT2TD2TPD": "BUT2-TPD",
    "BUT2TD3TPAAPP": "BUT2-APP",
    "BUT3ATP1FI": "BUT3-TPA",
    "BUT3ATP2FI": "BUT3-TPB",
    "BUT3AAPP": "BUT3-TPC",
    "BUT3BAPP": "BUT3-TPD",
}
DEFAULT_STRING_NO_LESSON = "Pas de cours prévu dans l'heure suivante"
NOTIFICATION_JSON_KEYS = [
    "next_lessons",  # Value for notification of the next lesson
    "homeworks",  # Value for notification of homeworks
]

TP_CONCERNED = {
    "BUT1 info": ("BUT1TD1TPA", "BUT1TD1TPB", "BUT1TD2TPC", "BUT1TD2TPD", "BUT1TD3TPE"),
    "BUT1 TPA": ["BUT1TD1TPA"],
    "BUT1 TPB": ["BUT1TD1TPB"],
    "BUT1 TPC": ["BUT1TD2TPC"],
    "BUT1 TPD": ["BUT1TD2TPD"],
    "BUT1 TPE": ["BUT1TD3TPE"],
    "BUT1 TD3": ["BUT1TD3TPE"],
    "BUT1 TD1": ("BUT1TD1TPA", "BUT1TD1TPB"),
    "BUT1 TD2": ("BUT1TD2TPC", "BUT1TD2TPD"),
    "BUT2 info": (
        "BUT2TD1TPA",
        "BUT2TD1TPB",
        "BUT2TD2TPC",
        "BUT2TD2TPD",
        "BUT2TD3TPAAPP",
        "BUT2TD3TPBAPP",
    ),
    "BUT2A FI": ("BUT2TD1TPA", "BUT2TD2TPC", "BUT2TD2TPD"),
    "BUT2A TPA": ["BUT2TD1TPA"],
    "BUT2B TPB": ["BUT2TD1TPB"],
    "BUT2A TPC": ["BUT2TD2TPC"],
    "BUT2A TPD": ["BUT2TD2TPD"],
    "BUT2 TD1": ("BUT2TD1TPA", "BUT2TD1TPB"),
    "BUT2 TD2": ("BUT2TD2TPC", "BUT2TD2TPD"),
    "BUT2 TPA APP": ["BUT2TD3TPAAPP"],
    "BUT2 TPB APP": ["BUT2TD3TPBAPP"],
    "BUT2 info App": ("BUT2TD3TPAAPP", "BUT2TD3TPBAPP"),
    "BUT3 info": ("BUT3AAPP", "BUT3ATP1", "BUT3ATP2", "BUT3BAPP"),
    "BUT3A FI": ("BUT3ATP1", "BUT3ATP2"),
    "BUT3A APP": ["BUT3AAPP"],
    "BUT3A TP1 FI": ["BUT3ATP1"],
    "BUT3A TP2 FI": ["BUT3ATP2"],
    "BUT3B APP/FI": ["BUT3BAPP"],
}

TP_SCHEDULE = {
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
AUTHORS = "C Square : Artu Florient, Bois Thimote, Bonnel Noah, Fourny Nathan, Prokopowicz Colin"

ZINCEID = 363011509564997642
TARGETED_HOUR_NOTIF_LESSONS = (1, 0)  # 1,0
TARGETED_HOUR_NOTIF_HOMEWORKS = (16, 26)  # 17,10


HELP = f"```Version 1\n\
Commands:\n\
schedule: Gives today schedule for the given TP, after 7pm gives tomorrow schedule\n\
    Args: (TP: str = '') | (day: int = 0)\n\
    TP (OPTIONNAL): Schedule asked for\n\
    day (OPTIONNAL): If you want a schedule for days in the futur\n\
    Exemple: /schedule BUT2TD2TPD 4\n\
    If you don't give any TP argument, use your TP rôle to give you your schedule\n\
\n\
homework: Gives the list of Homeworks depending of your TP role\n\
\n\
notif: To modify your notifications preference\n\
\n\
add_homework (Classroom representative ONLY): Add a new homework for your TP\n\
    Args: (ressource: str) | (prof: str) | (remember: str | int) | (date_rendue: date) | (description: str) | (note: bool = False)\n\
    ressource: module of the homework\n\
    prof: teacher\n\
    remember: str that represent the importance of the homework\n\
    date_rendue: deadline date\n\
    description: a small description of the homework\n\
    note (OPTIONNAL): True of it's a graded homework, False else\n\
    Exemple: /add_homework ressource: SAE prof: Synave member: critique date_rendu: 2023-09-29-15-45 description: SAE jeu vidéo note: true\n\
\n\
del_homework (Classroom representative ONLY): Delete an homework at a certain location\n\
    Args: (emplacement: int)\n\
    emplacement (OPTIONNAL): emplacement of the homework in the list (written from left to right then from top to bottom)\n\
    Exemple: /del_homework 2\n\
    If your emplacement = 0 OR if you didn't gave an emplacement, show your recorded homeworks\n\
```"

ADMIN_LIST = [363011509564997642, 238995072740229121, 534827724183699476]
IMPORTANT_FILES = [
    "JSON/homeworks.json",
    "JSON/index.json",
    "Logs/main_logs.txt",
    "Logs/discord_logs.txt",
]
