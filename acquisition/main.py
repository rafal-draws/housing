import concurrent.futures 
from engines import otodom_engine

voivodeships = [
    "pomorskie",
    "dolnoslaskie",
    "kujawsko--pomorskie",
    # "lubelskie",
    # "lubuskie",
    # "lodzkie",
    # "malopolskie",
    # "mazowieckie",
    # "opolskie",
    # "podkarpackie",
    # "podlaskie",
    # "slaskie",
    # "swietokrzyskie",
    # "warminsko--mazurskie",
    # "wielkopolskie",
    # "zachodniopomorskie"
]

def scrape_voivodeship(voivodeship):
    otodom_engine.initiate_voivodeship_scrapage(voivodeship)


def main():

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(scrape_voivodeship, voivodeships)


    print("scraping finished")



if __name__ == "__main__":
    main()