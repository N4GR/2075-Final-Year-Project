# A file to be used on its own.
from src.funcs import path
import json

def get_config(type: str) -> dict:
    with open(path("data/config.json")) as file:
        return json.load(file)[type]

class MainWindowConfig:
    def __init__(self):
        data = get_config("MainWindow")
        
        self.background_colour : str = data["BackgroundColour"]

class TopBarConfig:
    def __init__(self):
        data = get_config("TopBar")
        
        self.background_colour : str = data["BackgroundColour"]
        self.hide_button = self.Button(data["HideButton"])
        self.profile_button = self.Button(data["ProfileButton"])
    
    class Button:
        def __init__(self, button_data: dict):
            self.icon_src : str = button_data["src"]
            self.icon_colour : str = button_data["IconColour"]