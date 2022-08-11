# On importe selenium
from selenium import webdriver
import selenium.common.exceptions
import time
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import cuts

# Définition des options de navigation
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--strat-maximised")
option.add_argument('--ignore-certificate-errors')
option.add_argument('--ignore-ssl-errors')
option.add_argument('--log-level=3')
browser = webdriver.Chrome(ChromeDriverManager().install(), options=option,)


lien = input("Entrer l'url de la chanson : ")

browser.get(lien)

# On attend une seconde
time.sleep(1)
# Puis on clique sur le bouton accepter
try:
    button = browser.find_element_by_xpath(
        '/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/a/tp-yt-paper-button')
    button.click()
except selenium.common.exceptions.NoSuchElementException:
    try:
        button = browser.find_element_by_xpath(
            '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button')
        button.click()
    except selenium.common.exceptions.NoSuchElementException:
        pass

# Gestion de la pub
pubOuPas = input("Y a-t-il une pub ?")

# On récupère la durée
browser.implicitly_wait(1)
duree = browser.find_element_by_class_name('ytp-time-duration').text
if duree == "":
    try:
        duree = browser.find_element_by_xpath(
            "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[27]/div[2]/div[1]/div[1]/span[2]/span[3]").text
    except selenium.common.exceptions.NoSuchElementException:
        pass
if duree == "":
    duree = input(
        "Nous n'avons pas pu saisir la durée, veuillez la rentrer manuellement : ")
print("Durée de la vidéo : {}".format(duree))

# On récupère la durée de l'intro
dureeIntro = int(input("Entrer la durée de l'intro en nombre de secondes : "))

# On calcule les breaks
breaks = cuts.getBreaksInSecs(duree, dureeIntro)
dilatation = 1.2
breaks = [b*dilatation for b in breaks]
print("Les breaks auront lieu au secondes suivantes : {}".format(breaks))
gains = ["0€", "1000€", "2000€", "5000€", "10000€", "20000€"]
nbMots = ["2 ou 3", "4 ou 5", "6 à 8", "9 à 12", "13 à 18"]

# On récupère le lecteur
try:
    pause = browser.find_element_by_xpath(
        '//*[@id="movie_player"]/div[28]/div[2]/div[1]/button')
    print("Récupération par xpath 1")
except selenium.common.exceptions.NoSuchElementException:
    try:
        pause = browser.find_element_by_xpath(
            '//*[@id="movie_player"]/div[25]/div[2]/div[1]/button')
        print("Récupération par xpath 2")
    except selenium.common.exceptions.NoSuchElementException:
        try:
            pause = browser.find_element_by_class_name(
                "ytp-play-button_ytp-button")
            print("Récupération par la class")
        except selenium.common.exceptions.NoSuchElementException:
            try:
                pause = browser.find_element_by_id("ytd-player")
                print("Récupération par l'id")
            except selenium.common.exceptions.NoSuchElementException:
                try:
                    pause = browser.find_element_by_xpath(
                        "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player")
                    print("Récupération par xpath 3")
                except selenium.common.exceptions.NoSuchElementException:
                    pass

for i in range(1, 6):
    # print("Temps d'attente : {}s".format(breaks[i] - breaks[i - 1]))
    # print("Attente")
    time.sleep(breaks[i] - breaks[i - 1])
    # print("Fin de l'attente")

    # Coupure de la musique
    # print("Coupure de la musique")
    actions = ActionChains(browser)
    actions.move_to_element_with_offset(pause, 2, 2).click().perform()
    print(nbMots[i - 1] + " mots à trouver")
    VoF = input("Avez-vous trouvé les bonnes paroles ? ")

    # On a perdu, on quitte la boucle
    if VoF == "Non":
        i = i - 1
        break
    actions = ActionChains(browser)
    actions.move_to_element_with_offset(pause, 2, 2).click().perform()


print("Bravo vous avez gagné {}".format(gains[i]))
