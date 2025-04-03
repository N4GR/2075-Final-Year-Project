import ctypes

from src.application.application import Application
from src.windows.main_window import MainWindow

if __name__ == "__main__": # If the script is being launched from this point.
    # Set the APP ID for windows to recognise the icon in tool bar.
    app_id = "N4GR.Metaphrast.Metaphrast.1" # App ID for windows CTypes.
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    
    application = Application() # Initialise the application for PySide6 event loop.
    main_window = MainWindow() # Initialise the main window for the application.
    
    application.exec() # Execute the event loop.