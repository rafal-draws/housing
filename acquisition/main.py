import sys
import concurrent.futures 
import datetime

from engines import otodom_engine, otodom_intensive_engine

filetype = "" 
output_filename = ""

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


def main():


    voivodeships = []

    if len(sys.argv) > 1:
        try:
            print(f"Concurrent workers amount is {sys.argv[1]}")
            concurrent_workers = int(sys.argv[1])
            filetype = sys.argv[2]
            output_filename = sys.argv[3] + "/otodom_data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + f".{filetype}"
        except Exception as e:
            print(f"Couldn't parse first arg given to program.\nException: {e}")

    else:
        print("DEBUG MODE")
        concurrent_workers = 2
        filetype = "csv"
        output_filename =  "otodom_data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + f".{filetype}"
        voivodeships.append("pomorskie")



    for i in sys.argv:
        if i in available_voivodeships:
            voivodeships.append(i)

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_workers) as executor:
        executor.map(scrape_voivodeship, voivodeships)


    print("scraping finished")
    if filetype == "json":
        otodom_engine.clean_the_json(output_filename)
        
def scrape_voivodeship(voivodeship):
    
    otodom_intensive_engine.initiate_voivodeship_scrapage(voivodeship, output_filename, filetype)



if __name__ == "__main__":
    main()