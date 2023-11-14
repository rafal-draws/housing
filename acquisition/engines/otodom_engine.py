import re
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def initiate_voivodeship_scrapage(voivodeship:str):

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    voivodeship_articles = []

    iteration = 1
    url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}?viewType=listing&limit=72&page={iteration}"
    limit = int(get_limit(driver, url))

    print("limit is: ", limit)


    while iteration < limit:

        go_to_next_page(driver, iteration, voivodeship)
        current_page_articles = get_articles_list_from_page(driver, voivodeship)
        for article in current_page_articles:
            voivodeship_articles.append(article)
        print(f"Currently scraping:\n {voivodeship}, page {iteration}, found {len(voivodeship_articles)}")
        iteration += 1

        if iteration % 10 == 0:
            with open('./data/data.json', 'a', encoding='utf-8') as file:
                json.dump(voivodeship_articles, file, ensure_ascii=False, indent=4)
                file.close()
            voivodeship_articles = []
        
        if iteration % 25 == 0:
            driver.quit()
            driver = webdriver.Firefox(options=options)


        
    driver.quit()

    


def go_to_next_page(driver, page, voivodeship):
    url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}?viewType=listing&limit=72&page={page}"
    driver.get(url)

def get_articles_list_from_page(driver, voivodeship):
    
    article_list = []

    articles = driver.find_elements(By.TAG_NAME, 'article')
    
    for i in articles:
        try: 
            soup = BeautifulSoup(i.get_attribute('innerHTML'), "html.parser")

            title = soup.find("span", {"data-cy":"listing-item-title"}).text
        
            data = soup.find_all("div")[3].text.replace(u'\xa0', u' ').replace(' ', '').split("zł")
            data.append(re.findall(r'\d+(?:,\d+)?', data[-1])[1])
            data.append(re.findall(r'\d+(?:,\d+)?', data[2])[0])
        

            for data_split in i.text.split("\n"):
                if voivodeship in data_split:
                    location = data_split
                    break
                else:
                    location = "missing"

            article_list.append({
                "title": title,
                "price_pln": data[0],
                "price_pln_per_m": data[1],
                "area": data[3],
                "rooms": data[4],
                "location": location,
                "voivodeship": voivodeship
            })

        except Exception as e:
            print(f"exception occured, skipping a record")
            continue


    return article_list
    




def get_limit(driver, url):
    driver.get(url)
    try:
        driver.find_element(By.XPATH, "//*[@id='onetrust-accept-btn-handler']").click()
    except Exception as e:
        print(e)

    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//nav[@data-cy='pagination']"))
        )
    list_of_a = element.find_elements(By.TAG_NAME, 'a')

    limit = list_of_a[-1].text

    return limit