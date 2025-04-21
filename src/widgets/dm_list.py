from src.shared.imports import *

@Decorators.autolog
@Decorators.api
@Decorators.property
class DMListWidget(QWidget):
    api : ApiClient
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
        self._set_layout()
        
        self.api.get(API_GET_CHATS, self._get_chats_reply, auth = True)
    
    def _set_style(self):
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(50)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(
            "background-color: #171717;"
            "border-radius: 15px"
        )
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
    
    def _set_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(5, 10, 5, 10)
        self.main_layout.setSpacing(10)
        
        self.main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        
        self.setLayout(self.main_layout)
    
    def _get_chats_reply(self, data):
        data = json.loads(data)
        
        # Add all the chats to the DM list.
        for chat_data in data:
            self._add_dm(chat_data)
    
    def _add_dm(self, chat_data: dict):
        self.main_layout.insertWidget(self.main_layout.count() - 1, DM(self, chat_data))

@Decorators.api
class DM(QLabel):
    api : ApiClient
    
    def __init__(self, parent: QWidget, chat_data: dict):
        super().__init__(parent)
        self.id = UUID(chat_data["id"])
        self.recipient_id = UUID(chat_data["recipient_id"])
        self.sender_id = UUID(chat_data["sender_id"])
        self.created_at = datetime.fromtimestamp(chat_data["created_at"])
        
        self._set_style()
        self.get_pixmap()
        
    def _set_style(self):
        list_layout = self.parentWidget().layout()
        list_layout_left_margin = list_layout.contentsMargins().left()
        
        self.setFixedHeight(self.parentWidget().width() - (list_layout_left_margin * 2))
    
    def _set_pixmap(self, pixmap: QPixmap):
        self.setPixmap(pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
    
    def get_pixmap(self):
        def _get_user_reply(data):
            data = json.loads(data)
            
            pixmap = QPixmap()
            pixmap.loadFromData(bytes.fromhex(data["profile_picture"]))
            
            self._set_pixmap(pixmap)
        
        current_user_id = UUID(get_property("ID"))
        
        if current_user_id == self.sender_id:
            self.api.post(API_FILE_PROFILE, {"user_id": self.recipient_id.hex}, _get_user_reply, auth = True)
        
        else:
            self.api.post(API_FILE_PROFILE, {"user_id": self.sender_id.hex}, _get_user_reply, auth = True)
    
    def mousePressEvent(self, ev: QMouseEvent):
        if ev.button() == Qt.MouseButton.LeftButton:
            # Open the chat that the DM is a part of.
            chat_widget = get_property("ChatWidget")
            chat_widget.open_chat(self.id)
        
        return super().mousePressEvent(ev)