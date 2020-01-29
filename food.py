import requests
from api_cred import api_key
import json

class Food:
    def __init__(self, key:str=None):
        self.url = "https://api.nal.usda.gov/fdc/v1/search"
        self.key = api_key
        if key:
            self.key = key
    
    def search(self, food:str, require_all_words:bool=None):
        params = {
            "api_key": self.key,
            "generalSearchInput": food
        }
        if require_all_words is not None:
            if require_all_words is True:
                params["requireAllWords"] = "true"
            else:
                params["requireAllWords"] = "false"
        return requests.get(self.url, params)

if "__main__" in __name__:
    from pprint import pprint
    food = Food()
    pprint(food.search("rib eye").text)
