# On importe selenium
from selenium import webdriver
import selenium
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
browser = webdriver.Chrome(ChromeDriverManager().install(), options=option,)


lien = 'https://www.youtube.com/watch?v=Mpxaf3KPlcc'

browser.get(lien)
actions = ActionChains(browser)

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

# Si la vidéo fait 15 secondes, c'est une petite pub, on est obligé de la regarder
if duree == "0:15":
    print("Courte pub")
    time.sleep(15)
    actions.move_by_offset(30, 100).click().perform()
    duree = browser.find_element_by_class_name('ytp-time-duration').text
    print("Durée de la vidéo : {}".format(duree))
# Si la vidéo est plus longue, c'est une longue pub, on attent 5 secondes puis on la skip
elif cuts.timestampToSecs(duree) < 120:

    time.sleep(5)
    actions.move_by_offset(600, 332).click().perform()
    duree = browser.find_element_by_class_name('ytp-time-duration').text
    print("Durée de la vidéo : {}".format(duree))

# On récupère la durée de l'intro
dureeIntro = int(input("Entrer la durée de l'intro en nombre de secondes : "))

# On calcule les breaks
breaks = cuts.getBreaksInSecs(duree, dureeIntro)
print("Les breaks auront lieu au secondes suivantes : {}".format(breaks))

for i in range(1, 6):
    time.sleep(breaks[i] - breaks[i - 1])
    actions.move_by_offset(30, 100).click().perform()
    VoF = input("Avez-vous trouvé les bonnes paroles ? ")
    if VoF == "Non":
        break

print("Bravo vous avez gagné 20000€")

# On clique sur la vidéo pour mettre en pause
# video = browser.find_element_by_id('player')
# # x_body_offset = video.location["x"]
# # y_body_offset = video.location["y"]
# # print("Body coordinates : {}, {}".format(x_body_offset, y_body_offset))
# time.sleep(5)
# actions = ActionChains(browser)
# actions.move_by_offset(30, 100).click().perform()
