from src.modules.imports import *

# For logging.
from src.shared.logging import setup_logger

class SQL:
    def __init__(
            self,
            database_dir: str
    ) -> None:
        """SQL Object to handle database connection query.

        Args:
            database_dir (str): Path to the database.
            
        Attributes:
            connection (sqlite3.Connection): Connection object used to initialise the connection to the database.
            cursor (sqlite3.Connection.Cursor): Cursor object used to call queries on the database.
        """
        self.log = setup_logger("SRC.MODULES.SQL.SQL") # Setting up logging object.
        
        self.database_dir = database_dir
        self.connection = sqlite3.connect(self.database_dir)
        self.cursor = self.connection.cursor()
        
        self.log.info(f"Connected to {self.database_dir}")
    
    def _close(self):
        """Function to commit and close the connection to the database; careful - it's a command that cannot be undone, another connection will be needed to do any more query to the database."""
        self.connection.commit()
        self.connection.close()
        
        self.log.info(f"Closed connection to {self.database_dir}")
    
    def add_user(
            self,
            username: str,
            password: str,
            email: str,
            profile_picture : None | str = None,
    ):
        """Function to add a user to the user's database.

        Args:
            username (str): Username in text of the user.
            password (str): Password in text of the user.
            email (str): Email in text of the user.
            profile_picture (None | str, optional): Email of the user if given. Defaults to None.
        """
        
        pass