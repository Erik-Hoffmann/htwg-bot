from requests import ConnectionError
from requests import get
from pyquery import PyQuery as pq
import re
from pprint import pprint

class Speiseplan_extractor:

    address = "https://seezeit.com/essen/speiseplaene/mensa-htwg/"

    def __init__(self):
        self.speiseplan = self.get_menu()
        self.tag_map = self.build_tag_map()

    def get_menu(self):
        req = get(self.address)
        if not req.status_code == 200:
            raise ConnectionError(req)
        content = pq(req.content)
        return content(".tx-speiseplan")

    def get_aktiv_tab_id(self):
        menu = self.speiseplan
        return menu(".heute").attr("rel")

    def get_tab_content(self, tab_idx):
        menu = self.speiseplan
        return menu(f"#tab{tab_idx}")

    def get_tab_json(self, tab_idx=None):
        menu = self.speiseplan
        today_id = int(self.get_aktiv_tab_id())
        if tab_idx is None:
            idx = today_id
        else:
            idx = self.eval_index(today_id, tab_idx)
            if not menu(f"#tab{idx}"):
                raise IndexError("non existant tab id")
        return self.extract_categories(self.get_tab_content(idx))

    def eval_index(self, base_id: int, shift_id: str):
        if re.match(r"^[+-]?\d$", shift_id):
            try:
                shift_val = int(shift_id[-1])
            except Exception as err:
                raise err
            if shift_id.startswith('+'):
                return base_id + shift_val
            elif shift_id.startswith('-'):
                return base_id - shift_val
            else: return base_id + shift_val
        raise ValueError(f"Invalid input: shift_id={shift_id}")

    def extract_categories(self, tab):
        return [self.elem_to_json(elem) for elem in tab(".speiseplanTagKat")]

    def elem_to_json(self, elem):
        cat_html = pq(elem)
        cat_name = cat_html(".category").text()
        cat_food = cat_html(".title").text()
        tags_html = cat_html(".speiseplanTagKatIcon")
        cat_tags = self.map_tags(tags_html)
        return {"category": cat_name, "food": self.format_food(cat_food).rstrip(), "tags": cat_tags}
    
    def format_food(self,food):
        return re.sub(r"\(\d\d?\w?(,\d\d?\w?)*\)[ ]?",'', food)

    def build_tag_map(self):
        menu = self.speiseplan
        tags = menu(".tabsIcons")(".tabIcon")
        return {pq(elem).attr("class")[-1]: elem.text for elem in tags}
            
    def map_tags(self, tags):
        return list(
                map(
                    lambda x : self.tag_map.get(x, None),
                    [pq(tag).attr("class")[-1] for tag in tags]
                )
            )
            

            

if __name__ == '__main__':
    extractor = Speiseplan_extractor()
    pprint(
        extractor.get_tab_json()
    )

