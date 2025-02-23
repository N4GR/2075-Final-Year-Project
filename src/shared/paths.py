from src.shared.imports import *

class DatabasePaths:
    """DatabasePaths object containing data on the path of databases.
    
    Attributes:
        main_database (Path): Path object of the main database file.
    """
    def __init__(self):
        """Initialises the database path object; obtaining Path objects from Path."""
        current_working_directory = os.getcwd()
        
        self.main_database = Path(
            os.path.join(
                current_working_directory,
                "data/sql/main.sqlite"
            )
        )
    
class Path:
    """Path object from directory path.
    
    Attributes:
        directory (str): Full path name of the path.
        is_file (bool): Whether or not the path is a file.
        file (None | Path.File): If the path is a file, creates a file object from the path object.
    """
    def __init__(
        self,
        dir_path: str
    ) -> None:
        """Initialises the Path object.

        Args:
            dir_path (str): Full path of the directory.
        """
        self.directory = dir_path
        self.is_file = os.path.isfile(self.directory)
    
        # If the path is a file, get the File object using the dir_path string.
        self.file = self.File(dir_path) if self.is_file is True else None
    
    class File:
        """Object of a file from a given path.
        
        Attributes:
            name (str): Name of the file, extension included.
            type (str): Type of file from file name.
        """
        def __init__(
            self,
            dir_path: str
        ) -> None:
            """File object from a file path.

            Args:
                dir_path (str): Path of the file.
            """
            self.name = self._get_file_name(dir_path)
            self.type = self._get_file_type(self.name)
        
        def _get_file_name(
                self,
                dir_path: str
        ) -> str:
            """A function to get the name of a file from a given path.

            Args:
                dir_path (str): Name of the path to get the file name from.

            Returns:
                str: Name of the file, including extension example: main.sql
            """
            return dir_path.split("/")[-1]
        
        def _get_file_type(
                self,
                file_name: str
        ) -> str:
            """Function to get the file type of a given file name.

            Args:
                file_name (str): Name of the file name to get file type.

            Returns:
                str: Name of the file type. example: sql
            """
            return file_name.split(".")[-1]