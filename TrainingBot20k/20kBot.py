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


lien = 'https://www.youtube.com/watch?v=Mpxaf3KPlcc'

browser.get(lien)

# On attend une seconde
time.sleep(1)
# Puis on clique sur le bouton accepter
try:
    button = browser.find_element_by_xpath(
        '/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/a/tp-yt-paper-button')
    button.click()
except selenium.common.exceptions.NoSuchElementException:
    pass

# On récupère la durée
duree = browser.find_element_by_class_name('ytp-time-duration').text
print("Durée de la vidéo : {}".format(duree))

# On récupère la durée de l'intro
dureeIntro = int(input("Entrer la durée de l'intro en nombre de secondes : "))

# On calcule les breaks
breaks = cuts.getBreaksInSecs(duree, dureeIntro)
print("Les breaks auront lieu au secondes suivantes : {}".format(breaks))

# On récupère le lecteur
pause = browser.find_element_by_xpath(
    '//*[@id="movie_player"]/div[28]/div[2]/div[1]/button')

for i in range(1, 6):
    print("Temps d'attente : {}s".format(breaks[i] - breaks[i - 1]))
    print("Attente")
    time.sleep(breaks[i] - breaks[i - 1])
    print("Fin de l'attente")

    # Coupure de la musique
    print("Coupure de la musique")
    actions = ActionChains(browser)
    actions.move_to_element_with_offset(pause, 2, 2).click().perform()
    VoF = input("Avez-vous trouvé les bonnes paroles ? ")

    # On a perdu, on quitte la boucle
    if VoF == "Non":
        break
    # On a gagné, on relance la musique
    # elif VoF == "Oui":
    print("Remise de la musique")
    actions = ActionChains(browser)
    actions.move_to_element_with_offset(pause, 2, 2).click().perform()


print("Bravo vous avez gagné 20000€")
