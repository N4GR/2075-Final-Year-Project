from src.application.application import Application
from src.windows.main_window import MainWindow

if __name__ == "__main__": # If the script is being launched from this point.
    application = Application() # Initialise the application for PySide6 event loop.
    main_window = MainWindow() # Initialise the main window for the application.
    
    application.exec() # Execute the event loop.