import sys
import concurrent.futures 
import datetime

from engines import otodom_engine, otodom_intensive_engine

global filetype # csv or json
global output_filename

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

    #arg 1, workers

    try:
        print(f"Concurrent workers amount is {sys.argv[1]}")
        concurrent_workers = int(sys.argv[1])
    except Exception as e:
        print("Couldn't parse first arg given to program as int for concurrent workers. \nSetting as one.\nException: {e}")
        concurrent_workers = 1


    #arg 2, output type    
    try:
        filetype = sys.argv[2]
        print(f"Output filetype is ", filetype)
        
    except Exception as e:
        print(f"Couldn't retrieve filetype from {sys.argv[2]}\nsetting to csv by default /data\nException: {e}") 
        filetype = "csv"


    #arg 3, data path
    try:
        output_filename = sys.argv[3] + "/otodom_data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + f".{filetype}"
        print(f"Output filepath is ", output_filename)
        
    except Exception as e:
        print(f"Couldn't retrieve path from {sys.argv[3]}\nsetting data path casually to /data\nException: {e}") 
        output_filename = "otodom_data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + f".{filetype}"



    voivodeships = []

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