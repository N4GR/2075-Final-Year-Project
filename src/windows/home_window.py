from src.shared.imports import *

from src.widgets.dm_list import DMListWidget
from src.widgets.chat_widget import ChatWidget

@Decorators.autolog
@Decorators.property
class HomeWindow(QWidget):
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
        self._set_widgets()
        self._set_layout()
    
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
    
    def _set_widgets(self):
        self.dm_list_widget = DMListWidget(self)
        self.chat_widget = ChatWidget(self)
    
    def _set_layout(self):
        self.main_layout = QHBoxLayout()
        
        self.main_layout.addWidget(self.dm_list_widget)
        self.main_layout.addWidget(self.chat_widget)

        self.setLayout(self.main_layout)