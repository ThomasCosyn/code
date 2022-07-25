# On importe selenium
from selenium import webdriver
import selenium
import selenium.common.exceptions
import time
from selenium.webdriver.common.action_chains import ActionChains
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
try:
    button = browser.find_element_by_xpath(
        '/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/a/tp-yt-paper-button')
    button.click()
except selenium.common.exceptions.NoSuchElementException:
    pass

# On met sur pause (Et je coupe le son)
pauseButton = browser.find_element_by_tag_name('video')
# print(pauseButton)
# print(type(pauseButton))
# browser.implicitly_wait(10)
# browser.execute_script("document.getElementsByTagName('video')[0].pause()")

# On récupère la durée
duree = browser.find_element_by_class_name('ytp-time-duration').text
print("Durée de la vidéo : {}".format(duree))

# On clique sur la vidéo pour mettre en pause
video = browser.find_element_by_id('player')
x_body_offset = video.location["x"]
y_body_offset = video.location["y"]
print("Body coordinates : {}, {}".format(x_body_offset, y_body_offset))
time.sleep(5)
actions = ActionChains(browser)
# actions.move_to_element_with_offset(
#     video, -x_body_offset, -y_body_offset).click()
actions.move_by_offset(30, 100).click().perform()
