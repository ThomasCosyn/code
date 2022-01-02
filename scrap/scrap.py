# On importe selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import os
from webdriver_manager.chrome import ChromeDriverManager
import utils

# Définition des options de navigation
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--strat-maximised")
option.add_argument('--ignore-certificate-errors')
option.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(ChromeDriverManager().install(), options=option)

# Connexion à la base
conn, cur = utils.connexion()

# Variables liées aux tables SQL
idPassage, idEmission = utils.getSQLVariables(cur)

# On récupère la date actuelle
dateActuelle = datetime.today().date()
cheminActuel = utils.chemin(dateActuelle)

# On récupère la date des 4 dernières chansons à 20k
lastDate = utils.getLastDate(cur)
if lastDate == "Erreur":
    raise Exception("Dernière date non complète")
chemin = utils.chemin(lastDate)
print(chemin)
print(cheminActuel)

buttonClicked = False

while lastDate < dateActuelle:

    # On se place sur la page du mois concerné
    browser.get('https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/' + chemin)

    # On attend une seconde
    time.sleep(1)
    if not buttonClicked:
        # Puis on clique sur le bouton accepter
        button = browser.find_element_by_xpath(
            '//div[@class="NN0_TB_DIsNmMHgJWgT7U XHcr6qf5Sub2F2zBJ53S_"]')
        button.click()
        buttonClicked = True

    jours = browser.find_elements_by_xpath('//*[@id="mw-content-text"]/div/h2')
    nbJours = len(jours)
    donneesRecoltees = False
    u = 1

    for i in range(2, nbJours + 1):

        date = browser.find_element_by_xpath(
            '//*[@id="mw-content-text"]/div/h2[' + str(i) + ']').text
        dateListe = date.split(' ')
        dateListe[1] = dateListe[1].replace('1er', '1')
        # Transformation de la date et affichage de la navigation
        dateOk = str(lastDate.year) + '-' + \
            str(utils.mois[dateListe[2]]) + '-' + \
            dateListe[1]
        print(dateOk)
        print("i = " + str(i) + ", u = " + str(u))

        # Si on est le jour suivant, que ce n'est pas un prime et que l'on a pas encore récolté les données (c'est-à-dire si on est au bon endroit)
        if int(dateListe[1]) > lastDate.day and not donneesRecoltees and len(dateListe) == 3:

            # Récupération des chansons des deux émissions
            for _ in range(2):
                utils.emission(browser, u, cur,
                               dateOk, idEmission, idPassage)
                u += 1
                idEmission += 1

            # Commit en base
            conn.commit()

        # Sinon on fait avancer le compteur u du bon nombre d'unités
        else:

            nbP = browser.find_elements_by_xpath(
                '/html/body/div[4]/div[2]/div[2]/main/div[3]/div/div/p')
            if nbP == 4:
                u += 4

    lastDate = utils.getLastDate(cur)
    if lastDate == "Erreur":
        raise Exception("Dernière date non complète")
