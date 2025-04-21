# Python imports.
import os
import logging
import json
import sys
import random
from datetime import datetime
from uuid import UUID

# Third-party imports.
from PySide6.QtWidgets import (
    QWidget, QApplication, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout, QSpacerItem,
    QLineEdit, QPushButton, QGraphicsDropShadowEffect, QGridLayout, QFileDialog, QMessageBox,
    QScrollArea, QTextEdit
)

from PySide6.QtGui import (
    QResizeEvent, QColor, QPixmap, QIcon, QAction, QMouseEvent
)

from PySide6.QtCore import (
    Qt, QSize, Slot, QUrl, QByteArray, QObject, Signal, QTimer
)

from PySide6.QtNetwork import (
    QNetworkAccessManager, QNetworkRequest, QNetworkReply
)

import keyring

# Local imports.
from src.shared.globals import *
from src.shared.funcs import *
from src.shared.pil import *
from src.shared.objects import *
from src.shared.keys import *
from src.shared.decorators import Decorators

from src.widgets.network_manager import ApiClient
from src.widgets.topbar_widget import TopBarWidget

from src.windows.home_window import HomeWindow
from src.windows.login_window import LoginWindow
from src.windows.main_window import MainWindow

from src.application.application import Application
from src.application.sql_manager import SQLManager