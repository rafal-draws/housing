from engines import otodom_engine

voivodeships = [
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
    "pomorskie",
    "slaskie",
    "swietokrzyskie",
    "warminsko--mazurskie",
    "wielkopolskie",
    "zachodniopomorskie"
]

def main():
    
    for i in voivodeships:
        otodom_engine.initiate_voivodeship_scrapage(i)



if __name__ == "__main__":
    main()