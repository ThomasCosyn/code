# On importe selenium
from selenium import webdriver
import selenium
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import psycopg2
import utils
from webdriver_manager.chrome import ChromeDriverManager

# Connexion à la base de données locale
conn, cur = utils.connexion()

# Variables liées aux tables SQL
idPassage, idEmission = utils.getSQLVariables(cur)


categories = {1: '50', 2: '40', 3: '30', 4: '20', 5: '10', 6: 'MC', 7: '20k'}

# Définition des options de navigation
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--strat-maximised")
option.add_argument('--ignore-certificate-errors')
option.add_argument('--ignore-ssl-errors')
option.add_argument('--log-level=3')
browser = webdriver.Chrome(ChromeDriverManager().install(), options=option)


lien = 'https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/Septembre_2022'

# Gestion du temps

# Année
annee = lien[-4:]
print("Année : " + annee)

# Mois
mois = {"décembre": 12, "janvier": 1,
        "février": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7, "août": 8, "septembre": 9, "octobre": 10, "novembre": 11}

browser.get(lien)

# On attend une seconde
time.sleep(1)
# Puis on clique sur le bouton accepter
button = browser.find_element_by_xpath(
    '//div[@class="NN0_TB_DIsNmMHgJWgT7U XHcr6qf5Sub2F2zBJ53S_"]')
button.click()


jours = browser.find_elements_by_xpath('//*[@id="mw-content-text"]/div/h2')
nbJours = len(jours)
u = 5

# On itère sur les journées
for i in range(4, nbJours+1):

    date = browser.find_element_by_xpath(
        '//*[@id="mw-content-text"]/div/h2[' + str(i) + ']').text
    dateListe = date.split(' ')

    # On enlève les primes et émissions particulières
    if len(dateListe) == 3:
        dateOk = annee + '-' + \
            str(mois[dateListe[2]]) + '-' + \
            dateListe[1].replace('1er', '1')
        print(dateOk)
        print("i = " + str(i) + ", u = " + str(u))

        chansons = []
        # C'est parti pour la première émission
        for j in range(1, 8):

            ligne = browser.find_element_by_xpath(
                '//*[@id="mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']').text

            if j <= 5 and 'non pris' not in ligne.lower():
                (c1, c2) = utils.getChoisieNonChoisie(u, j, browser)
                chansons.append((c1, c2))
                print(chansons)
                c1 = c1.replace("'", "''")
                # Pour la chanson choisie
                utils.setNewPassage(cur, dateOk, categories,
                                    j, idEmission, idPassage, True)
                idChanson = utils.getIdChanson(cur, c1)
                cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                            str(idChanson) + "', '" + str(idPassage) + "');")
                idPassage += 1
                # Pour la chanson non choisie
                c2 = c2.replace("'", "''")
                utils.setNewPassage(cur, dateOk, categories,
                                    j, idEmission, idPassage, False)
                idChanson = utils.getIdChanson(cur, c2)
                cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                            str(idChanson) + "', '" + str(idPassage) + "');")
                idPassage += 1

            if j == 6:
                MC = ligne.split(' : ')[1].replace("'", "''")
                chansons.append(MC)
                print(chansons)
                utils.setNewPassage(cur, dateOk, categories,
                                    j, idEmission, idPassage, True)
                idChanson = utils.getIdChanson(cur, MC)
                cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                            str(idChanson) + "', '" + str(idPassage) + "');")
                idPassage += 1

            if j == 7:
                (c1, c2) = utils.getChoisieNonChoisie(u, j, browser)
                chansons.append((c1, c2))
                print(chansons)
                # Pour la chanson choisie
                c1 = c1.replace("'", "''")
                utils.setNewPassage(cur, dateOk, categories,
                                    j, idEmission, idPassage, True)
                idChanson = utils.getIdChanson(cur, c1)
                cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                            str(idChanson) + "', '" + str(idPassage) + "');")
                idPassage += 1
                # Pour la chanson non choisie
                c2 = c2.replace("'", "''")
                utils.setNewPassage(cur, dateOk, categories,
                                    j, idEmission, idPassage, False)
                idChanson = utils.getIdChanson(cur, c2)
                cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                            str(idChanson) + "', '" + str(idPassage) + "');")
                idPassage += 1

        print(chansons)
        u += 1
        idEmission += 1
        chansons = []

        # Et c'est reparti pour la deuxième
        for j in range(1, 8):

            ligne = browser.find_element_by_xpath(
                '//*[@id="mw-content-text"]/div/ul[' + str(u) + ']/li[' + str(j) + ']').text

            if j <= 5 and 'non pris' not in ligne.lower():
                (c1, c2) = utils.getChoisieNonChoisie(u, j, browser)
                chansons.append((c1, c2))
                print(chansons)
                c1 = c1.replace("'", "''")
                # Pour la chanson choisie
                utils.setNewPassage(cur, dateOk, categories,
                                    j, idEmission, idPassage, True)
                idChanson = utils.getIdChanson(cur, c1)
                # print("idChanson = " + str(idChanson) + ", " + c1)
                cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                            str(idChanson) + "', '" + str(idPassage) + "');")
                idPassage += 1
                # Pour la chanson non choisie
                c2 = c2.replace("'", "''")
                utils.setNewPassage(cur, dateOk, categories,
                                    j, idEmission, idPassage, False)
                idChanson = utils.getIdChanson(cur, c2)
                # print("idChanson = " + str(idChanson) + ", " + c2)
                cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                            str(idChanson) + "', '" + str(idPassage) + "');")
                idPassage += 1

            if j == 6:
                MC = ligne.split(' : ')[1].replace("'", "''")
                chansons.append(MC)
                print(chansons)
                utils.setNewPassage(cur, dateOk, categories,
                                    j, idEmission, idPassage, True)
                idChanson = utils.getIdChanson(cur, MC)
                cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                            str(idChanson) + "', '" + str(idPassage) + "');")
                idPassage += 1

            if j == 7:
                (c1, c2) = utils.getChoisieNonChoisie(u, j, browser)
                chansons.append((c1, c2))
                print(chansons)
                # Pour la chanson choisie
                c1 = c1.replace("'", "''")
                utils.setNewPassage(cur, dateOk, categories,
                                    j, idEmission, idPassage, True)
                idChanson = utils.getIdChanson(cur, c1)
                cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                            str(idChanson) + "', '" + str(idPassage) + "');")
                idPassage += 1
                # Pour la chanson non choisie
                c2 = c2.replace("'", "''")
                utils.setNewPassage(cur, dateOk, categories,
                                    j, idEmission, idPassage, False)
                idChanson = utils.getIdChanson(cur, c2)
                cur.execute("INSERT INTO public.\"Chanson_Passage\"(\"Chanson_id\", \"Passage_id\")	VALUES ('" +
                            str(idChanson) + "', '" + str(idPassage) + "');")
                idPassage += 1

        print(chansons)
        idEmission += 1
        u += 1

        conn.commit()

    else:
        if len(dateListe) > 3:
            u += 6
