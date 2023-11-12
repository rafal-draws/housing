import configparser

import concurrent.futures

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By



def initiate_voivodeship_scrapage(voivodeship:str):

    options = webdriver.FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)


    iteration = 1
    url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}?viewType=listing&limit=72&page={iteration}"

    limit = int(get_limit(driver, url))
    print(limit)

    while iteration < limit:
        go_to_next_page(driver, iteration, voivodeship)
        get_articles(driver)
        iteration += 1
        
    driver.quit()





def go_to_next_page(driver, page, voivodeship):
    url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}?viewType=listing&limit=72&page={page}"
    driver.get(url)

def get_articles(driver):
    articles = driver.find_elements(By.XPATH, "//li[@data-cy='listing-item']")
    print("current amount of articles: ", len(articles))    

def get_limit(driver, url):
    driver.get(url)
    try:
        driver.find_element(By.XPATH, "//*[@id='onetrust-accept-btn-handler']").click()
    except Exception as e:
        print(e)

    navigation = driver.find_element(By.XPATH, "//nav[@data-cy='pagination']")
    list_of_a = navigation.find_elements(By.TAG_NAME, 'a')

    limit = list_of_a[-1].text

    return limit