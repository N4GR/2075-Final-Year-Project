# Python imports.

# Third-party imports.
from PySide6.QtWidgets import (
    QWidget, QApplication, QLabel, QSizePolicy,
    QHBoxLayout, QVBoxLayout, QStackedLayout,
    QPushButton, QSpacerItem, QMainWindow
)

from PySide6.QtCore import (
    Qt, QSize, QPropertyAnimation, QEasingCurve,
    QPoint, QParallelAnimationGroup
)

from PySide6.QtGui import (
    QIcon, QColor, QPainter, QPixmap,
    QResizeEvent, QTransform
)

from PySide6.QtSvg import (
    QSvgRenderer
)

# Local imports.
from src.funcs import *
from src.windows.config import *