from PySide6.QtGui import QFont, QFontDatabase
from src.shared.funcs import *

class FontManager(QFontDatabase):
    """QFontDatabase subclass containing fonts related to the application.

    Attributes:
        caskaydia (Caskaydia): A class object containing QFonts related to the Caskaydia family.
    """    
    def __init__(self):
        super().__init__()
        """A subclass of QFontDatabase containing font families used in the application."""
        self.caskaydia = Caskaydia(self)
    
    def load_font(self, src: str) -> QFont:
        """A function to load a font using the QFontDatabase and return the font.

        Args:
            src (str): Source directory of the font to load in a valid font format.

        Returns:
            font (QFont): Font found from the source directory.
        """        
        font_id = self.addApplicationFont(src)
        font_family = self.applicationFontFamilies(font_id)[0]
        
        font = QFont(font_family)
        
        if "bold" in src.lower(): # Set the font to bold if "bold" is found in the source string.
            font.setBold(True)
        
        return font
        
class Caskaydia:
    def __init__(
            self,
            font_manager : FontManager
    ):
        """Caskaydia class object containing QFonts of each type related to the Caskaydia font family.

        Args:
            font_manager (FontManager): FontManager object that's a subclass of QFontDatabase.
        """        
        self.regular = font_manager.load_font(path("/assets/fonts/CaskaydiaCoveNerdFont-Regular.ttf"))
        self.light = font_manager.load_font(path("/assets/fonts/CaskaydiaCoveNerdFont-Light.ttf"))
        self.italic = font_manager.load_font(path("/assets/fonts/CaskaydiaCoveNerdFont-Italic.ttf"))
        self.bold = font_manager.load_font(path("/assets/fonts/CaskaydiaCoveNerdFont-Bold.ttf"))