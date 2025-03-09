from src.imports import *

# Widget imports.
from src.windows.widgets.top_bar import TopBar

class MainWindow(QWidget):
    def __init__(self, application: QApplication):
        super().__init__()
        self.application = application
        self.config = MainWindowConfig()
        
        self._set_design()
        self._init_widgets()
    
    def _set_design(self):
        """A function to add design to a Qt widget."""
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet(f"background-color: {self.config.background_colour}")
        
        self.main_layout = QVBoxLayout()
        self.main_layout.addSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(self.main_layout)
    
    def _init_widgets(self):
        self.top_bar = TopBar(
            parent = self,
            main_window = self
        )
        
        self.main_layout.addWidget(self.top_bar, alignment = Qt.AlignmentFlag.AlignTop)