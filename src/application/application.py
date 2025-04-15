from PySide6.QtWidgets import QApplication

from src.windows.main_window import MainWindow
from src.shared.funcs import load_font

class Application(QApplication):
    def __init__(self):
        super().__init__()
        self._set_style()
        self._set_widgets()

    def _set_style(self):
        regular_font = load_font("/assets/fonts/GeistMonoNerdFont-Regular.otf")
        
        self.setStyleSheet(
            "* {"
            f"font-family: {regular_font.family()};"
            "font-size: 10pt;"
            "}"
        )
    
    def _set_widgets(self):
        """Sets the widgets to the application."""
        self.main_window = MainWindow()
        self.main_window.show()