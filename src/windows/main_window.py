from src.shared.imports import *

# Local imports.
from src.windows.login_window import LoginWindow
from src.windows.widgets.topbar import TopBar

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
        self.setWindowTitle("Metaphrast | Morgan Wiggins - WIG21148347 | 2075 - Final Year Project")
        
        self.setMinimumSize(800, 600) # Set a minimum size for the window to be displayed as.
        
        # Set the window icon.
        self.setWindowIcon(QIcon(path("/assets/svg/logo.png")))
        
        # Set the window icon of the application.
        QApplication.setWindowIcon(QIcon(path("/assets/svg/logo.png")))
        
        # FOR TESTING PURPOSES, MOVING THE WINDOW TO A DIFFERENT DISPLAY.
        for screen in QApplication.screens():
            if screen.name() == "Acer P226HQ":
                self.setGeometry(screen.geometry())
    
    def _add_widgets(self):
        """A function to add widgets related to the widget to the widget."""
        self.background_label = self.BackgroundLabel(self)
        self.login_window = LoginWindow(self)
        self.top_bar = TopBar(self)
    
    def _add_layout(self):
        """A function to add the layout to the widget."""
        pass
    
    def resizeEvent(self, event: QResizeEvent):
        """A function called when the window is resized.

        Args:
            event (QResizeEvent): QResizeEvent from PySide6.
        """
        def resize_to_window(widget: QWidget):
            """A function to resize a widget to the size of the main window, avoiding runtime errors and attribute errors."""
            try:
                widget.setFixedSize(self.size())
            
            except AttributeError:
                pass
            
            except RuntimeError:
                pass
        
        def resize_to_width(widget: QWidget):
            """A function to resize a widget to the width of the main window, avoiding runtime errors and attribute errors."""
            try:
                widget.setFixedWidth(self.width())
            
            except AttributeError:
                pass
            
            except RuntimeError:
                pass
        
        resize_to_window(self.background_label)
        resize_to_window(self.login_window)
        
        # Resize topbar to the width of the main window.
        resize_to_width(self.top_bar)
        
        return super().resizeEvent(event)
    
    class BackgroundLabel(QLabel):
        def __init__(self, parent: QWidget):
            """A QLabel object functioning as the background label to fill the widget.

            Args:
                parent (QWidget): Parent widget of the label.
            """            
            super().__init__(parent)
            self.setFixedSize(parent.size())
            self.setStyleSheet("background-color: black;")