from src.imports import *

class Login(QWidget):
    def __init__(
            self,
            parent: QWidget,
            main_window: QWidget
    ):
        super().__init__(parent)
        
        # Assigning args to self.
        self.main_window = main_window
        self.config = LoginConfig()
    
        self._set_design()
        self._set_widgets()
    
    def _set_design(self):
        self.setFixedSize(self.parentWidget().size())
    
    def _set_widgets(self):
        self.background = self.Background(
            parent = self,
            config = self.config
        )
        
        self.texture = self.Texture(
            parent = self,
            config = self.config.texture
        )
        
        self.triangle = self.Triangle(
            parent = self,
            config = self.config.triangle
        )
    
        self.menu = self.Menu(
            parent = self,
            config = self.config.menu
        )
        
        self.title = self.Title(self)

    def resizeEvent(self, event: QResizeEvent):
        # Resize the background to fill the size of the login screen.
        self.background.setFixedSize(self.size())
        self.triangle.setFixedSize(self.size())
        
        half_x = int(self.width() / 2)
        half_y = int(self.height() / 2)
        
        self.texture.move(half_x, half_y)
        self.texture.setFixedSize(half_x, half_y)
        
        self.menu.move(
            int(self.width() / 2)
            - int(self.menu.width() / 2),
            int(self.height() / 2)
            - int(self.menu.height() / 2)
            - 50
        ) # Move menu to always centre with a -50 offset to the Y coordinate.
        
        # Move the title so it's stuck to the bottom.
        self.title.move(
            10,
            self.height() - (self.title.height() + 10)
        )
        
        return super().resizeEvent(event)
    
    class Title(QWidget):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self._set_design()
            self._set_widgets()
        
        def _set_design(self):
            self.setFixedSize(275, 64)
            
            self.main_layout = QHBoxLayout()
            self.main_layout.setSpacing(0)
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            
            self.setLayout(self.main_layout)
        
        def _set_widgets(self):
            self.icon = self.Icon(self)
            self.title = self.Title(self)
            
            self.main_layout.addWidget(self.icon)
            self.main_layout.addWidget(self.title)
        
        class Icon(QLabel):
            def __init__(self, parent: QWidget):
                super().__init__(parent)
                self._set_design()
            
            def _set_design(self):
                self.setFixedSize(64, 64)
                
                pixmap = QPixmap(
                    path("resources/assets/icons/icon.png")
                ).scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.FastTransformation
                )
                self.setPixmap(pixmap)
        
        class Title(QLabel):
            def __init__(self, parent: QWidget):
                super().__init__(parent)
                self._set_design()
            
            def _set_design(self):
                self.setText("METAPHRAST")
                
                self.setFont(self.get_font())
            
            def get_font(self) -> QFont:
                font_id = QFontDatabase.addApplicationFont(path("resources/assets/fonts/Outfit-Bold.ttf"))
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                
                font = QFont(font_families[0], 24)
                
                return font
       
    class Background(QLabel):
        def __init__(
                self,
                parent: QWidget,
                config: LoginConfig
        ):
            super().__init__(parent)
            self.config = config
            
            self.setFixedSize(self.parentWidget().size())
            self.setStyleSheet(f"background-color: {self.config.background_colour}")
    
    class Texture(QLabel):
        def __init__(
                self,
                parent: QWidget,
                config: LoginConfig.Texture
        ):
            super().__init__(parent)
            self.config = config
            
            self.dot_size = 50
            self.dot_offset = 10
            self.extra_items = 3
            
            self._set_design()
            
            self.dot_pixmap = self._get_dot_pixmap()
            
            self.required_columns = int(
                self.height()
                / (
                    self.dot_size
                    - self.dot_offset
                )
            ) + self.extra_items
            
            self.required_rows = int(
                self.width()
                / (
                    self.dot_size
                    - self.dot_offset
                )
            ) + self.extra_items
            
            self.setPixmap(self._get_pixmap())
        
        def _set_design(self):
            self.move(int(self.parentWidget().width() / 2), int(self.parentWidget().height() / 2))
            self.setFixedHeight(int(self.parentWidget().height() / 2))
            self.setFixedWidth(int(self.parentWidget().width() / 2))
            self.setStyleSheet("background-color: transparent;")
        
        def _get_dot_pixmap(self) -> QPixmap:
            colour_data = self.config.icon_colour.replace("rgb(", "").replace(")", "").split(",")
            red = int(colour_data[0])
            green = int(colour_data[1])
            blue = int(colour_data[2])

            dot_pixmap = change_svg_colour(
                src = path(self.config.icon_src),
                size = (self.dot_size, self.dot_size),
                colour = (red, green, blue)
            )
            
            return dot_pixmap
        
        def _get_pixmap(self) -> QPixmap:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.GlobalColor.transparent)
            
            # Create the painter object to paint to the new pixmap.
            painter = QPainter(pixmap)

            for row in range(self.required_rows):
                for column in range(self.required_columns):
                    position = QPoint(
                        (self.dot_size - self.dot_offset)
                        * row,
                        (self.dot_size - self.dot_offset)
                        * column
                    )
                    
                    painter.drawPixmap(position, self.dot_pixmap)
            
            painter.end()
            
            return pixmap
        
        def resizeEvent(self, event: QResizeEvent):
            self.setFixedHeight(int(self.parentWidget().height() / 2))
            self.setFixedWidth(int(self.parentWidget().width() / 2))
            
            self.required_columns = int(
                self.height()
                / (
                    self.dot_size
                    - self.dot_offset
                )
            ) + self.extra_items
            
            self.required_rows = int(
                self.width()
                / (
                    self.dot_size
                    - self.dot_offset
                )
            ) + self.extra_items
            
            self.setPixmap(self._get_pixmap())
            
            return super().resizeEvent(event)
        
    class Triangle(QLabel):
        def __init__(
                self,
                parent: QWidget,
                config: LoginConfig.Triangle
        ):
            super().__init__(parent)
            self.config = config
            
            self._set_design()

        def _set_design(self):
            self.setFixedSize(self.parentWidget().size())
            self.setPixmap(self.create_triangle_pixmap(self.width(), self.height()))
            self.setStyleSheet("background-color: transparent;") # So objects can be viewed behind it.

        def create_triangle_pixmap(self, width: int, height: int) -> QPixmap:
            colour_values = self.config.background_colour.replace("rgb(", "").replace(")", "").split(",")
            red = int(colour_values[0])
            green = int(colour_values[1])
            blue = int(colour_values[2])
            
            colour = QColor(red, green, blue)
            
            # Transparent pixmap to paint to.
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.GlobalColor.transparent)
            
            # Painter object to draw triangle.
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Define the points of the triangle.
            top_left = QPoint(0, 0)
            top_right = QPoint(self.width(), 0)
            right_middle = QPoint(self.width(), int(self.height() / 2))
            bottom_middle = QPoint(int(self.width() / 2), self.height())
            bottom_left = QPoint(0, self.height())
            
            # Draw the triangle.
            painter.setPen(colour) # Create the lines.
            painter.setBrush(colour) # Fill the triangle.
            
            draw_points = [
                top_left, top_right,
                right_middle, bottom_middle,
                bottom_left
            ] # Points to draw in order.
            
            painter.drawPolygon(draw_points) # Draw the shape.
            
            painter.end()
            
            return pixmap
        
        def resizeEvent(self, event: QResizeEvent):
            pixmap = self.create_triangle_pixmap(event.size().width(), event.size().height())
            self.setPixmap(pixmap)
            
            return super().resizeEvent(event)
    
    class Menu(QWidget):
        def __init__(
                self,
                parent: QWidget,
                config: LoginConfig.Menu
        ):
            super().__init__(parent)
            self.config = config

            self._set_design()
            self._set_widgets()
        
        def _set_design(self):
            self.setFixedSize(
                self.parentWidget().width() * 0.5,
                self.parentWidget().height() * 0.5
            )
            
            self.main_layout = QVBoxLayout()
            self.main_layout.setSpacing(10)
            self.main_layout.setContentsMargins(10, 10, 10, 10)
            
            self.setLayout(self.main_layout)
        
        def _set_widgets(self):
            self.background = self.Background(
                parent = self,
                config = self.config
            )
            
            self.username = self.UsernameInput(self)
            self.password = self.PasswordInput(self)
            
            self.buttons = self.Buttons(self)
            
            self.main_layout.addWidget(self.username)
            self.main_layout.addWidget(self.password)
            self.main_layout.addWidget(self.buttons)
        
        def resizeEvent(self, event: QResizeEvent):
            self.background.setFixedSize(self.size()) # Background to always fill widget.
            
            return super().resizeEvent(event)

        class Background(QLabel):
            def __init__(
                    self,
                    parent: QWidget,
                    config: LoginConfig
            ):
                super().__init__(parent)
                self.config = config
                
                self.setFixedSize(self.parentWidget().size())
                self.setStyleSheet(
                    f"background-color: {self.config.background_colour};"
                    "border-radius: 15px"
                )
        
        class InputArea(QWidget):
            def __init__(self, parent: QWidget, title: str):
                super().__init__(parent)
                self._set_design()
                
                self.text_input = self.TextInput(parent)
                self.label = self.TextInputLabel(parent, title)
            
                self.main_layout.addWidget(self.label)
                self.main_layout.addWidget(self.text_input)
            
            def _set_design(self):
                self.main_layout = QVBoxLayout()
                self.main_layout.setSpacing(0)
                self.main_layout.setContentsMargins(0, 0, 0, 0)
                
                self.setLayout(self.main_layout)
            
            class TextInput(QLineEdit):
                def __init__(self, parent: QWidget):
                    super().__init__(parent)
                    self._set_design()
            
                def _set_design(self):
                    self.setStyleSheet("border-radius: 5px;")
                    
                    self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    self.setFixedHeight(40)
                    
                    font = self.font()
                    font.setPointSize(10)
                    
                    self.setFont(font)
        
            class TextInputLabel(QLabel):
                def __init__(self, parent: QWidget, title: str):
                    super().__init__(parent, text = title)
                    self.setStyleSheet("background-color: transparent;")
                    
                    font = self.font()
                    font.setBold(True)
                    
                    self.setFont(font)
        
        class UsernameInput(InputArea):
            def __init__(self, parent: QWidget):
                super().__init__(parent, "USERNAME")
                
        class PasswordInput(InputArea):
            def __init__(self, parent: QWidget):
                super().__init__(parent, "PASSWORD")
                self.text_input.setEchoMode(QLineEdit.EchoMode.Password)

        class Buttons(QWidget):
            def __init__(self, parent: QWidget):
                super().__init__(parent)
                self._set_design()
                self._set_widgets()
            
            def _set_design(self):
                self.main_layout = QVBoxLayout()
                
                self.setLayout(self.main_layout)
            
            def _set_widgets(self):
                self.login = self.LoginButton(self.parentWidget())
                self.register = self.RegisterButton(self.parentWidget())
                
                self.main_layout.addWidget(self.login, alignment = Qt.AlignmentFlag.AlignCenter)
                self.main_layout.addWidget(self.register, alignment = Qt.AlignmentFlag.AlignLeft)
                
            class LoginButton(QPushButton):
                def __init__(self, parent: QWidget):
                    super().__init__(parent)
                    
                    self._set_design()
                    self._set_connections()
                
                def _set_design(self):
                    self.setFixedHeight(50)
                    self.setFixedWidth(150)
                    
                    self.setStyleSheet(
                        "border-radius: 8px;"
                    )
                    
                    font = self.font()
                    font.setPointSize(13)
                    font.setBold(True)
                    
                    self.setFont(font)
                    
                    self.setText("Log In")
                
                def _set_connections(self):
                    self.clicked.connect(self._on_click)
                    self.pressed.connect(self._on_press)
                    self.released.connect(self._on_release)
                
                def _on_press(self):
                    pass
                
                def _on_release(self):
                    pass
                
                def _on_click(self):
                    print("Profile clicked!")
                    self.login_widget = self.parentWidget().parentWidget().parentWidget()
                    self.main_menu = self.login_widget.parentWidget()
                    
                    # Show the topbar.
                    self.main_menu.top_bar.show()
            
                    # Delete the login menu widget.
                    self.login_widget.deleteLater()
            
            class RegisterButton(QPushButton):
                def __init__(self, parent: QWidget):
                    super().__init__(parent)
                    
                    self._set_design()
                    self._set_connections()
                
                def _set_design(self):
                    self.setFixedWidth(100)
                    
                    font = self.font()
                    font.setPointSize(10)
                    font.setBold(True)
                    
                    self.setFont(font)
                    
                    self.setText("Register")
                    self.setStyleSheet(
                        "background-color: transparent;"
                        "border: none;"
                        "color: rgb(128, 0, 32);"
                        "text-align: left;"
                    )
                
                def _set_connections(self):
                    self.clicked.connect(self._on_click)
                
                def _on_click(self):
                    print("Button clicked!")