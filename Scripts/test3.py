from ics import Calendar
from pytz import timezone
from calendar import datetime
from datetime import timedelta

# Chemin vers le fichier iCalendar
ics_file = 'Calendar/ADECal.ics'

# Date de référence pour la conversion (par exemple, la date actuelle)
reference_date = datetime.date.today()

# Lecture du fichier iCalendar
with open(ics_file, 'r') as file:
    ical_data = file.read()

# Analyse du fichier iCalendar
calendar = Calendar(ical_data)

# Fuseau horaire de référence (par exemple, le fuseau horaire local)
reference_timezone = timezone('Europe/Paris')

# Parcourir les événements du calendrier
for event in calendar.events:
    # Convertir la date de début en UTC
    start_utc = event.begin.astimezone(timezone('UTC')) + timedelta(minutes=120)

    # Convertir la date de fin en UTC
    end_utc = event.end.astimezone(timezone('UTC')) + timedelta(minutes=120)

    print("Titre :", event.name)
    print("Date de début (UTC) :", start_utc)
    print("Date de fin (UTC) :", end_utc)
    print("Description :", event.description)
    # Comparer la date actuel avec la date de début du module pour filtrer les événements au jour même
    #if start_utc.date() == reference_date:

