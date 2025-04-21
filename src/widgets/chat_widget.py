from src.shared.imports import *
from src.shared.keys import *

from uuid import UUID

@Decorators.autolog
@Decorators.api
@Decorators.property
class CreateChatObject(QObject):
    log : logging.Logger
    api : ApiClient
    
    error_signal = Signal(dict)
    
    def __init__(self, parent: QWidget, message: str, recipient_username: str):
        super().__init__(parent)
        self.message = message
        self.recipient_username = recipient_username
    
    def create_chat(self):
        self.api.post(
            API_GET_PUBLIC_KEY,
            {"username": self.recipient_username},
            self._recipient_key_reply,
            auth = True
        )
    
    def _recipient_key_reply(self, data):
        data = json.loads(data)
        recipient_public_key = bytes.fromhex(data.get("public_key"))
        self.recipient_id = data.get("id")
        sender_id = get_property("ID")

        shared_secret = os.urandom(32)

        self.sender_shared_secret = generate_shared_secret(shared_secret, get_property("PublicKey"))
        self.recipient_shared_secret = generate_shared_secret(shared_secret, recipient_public_key)
        
        self.iv, self.encrypted_message = encrypt_message(self.message, shared_secret)
        
        # Send all to database
        self.api.post(
            url = API_SEND_MESSAGE,
            payload = {
                "sender_id": sender_id,
                "recipient_id": self.recipient_id,
                "encrypted_message": self.encrypted_message.hex(),
                "iv": self.iv.hex(),
                "encrypted_secret_sender_hex": self.sender_shared_secret.hex(),
                "encrypted_secret_recipient_hex": self.recipient_shared_secret.hex()
            },
            connection = self._message_sent_reply,
            auth = True
        )
    
    def _message_sent_reply(self, data):
        data = json.loads(data)
        message_id = data.get("message_id")
        self.chat_id = data.get("chat_id")
        sender_id = get_property("ID")
        
        # Add the chat to chats SQL table.
        sql_manager : SQLManager = get_property("SQLManager")
        existing_chat = sql_manager.get_chat(self.chat_id)
        
        if not existing_chat:
            sql_manager.add_chat(self.chat_id, sender_id, self.recipient_id)

@Decorators.autolog
@Decorators.api
@Decorators.property
class GetMessagesObject(QObject):
    log : logging.Logger
    api : ApiClient
    
    error_signal = Signal(dict)
    messages_signal = Signal(list)
    
    def __init__(self, parent: QWidget, chat_id: str):
        super().__init__(parent)
        self.chat_id = chat_id
        
    def get_messages(self):
        self.api.post(
            API_GET_MESSAGES,
            {"chat_id": self.chat_id},
            self._get_messages_reply,
            auth = True
        )
    
    def _get_messages_reply(self, data):
        data = json.loads(data)
        
        # Add the messages to messages SQL table.
        sql_manager : SQLManager = get_property("SQLManager")
        
        for message in data:
            existing_message = sql_manager.get_message(message["message_id"])
            
            if not existing_message:
                sql_manager.add_message(
                    message_id = message["message_id"],
                    chat_id = message["chat_id"],
                    sender_id = message["sender_id"],
                    encrypted_message = bytes.fromhex(message["encrypted_message"]),
                    iv = bytes.fromhex(message["iv"]),
                    encrypted_shared_secret_for_sender = bytes.fromhex(message["encrypted_shared_secret_for_sender"]),
                    encrypted_shared_secret_for_recipient = bytes.fromhex(message["encrypted_shared_secret_for_recipient"]),
                    sent_at = message["sent_at"]
                )
        
        messages_from_db = sql_manager.get_messages(self.chat_id)
        self.messages_signal.emit(messages_from_db)

@Decorators.api
@Decorators.autolog
class Message(QObject):
    api: ApiClient
    log: logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
    
    def send(self, chat_id: UUID, message: str):
        """Sends a message to a user by their ID.
        
        Args:
            recipient_id (UUID): ID of the user to send the message to.
            message (str): Message to send to the user.
        """
        def _public_key_reply(data):
            data = json.loads(data)
        
            _encrypt_and_send(bytes.fromhex(data.get("public_key")))
        
        def _encrypt_and_send(recipient_public_key: bytes):
            # Generate a shared secret for the sender and recipient.
            shared_secret = os.urandom(32)
            sender_shared_secret = generate_shared_secret(shared_secret, get_property("PublicKey"))
            recipient_shared_secret = generate_shared_secret(shared_secret, recipient_public_key)
            
            # Encrypt the message being sent.
            iv, encrypted_message = encrypt_message(message, shared_secret)
            
            # Send the data to the API.
            self.api.post(
                url = API_SEND_MESSAGE,
                payload = {
                    "sender_id": get_property("ID"),
                    "recipient_id": recipient_id.hex,
                    "encrypted_message": encrypted_message.hex(),
                    "iv": iv.hex(),
                    "encrypted_secret_sender_hex": sender_shared_secret.hex(),
                    "encrypted_secret_recipient_hex": recipient_shared_secret.hex()
                },
                connection = _message_sent_reply,
                auth = True
            )
        
        def _message_sent_reply(data):
            data = json.loads(data)
            
            # Add the message to the chat.
            chat_widget : ChatWidget = get_property("ChatWidget")
            scroll_layout : QVBoxLayout = chat_widget.scroll_layout
            
            scroll_layout.addWidget(MessageWidget(
                chat_widget,
                {
                    "message_id": UUID(data.get("message_id")),
                    "chat_id": UUID(data.get("chat_id")),
                    "sender_id": UUID(data.get("sender_id")),
                    "recipient_id": UUID(data.get("recipient_id")),
                    "encrypted_message": bytes.fromhex(data.get("encrypted_message")),
                    "iv": bytes.fromhex(data.get("iv")),
                    "encrypted_shared_secret_for_sender": bytes.fromhex(data.get("encrypted_secret_for_sender")),
                    "encrypted_shared_secret_for_recipient": bytes.fromhex(data.get("encrypted_secret_for_recipient")),
                    "sent_at": datetime.fromtimestamp(float(data.get("sent_at")))
                }
            ))
        
        # Obtain the chat data.
        sql_manager : SQLManager = get_property("SQLManager")
        chat_data = sql_manager.get_chat(chat_id.hex)
        
        if chat_data["sender_id"] == UUID(get_property("ID")):
            recipient_id = chat_data["recipient_id"]
        
        else:
            recipient_id = chat_data["sender_id"]
        
        self.api.post(API_GET_PUBLIC_KEY, {"id": recipient_id.hex}, _public_key_reply, auth = True)

class MessageListener(QObject):
    on_message_signal = Signal(dict)
    
    def __init__(self, parent: QWidget):
        """A Qobject intended to be used as a QThread to listen for incoming messages."""
        super().__init__(parent)

    

@Decorators.autolog
@Decorators.api
@Decorators.property
class ChatWidget(QWidget):
    api : ApiClient
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
        self._set_layout()
        
        self._opened_chat = []
    
    def _set_style(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
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
        #self.main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        
        self.scroll_area.setWidget(scroll_content)
        
        self.main_layout.addWidget(self.scroll_area)
        
        self.setLayout(self.main_layout)
    
    def create_chat(self, recipient_username: str, message: str):
        self.create_chat_object = CreateChatObject(self, message, recipient_username)
        self.create_chat_object.create_chat()
    
    def get_messages(self, chat_id: str):
        self.get_messages_object = GetMessagesObject(self, chat_id)
        self.get_messages_object.messages_signal.connect(self._get_messages_reply)
        self.get_messages_object.get_messages()
    
    def _get_messages_reply(self, reply: dict):
        print(reply)
    
    def open_chat(self, chat_id: UUID):
        def get_chat_messages():
            def _messages_reply(data: list):
                for message in data:
                    self.scroll_layout.addWidget(MessageWidget(self, message))

            self.get_messages_object = GetMessagesObject(self, self.chat_id.hex)
            self.get_messages_object.messages_signal.connect(_messages_reply)
            self.get_messages_object.get_messages()
        
        self.message_box = MessageBox(self)
        self.main_layout.addWidget(self.message_box)
        
        self.chat_id = chat_id
        get_chat_messages()
        
        self.log.info(f"Opening chat: {chat_id.hex}")

@Decorators.api
@Decorators.property
class MessageWidget(QWidget):
    api : ApiClient
    
    def __init__(self, parent: QWidget, message_data: dict):
        super().__init__(parent)
        self.message_id = message_data["message_id"]
        self.chat_id = message_data["chat_id"]
        self.sender_id = message_data["sender_id"]
        self.encrypted_message = message_data["encrypted_message"]
        self.iv = message_data["iv"]
        self.encrypted_shared_secret_for_sender = message_data["encrypted_shared_secret_for_sender"]
        self.encrypted_shared_secret_for_recipient = message_data["encrypted_shared_secret_for_recipient"]
        self.sent_at = message_data["sent_at"]
        
        if UUID(get_property("ID")) == self.sender_id:
            self.decryped_secret = decrypt_shared_secret(
                self.encrypted_shared_secret_for_sender,
                get_property("PrivateKey")
            )
            
            self.decrypted_message = decrypt_message(
                self.iv,
                self.encrypted_message,
                self.decryped_secret
            )
        
        else:
            self.decryped_secret = decrypt_shared_secret(
                self.encrypted_shared_secret_for_recipient,
                get_property("PrivateKey")
            )
            
            self.decrypted_message = decrypt_message(
                self.iv,
                self.encrypted_message,
                self.decryped_secret
            )
        
        self._set_style()
        self._set_layout()
        self._set_user_label()
        self._set_text()
        
        # Scroll to bottom after the UI has updated
        chat_widget : ChatWidget = get_property("ChatWidget")
        scroll_area = chat_widget.scroll_area
        
        QTimer.singleShot(1000, lambda: scroll_area.verticalScrollBar().setValue(
            scroll_area.verticalScrollBar().maximum()
        ))
    
    def _set_style(self):
        self.setFixedHeight(40)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        
        self.effect = QGraphicsDropShadowEffect(self)
        self.effect.setBlurRadius(10)
        self.effect.setOffset(0, 5)
        self.effect.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(self.effect)
    
    def _set_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        
        self.setLayout(self.main_layout)
    
    def _set_user_label(self):
        def _get_profile_reply(data):
            if type(data) != dict:
                data = json.loads(data)
            
            if type(data["profile_picture"]) != bytes:
                profile_picture = bytes.fromhex(data["profile_picture"])
            
            else:
                profile_picture = data["profile_picture"]
                
            username = data["username"]
            
            pixmap = QPixmap()
            pixmap.loadFromData(profile_picture)
            
            self.user_picture.setPixmap(pixmap.scaled(
                self.user_picture.size(),
                mode = Qt.TransformationMode.SmoothTransformation
            ))

            self.user_name.setText(username)
            
            # Add the user's profile to the database.
            sql_manager : SQLManager = get_property("SQLManager")
            profile = sql_manager.get_profile(user_id = self.sender_id)
            
            if not profile:
                sql_manager.add_profile(self.sender_id, username, profile_picture)
        
        self.user_layout = QHBoxLayout()
        self.user_layout.setSpacing(10)
        
        self.user_picture = QLabel(self)
        self.user_picture.setFixedSize(20, 20)
        
        self.user_name = QLabel(self)
        
        sql_manager : SQLManager = get_property("SQLManager")
        profile = sql_manager.get_profile(user_id = self.sender_id)
        
        if not profile:
            self.api.post(API_FILE_PROFILE, {"user_id": self.sender_id.hex}, _get_profile_reply, auth = True)
        else:
            _get_profile_reply(data = {
                "username": profile["username"],
                "profile_picture": profile["profile"]
            })

        self.timestamp = QLabel(self)
        self.timestamp.setText(self.sent_at.strftime("%d/%m/%Y, %H:%M:%S"))
        
        self.user_layout.addWidget(self.user_picture)
        self.user_layout.addWidget(self.user_name)
        self.user_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.user_layout.addWidget(self.timestamp)
        
        self.main_layout.addLayout(self.user_layout)
    
    def _set_text(self):
        self.text_label = QLabel(self)
        self.text_label.setText(self.decrypted_message)
        self.text_label.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.text_label)

class MessageBox(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
        self._set_layout()
        self._set_widgets()
    
    def _set_style(self):
        self.setFixedHeight(100)
    
    def _set_layout(self):
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
    
    def _set_widgets(self):
        self.message_area = self.MessageArea(self)
        self.send_message_button = self.SendMessageButton(self)
        
        self.main_layout.addWidget(self.message_area)
        self.main_layout.addWidget(self.send_message_button)
    
    class MessageArea(QTextEdit):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self._set_style()
            
        def _set_style(self):
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
    
    @Decorators.autolog
    class SendMessageButton(QPushButton):
        log : logging.Logger
        
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self._set_style()
            self.clicked.connect(self._on_click)
        
        def _set_style(self):
            self.setIcon(QPixmap(path("/assets/icons/upload.png")))
            
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
        
        def _on_click(self):
            message_area : QTextEdit = self.parentWidget().message_area
            message_widget : MessageWidget = get_property("MessageWidget")
            
            message_text = message_area.toPlainText()
            if not message_text:
                return
            
            self.message = Message(self)
            self.message.send(message_widget.chat_id, message_text)
            
            self.log.info(f"Sending message to chat [{message_widget.chat_id}]")