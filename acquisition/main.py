import sys
import concurrent.futures 
import datetime

from engines import otodom_engine, otodom_intensive_engine

filetype = "csv" # csv or json

output_filename = "otodom_data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + f".{filetype}"

available_voivodeships = [
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
    
    otodom_intensive_engine.initiate_voivodeship_scrapage(voivodeship, output_filename, filetype)


def main():
    try:
        concurrent_workers = int(sys.argv[1])
    except Exception as e:
        print("Couldn't parse first arg given to program as int for concurrent workers. Setting as one.")
        concurrent_workers = 1

    voivodeships = []

    for i in sys.argv:
        if i in available_voivodeships:
            voivodeships.append(i)

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_workers) as executor:
        executor.map(scrape_voivodeship, voivodeships)


    print("scraping finished")
    if filetype == "json":
        otodom_engine.clean_the_json(output_filename)


if __name__ == "__main__":
    main()