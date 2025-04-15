from src.shared.imports import *

@Decorators.autolog
@Decorators.property
class LoginWindow(QWidget):
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.open_panel : QWidget = None
        
        self._set_style()
        self._set_layout()
        
        self.change_panel(LoginPanel)
        
    def _set_style(self):
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(
            "background-color: #1f1f1f;"
            "border-radius: 15px;"
        )
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
    
    def _set_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(100, 0, 100, 0)
            
        self.setLayout(self.main_layout)
    
    def change_panel(self, panel: QWidget) -> bool:
        """Changes the panel to a QWidget.

        Args:
            panel (QWidget): Panel to change to.

        Returns:
            bool: False if already open, True if change successful.
        """
        panel_name = panel.__name__
        
        if self.open_panel:
            self.open_panel.deleteLater()
        
        self.open_panel = panel(self)
        self.main_layout.addWidget(self.open_panel)
        
        return True

@Decorators.autolog
@Decorators.property
class RegisterPanel(QWidget):
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self._set_style()
        self._set_widgets()
        self._set_buttons()
        self._set_layout()
    
    def _set_style(self):
        self.setMaximumWidth(500)
        self.setMaximumHeight(500)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(
            "background-color: #171717;"
            "border-radius: 15px;"
        )
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
    
    def _set_widgets(self):
        self.username_input = UsernameInput(self)
        self.password_input = PasswordInput(self)
        self.profile_selection = ProfileSelection(self)
    
    def _set_buttons(self):
        self.button_layout = QHBoxLayout()
        
        self.login_button = LoginButton(self)
        self.register_button = RegisterButton(self)
        
        self.button_layout.addWidget(self.login_button)
        self.button_layout.addWidget(self.register_button)
    
    def _set_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 10, 20, 10)
        
        self.main_layout.addWidget(self.username_input)
        self.main_layout.addWidget(self.password_input)
        self.main_layout.addWidget(self.profile_selection)
        self.main_layout.addLayout(self.button_layout)
        
        self.setLayout(self.main_layout)

@Decorators.autolog
@Decorators.property
class LoginPanel(QWidget):
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
        self._set_widgets()
        self._set_buttons()
        self._set_layout()
    
    def _set_style(self):
        self.setMaximumWidth(500)
        self.setMaximumHeight(500)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(
            "background-color: #171717;"
            "border-radius: 15px;"
        )
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
    
    def _set_widgets(self):
        self.username_input = UsernameInput(self)
        self.password_input = PasswordInput(self)
    
    def _set_buttons(self):
        self.button_layout = QHBoxLayout()
        
        self.login_button = LoginButton(self)
        self.register_button = RegisterButton(self)
        
        self.button_layout.addWidget(self.login_button)
        self.button_layout.addWidget(self.register_button)
    
    def _set_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 10, 20, 10)
        
        self.main_layout.addWidget(self.username_input)
        self.main_layout.addWidget(self.password_input)
        self.main_layout.addLayout(self.button_layout)
        
        self.setLayout(self.main_layout)

class UserInput(QLineEdit):
    def __init__(self, parent: QWidget, input_type: str):
        super().__init__(parent)
        self.input_type = input_type
        self.error_showing = False
        
        self._set_style()
    
    def _set_style(self):
        self.setPlaceholderText(self.input_type.capitalize())
        self.setFixedHeight(50)
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
        
        self.setStyleSheet(
            "background-color: #1f1f1f;"
            "font-size: 15pt;"
        )
    
    def set_error(self, error_message: str):
        self.setStyleSheet(
            "background-color: #1f1f1f;"
            "font-size: 15pt;"
            "border: 2px solid red;"
            "border-radius: 15px;"
        )
        
        warning_icon = QIcon(path("/assets/icons/warning.png"))
        warning_action = QAction(warning_icon, error_message, self)
        warning_action.setVisible(True)
        
        self.addAction(warning_action, QLineEdit.ActionPosition.TrailingPosition)
        
        self.error_showing = True
    
    def reset(self):
        if self.error_showing is False:
            return
        
        for action in self.actions():
            self.removeAction(action)
        
        self.setStyleSheet(
            "background-color: #1f1f1f;"
            "font-size: 15pt;"
        )
        
        self.error_showing = False

class UsernameInput(UserInput):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "username")
    
class PasswordInput(UserInput):
    def __init__(self, parent: QWidget):
        super().__init__(parent, "password")
        self.setEchoMode(QLineEdit.EchoMode.Password)

class Button(QPushButton):
    def __init__(self, parent: QWidget, button_type: str):
        super().__init__(parent)
        self.button_type = button_type
        self.setText(button_type.upper())
        
        self.setFixedSize(200, 100)
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
        
        self.setStyleSheet(
            "background-color: #1f1f1f;"
            "color: white;"
            "font-weight: bold;"
            "font-size: 20pt;"
        )

@Decorators.autolog
class LoginButton(Button):
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent, "login")
        
        self.clicked.connect(self._on_click)
        
    def _on_click(self):
        window : LoginWindow = get_property("LoginWindow")
        open_panel : QWidget = window.open_panel

        if not open_panel.__class__.__name__ == "LoginPanel":
            window.change_panel(LoginPanel)
            
            return
        
        # Input variables.
        panel : LoginPanel = self.parentWidget()
        username_input : UsernameInput = panel.username_input
        password_input : PasswordInput = panel.password_input
        
        username_input.reset()
        password_input.reset()
        
        if username_input.text() == "":
            username_input.set_error("Missing username.")

            return
        
        if password_input.text() == "":
            password_input.set_error("Missing password.")
            
            return
        
        username = username_input.text()
        password = password_input.text()
        
        self.login_user(username, password, "default")

    @Decorators.api
    def login_user(self, username: str, password: str, profile: str):
        self.api : ApiClient = self.api
        payload = {
            "username": username,
            "password": password,
            "profile": "default"
        }
        
        self.api.post("http://localhost:8080/login", payload, self._api_response)

    def _api_response(self, response: dict):
        if "sucess" in response:
            self.log.info("Login successful.")
            
            return
        
        panel : RegisterPanel = self.parentWidget()
        username_input : UsernameInput = panel.username_input
        password_input : PasswordInput = panel.password_input
        
        username_input.reset()
        password_input.reset()
        
        if "error" in response:
            result_text = response["error"]
            
            if result_text == "Password doesn't match.":
                password_input.set_error("Password doesn't match.")
                
                return
            
            if result_text == "Username not found.":
                username_input.set_error("User not found.")
                
                return
        
        
        print(response)

@Decorators.autolog
class RegisterButton(Button):
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent, "register")
        
        self.clicked.connect(self._on_click)
        
    def _on_click(self):
        window : LoginWindow = get_property("LoginWindow")
        open_panel : QWidget = window.open_panel

        if not open_panel.__class__.__name__ == "RegisterPanel":
            window.change_panel(RegisterPanel)
            
            return
        
        # Input variables.
        panel : RegisterPanel = self.parentWidget()
        username_input : UsernameInput = panel.username_input
        password_input : PasswordInput = panel.password_input
        profile_selection : ProfileSelection = panel.profile_selection
        
        username_input.reset()
        password_input.reset()
        
        if username_input.text() == "":
            username_input.set_error("Missing username.")

            return
        
        if password_input.text() == "":
            password_input.set_error("Missing password.")
            
            return
        
        username = username_input.text()
        password = password_input.text()
        
        self.register_user(username, password, "test")
    
    @Decorators.api
    def register_user(self, username: str, password: str, profile: str):
        self.api : ApiClient = self.api
        payload = {
            "username": username,
            "password": password,
            "profile": "default"
        }
        
        self.api.post("http://localhost:8080/register", payload, self._api_response)
    
    def _api_response(self, response: dict):
        if "success" in response:
            self.log.info("Registration successful.")
            
            return
        
        panel : RegisterPanel = self.parentWidget()
        username_input : UsernameInput = panel.username_input
        username_input.reset()
        
        if "error" in response:
            result_text = response["error"]
            
            if result_text == "Username exists.":
                username_input.set_error("Username exists.")
                
                return
        

class ProfileSelection(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.max_columns = 8
        self.max_rows = 2

        self._set_layout()
        self.load_profile_pictures()
        
        self.setFixedHeight(self.sizeHint().height())
    
        self.selected_profile : ProfilePicture = self.main_layout.itemAtPosition(0, 0).widget()
        self.selected_profile.set_selected()
    
    def _set_layout(self):
        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(self.main_layout)
    
    def load_profile_pictures(self):
        profile_pictures = [path("/assets/profiles") + f"/{x}" for x in os.listdir(path("/assets/profiles"))]
        
        for row in range(self.max_rows):
            for column in range(self.max_columns):
                item_count = (self.max_columns * (row) + column)
                self.main_layout.addWidget(ProfilePicture(self, profile_pictures[item_count]), row, column)
                
class ProfilePicture(QPushButton):
    def __init__(self, parent: QWidget, icon_src: str):
        super().__init__(parent)
        self.icon_src = icon_src
        self._set_style()
        
        self.clicked.connect(self._on_click)

    def _set_style(self):
        self.setFixedSize(50, 50)
        
        self.setIcon(
            QPixmap(self.icon_src).scaled(
                self.size(),
                aspectMode = Qt.AspectRatioMode.IgnoreAspectRatio,
                mode = Qt.TransformationMode.SmoothTransformation
            )
        )
        self.setIconSize(QSize(self.height() - 5, self.width() - 5))
    
    def set_selected(self):
        self.is_selected = True
        
        self.setStyleSheet("border-radius: 25px; border: 5px solid green;")
    
    def set_unselected(self):
        self.is_selected = False
        
        self.setStyleSheet("")
    
    def _on_click(self):
        register_panel : RegisterPanel = get_property("RegisterPanel")
        parent : ProfileSelection = self.parentWidget()
        selected_profile = parent.selected_profile
        
        if selected_profile.icon_src == self.icon_src:
            return
        
        selected_profile.set_unselected()
        self.set_selected()
        
        parent.selected_profile = self