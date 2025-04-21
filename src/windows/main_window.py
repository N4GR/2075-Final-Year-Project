from src.shared.imports import *

@Decorators.autolog
@Decorators.property
class MainWindow(QWidget):
    log : logging.Logger
    
    def __init__(self):
        super().__init__()
        self._set_style()
        self._set_widgets()
        self._set_layout()
        
        self.open_window(LoginWindow)
    
    def _set_style(self):
        self.setMinimumSize(800, 600)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    
    def _set_widgets(self):
        self.topbar = TopBarWidget(self)
    
    def _set_layout(self):
        self.main_layout = QVBoxLayout()
        
        self.main_layout.addWidget(self.topbar)
        
        self.setLayout(self.main_layout)
    
    def open_window(self, window: QWidget):
        """Opens a window in the main window."""
        current_window : QWidget = get_property("OpenedWindow")
        
        if current_window:
            if window.__name__ == current_window.__class__.__name__:
                self.log.warning(f"Attempting to open {window.__name__} when {current_window.__class__.__name__} is already open, ignoring.")
                
                return
            
            else:
                current_window.deleteLater()
        
        self.opened_window : QWidget = window(self)
        set_property("OpenedWindow", self.opened_window)
        
        self.main_layout.addWidget(self.opened_window)