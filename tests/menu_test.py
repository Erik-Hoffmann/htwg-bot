from datetime import date

from bs4 import BeautifulSoup
import requests
import re



MENSA_HTWG = 'https://seezeit.com/essen/speiseplaene/mensa-htwg/'

# Utility
def validateIngr(sup):
    return bool(re.match("\((\d\w?,?)+\)", sup))

def attr_lookup(attribute):
    print(attribute)
    lookup = {
            "Veg": "Vegetarisch",
            "Vegan": "Vegan",
            "Sch": "Schwein",
            "R": "Rind/Kalb",
            "G": "Geflügel",
            "L": "Lamm",
            "W": "Wild",
            "F": "Fisch/Meeresfrüchte"
            }
    result = []
    if attribute:
        for attr in attribute:
            if attr in lookup:
                result.append(lookup[attr])
    return ", ".join(result) if result else ""

def menu():
    page_response = requests.get(MENSA_HTWG)
    soup = BeautifulSoup(page_response.content, 'html.parser')
    contents = soup.find('div', class_='tx-speiseplan')
    date_tabs = contents.find_all('a', class_='tab')
    current_tab = None
    current_tab_class = None
    attr_class='speiseplanTagKatIcon'
    for tab in date_tabs:
        current_tab = tab.text
        if date.today().strftime("%d.%m.") in current_tab:
        # if "16.05." in current_tab:
            current_tab_class = tab.get('class')[1]
            break
    response={
        "categories": []
            }
    if not current_tab_class is None:

        day = contents.find('div', {"id":current_tab_class})
        menus = day.find_all('div', class_='speiseplanTagKat')


        for menu in menus:
            category=menu.find('div', class_='category')
            food=menu.find('div', class_='title_preise_1').find('div', class_='title')
            for sup in food.select('sup'):
                if not validateIngr(sup.text): sup.unwrap()
                else : sup.decompose()
            attribute=menu.find('div', class_='title_preise_2').find('div', class_=attr_class)['class']
            response["categories"].append({
                "title": category.text,
                "value": food.text,
                "attribute": attr_lookup(attribute)
                    })

    else:
        response["error"] = "Heut wohl nix, zu oder so"

    print(response)


if __name__ == "__main__": menu()
