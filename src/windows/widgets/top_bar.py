from src.imports import *

from src.windows.widgets.login import Login

class TopBar(QWidget):
    def __init__(
            self,
            parent: QWidget,
            main_window: QWidget
    ):
        super().__init__(parent)
        
        # Assigning args to self.
        self.main_window = main_window
        self.config = TopBarConfig()

        self._set_design() # Adding design elements to widget.
        self._set_widgets()
    
    def _set_design(self):
        pass
    
    def _set_widgets(self):
        self.background = self.Background(
            parent = self,
            config = self.config
        )
        
        self.buttons = self.Buttons(
            parent = self,
            main_window = self.main_window,
            config = self.config
        )
        
        self.hide_button = HideButton(
            self,
            self.config.hide_button
        )
    
    def resizeEvent(self, event: QResizeEvent):
        # Move the background colour with the top_bar widget.
        self.background.update_width(self.width())
        
        # Resize the buttons widget to the width of the top_bar.
        self.buttons.setFixedWidth(self.width())
        
        return super().resizeEvent(event)
    
    class Background(QLabel):
        def __init__(
                self,
                parent: QWidget,
                config: TopBarConfig
        ):
            super().__init__(parent)
            self.setStyleSheet(f"background-color: {config.background_colour}")
            self.setFixedHeight(50)
        
        def update_width(self, width: int):
            self.setFixedWidth(width)

    class Buttons(QWidget):
        def __init__(
                self,
                parent: QWidget,
                main_window: QWidget,
                config: TopBarConfig
        ):
            super().__init__(parent)
            
            # Assigning args to self.
            self.main_window = main_window
            self.config = config
        
            self._set_design() # Adding design element to widget.
            self._set_layouts()
            self._set_widgets()
        
        def _set_design(self):
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.setFixedHeight(50)
        
        def _set_layouts(self):
            self.left_layout = QHBoxLayout()
            self.left_layout.setContentsMargins(0, 0, 0, 0)
            self.left_layout.setSpacing(0)
            
            self.right_layout = QHBoxLayout()
            self.right_layout.setContentsMargins(0, 0, 0, 0)
            self.right_layout.setSpacing(0)
            
            self.main_layout = QHBoxLayout()
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            self.main_layout.setSpacing(0)
            
            self.main_layout.addLayout(self.left_layout)
            self.main_layout.addStretch()
            self.main_layout.addLayout(self.right_layout)
            
            self.setLayout(self.main_layout)
        
        def _set_widgets(self):
            self.profile_button = ProfileButton(self, self.config.profile_button, self.main_window)
            self.right_layout.addWidget(self.profile_button)

class TopBarButton(QPushButton):
    def __init__(
            self,
            parent: QWidget,
            config: TopBarConfig.ProfileButton
    ):
        super().__init__(parent)
        self.config = config
        
        self.original_width = 50
        self.original_height = 50
        
        self._set_design()
        self._set_connections()
        
    def _set_design(self):
        self.setStyleSheet("background-color: transparent; border: none;")
        
        self.setFixedSize(self.original_width, self.original_height)
        
        self._set_icon()
    
    def _set_icon(self) -> QIcon:
        values = self.config.icon_colour.replace("rgb(", "").replace(")", "").split(",")
        red = int(values[0])
        green = int(values[1])
        blue = int(values[2])
        
        self.recoloured_svg = change_svg_colour(
            src = self.config.icon_src,
            size = (self.original_width, self.original_height),
            colour = (red, green, blue)
        )
        
        self.setIcon(QIcon(self.recoloured_svg))
        self.setIconSize(QSize(self.original_width, self.original_height))
        
    def _set_connections(self):
        self.pressed.connect(self._on_press)
        self.released.connect(self._on_release)
    
    def _on_press(self):
        pressed_width = self.original_width - 5
        pressed_height = self.original_height - 5
        
        self.setIconSize(QSize(pressed_width, pressed_height))
    
    def _on_release(self):
        self.setIconSize(QSize(self.original_width, self.original_height))
    
    def change_icon(self, src: str):
        """A function to change the icon of the button, re-colouring the icon's SVG to the base icon colour.

        Args:
            src (str): Relative path of the icon.
        """
        values = self.config.icon_colour.replace("rgb(", "").replace(")", "").split(",")
        red = int(values[0])
        green = int(values[1])
        blue = int(values[2])
        
        self.recoloured_svg = change_svg_colour(
            src = path(src),
            size = (self.original_width, self.original_height),
            colour = (red, green, blue)
        )
        
        self.setIcon(QIcon(self.recoloured_svg))
        self.setIconSize(QSize(self.original_width, self.original_height))
        
class HideButton(TopBarButton):
    def __init__(
            self,
            parent: QWidget,
            config: TopBarConfig.Button
    ):
        super().__init__(parent, config)
        self._is_hidden = False
        
        self.clicked.connect(self._on_click)
    
    def get_hideable_widgets(self) -> list[QWidget]:
        """A function to retrieve a list of widgets wanted to animate in the hide button.

        Returns:
            list[QWidget]: A list of widgets to hide.
        """
        top_bar = self.parentWidget()
        buttons = self.parentWidget().buttons
        
        hideable_widgets : list[QWidget] = []
        hideable_widgets.append(buttons)
        hideable_widgets.append(top_bar.background) # Background widget.
        
        return hideable_widgets
    
    def _on_click(self):
        def get_animation(widget: QWidget, anim_type: str) -> QPropertyAnimation:
            """A function to initialise a hide animation on a widget.

            Args:
                widget (QWidget): The widget to hide.
                type (str): Type of animation to initialise, "show" or "hide"
            """
            start_position = widget.pos()

            if anim_type == "hide":
                end_position = QPoint(widget.x(), widget.y() - 50)
                
            elif anim_type == "show":
                end_position = QPoint(widget.x(), widget.y() + 50)
            
            animation = QPropertyAnimation(widget, b"pos") # Animating widgets position.
            animation.setStartValue(start_position)
            animation.setEndValue(end_position)
            animation.setDuration(100) # 0.1 second.
            animation.setEasingCurve(QEasingCurve.Type.OutQuad)
            
            return animation
        
        # Set the anim type and the icon to match the type.
        if self._is_hidden is False:
            print("Hiding topbar")
            
            self.change_icon("resources/assets/icons/buttons/show_up.svg")
            self._is_hidden = True
            
            anim_type = "hide"
        
        else:
            print("Showing topbar")
            
            self.change_icon("resources/assets/icons/buttons/hide_up.svg")
            self._is_hidden = False
            
            anim_type = "show"
        
        animation_group = QParallelAnimationGroup(self) # Create a group of animations to execute simultaneously.
        
        for widget in self.get_hideable_widgets(): # Add each hide animation to the animation group.
            animation = get_animation(widget, anim_type)
            animation_group.addAnimation(animation)
            
        animation_group.start() # Start the group.
                
class ProfileButton(TopBarButton):
    def __init__(
            self,
            parent: QWidget,
            config: TopBarConfig.ProfileButton,
            main_window: QWidget
    ):
        super().__init__(parent, config)
        self.main_window = main_window
        self._is_showing = False

        self.clicked.connect(self._on_click)
    
    def _on_click(self):
        print("Clicking profile...")
        if self._is_showing is True:
            self.drop_menu.deleteLater()
            self._is_showing = False
            
            return
        
        self.drop_menu = self.DropDownMenu(
            self.main_window,
            self.main_window,
            self.config.drop_menu
        )
        
        self._is_showing = True
    
    class DropDownMenu(QWidget):
        def __init__(
                self,
                parent: QWidget,
                main_window: QWidget,
                config: TopBarConfig.ProfileButton.DropMenu
        ):
            super().__init__(parent)
            self.main_window = main_window
            self.config = config
            
            self._set_design()
            self._set_widgets()
            
            self.shadow_size_offset = 10
            self.setFixedHeight(self.sizeHint().height() + self.shadow_size_offset)
            self.setFixedWidth(self.sizeHint().width() + self.shadow_size_offset)
            
            self.setGraphicsEffect(self.get_dropshadow())
            self.show()
        
        def _set_design(self):
            # Create a layout for the drop menu.
            self.main_layout = QVBoxLayout()
            self.main_layout.setSpacing(3)
            self.main_layout.setContentsMargins(0, 5, 0, 5)
            self.setLayout(self.main_layout)
            
            # Move the menu relative to the cursor clicked position.
            global_position = QCursor.pos() # QPoint position of the cursor.
            relative_position = self.main_window.mapFromGlobal(global_position) # Cursor QPoint relative to main window.
            
            self.move(
                relative_position.x() - self.width(),
                relative_position.y()
            ) # Move to cursor position.
        
        def _set_widgets(self):
            self.background = self.Background(self, self.config)
            self.username = self.Username(self, self.config)
            self.settings = self.SettingsButton(self, self.config)
            self.logout = self.LogoutButton(
                self,
                self.main_window,
                self.config
            )
            
            self.main_layout.addWidget(
                self.username,
                alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
            )
            self.main_layout.addWidget(self.settings)
            self.main_layout.addWidget(self.logout)
            
        def get_dropshadow(self) -> QGraphicsDropShadowEffect:
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(10)
            shadow.setOffset(0, 0)
            shadow.setColor(QColor(0, 0, 0, 160))
            
            return shadow
        
        def resizeEvent(self, event):
            self.background.setFixedHeight(self.height() - self.shadow_size_offset)
            self.background.setFixedWidth(self.width() - self.shadow_size_offset)
            
            return super().resizeEvent(event)
        
        class Background(QLabel):
            def __init__(
                    self,
                    parent: QWidget,
                    config: TopBarConfig.ProfileButton.DropMenu
            ):
                super().__init__(parent)
                self.shadow_size_offset = 10
                
                self.setFixedHeight(self.parentWidget().height() - self.shadow_size_offset)
                self.setFixedWidth(self.parentWidget().width() - self.shadow_size_offset)
                
                border_radius = 10
                self.setStyleSheet(
                    f"background-color: {config.background_colour};"
                    f"border-top-left-radius: {border_radius}px;"
                    f"border-bottom-left-radius: {border_radius}px;"
                    f"border-bottom-right-radius: {border_radius}px;"
                )
        
        class Username(QLabel):
            def __init__(
                    self,
                    parent: QWidget,
                    config: TopBarConfig.ProfileButton.DropMenu
            ):
                super().__init__(parent)
                self.setText("Karl")
                self.setStyleSheet(
                    "background-color: transparent;"
                    f"color: {config.text_colour};"
                )
                
                self.setFixedHeight(self.sizeHint().height())
                self.setFixedWidth(100)
                
                font = get_font(weight = "bold")
                font.setPointSize(12)
                
                self.setFont(font)

        class Button(QPushButton):
            def __init__(
                    self,
                    parent: QWidget,
                    config: TopBarConfig.ProfileButton.DropMenu
            ):
                super().__init__(parent)
                self.setFixedHeight(25)
                self.setFixedWidth(100)
                
                font = get_font()
                font.setPointSize(10)
                self.setFont(font)
                
                self.setStyleSheet(
                    f"background-color: {config.label_colour};"
                    f"color: {config.text_colour};"
                    "padding: 0px;"
                )
        
        class SettingsButton(Button):
            def __init__(
                    self,
                    parent: QWidget,
                    config: TopBarConfig.ProfileButton.DropMenu
            ):
                super().__init__(parent, config)
                self.setText("Settings")
        
        class LogoutButton(Button):
            def __init__(
                    self,
                    parent: QWidget,
                    main_window: QWidget,
                    config: TopBarConfig.ProfileButton.DropMenu
            ):
                super().__init__(parent, config)
                self.setText("Logout")
                
                self.main_window = main_window
                
                self.clicked.connect(self._on_click)
            
            def _on_click(self):
                """A function to hide the top_bar and recreate the login screen."""
                top_bar : QWidget = self.main_window.top_bar
                top_bar.hide()
                
                self.main_window.login = Login(
                    parent = self.main_window,
                    main_window = self.main_window
                )
                self.main_window.login.show()
                
                profile_button = top_bar.buttons.profile_button
                profile_button._is_showing = False
                
                # Delete the dropdown menu.
                profile_button.drop_menu.deleteLater()