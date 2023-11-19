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
    
    information_table_parameters = [
        "Powierzchnia", "Forma własności", "Liczba Pokoi",
        "Stan Wykończenia", "Piętro", "Balkon / ogród / taras",
        "Czynsz", "Miejsce parkingowe", "Obsługa zdalna", "Ogrzewanie"
    ]

    additional_info_parameters = [
        "Rynek", "Typ ogłoszeniodawcy", "Dostępne od",
        "Rok budowy", "Rodzaj zabudowy", "Okna",
        "Winda", "Media", "Zabezpieczenia",
        "Wyposażenie", "Informacje dodatkowe", "Materiał budynku"
    ]



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
            info_table_values   = []
            
            for table_param in information_table_parameters:
                try:
                    info_table_values.append(info_table.find("div", {"aria-label": f"{table_param}"}).find("div", {"data-testid": "table-value-area"}).text)
                except:
                    info_table_values.append("missing")

            m2                  = info_table_values[0]
            type_of_ownership   = info_table_values[1]
            rooms               = info_table_values[2]
            finishing_condition = info_table_values[3]
            floor               = info_table_values[4]
            balcony             = info_table_values[5]
            rent                = info_table_values[6]
            parking             = info_table_values[7]
            tele_control        = info_table_values[8]
            heating             = info_table_values[9]
            
            description         = soup.find("div", {"data-cy": "adPageAdDescription"}).text

            add_info_elem       = soup.find("div", {"data-testid":"ad.additional-information.table"})
            add_info_values     = []

            for additional_info_param in additional_info_parameters:
                try:
                    add_info_values.append(add_info_elem.find("div", {"data-testid":"table-value-extras_types"}).text)
                except:
                    add_info_values.append("missing")

            



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
