from bs4 import BeautifulSoup

html_content = '''
<div unselectable="on" id="inner69" class="eventText" style="position: relative; display: block; text-align: center; line-height: 110%;" tabindex="0" aria-owns="Planning" aria-label=" R2-05 réseaux TPE null 16h00 - 17h30 null  null BUT1 TPE null DESOMBRE Thierry null S128 null BÂTIMENT IUT null  null "><b unselectable="on" class="eventText">R2-05&nbsp;réseaux&nbsp;TPE</b><br>16h00&nbsp;-&nbsp;17h30<br><br>BUT1&nbsp;TPE<br>DESOMBRE&nbsp;Thierry<br>S128<br>BÂTIMENT&nbsp;IUT<br><br></div>
'''

soup = BeautifulSoup(html_content, 'html.parser')

# Récupérer le nom du cours
nom_cours = soup.b.text.strip()

# Récupérer l'heure du cours
heure_cours = soup.find('br').next_sibling.strip()

# Récupérer le TP concerné
tp_concerne = soup.find_all('br')[2].next_sibling.strip()

# Récupérer le nom du professeur
professeur = soup.find_all('br')[3].next_sibling.strip()

print("Nom du cours :", nom_cours)
print("Heure du cours :", heure_cours)
print("TP concerné :", tp_concerne)
print("Professeur :", professeur)
