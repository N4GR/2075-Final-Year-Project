from src.imports import *

# Widget imports.
from src.windows.widgets.top_bar import TopBar
from src.windows.widgets.login import Login

class MainWindow(QWidget):
    def __init__(
            self,
            application: QApplication,
            network_manager: NetworkManager
    ):
        super().__init__()
        self.application = application
        self.network_manager = network_manager
        self.config = MainWindowConfig()
        
        self._set_design()
        self._init_widgets()
        self._init_layout()
    
    def _set_design(self):
        """A function to add design to a Qt widget."""
        self.setGeometry(0, 0, 800, 600)
        self.setMinimumSize(400, 400)
        self.setStyleSheet(f"background-color: {self.config.background_colour}")
        
        self.setWindowIcon(QPixmap(path("resources/assets/icons/icon.png")))
        self.setWindowTitle("Metaphrast")
    
    def _init_widgets(self):
        self.login = Login(
            parent = self,
            main_window = self
        )
        
        self.top_bar = TopBar(
            parent = self,
            main_window = self
        )
        
        # Hide the topbar only until login is complete.
        self.top_bar.hide()
    
    def _init_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
    
    def resizeEvent(self, event):
        self.top_bar.setFixedWidth(self.width()) # Top_Bar widget to fill main_window width.
        
        try:
            self.login.setFixedSize(self.width(), self.height()) # Resize login screen to fill main_window area.
        except RuntimeError:
            pass # If the login screen is deleted, ignore Runtime errors.
        
        return super().resizeEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent):
        try:
            profile_button = self.top_bar.buttons.profile_button
            drop_menu = profile_button.drop_menu
            
            if not drop_menu.geometry().contains(event.pos()): # User clicked outside drop menu.
                drop_menu.deleteLater() # Delete the drop menu.
                profile_button._is_showing = False # Set the drop_menu as no longer showing.
        
        except AttributeError:
            pass # If the variables don't exist, pass the error and ignore it.
        
        except RuntimeError:
            pass # Once the widget is deleted, runtime error occours - ignore.
        
        return super().mousePressEvent(event)