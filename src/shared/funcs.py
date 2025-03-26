from PySide6.QtSvg import QtSvg, QSvgRenderer
from PySide6.QtGui import QPainter, QPixmap, QColor, QBrush
from PySide6.QtCore import QSize, Qt

def path(src: str) -> str:
    """A function to fix paths

    Args:
        src (str): Source directory to be fixed.

    Returns:
        str: Fixed Source directory.
    """
    if src[0] == "/": # Removes the first / from the relative path.
        src = src[1:]
    
    return src

def get_svg(src: str, size: QSize = None, colour: QColor = None) -> QPixmap:
    renderer = QSvgRenderer(path(src))
    pixmap = QPixmap(renderer.defaultSize())
    
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    
    painter.setCompositionMode(painter.CompositionMode.CompositionMode_SourceIn)
    
    if colour is None:
        painter.fillRect(pixmap.rect(), QColor(255, 0, 0))
    else:
        painter.fillRect(pixmap.rect(), colour)
    
    painter.end()
    
    return pixmap.scaled(
        size,
        aspectMode = Qt.AspectRatioMode.IgnoreAspectRatio,
        mode = Qt.TransformationMode.SmoothTransformation
    )