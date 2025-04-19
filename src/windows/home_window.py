from src.shared.imports import *

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
        self.server_list_widget = ServerListWidget(self)
    
    def _set_layout(self):
        self.main_layout = QHBoxLayout()
        
        self.main_layout.addWidget(self.server_list_widget, alignment = Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        
        self.setLayout(self.main_layout)