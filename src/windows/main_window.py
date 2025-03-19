from src.shared.imports import *

# Local imports.
from src.windows.widgets.login_window import LoginWindow

class MainWindow(QMainWindow):
    def __init__(self):
        """A class object that's a subclass of QMainWindow to function as the main window object."""
        super().__init__()
        self._add_design()
        self._add_widgets()
        self._add_layout()
        
        self.showMaximized() # Show the window after all elements have loaded.
    
    def _add_design(self):
        """A function to add design elements to the widget."""
        self.setMinimumSize(800, 600) # Set a minimum size for the window to be displayed as.
        
        # FOR TESTING PURPOSES, MOVING THE WINDOW TO A DIFFERENT DISPLAY.
        for screen in QApplication.screens():
            if screen.name() == "Acer P226HQ":
                self.setGeometry(screen.geometry())
    
    def _add_widgets(self):
        """A function to add widgets related to the widget to the widget."""
        self.background_label = self.BackgroundLabel(self)
        
        self.login_window = LoginWindow(self)
    
    def _add_layout(self):
        """A function to add the layout to the widget."""
        pass
    
    def resizeEvent(self, event: QResizeEvent):
        """A function called when the window is resized.

        Args:
            event (QResizeEvent): QResizeEvent from PySide6.
        """
        self.background_label.setFixedSize(self.size()) # Set the size of the label to fill the window.
        self.login_window.setFixedSize(self.size()) # Set the size of the login window to fill the main window.
        
        return super().resizeEvent(event)
    
    class BackgroundLabel(QLabel):
        def __init__(self, parent: QWidget):
            """A QLabel object functioning as the background label to fill the widget.

            Args:
                parent (QWidget): Parent widget of the label.
            """            
            super().__init__(parent)
            self.setFixedSize(parent.size())
            self.setStyleSheet("background-color: red;")