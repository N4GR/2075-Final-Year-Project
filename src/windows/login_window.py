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
        self.profile_upload = ProfileUpload(self)
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
        self.main_layout.addWidget(self.profile_upload)
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
    
    @Decorators.api
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
        
        # API handling.
        self.api : ApiClient
        
        username = username_input.text()
        password = password_input.text()
        
        from src.widgets.authentication import Login
        
        self.login = Login(self, username, password).run()
    
@Decorators.autolog
class RegisterButton(Button):
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent, "register")
        
        self.clicked.connect(self._on_click)
    
    @Decorators.api
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
        profile_upload : ProfileUpload = panel.profile_upload
        
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
        
        if profile_upload.uploading_profile is None:
            profile_src = path(profile_selection.selected_profile.icon_src)
            
            profile_size = os.path.getsize(profile_src)
            profile_file_size_kb = round(profile_size / 1024, 2)
            progress_label : FileUploadProgressLabel = profile_upload.file_upload_progress_label
            progress_label.setText(f"0/{profile_file_size_kb}KB")
            progress_label.setHidden(False)
        
        else:
            profile_src = path(profile_upload.uploading_profile)
        
        from src.widgets.authentication import Register
        
        self.register = Register(self, username, password, profile_src).run()
    
    def _registration_complete(self):
        from src.widgets.authentication import Login
        
        panel : RegisterPanel = self.parentWidget()
        username_input : UsernameInput = panel.username_input
        password_input : PasswordInput = panel.password_input
        
        username = username_input.text()
        password = password_input.text()
        
        self.login = Login(self, username, password).run()

@Decorators.property
class ProfileSelection(QWidget):
    def __init__(self, parent: QWidget):
        """Profile selection QWidget, used for the user to select a profile from the defaults available.
        
        Args:
            parent (QWidget): Parent of the QWidget.
        """
        super().__init__(parent)
        self._loaded_profiles : list[ProfilePicture] = [] # List of loaded ProfilePicture objects.
        self.max_columns = 8 # Maximum columns in QGridLayout.
        self.max_rows = 2 # Maximum rows in QGridLayout.
        self.selected_profile : ProfilePicture = None # The user's selected profile picture.

        self._set_layout()
        self.load_profile_pictures()
        self.set_default_profile()
        
        # Adjust height after layout loaded.
        self.setFixedHeight(self.sizeHint().height())
    
    def _set_layout(self):
        """Sets the layout of the widget."""
        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(self.main_layout)
    
    def set_default_profile(self):
        """Randomly selects a loaded default profile picture."""
        random_profile = random.choice(self._loaded_profiles)
        random_profile.set_selected()
        
        self.selected_profile = random_profile
    
    def load_profile_pictures(self):
        """Loads images from /assets/profiles into the QGridLayout."""
        profile_pictures = [path("/assets/profiles") + f"/{x}" for x in os.listdir(path("/assets/profiles"))]
        
        for row in range(self.max_rows):
            for column in range(self.max_columns):
                item_count = (self.max_columns * (row) + column)
                
                profile_obj = ProfilePicture(self, profile_pictures[item_count])
                self.main_layout.addWidget(profile_obj, row, column)
                self._loaded_profiles.append(profile_obj)
                
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
        
        self.setStyleSheet("border-radius: 25px;")
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 0)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
    
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

@Decorators.property
class ProfileUpload(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_widgets()
        self._set_layout()
        
        self.uploading_profile : str | None = None # Profile selected to be uploaded.
        
        # Resize after layout widgets added.
        self.setFixedHeight(self.sizeHint().height())
    
    def _set_widgets(self):
        self.file_button = FileButton(self)
        self.file_name_label = FileNameLabel(self)
        self.file_correct_label = FileCorrectLabel(self)
        self.file_upload_progress_label = FileUploadProgressLabel(self)
        
        # Move correct label to top right of file_button.
        self.file_correct_label.move(self.file_button.rect().topRight())
    
    def _set_layout(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setSpacing(10)
        
        self.main_layout.addWidget(self.file_button)
        self.main_layout.addWidget(self.file_name_label)
        self.main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.main_layout.addWidget(self.file_upload_progress_label)
        
        self.setLayout(self.main_layout)

@Decorators.autolog
class FileButton(QPushButton):
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
        
        self.max_file_size_mb = 1
        self.max_file_size_kb = self.max_file_size_mb * 1024
        self.max_file_size_b = self.max_file_size_kb * 1024
        
        self.accepted_file_types = [
            "*.png", "*.jpg", "*.jpeg", "*.webp"
        ]
        
        self.clicked.connect(self._on_click)
    
    def _set_style(self):
        self.setFixedSize(50, 50)
    
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
        
        self.setIcon(QPixmap(path("/assets/icons/upload.png")))
        self.setIconSize(QSize(self.height() - 20, self.width() - 20))
    
    def _on_click(self):
        """Opens a QFileDialog object to accept an image file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select an image.",
            "",
            f"Image File ({' '.join(self.accepted_file_types)})"
        )
        
        parent : ProfileUpload = self.parentWidget()
        parent.file_correct_label.setHidden(True)
        parent.file_upload_progress_label.setHidden(True)
        
        file_name = os.path.basename(file_path)
        
        if file_path:
            file_size = os.path.getsize(file_path)
            
            file_size_kb = round(file_size / 1024, 2)
            file_size_mb = round(file_size_kb / 1024, 2)
            
            if file_size <= self.max_file_size_b: # File size is correct.
                self.log.info(f"Profile selected successfully ({file_size_kb}kb)[{file_path}]")
                
                parent.uploading_profile = file_path
                parent.file_name_label.setText(file_name)
                parent.file_upload_progress_label.setText(f"0/{file_size_kb}KB")
                parent.file_upload_progress_label.setHidden(False)
                parent.file_correct_label.setHidden(False)
            
            else: # File size too large.
                self.log.info(f"Failed profile selection [{file_name} {file_size_kb} kb] limit = [{self.max_file_size_kb} kb]")
                
                QMessageBox.warning(
                    self,
                    "File Too Large",
                    f"File exceeded the maximum file size of {self.max_file_size_mb}MB, your file is {file_size_mb}MB"
                )
                
                return

class FileNameLabel(QLabel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setText("Upload a profile or select one from defaults.")

class FileCorrectLabel(QLabel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.setFixedSize(20, 20)
        pixmap = change_image_colour(path("/assets/icons/check_circle.png"), (38, 255, 0))
        self.setPixmap(pixmap.scaled(
            self.size(),
            aspectMode = Qt.AspectRatioMode.IgnoreAspectRatio,
            mode = Qt.TransformationMode.SmoothTransformation
        ))
        self.setHidden(True) # Start hidden.
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

class FileUploadProgressLabel(QLabel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setHidden(True)