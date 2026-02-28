import requests 
from bs4 import BeautifulSoup
import json

URL = "https://www.sar.unicamp.br/RU/view/site/cardapio.php"


def process_option(option:Tag) -> dict:
    items = option.find_all("td")
    
    if len(items) < 6:
        return {}

    option = {}

    option['Acompanhamentos'] = items[0].contents[2]
    option['Prato Principal'] = items[1].contents[2]
    option['Guarnição'] = items[2].contents[2]
    option['Salada'] = items[3].contents[2]
    option['Sobremesa'] = items[4].contents[2]
    option['Refresco'] = items[5].contents[2]
    
    return option

def process_meal(meal: Tag) -> dict:
    options = meal.find_all("div", class_="col-6")

    normal = process_option(options[0])
    vegan  = process_option(options[1])

    meal = {}
    meal['Vegano'] = vegan
    meal['Normal'] = normal

    return meal

def get_todays_menu() -> dict:
    r = requests.get(URL)
    
    soup = BeautifulSoup(r.text, 'html.parser')

    dia = soup.find(id='dia')

    # Yes, I know the id's don't make sense but it is right
    # There was probably some confusion while designing the website 
    lunch = process_meal(dia.find(id='normal'))
    dinner = process_meal(dia.find(id='vegetariano'))

    menu = {}

    menu['Almoço'] = lunch
    menu['Jantar'] = dinner

    return menu
    
if __name__ == "__main__":
    menu = get_todays_menu()
    parsed = json.dumps(menu, indent=4, ensure_ascii=False).encode('utf8')
    print(parsed.decode())
