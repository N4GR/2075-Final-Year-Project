from src.shared.imports import *

@Decorators.property
class TopBarWidget(QWidget):
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.current_style : QWidget = None
        
        self._set_style()
        self._set_layout()
        
        self.set_logged_out()
    
    def _set_style(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(50)
        
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
    
    def set_logged_in(self):
        """Sets the topbar as the logged_in style."""
        if self.current_style:
            self.current_style.deleteLater()
        
        self.current_style = LoggedIn(self)
        self.add_to_layout(self.current_style)
    
    def set_logged_out(self):
        """Sets the topbar as the logged_out style."""
        if self.current_style:
            self.current_style.deleteLater()
            
        self.current_style = LoggedOut(self)
        self.add_to_layout(self.current_style)
    
    def _set_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(self.main_layout)
    
    def add_to_layout(self, widget: QWidget):
        self.main_layout.addWidget(widget)

@Decorators.api
class LoggedIn(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
        self._set_widgets()
        self._set_layout()

    def _set_style(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _set_widgets(self):
        self.current_user_image = CurrentUserImage(self)
    
    def _set_layout(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 0, 10)
        
        self.main_layout.addWidget(self.current_user_image, alignment = Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(self.main_layout)

class CurrentUserImage(QLabel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
        self._set_image()

    def _set_style(self):
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        topbar_widget : TopBarWidget = get_property("TopBarWidget")
        self.setFixedSize(topbar_widget.height(), topbar_widget.height())
        
        self.setStyleSheet(f"border-radius: {topbar_widget.height() / 2}px")
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
    
    def _set_image(self):
        pixmap = QPixmap()
        pixmap.loadFromData(get_property("ProfilePicture"))
        
        self.setPixmap(pixmap.scaled(
            QSize(
                self.width() - 10,
                self.height() - 10
            ),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
    
@Decorators.api
@Decorators.autolog
class UserImage(QLabel):
    def __init__(self, parent: QWidget, id: str):
        super().__init__(parent)
        self.id = id
        self._set_style()
        
        self.api.get_user(self.id, self._user_reply)
        
    def _set_style(self):
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        topbar_widget : TopBarWidget = get_property("TopBarWidget")
        self.setFixedSize(topbar_widget.height(), topbar_widget.height())
        
        self.setStyleSheet(f"border-radius: {topbar_widget.height() / 2}px")
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
    
    def _user_reply(self, data):
        data = json.loads(data)
        id : str = data.get("id")
        username : str = data.get("username")
        profile_picture : bytes = data.get("profile_picture")
        
        for key, value in {"id": id, "username": username, "profile_picture": profile_picture}.items():
            if not value:
                self.log.info(f"Didn't receive {key} for user: [{self.id}]")
                
                return

        profile_pixmap = QPixmap()
        profile_pixmap.loadFromData(bytes.fromhex(profile_picture))
        
        self.set_pixmap(profile_pixmap)
        
        # Create a user object from the returned values.
        set_property(id, User(id, username, profile_picture))

    def set_pixmap(self, pixmap: QPixmap):
        self.setPixmap(pixmap.scaled(
            QSize(
                self.width() - 10,
                self.height() - 10
            ),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))

class LoggedOut(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self._set_widgets()
        self._set_layout()
        
    def _set_widgets(self):
        self.title_label = self.TitleLabel(self)
    
    def _set_layout(self):
        self.main_layout = QHBoxLayout()
        
        self.main_layout.addWidget(self.title_label)
        
        self.setLayout(self.main_layout)
    
    class TitleLabel(QLabel):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self.setText("METAPHRAST")
            self.setStyleSheet("font-weight: bold; font-size: 20pt;")