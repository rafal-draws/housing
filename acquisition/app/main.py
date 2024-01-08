import sys
import datetime

from engines import otodom_intensive_engine, voivodeship_gen

### args
# 1: csv | json
# 2: path
# 3: firefox | anything == chrome
# n: voivodeship

def main():


    voivodeships = []

    if len(sys.argv) > 1:
        try:
            filetype = sys.argv[1]
            output_filename = sys.argv[2] + "/otodom_data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + f".{filetype}"
            browser = sys.argv[3]

            
            # for i in sys.argv:
            #     if i in voivodeship_gen.available_voivodeships:
            #         print(f"COMMAND PROVIDED VOIVODESHIP: {i}")
            #         voivodeships.append(i)

            #     else:
            print("GENERATING VOIVODESHIPS BASED ON DAY")
            [voivodeships.append(x) for x in voivodeship_gen.choose_voivodeships()]
            print(voivodeships)

        except Exception as e:
            print(f"Couldn't parse first arg given to program.\nException: {e}")



    else:
        print("DEBUG MODE")
        browser = "firefox"
        filetype = "csv"
        output_filename =  "otodom_data_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + f".{filetype}"
        voivodeships.append("pomorskie")
    
    for voivodeship in voivodeships:
        otodom_intensive_engine.initiate_voivodeship_scrapage(voivodeship, output_filename, filetype, browser)


    print("scraping finished")
    # if filetype == "json":
    #     otodom_engine.clean_the_json(output_filename)
        


if __name__ == "__main__":
    main()