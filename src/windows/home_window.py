from src.shared.imports import *

from src.widgets.dm_list import DMListWidget
from src.widgets.chat_widget import ChatWidget

@Decorators.autolog
@Decorators.property
@Decorators.api
class HomeWindow(QWidget):
    api : ApiClient
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
        self._set_layout()
        self._startup()
        
        # Initialise socket connection.
        self.message_listener = MessageListener()
        self.message_listener.on_error_signal.connect(self._on_poll_error)
        self.message_listener.on_message_signal.connect(self._on_message_given)
        self.message_listener.start()
        
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
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        
        self.setLayout(self.main_layout)
    
    def _startup(self):
        """Starts the loading process, displaying a loading screen."""
        def _get_all_chats_reply(data):
            """Adds all the chats to the SQLManager once a successful call."""
            if "error" in data:
                self.log.info(f"[{data['code']}] - {data['error']}")
                
                self.on_loading_complete()
                
                return
            
            sql_manager : SQLManager = get_property("SQLManager")
            for chat in data:
                # Check if the chat is already in there.
                if not sql_manager.get_chat(chat["id"]):
                    sql_manager.add_chat(
                        chat["id"],
                        chat["sender_id"],
                        chat["recipient_id"],
                        str(chat["created_at"])
                    )
        
            _get_chat_profile()
        
        def _get_chat_profile():
            """Loads all user profiles found in chats to SQLManager."""
            def _on_profile_reply(data):
                """Adds the user's profile to the SQLManager."""
                data = json.loads(data)
                
                sql_manager : SQLManager = get_property("SQLManager")
                
                if not sql_manager.get_profile(user_id = UUID(data.get("user_id"))):
                    sql_manager.add_profile(
                        user_id = UUID(data.get("user_id")),
                        username = data.get("username"),
                        profile = bytes.fromhex(data.get("profile_picture"))
                    )
                
                self._profiles_to_load -= 1
                if self._profiles_to_load <= 0:
                    self.on_loading_complete()
            
            sql_manager : SQLManager = get_property("SQLManager")
            all_chats = sql_manager.get_all_chats()
            
            for chat in all_chats:
                chat_id = chat["chat_id"]
                sender_id = chat["sender_id"]
                recipient_id = chat["recipient_id"]
                created_at = chat["created_at"]
                
                # Only get other user's profile.
                if sender_id == get_property("ID"):
                    # Get recipient.
                    self.api.post(API_FILE_PROFILE, {"user_id": recipient_id}, _on_profile_reply, True)
                
                else:
                    # Get sender.
                    self.api.post(API_FILE_PROFILE, {"user_id": sender_id}, _on_profile_reply, True)
                
                self._profiles_to_load += 1
        
        self.loading_overlay = LoadingOverlay(self.parentWidget())
        self.loading_overlay.show()

        self._profiles_to_load = 0 # Keep track of loading profiles.
        
        # Begin the startup process.
        from src.widgets.chat_widget import Chat
        self.chat : Chat = Chat(self)
        
        self.chat.get_all(_get_all_chats_reply)

    def _on_poll_error(self, data: dict):
        print(data)
    
    def _on_message_given(self, data: dict):
        # Add the message to the chat.
        chat_widget : ChatWidget = get_property("ChatWidget")
        scroll_layout : QVBoxLayout = chat_widget.scroll_layout
        
        from src.widgets.chat_widget import MessageWidget
        scroll_layout.addWidget(MessageWidget(
            chat_widget,
            {
                "message_id": UUID(data.get("message_id")),
                "chat_id": UUID(data.get("chat_id")),
                "sender_id": UUID(data.get("sender_id")),
                "recipient_id": UUID(data.get("recipient_id")),
                "encrypted_message": bytes.fromhex(data.get("encrypted_message")),
                "iv": bytes.fromhex(data.get("iv")),
                "encrypted_shared_secret_for_sender": bytes.fromhex(data.get("encrypted_shared_secret_for_sender")),
                "encrypted_shared_secret_for_recipient": bytes.fromhex(data.get("encrypted_shared_secret_for_recipient")),
                "sent_at": datetime.fromtimestamp(float(data.get("sent_at")))
            }
        ))
    
    def on_loading_complete(self):
        """Called once loading is complete."""
        # Add relevant widgets.
        self.dm_list_widget = DMListWidget(self)
        self.chat_widget = ChatWidget(self)
        
        # Add the widgets to the layout.
        self.main_layout.addWidget(self.dm_list_widget)
        self.main_layout.addWidget(self.chat_widget)
        
        self.loading_overlay.set_complete()
    
    def resizeEvent(self, event: QResizeEvent):
        try:
            self.loading_overlay.setFixedSize(
                self.parentWidget().width() - 20,
                self.parentWidget().height() - 20
            )
            self.loading_overlay.move(10, 10)
            
        except:
            pass
        
        return super().resizeEvent(event)

class LoadingOverlay(QLabel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
    
    def _set_style(self):
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        self.loading_movie = QMovie(path("/assets/gifs/loading.gif"))
        self.loading_movie.setScaledSize(QSize(100, 100))

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(
            "background-color: #171717;"
            "border-radius: 15px;"
        )

        self.setMovie(self.loading_movie)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_movie.start()
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.repaint()
    
    def hide_animation(self):
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        self.animation.finished.connect(self.deleteLater)
        
        self.animation.start()

    def set_complete(self):
        self.hide_animation()