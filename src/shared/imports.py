# Python imports.

# Third-party imports.
import requests

from PySide6.QtWidgets import (
    QWidget, QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout,
    QPushButton, QHBoxLayout, QGridLayout
)

from PySide6.QtGui import (
    QResizeEvent, QPainter, QPixmap, QColor, QBrush
)

from PySide6.QtCore import (
    QPoint, Qt, QSize
)

from PySide6.QtSvg import (
    QtSvg, QSvgRenderer
)

# Local imports.
from src.shared.funcs import *
from src.application.managers.font_manager import FontManager