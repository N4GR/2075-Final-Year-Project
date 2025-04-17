from src.shared.imports import *

@Decorators.property
class TopBarWidget(QWidget):
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.current_style : QWidget = None
        
        self._set_style()
        self._set_layout()
        
        self.set_logged_out()
    
    def _set_style(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(50)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(
            "background-color: #171717;"
            "border-radius: 15px;"
        )
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
    
    def set_logged_in(self):
        """Sets the topbar as the logged_in style."""
        if self.current_style:
            self.current_style.deleteLater()
        
        self.current_style = LoggedIn(self)
        self.add_to_layout(self.current_style)
    
    def set_logged_out(self):
        """Sets the topbar as the logged_out style."""
        if self.current_style:
            self.current_style.deleteLater()
            
        self.current_style = LoggedOut(self)
        self.add_to_layout(self.current_style)
    
    def _set_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(self.main_layout)
    
    def add_to_layout(self, widget: QWidget):
        self.main_layout.addWidget(widget)

class LoggedIn(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

class LoggedOut(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self._set_widgets()
        self._set_layout()
        
    def _set_widgets(self):
        self.title_label = self.TitleLabel(self)
    
    def _set_layout(self):
        self.main_layout = QHBoxLayout()
        
        self.main_layout.addWidget(self.title_label)
        
        self.setLayout(self.main_layout)
    
    class TitleLabel(QLabel):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self.setText("METAPHRAST")
            self.setStyleSheet("font-weight: bold; font-size: 20pt;")