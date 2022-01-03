from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import utils
import time

# Test de calendrier
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get('https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/Décembre_2021')
time.sleep(1)
button = browser.find_element_by_xpath(
    '//div[@class="NN0_TB_DIsNmMHgJWgT7U XHcr6qf5Sub2F2zBJ53S_"]')
button.click()
cal = utils.calendrier(browser)
print(cal[0])
print(cal[1])
