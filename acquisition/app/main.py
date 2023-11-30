import sys
import datetime

from engines import otodom_intensive_engine

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
            filetype = sys.argv[1]
            output_filename = sys.argv[2] + "/otodom_data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + f".{filetype}"
        except Exception as e:
            print(f"Couldn't parse first arg given to program.\nException: {e}")

    else:
        print("DEBUG MODE")
        filetype = "csv"
        output_filename =  "otodom_data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + f".{filetype}"
        voivodeships.append("pomorskie")



    for i in sys.argv:
        if i in available_voivodeships:
            voivodeships.append(i)


    for voivodeship in voivodeships:
        otodom_intensive_engine.initiate_voivodeship_scrapage(voivodeship, output_filename, filetype)


    print("scraping finished")
    # if filetype == "json":
    #     otodom_engine.clean_the_json(output_filename)
        


if __name__ == "__main__":
    main()