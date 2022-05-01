# On importe selenium
from matplotlib.pyplot import pause
from selenium import webdriver
import selenium
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import psycopg2
from webdriver_manager.chrome import ChromeDriverManager

# Définition des options de navigation
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--strat-maximised")
option.add_argument('--ignore-certificate-errors')
option.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(ChromeDriverManager().install(), options=option)


lien = 'https://www.youtube.com/watch?v=lKLQzlJwgtQ'

browser.get(lien)

# On attend une seconde
time.sleep(1)
# Puis on clique sur le bouton accepter
button = browser.find_element_by_xpath(
    '/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[5]/div[2]/ytd-button-renderer[2]/a')
button.click()

# On rentre dans le iframe de lecture de vidéo
# browser.switch_to.frame(0)

# On met sur pause (Et je coupe le son)
# pauseButton = browser.find_element_by_xpath(
#     '//*[@id="movie_player"]/div[26]/div[2]/div[1]/button')
# #pauseButton = browser.find_element_by_('ytp-play-button ytp-button')
# browser.execute_script("arguments[0].click();", pauseButton)
# pauseButton.click()
pauseButton = browser.find_element_by_tag_name('video')
print(pauseButton)
print(type(pauseButton))
browser.implicitly_wait(10)
browser.execute_script("document.getElementsByTagName('video')[0].pause()")

# On récupère la durée
# duree = browser.find_element_by_xpath(
#     '//*[@id="movie_player"]/div[26]/div[2]/div[1]/div[1]/span[2]/span[3]').text
# print(duree)
