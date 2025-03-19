# Python imports.

# Third-party imports.
import requests

from PySide6.QtWidgets import (
    QWidget, QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout,
    QPushButton, QHBoxLayout
)

from PySide6.QtGui import (
    QResizeEvent
)

# Local imports.
from src.shared.funcs import *
from src.application.managers.font_manager import FontManager