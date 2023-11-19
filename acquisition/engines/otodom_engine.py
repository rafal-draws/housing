import re
import json

import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def initiate_voivodeship_scrapage(voivodeship, output_filename):


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
            with open(f'./data/{output_filename}', 'a', encoding='utf-8') as file:
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

    
    lis = driver.find_elements(By.XPATH, '//li[.//article]')
    
    for li in lis:
        try: 
            soup = BeautifulSoup(li.get_attribute('innerHTML'), "html.parser")

            url = soup.find('a')['href']

            title = soup.find("span", {"data-cy":"listing-item-title"}).text
        
        
            meters = ''.join(re.findall(r'\d+', soup.find_all("span")[-1].text))
            rooms = ''.join(re.findall(r'\d+', soup.find_all("span")[-2].text))
            price_per_m = ''.join(re.findall(r'\d+', soup.find_all("span")[-3].text.replace("\xa0", "")))
            total_price = ''.join(re.findall(r'\d+', soup.find_all("span")[-4].text.replace("\xa0", "")))


            for data_split in li.text.split("\n"):
                if voivodeship in data_split:
                    location = data_split
                    break
                else:
                    location = "missing"
            for data_split in li.text.split("\n"):
                if "Oferta prywatna" in data_split:
                    private = "1"
                else:
                    private = "0"




            article_list.append({
                "id": url[-7:],
                "title": title,
                "total_price_pln": total_price,
                "price_per_m_pln": price_per_m,
                "area_in_meters": meters,
                "rooms": rooms,
                "location": location,
                "voivodeship": voivodeship,
                "url": url,
                "private": private
            })

        except Exception as e:
            print("exception!", e)
            continue


    return article_list
    




def get_limit(driver, url):
    driver.get(url)
    try:
        driver.find_element(By.XPATH, "//*[@id='onetrust-accept-btn-handler']").click()
    except Exception as e:
        "no js!! haha"

    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//nav[@data-cy='pagination']"))
        )
    list_of_a = element.find_elements(By.TAG_NAME, 'a')

    limit = list_of_a[-1].text

    return limit

def clean_the_json(filename):
    with open(f'../data/{filename}', 'r', encoding='utf-8') as f:
        data = f.read()
        data = data.replace("][", ',')

    with open(f'./data/cleaned_{filename}', 'w', encoding='utf-8') as f:
        f.write(data)
        print("'][' replaced with ','")
        f.close()