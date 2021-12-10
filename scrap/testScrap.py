import utils
from selenium import webdriver
import os

# Définition des options de navigation
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("--strat-maximised")
option.add_argument('--ignore-certificate-errors')
option.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(executable_path=str(
    os.getcwd())+"\chromedriver", options=option)

lien = 'https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/Juin_2020'

browser.get(lien)

# print(utils.getChoisieNonChoisie(3, 1, browser))
tafete = browser.find_element_by_xpath(
    '//*[@id="mw-content-text"]/div/ul[4]/li[2]/a[2]').text
lafete = browser.find_element_by_xpath(
    '//*[@id="mw-content-text"]/div/ul[4]/li[2]/a[1]').text
lesfete = browser.find_elements_by_xpath(
    '//*[@id="mw-content-text"]/div/ul[4]/li[2]/a')

print(len(lesfete))

print(lesfete[0].text)
print(lesfete[1].text)
