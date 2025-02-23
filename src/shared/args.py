from src.shared.imports import *

class Args:
    def __init__(self):
        self.passed_args = sys.argv
        
        if "--to_file" in self.passed_args:
            self.origin_was_deleted = self.delete_log_dir()
    
    def show_help(self):
        """Function to show the help message if --help argument is issued."""
        pass
    
    def contains_arg(self, arg: str) -> bool:
        """Function that will return a bool on whether an argument is given or not.

        Args:
            arg (str): Argument to see if it's given.

        Returns:
            bool: True | False value on existence of arg in given args.
        """
        if arg in self.passed_args:
            return True
        else:
            return False
    
    def delete_log_dir(self) -> bool:
        """Function that will be used to delete the logs directory when the program is executed - only to be used if --to_file flag is set in launch arguments.

        Returns:
            bool: True | False - whether or not the directory was deleted.
        """
        logs_dir = "logs"
        
        if os.path.isdir(logs_dir): # If the logs directory exists.
            shutil.rmtree(logs_dir) # Remove directory and its contents.
            
            return True
        else:
            return False