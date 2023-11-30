import json
import csv
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def initiate_voivodeship_scrapage(voivodeship, output_filename, filetype):


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)



    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.otodom.pl/")
    print(driver.page_source)

    if driver:
        print("driver initiated")
    else:
        print("driver couldn't initiate")

    header = ["id", "price", "voivodeship", "district", "city", "m2", "type_of_ownership", "rooms",
              "finishing_condition", "floor", "balcony", "rent", "parking", "heating",
              "market", "advertiser_type", "free_from", "build_year", "building_type",
              "windows_type", "lift", "media_types", "security_types", "equipment_types",
              "extras_types", "building_material", "url"]

    if filetype == "csv":
        with open(output_filename, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerow(header)
            file.close()



    iteration = 1
    url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}?viewType=listing&limit=72&page={iteration}"
    time.sleep(10)
    
    limit = int(get_limit(driver, url))

    print("limit is: ", limit)

    voivodeship_articles = []

    while iteration < limit:

        go_to_next_page(driver, iteration, voivodeship)
        current_page_articles = get_articles_list_from_page(driver, voivodeship)

        for article in current_page_articles:
            voivodeship_articles.append(article)
        print(f"Currently scraping:\n {voivodeship}, page {iteration}, found {len(voivodeship_articles)}")
        iteration += 1

        if filetype == "json":

            if iteration % 10 == 0:
                with open(output_filename, 'a', encoding='utf-8') as file:
                    json.dump(voivodeship_articles, file, ensure_ascii=False, indent=4)
                    file.close()
                voivodeship_articles = []


        if filetype == "csv":
            if iteration % 5 == 0:
                with open(output_filename, 'a', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file, delimiter='|')
                    writer.writerows(voivodeship_articles)
                voivodeship_articles = []




        if iteration % 5 == 0:
            driver.quit()
            driver = webdriver.Chrome(options=chrome_options)


        
    driver.quit()


def get_articles_list_from_page(driver, voivodeship:str):
    
    
    article_list = []

    urls = []
    current_page_src = driver.page_source
    soup = BeautifulSoup(current_page_src, "html.parser")
    lis = soup.select('li:has(article)')

    for elem in lis:
        urls.append(elem.find('a')['href'])



    information_table_parameters = [
        "table-value-area", "table-value-building_ownership", "table-value-rooms_num",
        "table-value-construction_status", "table-value-floor", "table-value-outdoor",
        "table-value-rent", "table-value-car", "table-value-heating"
    ]

    additional_info_parameters = [
        "table-value-market", "table-value-advertiser_type", "table-value-free_from",
        "table-value-build_year", "table-value-building_type", "table-value-windows_type",
        "table-value-lift", "table-value-media_types", "table-value-security_types",
        "table-value-equipment_types", "table-value-extras_types", "table-value-building_material"
    ]



    for article_url in urls:
        try: 

            driver.get("http://www.otodom.pl/" + article_url)

            src                 = driver.page_source

            soup                = BeautifulSoup(src, "html.parser")

            try:
                price           = soup.find("strong", {"data-cy":"adPageHeaderPrice"}).text
            except:
                price           = "0 zł"


            info_table          = soup.find("div", {"data-testid": "ad.top-information.table"})
            info_table_values   = []
            
            for table_param in information_table_parameters:
                try:
                    info_table_values.append(info_table.find("div", {"data-testid": f"{table_param}"}).text)
                except:
                    info_table_values.append("missing")

            add_info_elem       = soup.find("div", {"data-testid":"ad.additional-information.table"})
            add_info_values     = []

            for additional_info_param in additional_info_parameters:
                try:
                    add_info_values.append(add_info_elem.find("div", {"data-testid":f"{additional_info_param}"}).text)
                except:
                    add_info_values.append("missing")


            id                  = article_url[-7:]
            
            location            = soup.find("div", {"data-testid":"ad.breadcrumbs"}).find_all("a")
            district            = location[-1].text
            city                = location[5].text

            m2                  = info_table_values[0]
            type_of_ownership   = info_table_values[1]
            rooms               = info_table_values[2]
            finishing_condition = info_table_values[3]
            floor               = info_table_values[4]
            balcony             = info_table_values[5]
            rent                = info_table_values[6]
            parking             = info_table_values[7]
            heating             = info_table_values[8]

            # description         = soup.find("div", {"data-cy": "adPageAdDescription"}).text

            article = [id, price, voivodeship, district,
                city, m2, type_of_ownership,
                rooms, finishing_condition, floor,
                balcony, rent, parking, heating, article_url]

            for param in add_info_values:
                article.append(param)

            # article.append(description)

            article_list.append(article)

        except Exception as e:
            print("exception!", e)
            continue

    return article_list



def go_to_next_page(driver, page, voivodeship):
    url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}?viewType=listing&limit=72&page={page}"
    driver.get(url)

def get_limit(driver, url):
    driver.get(url)
    try:
        driver.find_element(By.XPATH, "//*[@id='onetrust-accept-btn-handler']").click()
    except Exception as e:
        "no js!! haha"
    print(driver.title)
    print("current source:")

    print(driver.page_source)


    try:
        element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//nav[@data-cy='pagination']"))
            )
        
        list_of_a = element.find_elements(By.TAG_NAME, 'a')

        limit = list_of_a[-1].text

    except Exception as e:
        print(e)
        limit = 50
    finally:
        return limit