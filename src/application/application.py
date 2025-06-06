from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread

from src.application.sql_manager import SQLManager
from src.windows.main_window import MainWindow
from src.shared.funcs import *
from src.application.ai import AI

class Application(QApplication):
    def __init__(self):
        super().__init__()
        self._set_style()
        self._set_widgets()
        self.load_ai()
        
        self.ai = AI()

    def _set_style(self):
        regular_font = load_font("/assets/fonts/GeistMonoNerdFont-Regular.otf")
        
        self.setStyleSheet(
            "* {"
            f"font-family: {regular_font.family()};"
            "font-size: 10pt;"
            "}"
        )
    
    def _set_widgets(self):
        """Sets the widgets to the application."""
        self.main_window = MainWindow()
        self.main_window.show()
        
        self.sql_manager = SQLManager()
    
    def load_ai(self):
        """Deploys the translation AI into a running QThread."""
        self.ai_thread = QThread()
        self.ai_worker = AI()
        self.ai_worker.moveToThread(self.ai_thread)
        
        # Load the model on startup.
        self.ai_worker.modelLoaded.connect(self.model_loaded)
        self.ai_thread.started.connect(self.ai_worker.load_model)
        self.ai_thread.start()
    
    def model_loaded(self):
        def translation_found(value: tuple):
            origin_text, translated_text, source_lang, target_lang = value
            
            print(f"{source_lang} -> {target_lang} | {origin_text} -> {translated_text}")
            
        def error_found(text: str):
            print(text)
        
        self.ai_worker.translationReady.connect(translation_found)
        self.ai_worker.errorOccurred.connect(error_found)
        
        print("Running test translations:")
        self.ai_worker.translate("This is a test of the local translation module!", "en", "fr")
        self.ai_worker.translate("Hey, I'm testing the local translation module!", "en", "zh")
        self.ai_worker.translate("Wow, I wonder how well the local translation module works...", "en", "de")