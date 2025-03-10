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
            self.icon_src : str = path(button_data["src"])
            self.icon_colour : str = button_data["IconColour"]

class LoginConfig:
    def __init__(self):
        data = get_config("Login")
        
        self.background_colour : str = data["BackgroundColour"]
        self.triangle = self.Triangle(data["Triangle"])
        self.texture = self.Texture(data["Texture"])
        self.menu = self.Menu(data["Menu"])
    
    class Texture:
        def __init__(self, texture_data: dict):
            self.icon_src : str = path(texture_data["src"])
            self.icon_colour : str = texture_data["IconColour"]
    
    class Triangle:
        def __init__(self, triangle_data: dict):
            self.background_colour : str = triangle_data["BackgroundColour"]
    
    class Menu:
        def __init__(self, menu_data: dict):
            self.background_colour : str = menu_data["BackgroundColour"]
            
            self.login = self.Button(menu_data["LoginButton"])
            self.register = self.Button(menu_data["RegisterButton"])
        
        class Button:
            def __init__(self, button_data: dict):
                self.icon_src : str = path(button_data["src"])
                self.icon_colour : str = button_data["IconColour"]