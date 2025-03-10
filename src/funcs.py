# To be ran solo.
import os
import sys

from PySide6.QtGui import QColor, QPainter, QPixmap, QFontDatabase, QFont
from PySide6.QtCore import QSize, Qt
from PySide6.QtSvg import QSvgRenderer

def path(src: str) -> str:
    """A function to retrieve the real path of a file.

    Args:
        src (str): Source of the file in relative format.

    Returns:
        str: Absolute directory to the file.
    """
    try:
        # Pyinstaller creates a temp folder and stores the path in _MEIPASS
        path = sys._MEIPASS
    
    except AttributeError:
        # If _MEIPASS isn't found, signifying a non-exe, use the original path.
        path = os.path.abspath(".")
    
    # Return the relative path with the real base_path attached.
    return os.path.join(path, src)

def change_svg_colour(
        src: str,
        size: tuple[int, int],
        colour: tuple[int, int, int]
) -> QPixmap:
    """A function to change the colour of an SVG file.

    Args:
        src (str): Relative path of the SVG file.
        size (tuple): Size of the outputted QPixmap (width, height)
        colour (tuple): Colour of the outputted QPixmap from SVG (red, green, blue)

    Returns:
        QPixmap: QPixmap object of the outputted SVG recoloured.
    """
    red, green, blue = colour
    width, height = size
    
    icon_colour = QColor(red, green, blue)
    
    renderer = QSvgRenderer(path(src))
    
    pixmap = QPixmap(QSize(width, height))
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter) # this is the destination, and only its alpha is used!
    painter.setCompositionMode(painter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), icon_colour)
    painter.end()

    return pixmap

def get_font(
        family: str = "outfit",
        weight: str = "regular"
) -> QFont:
    if family == "outfit":
        src = f"resources/assets/fonts/Outfit-{weight.capitalize()}.ttf"
    
    font_id = QFontDatabase.addApplicationFont(src)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    
    font = QFont(font_family)
    
    if "bold" in src.lower():
        font.setBold(True)
    
    return font