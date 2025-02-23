from src.window.imports import *

class MainWindow(QWidget):
    def __init__(
            self,
            application: QApplication
    ) -> None:
        """Main window object from QWidget which will be the main window of the application.

        Args:
            application (QApplication): QApplication object created in main.py
        """
        super().__init__()
        self.application = application
    
        self._set_design()
    
    def _set_design(self):
        """Function to set the design of the QWidget object."""
        self.setFixedSize( # Setting the window to a fixed size of 800x600.
            800, # 800px wide.
            600 # 600px tall.
        )