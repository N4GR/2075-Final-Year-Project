# Local imports.
from src.modules.sql import SQL
from src.shared.paths import DatabasePaths
from src.window.main_window import MainWindow

# For creating the application object.
from src.window.imports import QApplication

# For logging.
from src.shared.logging import setup_logger

class Main:
    def __init__(self):
        """Main class object that should handle all the main operations."""
        self.log = setup_logger("SRC.MAIN.MAIN") # Setting up logging object.
        
        self._create_database()
        self._create_window()
    
    def _create_window(self):
        """Function to create the window variables to self, also creating the PySide6 QApplication and executing it to run the program loop."""
        def _run_application():
            self.application.exec_()
        
        self.application = QApplication([])
        self.main_window = MainWindow(application = self.application)
        self.main_window.show() # Showing the main window QWidget.
    
        _run_application()
    
    def _create_database(self):
        """Function to create the database variables to self, initialising the connection to the relevant databases from DatabasePaths object."""
        self.database_paths = DatabasePaths()
        self.main_database = SQL(
            database_dir = self.database_paths.main_database.directory
        )