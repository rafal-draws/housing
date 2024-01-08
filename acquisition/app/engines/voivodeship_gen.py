from datetime import datetime

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
def choose_voivodeships() -> [str]:
    day = datetime.now().weekday()

    return [available_voivodeships[day], available_voivodeships[day+7]]
