# On importe selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import psycopg2

# Connexion à la base de données locale
conn = psycopg2.connect(host="localhost",
                        database="NOPLP",
                        user="postgres",
                        password="Objectifcentrale2019!")
cursor = conn.cursor()


# Définition des options de navigation
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--strat-maximised")
option.add_argument('--ignore-certificate-errors')
option.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(executable_path=str(
    os.getcwd())+"\chromedriver", options=option)

lienParent = 'https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/Liste_des_chansons_existantes'
browser.get(lienParent)

# On attend une seconde
time.sleep(1)
# Puis on clique sur le bouton accepter
button = browser.find_element_by_xpath(
    '//div[@class="NN0_TB_DIsNmMHgJWgT7U XHcr6qf5Sub2F2zBJ53S_"]')
button.click()

artistes = browser.find_elements_by_xpath('//*[@id="mw-content-text"]/div/h3')
nbArtistes = len(artistes)
print(str(nbArtistes) + " artistes à scraper")

for i in range(484, nbArtistes+1):
    chansons = browser.find_elements_by_xpath(
        '//*[@id="mw-content-text"]/div/ul[' + str(i) + ']/li')
    nbChansons = len(chansons)
    print(str(nbChansons) + " chansons à scraper pour cet artiste")

    for j in range(1, nbChansons+1):
        lienVersChanson = browser.find_element_by_xpath(
            '//*[@id="mw-content-text"]/div/ul[' + str(i) + ']/li[' + str(j) + ']/a')
        lienVersChanson.click()

        titre = browser.find_element_by_xpath('//*[@id="firstHeading"]').text
        titre = titre.replace("'", "''")
        annee = browser.find_element_by_xpath(
            '//*[@id="mw-content-text"]/div/p[3]').text[8:12]
        if len(annee) < 4 or annee[0] not in ['1', '2']:
            annee = "NULL"
        print("Artiste numéro : " + str(i) +
              ", chanson : " + titre + " sortie en " + annee)
        cursor.execute("INSERT INTO public.\"Chanson\"(titre, \"année\", id_artiste) VALUES ('" +
                       titre + "'," + annee + "," + str(i) + ");")

        browser.get(lienParent)

    conn.commit()
