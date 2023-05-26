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





# Renvoies les cours de la journée pour le TP mis en paramètre
def lessons_TP(tp: str):
    tp = tp.upper()
    lessons = {}
    listCours = [" CM", " DS", " PFT" , tp[-3:], tp[4:7], f"{tp[-3]} {tp[-1]}", f"{tp[-2] [-1]}"]
    
    for event in calendar.events:
        # Convertir la date de début en UTC + 2h pour se mettre à l'heure
        start_utc = event.begin.astimezone(timezone('UTC')) + timedelta(minutes=1650) #120
        # Convertir la date de fin en UTC + 2h pour se mettre à l'heure
        end_utc = event.end.astimezone(timezone('UTC')) + timedelta(minutes=1650)   
        
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

def trie(cours_dict):
    sorted_dict = dict(sorted(cours_dict.items(), key=lambda x: x[0]))
    return sorted_dict


print(trie(lessons_TP("BUT1TD2TPD")))