from src.shared.imports import *

@Decorators.autolog
@Decorators.property
class HomeWindow(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
    
    def _set_style(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(
            "background-color: #1f1f1f;"
            "border-radius: 15px;"
        )
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)