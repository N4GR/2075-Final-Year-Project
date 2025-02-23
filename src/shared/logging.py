from src.shared.imports import *

class Logger:
    def __init__(
        self,
        class_name: str
    ) -> None:
        """Logger object that will initialise and handle all logging to terminal and file.

        Args:
            class_name (str): _description_
        """
        self.log = logging.getLogger(class_name) # Obtaining the logger of the class.
        self.handlers = self._get_handlers()
        
        self._launch_config()

    def _get_handlers(self) -> list[logging.Handler]:
        launch_args = sys.argv # Arguments given when launching the program.
        handlers = []
        
        if "--debug" in launch_args:
            handlers.append(
                logging.StreamHandler()
            ) # Handler to print to terminal.
        
        if "--to_file" in launch_args:
            os.makedirs("logs", exist_ok = True) # Creating logs directory if it doesn't exist.
            
            handlers.append(
                logging.FileHandler("logs/latest.log"),
            ) # Handler to print to file.
        
        return handlers
    
    def _launch_config(self) -> None:
        logging.basicConfig(
            level = logging.DEBUG,
            format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers = self.handlers
        )
    
    def _create_except_hook(
        self,
        exc_type,
        exc_value,
        exc_traceback
    ) -> None:
        """Custom except hook that will capture exceptions for logging purposes.

        Args:
            exc_type (_type_): _description_
            exc_value (_type_): _description_
            exc_traceback (_type_): _description_
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # Allow the program to terminal logging on a keyboard interrupt execution.
            sys.__excepthook__(
                exc_type,
                exc_value,
                exc_traceback
            )
            
            return
        
        logging.error(
            msg = "Uncaught Exception",
            exc_info = (
                exc_type,
                exc_value,
                exc_traceback
            )
        )

def setup_logger(class_name: str) -> logging.Logger:
    logging = Logger(class_name)
    log = logging.log
    
    # Setting exception hook.
    sys.excepthook = logging._create_except_hook
    
    return log