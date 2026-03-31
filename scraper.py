import json
import locale
from datetime import datetime as dt
from datetime import timedelta
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup, Tag

URL = "https://www.sar.unicamp.br/RU/view/site/cardapio.php"


def process_option(option: Tag) -> dict:
    items = option.find_all("td")

    if len(items) < 6:
        return {}

    option = {}

    option["Acompanhamentos"] = items[0].contents[2]
    option["Prato Principal"] = items[1].contents[2]
    option["Guarnição"] = items[2].contents[2]
    option["Salada"] = items[3].contents[2]
    option["Sobremesa"] = items[4].contents[2]
    option["Refresco"] = items[5].contents[2]

    return option


def process_meal(meal: Tag) -> dict:
    options = meal.find_all("div", class_="col-6")

    normal = process_option(options[0])
    vegan = process_option(options[1])

    meal = {}
    meal["Vegano"] = vegan
    meal["Normal"] = normal

    return meal


def process_day(day: Tag) -> dict:
    # Yes, I know the id's don't make sense but it is right
    # There was probably some confusion while designing the website
    lunch = process_meal(day.find(id="normal"))
    dinner = process_meal(day.find(id="vegetariano"))

    menu = {}

    menu["Almoço"] = lunch
    menu["Jantar"] = dinner

    return menu


def get_todays_menu() -> dict:
    r = requests.get(URL)

    soup = BeautifulSoup(r.text, "html.parser")

    day = soup.find(id="dia")

    return process_day(day)


def get_weekly_menu() -> dict:

    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    today = dt.now(ZoneInfo("America/Sao_Paulo"))

    week = {}

    for i in range(1, 7):
        date = today + timedelta(days=i)

        date_name = date.strftime("%Y-%m-%d")
        date_week_name = date.strftime("%A")

        r = requests.post(URL, {"data": date_name})
        soup = BeautifulSoup(r.text, "html.parser")
        day = soup.find(id="dia")

        week[date_week_name] = process_day(day)

    return week


if __name__ == "__main__":
    menu = get_weekly_menu()
    parsed = json.dumps(menu, indent=4, ensure_ascii=False).encode("utf8")
    print(parsed.decode())
