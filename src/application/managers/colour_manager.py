import json
from src.shared.funcs import *

class ColourManager:
    def __init__(self):
        colour_data = self.get_colour_data()
        
        self.error = colour_data["error"]
        self.success = colour_data["success"]
    
    def get_colour_data(self) -> dict:
        with open(path("/data/colours.json"), "r", encoding = "utf-8") as file:
            return json.load(file)