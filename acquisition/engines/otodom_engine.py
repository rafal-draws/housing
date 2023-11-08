import requests
import configparser
import concurrent.futures
from bs4 import BeautifulSoup


def initiate_voivodeship_scrapage(voivodeship:str):


    iteration = 1

    url = f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/{voivodeship}?viewType=listing&limit=72&page={iteration}"

    limit = get_limit(url)



def get_limit(url):
    site_src = requests.get(url)

    s = BeautifulSoup(site_src, 'html.parser')
    last_page = s.find(attrs={"role":"navigation"}).find_all("a")[-1].text
    print(last_page)