import re
import json

from bs4 import BeautifulSoup

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from .otodom_engine import get_limit, go_to_next_page


def initiate_voivodeship_scrapage(voivodeship, output_filename):


    options = Options()
    # options.add_argument("--headless")
    #  options.add_argument('--disable-gpu')
    driver = Firefox(options=options)
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
            driver = Firefox(options=options)


        
    driver.quit()


def get_articles_list_from_page(driver, voivodeship):
    
    
    article_list = []

    
    lis = driver.find_elements(By.XPATH, '//li[.//article]')
    
    for li in lis:
        try: 
            soup                = BeautifulSoup(li.get_attribute('innerHTML'), "html.parser")
            url                 = soup.find('a')['href']

            driver.get("http://www.otodom.pl/" + url)

            src                 = driver.page_source
            id                  = url[-7:]


            # location
            location            = soup.find("div", {"data-testid":"ad.breadcrumbs"}).find_all("a") # dzielnica
            district            = location[-1]
            city                = location[5]

            info_table          = soup.find("div", {"data-testid": "ad.top-information.table"})

            m2                  = info_table.find("div", {"aria-label": "Powierzchnia"}).find("div", {"data-testid": "table-value-area"}).text
            type_of_ownership   = info_table.find("div", {"aria-label": "Forma własności"}).find("div", {"data-testid": "table-value-area"}).text
            rooms               = info_table.find("div", {"aria-label": "Liczba Pokoi"}).find("div", {"data-testid": "table-value-area"}).text
            finishing_condition = info_table.find("div", {"aria-label": "Stan Wykończenia"}).find("div", {"data-testid": "table-value-area"}).text
            floor               = info_table.find("div", {"aria-label": "Piętro"}).find("div", {"data-testid": "table-value-area"}).text
            balcony             = info_table.find("div", {"aria-label": "Balkon / ogród / taras"}).find("div", {"data-testid": "table-value-area"}).text
            rent                = info_table.find("div", {"aria-label": "Czynsz"}).find("div", {"data-testid": "table-value-area"}).text
            parking             = info_table.find("div", {"aria-label": "Miejsce parkingowe"}).find("div", {"data-testid": "table-value-area"}).text
            tele_control        = info_table.find("div", {"aria-label": "Obsługa zdalna"}).find("div", {"data-testid": "table-value-area"}).text
            heating             = info_table.find("div", {"aria-label": "Ogrzewanie"}).find("div", {"data-testid": "table-value-area"}).text
            
            description         = soup.find("div", {"data-cy": "adPageAdDescription"}).text
            



            print(id)

            # article_list.append({
            #     "id": url[-7:],
            #     "title": title,
            #     "total_price_pln": total_price,
            #     "price_per_m_pln": price_per_m,
            #     "area_in_meters": meters,
            #     "rooms": rooms,
            #     "location": location,
            #     "voivodeship": voivodeship,
            #     "url": url,
            #     "private": private
            
            # })

        except Exception as e:
            print("exception!", e)
            continue


    return article_list
