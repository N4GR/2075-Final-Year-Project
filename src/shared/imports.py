# Python imports.

# Third-party imports.
import requests

from PySide6.QtWidgets import (
    QWidget, QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout,
    QPushButton, QHBoxLayout, QGridLayout
)

from PySide6.QtGui import (
    QResizeEvent, QPainter, QPixmap, QColor, QBrush, QIcon
)

from PySide6.QtCore import (
    QPoint, Qt, QSize
)

from PySide6.QtSvg import (
    QtSvg, QSvgRenderer
)

from PySide6.QtXml import (
    QDomDocument
)

# Local imports.
from src.shared.funcs import *
from src.application.managers.font_manager import FontManager
from src.application.managers.colour_manager import ColourManager