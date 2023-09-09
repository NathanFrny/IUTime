TOKEN = "MTExMDk2NzMxODU1MDQzMzgyMw.GiO2NB.1Gevd3Q159xq0hvItQd016xH97EnSP4RpaMofI"
LOGOPATH = "https://i.imgur.com/zNMQ14u.png"
DATASOURCES = "index.json"
HOMEWORKSOURCES = "homeworks.json"
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
    "BUT2-TPC" : "BUT2TD2TPC",
    "BUT2-TPD" : "BUT2TD2TPD",
    "BUT2-APP" : "BUT2TPAAPP"
}
TP_SCHEDULE_TO_DISCORD = {
    "BUT2TD2TPC" : "BUT2-TPC",
    "BUT2TD2TPD" : "BUT2-TPD",
    "BUT2TPAAPP" : "BUT2-APP"
}
DEFAULT_STRING_NO_LESSON = "Pas de cours prévu dans l'heure suivante"
NOTIFICATION_JSON_KEYS = [
    "next_lesson",  # Value for notification of the next lesson
    "homeworks",  # Value for notification of homeworks
]

TP_CONCERNED = {"BUT1 info" : ("BUT1TD1TPA", "BUT1TD1TPB", "BUT1TD2TPC", "BUT1TD2TPD", "BUT1TD3TPE"),
                "BUT1 TPA" : ["BUT1TD1TPA"],
                "BUT1 TPB" : ["BUT1TD1TPB"],
                "BUT1 TPC" : ["BUT1TD2TPC"],
                "BUT1 TPD" : ["BUT1TD2TPD"],
                "BUT1 TPE" : ["BUT1TD3TPE"],
                "BUT1 TD3" : ["BUT1TD3TPE"],
                "BUT1 TD1" : ("BUT1TD1TPA", "BUT1TD1TPB"),
                "BUT1 TD2" : ("BUT1TD2TPC", "BUT1TD2TPD"),
                "BUT2 info" : ("BUT2TD1TPA", "BUT2TD1TPB", "BUT2TD2TPC", "BUT2TD2TPD", "BUT2TPAAPP", "BUT2TPBAPP"),
                "BUT2A FI" : ("BUT2TD1TPA", "BUT2TD2TPC", "BUT2TD2TPD"),
                "BUT2A TPA" : ["BUT2TD1TPA"],
                "BUT2B TPB" : ["BUT2TD1TPB"],
                "BUT2A TPC" : ["BUT2TD2TPC"],
                "BUT2A TPD" : ["BUT2TD2TPD"],
                "BUT2 TD1" : ("BUT2TD1TPA", "BUT2TD1TPB"),
                "BUT2 TD2" : ("BUT2TD2TPC", "BUT2TD2TPD"),
                "BUT2 TPA APP" : ["BUT2TPAAPP"],
                "BUT2 TPB APP" : ["BUT2TPBAPP"],
                "BUT2 info App" : ("BUT2TPAAPP", "BUT2TPBAPP"),
                "BUT3 info" : ("BUT3AAPP", "BUT3ATP1", "BUT3ATP2", "BUT3BAPP"),
                "BUT3A FI" : ("BUT3ATP1", "BUT3ATP2"),
                "BUT3A APP": ["BUT3AAPP"],
                "BUT3A TP1 FI" : ["BUT3ATP1"],
                "BUT3A TP2 FI" : ["BUT3ATP2"],
                "BUT3B APP/FI" : ["BUT3BAPP"]}

AUTHORS = "C Square : Bonnel Noah, Fourny Nathan, Artu Florient, Thimoté Bois, Colin Prokopowicz"
ZINCEID = 363011509564997642
TARGETED_HOUR = (3, 0)
