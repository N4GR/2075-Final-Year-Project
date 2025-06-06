from src.shared.imports import *
from src.shared.pre_startup import run_startup

if __name__ == "__main__":
    # Pre-run startup before application.
    run_startup()
    
    application = Application()
    
    # Execute application.
    application.exec()