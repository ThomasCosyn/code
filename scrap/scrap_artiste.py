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

browser.get(
    'https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/Liste_des_chansons_existantes')

# On attend une seconde
time.sleep(1)
# Puis on clique sur le bouton accepter
button = browser.find_element_by_xpath(
    '//div[@class="NN0_TB_DIsNmMHgJWgT7U XHcr6qf5Sub2F2zBJ53S_"]')
button.click()


for i in range(3, 587):

    artiste = browser.find_element_by_xpath(
        '//div[@class="mw-parser-output"]/h3['+str(i)+']/span/b').text
    artiste = artiste.replace("'", "''")
    print(str(i) + ' : ' + artiste)
    if i > 580:
        cursor.execute(
            "INSERT INTO public.\"Artiste\" (id_artiste, artiste) VALUES (" + str(i) + ",'" + artiste + "');")
    if i % 50 == 0:
        conn.commit()

conn.commit()
