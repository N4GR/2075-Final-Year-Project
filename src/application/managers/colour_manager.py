import json
from src.shared.funcs import *

class ColourManager:
    def __init__(self):
        self.data = self.get_colour_data()
    
    def get_colour_data(self) -> dict:
        with open(path("/data/colours.json"), "r", encoding = "utf-8") as file:
            return json.load(file)