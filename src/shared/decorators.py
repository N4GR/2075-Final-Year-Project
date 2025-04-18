from src.shared.funcs import *
import logging
from functools import wraps
from inspect import isfunction, isclass

logging.basicConfig(
    level = logging.INFO,
    format = "[%(asctime)s] [%(name)s]: %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
    handlers = [
        # Save to a shared file
        logging.FileHandler("logs/recent.log"),
        logging.StreamHandler()
    ]
)

class Decorators:
    @staticmethod
    def property(cls):
        """A decorator to assign a window QWidget as a property in QApplication."""
        class Wrapped(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                
                # Store an instance of the class.
                set_property(name = cls.__name__, value = self)

        Wrapped.__name__ = cls.__name__
        Wrapped.__qualname__ = cls.__qualname__
        
        return Wrapped
    
    @staticmethod
    def autolog(cls):
        original_new = cls.__new__

        def logger_injected_new(cls, *args, **kwargs):
            instance = original_new(cls, *args, **kwargs) if original_new \
                else super(cls, cls).__new__(cls)
            instance.log = logging.getLogger(cls.__name__)
            return instance

        cls.__new__ = logger_injected_new
        return cls
    
    @staticmethod
    def api(target):
        from src.widgets.network_manager import ApiClient
        
        if isfunction(target):
            @wraps(target)
            def wrapper(self, *args, **kwargs):
                if not hasattr(self, "api") or self.api is None:
                    self.api = ApiClient()
            
                return target(self, *args, **kwargs)

            return wrapper
        
        elif isclass(target):
            original_init = target.__init__
            
            @wraps(original_init)
            def new_init(self, *args, **kwargs):
                self.api = ApiClient()
                original_init(self, *args, **kwargs)
            
            target.__init__ = new_init
            
            for attr_name in dir(target):
                if attr_name.startswith("__"):
                    continue
                
                attr = getattr(target, attr_name)
                if isfunction(attr):
                    decorated = Decorators.api(attr)
                    setattr(target, attr_name, decorated)
            
            return target

        else:
            raise TypeError("@Decorators.api can only be used on a function or class.")