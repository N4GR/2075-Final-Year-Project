from src.windows.main_window import MainWindow
from src.imports import QApplication
from src.network.manager import NetworkManager

if __name__ == "__main__":
    network_manager = NetworkManager() # Create the networkmanager object, getting a session token.
    
    application = QApplication([]) # Create the Qt application.
    main_window = MainWindow(application, network_manager) # Create the main window object, parsing application.
    main_window.show() # Show the main window.
    
    application.exec() # Execute the Qt event loop.