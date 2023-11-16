import concurrent.futures 
import datetime

from engines import otodom_engine


output_filename = "otodom_data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + ".json"

voivodeships = [
    "pomorskie",
    "dolnoslaskie",
    "kujawsko--pomorskie",
    "lubelskie",
    "lubuskie",
    "lodzkie",
    "malopolskie",
    "mazowieckie",
    "opolskie",
    "podkarpackie",
    "podlaskie",
    "slaskie",
    "swietokrzyskie",
    "warminsko--mazurskie",
    "wielkopolskie",
    "zachodniopomorskie"
]

def scrape_voivodeship(voivodeship):
    
    otodom_engine.initiate_voivodeship_scrapage(voivodeship, output_filename)


def main():

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(scrape_voivodeship, voivodeships)


    print("scraping finished")

    otodom_engine.clean_the_json(output_filename)


if __name__ == "__main__":
    main()