# On importe selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import os
from webdriver_manager.chrome import ChromeDriverManager

# Définition des options de navigation
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--strat-maximised")
option.add_argument('--ignore-certificate-errors')
option.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(ChromeDriverManager().install(), options=option)

# On récupère la date
date = datetime.now()
annee = str(date.year)
conversionMois = {1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
                  7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"}
mois = conversionMois[date.month]
chemin = mois + "_" + annee
# print(chemin)

# On se place sur la page du mois concerné
browser.get('https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/' + chemin)

# On récupère les titres tombés le jour j
spanJour = browser.find_elements_by_xpath(
    '//div[@class="mw-parser-output"]/h2[2]/span')
jour = spanJour[0].text
for i, elem in enumerate(spanJour):
    print(elem.text)
liste = browser.find_elements_by_xpath(
    '//div[@class="mw-parser-output"]/ul[7]/li[0]')

# chanson1 = liste.find_elements_by_tag_name('a')
# chanson2 = liste.find_elements_by_tag_name('a')

# print(chanson1)
# print(chanson2)
