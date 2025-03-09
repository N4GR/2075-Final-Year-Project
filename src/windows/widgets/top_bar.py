from src.imports import *

class TopBar(QWidget):
    def __init__(self, parent: QWidget, main_window: QWidget):
        super().__init__(parent)
        
        # Assigning args to self.
        self.main_window = main_window
        self.config = TopBarConfig()

        self._set_design() # Adding design elements to widget.
        self._set_widgets()
    
    def _set_design(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(50)
        
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.setLayout(self.main_layout)
    
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
        
        self.main_layout.addWidget(self.buttons)
    
    def resizeEvent(self, event: QResizeEvent):
        self.background.update_width(self.width())
        
        return super().resizeEvent(event)
    
    class Background(QLabel):
        def __init__(
                self,
                parent: QWidget,
                config: TopBarConfig
        ):
            super().__init__(parent)
            
            self.setStyleSheet(f"background-color: {config.background_colour}")
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
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
            self.hide_button = self.HideButton(self, self.config.hide_button)
            self.left_layout.addWidget(self.hide_button)
            
            self.profile_button = self.ProfileButton(self, self.config.profile_button)
            self.right_layout.addWidget(self.profile_button)

        class TopBarButton(QPushButton):
            def __init__(self, parent: QWidget, config: TopBarConfig.Button):
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
        
        class HideButton(TopBarButton):
            def __init__(self, parent: QWidget, config: TopBarConfig.Button):
                super().__init__(parent, config)
            
            def _on_click(self):
                pass
        
        class ProfileButton(TopBarButton):
            def __init__(self, parent: QWidget, config: TopBarConfig.Button):
                super().__init__(parent, config)
            
            def _on_click(self):
                pass