from ics import Calendar
from pytz import timezone
from calendar import datetime
from datetime import timedelta

# Chemin vers le fichier iCalendar
ics_file = 'Calendar/ADECal.ics'

# Lecture du fichier iCalendar
with open(ics_file, 'r', encoding="utf-8") as file:
    ical_data = file.read()

# Analyse du fichier iCalendar
calendar = Calendar(ical_data)

# Récupère la date du jour
reference_date = datetime.date.today()
reference_hour = datetime.datetime.now().hour
print(reference_date)
print(reference_hour)





# Renvoies les cours de la journée pour le TP mis en paramètre
def lessons_TP(tp: str):
    tp = tp.upper()
    lessons = {}
    listCours = [" CM", " DS", " PFT" , tp[-3:], tp[4:7], f"{tp[-3]} {tp[-1]}", f"{tp[-2] [-1]}", f"{tp[0:4]}"]
    
    for event in calendar.events:
        # Convertir la date de début en UTC + 2h pour se mettre à l'heure
        start_utc = event.begin.astimezone(timezone('UTC')) + timedelta(minutes=120) 
        # Convertir la date de fin en UTC + 2h pour se mettre à l'heure
        end_utc = event.end.astimezone(timezone('UTC')) + timedelta(minutes=120)   
        
        # Si l'évênement est aujourd'hui
        if start_utc.date() == reference_date:
            event.name = event.name.upper()
            if event.name[-3:] in listCours:
                
                start_hour = start_utc.strftime("%H:%M")
                end_hour = end_utc.strftime("%H:%M")
                
                # On récupère les profs du cours
                description = event.description
                lines = description.split('\n')
                # Suppression des lines contenant "BUT" ou des parenthèses
                teacher= [ligne for ligne in lines if "BUT" not in ligne and "(" not in ligne and ")" not in ligne and ligne.strip() != ""]
                
                # Si il y a un profs alors on récupère uniquement le teacheren string sinon on indique qu'il n'y a aucun prof
                if len(teacher) > 0:
                    teacher= teacher[0]
                else:
                    teacher= "Aucun prof"
                
                # On crée la valeur du dictionnaire contenant le cours (la clé est l'heure de début du cours)
                lessons[start_hour] = {"Cours" : event.name[:-3],
                                "Salle" : event.location,
                                "Prof" : teacher,
                                "Heure de fin" : end_hour}
    
    return lessons

def next_lessons(roles: list):
    
    lessons = {}
    
    # Extraction des valeurs comportant "BUT"
    but = [valeur for valeur in roles if "BUT" in valeur][0]

    # Extraction des valeurs comportant "TP"
    tp = [valeur for valeur in roles if "TP" in valeur][0]
    
    # Récupération du TD
    if tp == "TPA" or tp == "TPB":
        td = "TD1"
    if tp == "TPC" or tp == "TPD":
        td = "TD2"
    else:
        td = "TD3"
        
    # Récupération des valeurs HORRIBLE à checker
    if tp == "TPA":
        tdtp1 = "TP A"
        tdtp2 = "A 1"
        tdtp3 = "A 2"
    if tp == "TPB":
        tdtp1 = "TP B"
        tdtp2 = "B 1"
        tdtp3 = "B 2"
    if tp == "TPC":
        tdtp1 = "TP C"
        tdtp2 = "C 1"
        tdtp3 = "C 2"
    if tp == "TPD":
        tdtp1 = "TP D"
        tdtp2 = "D 1"
        tdtp3 = "D 2"
    if tp == "TPE":
        tdtp1 = "TP E"
        tdtp2 = "E 1"
        tdtp3 = "E 2"
        
        
        
    
    for event in calendar.events:
        
        # Convertir la date de début en UTC + 2h pour se mettre à l'heure
        start_utc = event.begin.astimezone(timezone('UTC')) + timedelta(minutes=120)
        print(start_utc)
        # Convertir la date de fin en UTC + 2h pour se mettre à l'heure
        end_utc = event.end.astimezone(timezone('UTC')) + timedelta(minutes=120)
        
        # Si l'évênement est aujourd'hui
        if start_utc.date() == reference_date:
            
            get_description = event.description
            split_lines = get_description.split('\n')
            description_but = [valeur for valeur in split_lines if "BUT" in valeur][0]

            if but == description_but[:4]:
            
                if event.name[-3:] == tp or event.name[-3:] == " CM" or event.name[-3:] == td or event.name[-3:] == " DS" or event.name[-3:] == " Ds" or event.name[-3:] == "PFT" or event.name[-3:] == tdtp1 or event.name[-3:] == tdtp2 or event.name[-3:] == tdtp3:
                

                    start_hour = start_utc.strftime("%H:%M")
                    end_hour = end_utc.strftime("%H:%M")

                    # On récupère les profs du cours
                    description = event.description
                    lines = description.split('\n')
                    # Suppression des lines contenant "BUT" ou des parenthèses
                    teacher= [ligne for ligne in lines if "BUT" not in ligne and "(" not in ligne and ")" not in ligne and ligne.strip() != ""]
                    # Si il y a un profs alors on récupère uniquement le teacheren string sinon on indique qu'il n'y a aucun prof
                    if len(teacher) > 0:
                        teacher= teacher[0]
                    else:
                        teacher= "Aucun prof"
                    # On crée la valeur du dictionnaire contenant le cours (la clé est l'heure de début du cours)
                    lessons[start_hour] = {"Cours" : event.name[:-3],
                                    "Salle" : event.location,
                                    "Prof" : teacher,
                                    "Heure de fin" : end_hour}
                    return lessons

def trie(cours_dict):
    sorted_dict = dict(sorted(cours_dict.items(), key=lambda x: x[0]))
    return sorted_dict


#print(trie(lessons_TP("BUT1TD2TPD")))
print(next_lessons(["ABC","BUT1", "Enseignant", "TPA"]))