from typing import Any
import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

def get_property(name: str) -> Any:
    """Return a property from the current instance of the application.
    
    Args:
        name (str): Property name used when setting the property.
    
    Returns
        Any: Any property set in the application.
    """
    fetched_property = QApplication.instance().property(name)

    return fetched_property

def set_property(name: str, value: Any):
    """Set a property in the application to be globally accesible from get_property.

    Args:
        name (str): Name of the property to use when retrieving the property.
        value (Any): Anything you'd like to set as the property.
    """
    QApplication.instance().setProperty(name, value)

def path(src: str) -> str:
    """Path handling for when packaged with onefile.
    
    Args:
        src (str): Path of the file or directory to obtain.
    
    Returns:
        str: Absolute path returned pyinstaller onefile compatible.
    """
    if src[0] == "/":
        src = src[1:]
    
    if hasattr(sys, "_MEIPASS"):
        # Running packaged.
        return os.path.join(sys._MEIPASS, src)
    
    else:
        return os.path.join(os.path.abspath("."), src)

def load_font(font_src: str) -> QFont:
    """Creates a QFont object from a font file.

    Args:
        font_src (str): Relative path to the font file.

    Returns:
        QFont: QFont object generated from the file.
    """
    font_id = QFontDatabase.addApplicationFont(path(font_src))
    
    if font_id == -1:
        return None
    
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    
    return QFont(font_family)