from src.shared.imports import *

class LoginWindow(QWidget):
    def __init__(self, parent: QMainWindow):
        """A QWidget subclass functioning as the LoginWindow of the application.

        Args:
            parent (QMainWindow): Parent of the login window, a QMainWindow object.
        """        
        super().__init__(parent)
        
        self._add_design()
        self._add_widgets()
        self._add_layout()
        
        self.show() # Show the window once all has loaded.
    
    def _add_design(self):
        """A function to add design elements to the widget."""
        self.setFixedSize(self.parentWidget().size()) # Set a minimum size for the window to be displayed as.
    
    def _add_widgets(self):
        """A function to add widgets related to the widget to the widget."""
        self.background_label = self.BackgroundLabel(self)
        self.login_panel = self.LoginPanel(self)
    
    def _add_layout(self):
        """A function to add the layout to the widget."""
        pass
    
    def resizeEvent(self, event: QResizeEvent):
        """A function called when the window is resized.

        Args:
            event (QResizeEvent): QResizeEvent from PySide6.
        """
        self.background_label.setFixedSize(self.size()) # Set the size of the label to fill the window.
        
        self.login_panel.move(
            self.width() * 0.1, # 10% of the window width.
            self.height() / 2
            - self.login_panel.height() / 2 # To centre the panel vertically.
            - self.height() * 0.1 # 10% offset to push upward.
        )
        
        return super().resizeEvent(event)
    
    class BackgroundLabel(QLabel):
        def __init__(self, parent: QWidget):
            """A QLabel object functioning as the background label to fill the widget.

            Args:
                parent (QWidget): Parent widget of the label.
            """            
            super().__init__(parent)
            self.setFixedSize(parent.size())
            self.setStyleSheet("background-color: #313338;")
    
    class LoginPanel(QWidget):
        def __init__(self, parent: QWidget):
            """A QWidget object containing other widgets related to the login panel - username, password ect.

            Args:
                parent (QWidget): Parent widget of the widget.
            """            
            super().__init__(parent)
            self.setFixedSize(
                400, 400
            )
            
            self.background_label = self.BackgroundLabel(self)
            
            self.username_input = self.Username(self)
            self.password_input = self.Password(self)
            self.buttons = self.Buttons(self)
            
            self.main_layout = QVBoxLayout()
            self.main_layout.addWidget(self.username_input)
            self.main_layout.addWidget(self.password_input)
            self.main_layout.addWidget(self.buttons)
            
            self.setLayout(self.main_layout)
        
        def resizeEvent(self, event: QResizeEvent):
            """A function called when the window is resized.

            Args:
                event (QResizeEvent): QResizeEvent from PySide6.
            """
            self.background_label.setFixedSize(self.size()) # Set the size of the label to fill the window.
            
            return super().resizeEvent(event)
            
        class BackgroundLabel(QLabel):
            def __init__(self, parent: QWidget):
                """A QLabel object functioning as the background label to fill the widget.

                Args:
                    parent (QWidget): Parent widget of the label.
                """            
                super().__init__(parent)
                self.setFixedSize(parent.size())
                self.setStyleSheet(
                    "background-color: #1e1f22;"
                    "border-radius: 15px;" # Add a rounded border to the widget.
                )
        
        class UserInput(QWidget):
            def __init__(self, parent: QWidget, input_type: str):
                """A QWidget subclass used as the main class of a user input - containing a QLabel followed by a QTextEdit.

                Args:
                    parent (QWidget): Parent widget of the widget.
                    input_type (str): Input type to be used as the text label and input placeholder text.
                """
                super().__init__(parent)
                self.text_label = self.get_text_label(input_type)
                self.text_input = self.get_text_input(input_type)
                
                self.main_layout = QVBoxLayout()
                self.main_layout.addWidget(self.text_label)
                self.main_layout.addWidget(self.text_input)
                
                self.setLayout(self.main_layout)

            def get_text_label(self, text: str) -> QLabel:
                """A function to retrieve the text label in the user input.

                Args:
                    text (str): Text to be displayed on the label.

                Returns:
                    QLabel: Generated returned label.
                """
                font_manager : FontManager = QApplication.instance().property("FontManager") # Get the font manager from the Application instance.
                font = font_manager.caskaydia.bold # Retrieve the caskaydia bold font.
                font.setPointSize(20)
                
                text_label = QLabel()
                text_label.setText(text.upper())
                text_label.setFont(font)
                
                return text_label
            
            def get_text_input(self, text: str) -> QLineEdit:
                """A function to retrieve the text input widget.

                Args:
                    text (str): Text to be displayed on the QLineEdit

                Returns:
                    QLineEdit: Generated returned QLineEdit.
                """
                font_manager : FontManager = QApplication.instance().property("FontManager") # Get the font manager from the Application instance.
                font = font_manager.caskaydia.regular # Retrieve the caskaydia regular font.
                font.setPointSize(10)
                
                text_edit = QLineEdit()
                text_edit.setPlaceholderText(text)
                text_edit.setFont(font)
                text_edit.setFixedHeight(40)
                text_edit.setStyleSheet("""
                    QLineEdit {
                        border: 2px solid #4f525a;
                        border-radius: 5px;
                        background-color: #383a40;
                    }
                """)

                return text_edit

        class Username(UserInput):
            def __init__(self, parent: QWidget):
                """A UserInput subclass for the Username in the login panel.

                Args:
                    parent (QWidget): Parent of the widget.
                """                
                super().__init__(parent, "Username")
        
        class Password(UserInput):
            def __init__(self, parent: QWidget):
                """A UserInput subclass for the Password input in the login panel.

                Args:
                    parent (QWidget): Parent of the widget.
                """                
                super().__init__(parent, "Password")
                self.text_input.setEchoMode(QLineEdit.EchoMode.Password) # Replace text added to the password input with *
        
        class Buttons(QWidget):
            def __init__(self, parent: QWidget):
                """A QWidget subclass containing buttons related to the login panel.

                Args:
                    parent (QWidget): Parent of the widget.
                """
                super().__init__(parent)
                self.login_button = self.Login(self)
                self.register_button = self.Register(self)
                
                self.main_layout = QHBoxLayout()
                self.main_layout.addWidget(self.login_button)
                self.main_layout.addWidget(self.register_button)
                self.setLayout(self.main_layout)
            
            class Button(QPushButton):
                def __init__(self, parent: QWidget, button_name: str):
                    """A QPushButton subclass being the main class of all button widgets related to the buttons class.

                    Args:
                        parent (QWidget): Parent of the widget.
                    """
                    super().__init__(parent)
                    font_manager : FontManager = QApplication.instance().property("FontManager") # Get the font manager from the Application instance.
                    font = font_manager.caskaydia.bold # Retrieve the caskaydia bold font.
                    font.setPointSize(15)
                    
                    self.setText(button_name.upper())
                    self.setFont(font)
                    
                    self.setFixedHeight(50)
            
            class Login(Button):
                def __init__(self, parent: QWidget):
                    """A Login class of the Button subclass to handle logging in functionality.

                    Args:
                        parent (QWidget): Parent of the widget.
                    """                    
                    super().__init__(parent, "Login")
                    self.clicked.connect(self._click)
                
                def _click(self):
                    pass
            
            class Register(Button):
                def __init__(self, parent: QWidget):
                    """A Register class of the Button subclass to handle registering functionality.

                    Args:
                        parent (QWidget): Parent of the widget.
                    """                    
                    super().__init__(parent, "Register")
                    self.clicked.connect(self._click)
                
                def _click(self):
                    pass
            
            