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

# Gestion du pop-up d'arrivée sur le site
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

    # Récupération du calendrier
    cal = utils.calendrier(browser)
    mauvaisJours, speciales = cal

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

        # Si c'est un mauvais jour, on ne fait rien
        if dateListe[1] in mauvaisJours:
            print("Le {0} est un jour où l'émission a été annulée, je ne fais rien".format(
                dateListe[1]))

        # Si c'est une émission spéciale, il y a en général 4 duels donc on incrémente de 4 la variable u
        elif dateListe[1] in speciales and len(dateListe) > 3:
            print("Le {0} il y a eu une émission spéciale, j'incrémente donc la variable u de 4".format(
                dateListe[1]))
            u += 5

        # Sinon on est un jour postérieur au dernier jour de récupération, que l'on a pas encore récolté les données et que c'est bien une émission classique, on récupère les données
        elif int(dateListe[1]) > lastDate.day and not donneesRecoltees and len(dateListe) == 3:

            # Récupération des chansons des deux émissions
            for _ in range(2):
                idPassage = utils.emission(browser, u, cur,
                                           dateOk, idEmission, idPassage)
                print(idPassage)
                u += 1
                idEmission += 1

            # Commit en base
            conn.commit()
            donneesRecoltees = True

        # Sinon c'est une émission classique, on incrémente u de 2
        else:
            print("Le {0} il y a eu une émission classique, on incrémente u de 2".format(
                dateListe[1]))
            u += 2

    # Mise à jour de la variable lastDate
    lastDate = utils.getLastDate(cur)
    if lastDate == "Erreur":
        raise Exception("Dernière date non complète")

    # Si on est un premier de mois, on change de page
    if lastDate.day == 1:
        chemin = utils.chemin(lastDate)
