from PySide6.QtWidgets import QApplication

# Local imports.
from src.application.managers.font_manager import FontManager
from src.application.managers.colour_manager import ColourManager

class Application(QApplication):
    def __init__(self):
        super().__init__()
        """A function to initialise the Application, a subclass of QApplication containing properties shared during runtime like FontManager, ect."""        
        self._add_widgets()
        self._add_properties()
    
    def _add_widgets(self):
        """A function to add all related widgets to the QApplication."""        
        self.font_manager = FontManager()
        self.colour_manager = ColourManager()
    
    def _add_properties(self):
        """A function to add properties to the QApplication that can be called during runtime."""
        self.setProperty("FontManager", self.font_manager)
        self.setProperty("ColourManager", self.colour_manager)