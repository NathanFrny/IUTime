from ics import Calendar
from pytz import timezone
from calendar import datetime
from datetime import timedelta

# Chemin vers le fichier iCalendar
ics_file = './Calendar/ADECal.ics'

# Lecture du fichier iCalendar
with open(ics_file, 'r') as file:
    ical_data = file.read()

# Analyse du fichier iCalendar
calendar = Calendar(ical_data)

# Variables pour requêtes
myTP = "TPA"
myTD = "TD1"
TPA_mod_size = 0
TPA_only_mod_size = 0
TD1_mod_size = 0

# Parcourir les événements du calendrier
for event in calendar.events:
    # Convertir la date de début en UTC + 2h pour se mettre à l'heure
    start_utc = event.begin.astimezone(timezone('UTC')) + timedelta(minutes=120)

    # Convertir la date de fin en UTC + 2h pour se mettre à l'heure
    end_utc = event.end.astimezone(timezone('UTC')) + timedelta(minutes=120)

    # Récupère le nom de l'évênement actuel
    module_name = event.name
    
    # Vérifie le nombre de cours restants des étudiants du TPA
    if module_name[-3:] == myTP or module_name[-3:] == myTD or module_name[-3:] == " CM" or module_name[-3:] == " DS" or module_name[-3:] == "A 1" or module_name[-3:] == "A 2" or module_name[-3:] == " Ds" or module_name[-3:] == "PFT" or module_name[-3:] == "P A":
        TPA_mod_size += 1
    # Vérifie le nombre de cours restants des étudiants du TPA en TP
    if module_name[-3:] == myTP:
        TPA_only_mod_size += 1
    # Vérifie le nombre de cours restants des étudiants du TPA en TD
    if module_name[-3:] == myTD:
        TD1_mod_size += 1
        
print()
print("Nombre de cours restant pour le TPA :    ", TPA_mod_size)
print("Nombre de cours restant du TPA en TP :   ", TPA_only_mod_size)
print("Nombre de cours restant du TPA en TD :   ", TD1_mod_size)
print()