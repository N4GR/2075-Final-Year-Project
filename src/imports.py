# Python imports.
import random

# Third-party imports.
import requests

from PySide6.QtWidgets import (
    QWidget, QApplication, QLabel, QSizePolicy,
    QHBoxLayout, QVBoxLayout, QStackedLayout,
    QPushButton, QSpacerItem, QMainWindow, QGridLayout,
    QLineEdit, QGraphicsDropShadowEffect, QComboBox
)

from PySide6.QtCore import (
    Qt, QSize, QPropertyAnimation, QEasingCurve,
    QPoint, QParallelAnimationGroup, QObject,
    QUrl, QJsonDocument, Slot, Signal, QEvent
)

from PySide6.QtNetwork import (
    QNetworkAccessManager, QNetworkRequest,
    QNetworkReply
)

from PySide6.QtGui import (
    QIcon, QColor, QPainter, QPixmap,
    QResizeEvent, QTransform, QFont,
    QFontDatabase, QCursor, QMouseEvent
)

from PySide6.QtSvg import (
    QSvgRenderer
)

# Local imports.
from src.funcs import *
from src.windows.config import *
from src.network.manager import NetworkManager