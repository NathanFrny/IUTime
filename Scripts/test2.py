from bs4 import BeautifulSoup

html_content_1 = '''<div unselectable="on" id="inner53" class="eventText" style="position: relative; display: block; text-align: center; line-height: 110%;" tabindex="0" aria-owns="Planning" aria-label=" R2-12 anglais TPD null 10h00 - 11h30 null  null BUT1 TPD null MALEC Pauline null S138 null BÂTIMENT IUT null  null "><b unselectable="on" class="eventText">R2-12&nbsp;anglais&nbsp;TPD</b><br>10h00&nbsp;-&nbsp;11h30<br><br>BUT1&nbsp;TPD<br>MALEC&nbsp;Pauline<br>S138<br>BÂTIMENT&nbsp;IUT<br><br></div>'''

html_content_2 = '''<div unselectable="on" id="inner16" class="eventText" style="position: relative; display: block; text-align: center; line-height: 110%;" tabindex="0" aria-owns="Planning" aria-label=" R2-09 Meth num TD1 null 08h30 - 10h00 null  null BUT1 TD1 null CHRETIEN Bernard null S135 null BÂTIMENT IUT null  null "><b unselectable="on" class="eventText">R2-09&nbsp;Meth&nbsp;num&nbsp;TD1</b><br>08h30&nbsp;-&nbsp;10h00<br><br>BUT1&nbsp;TD1<br>CHRETIEN&nbsp;Bernard<br>S135<br>BÂTIMENT&nbsp;IUT<br><br></div>'''

html_content_3 = '''<div unselectable="on" id="inner23" class="eventText" style="position: relative; display: block; text-align: center; line-height: 110%;" tabindex="0" aria-owns="Planning" aria-label=" S2 SAE TI TPD null 14h30 - 16h00 null  null BUT1 TPD null S137 null BÂTIMENT IUT null  null "><b unselectable="on" class="eventText">S2&nbsp;SAE&nbsp;TI&nbsp;TPD</b><br>14h30&nbsp;-&nbsp;16h00<br><br>BUT1&nbsp;TPD<br>S137<br>BÂTIMENT&nbsp;IUT<br><br></div>'''

def extract_course_info(html_content):
    
    soup = BeautifulSoup(html_content, 'html.parser')

    # Récupérer le nom du cours
    nom_cours = soup.b.text.strip()

    # Récupérer l'heure du cours
    heure_cours = soup.find('br').next_sibling.strip()

    # Récupérer le TP concerné
    tp_concerne = soup.find_all('br')[2].next_sibling.strip()

    # Récupérer le nom du professeur
    professeur = soup.find_all('br')[3].next_sibling.strip()
    
    # Récupère la salle
    salle_cours = soup.find_all('br')[4].next_sibling.strip()

    return {"Cours" : nom_cours,
            "Heures" : heure_cours,
            "TP" : tp_concerne,
            "Prof" : professeur,
            "Salle" : salle_cours}

# Exemple d'utilisation avec les nouvelles données HTML
course_info_1 = extract_course_info(html_content_1)
course_info_2 = extract_course_info(html_content_2)
course_info_3 = extract_course_info(html_content_3)

print("Informations du cours 1:")
print(course_info_1["Prof"])
print()

print("Informations du cours 2:")
print(str(course_info_2))
print()

print("Informations du cours 3:")
for key, value in course_info_3.items():
    print(value)
print()
