from src.shared.imports import *

@Decorators.autolog
@Decorators.api
@Decorators.property
class DMListWidget(QWidget):
    api : ApiClient
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.shown_dms : dict[UUID, DM] = {}
        
        self._set_style()
        self._set_layout()
        self._set_widgets()
        
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
    
    def _set_widgets(self):
        self.add_dm_button = AddDMButton(self)
        
        self.main_layout.insertWidget(self.main_layout.count() - 1, self.add_dm_button)
    
    def _get_chats_reply(self, data):
        data = json.loads(data)
        
        if "error" in data:
            self.log.info(f"[{data['code']}] - {data['error']}")
            
            return
        
        # Add all the chats to the DM list.
        for chat_data in data:
            self._add_dm(chat_data)
    
    def _add_dm(self, chat_data: dict):
        self.main_layout.insertWidget(self.main_layout.count() - 1, DM(self, chat_data))

@Decorators.autolog
@Decorators.property
class AddDMButton(QPushButton):
    log : logging.Logger
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._set_style()
        
        self.clicked.connect(self._on_click)
    
    def _set_style(self):
        list_layout = self.parentWidget().layout()
        list_layout_left_margin = list_layout.contentsMargins().left()
        
        self.setFixedHeight(self.parentWidget().width() - (list_layout_left_margin * 2))
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("background-color: #1c1c1c; border-radius: 15px")
        
        self.setIcon(QPixmap(path("/assets/icons/dm.png")))
        self.setIconSize(QSize(self.height() - 10, self.width() - 10))
    
    def _on_click(self):
        self.log.info("Clicked.")
        
        self.add_dm_input = AddDMInput(get_property("MainWindow"))
        self.add_dm_input.show()

@Decorators.autolog
@Decorators.api
@Decorators.property
class AddDMInput(QWidget):
    log : logging.Logger
    api : ApiClient
    
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self._set_style()
        self._set_widgets()
        self._set_layout()
        
        # Bring DM list back to front.
        dm_list : QWidget = get_property("DMListWidget")
        dm_list.raise_()
    
    def _set_style(self):
        self.setFixedSize(300, 40)
        
        main_window : QWidget = get_property("MainWindow")
        dm_button : QWidget = get_property("AddDMButton")
        
        dm_button_position = dm_button.mapTo(main_window, dm_button.rect().topLeft())
        
        self.move(dm_button_position)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet(
            "background-color: #1c1c1c;"
            "border-radius: 15px"
        )
    
    def _set_widgets(self):
        self.line_edit = self.LineEdit(self)
        self.submit_button = self.SubmitButton(self)
        self.exit_button = self.ExitButton(self)
        
    def _set_layout(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        
        self.main_layout.addWidget(self.exit_button)
        self.main_layout.addWidget(self.line_edit)
        self.main_layout.addWidget(self.submit_button)
        
        self.setLayout(self.main_layout)

    class LineEdit(QLineEdit):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self.error_showing = False
        
            self._set_style()
        
        def _set_style(self):
            self.setStyleSheet(
                "background-color: #1f1f1f;"
                "font-size: 15pt;"
            )
        
        def set_error(self, error_message: str):
            if self.error_showing is True:
                for action in self.actions():
                    self.removeAction(action)
                
                self.setStyleSheet(
                    "background-color: #1f1f1f;"
                    "font-size: 15pt;"
                )
                
                self.error_showing = False
                
                return
            
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

    @Decorators.autolog
    class SubmitButton(QPushButton):
        log : logging.Logger
        
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self._set_style()
            
            self.clicked.connect(self._on_click)
        
        def _set_style(self):
            parent_height = self.parentWidget().height()
            
            self.setFixedSize(parent_height, parent_height)
            
            self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
            self.setStyleSheet(
                "background-color: #161616;"
                "border-radius: 15px"
            )
            
            self.setIcon(QPixmap(path("/assets/icons/send.png")))
            self.setIconSize(QSize(self.height() - 10, self.width() - 10))
        
        def _on_click(self):
            def _on_error(data):
                line_edit : QLineEdit = self.parentWidget().line_edit
                line_edit.set_error(f"[{data['code']}] - {data['error']}")
            
            def _on_finish(data):
                chat_id = data.get("chat_id")
                
                # Check if that chat is already displayed.
                dm_list : QWidget = get_property("DMListWidget")
                shown_dms = dm_list.shown_dms
                
                this_dm = shown_dms.get(UUID(chat_id))
                
                if this_dm:
                    self.log.info(f"{chat_id} Already displayed, not adding again.")
                    
                    line_edit : QLineEdit = self.parentWidget().line_edit
                    line_edit.set_error(f"DM already showing!")

                    return
                
                # Get the chat data and add it to the DM list.
                sql_manager : SQLManager = get_property("SQLManager")
                chat_data = sql_manager.get_chat(chat_id)
                
                dm_list : DMListWidget = get_property("DMListWidget")
                dm_list._add_dm({
                    "id": chat_data["chat_id"],
                    "sender_id": chat_data["sender_id"],
                    "recipient_id": chat_data["recipient_id"],
                    "created_at": chat_data["created_at"]
                })
                
                # Get the parent and delete it.
                parent = self.parentWidget()
                parent.deleteLater()
            
            line_edit : QLineEdit = self.parentWidget().line_edit
            line_edit.reset()
            recipient_username = line_edit.text()
            
            if not recipient_username:
                line_edit.set_error(f"No username submitted.")
                
                return
            
            from src.widgets.chat_widget import CreateChatObject
            self.create_chat_object = CreateChatObject(self, "👋", recipient_username)
            self.create_chat_object.error_signal.connect(_on_error)
            self.create_chat_object.finished.connect(_on_finish)
            self.create_chat_object.create_chat()
    
    class ExitButton(QPushButton):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self._set_style()
            
            self.clicked.connect(self._on_click)
        
        def _set_style(self):
            parent_height = self.parentWidget().height()
            
            self.setFixedSize(parent_height, parent_height)
            
            self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
            self.setStyleSheet(
                "background-color: #161616;"
                "border-radius: 15px"
            )
            
            self.setIcon(QPixmap(path("/assets/icons/cancel.png")))
            self.setIconSize(QSize(self.height() - 10, self.width() - 10))
        
        def _on_click(self):
            # Get the parent and delete it.
            parent = self.parentWidget()
            parent.deleteLater()
            
@Decorators.api
class DM(QLabel):
    api : ApiClient
    
    def __init__(self, parent: QWidget, chat_data: dict):
        super().__init__(parent)
        if not isinstance(chat_data["id"], UUID):
            self.id = UUID(chat_data["id"])
        
        else:
            self.id = chat_data["id"]
        
        if not isinstance(chat_data["recipient_id"], UUID):
            self.recipient_id = UUID(chat_data["recipient_id"])
        
        else:
            self.recipient_id = chat_data["recipient_id"]
        
        if not isinstance(chat_data["sender_id"], UUID):
            self.sender_id = UUID(chat_data["sender_id"])
        
        else:
            self.sender_id = chat_data["sender_id"]
        
        if not isinstance(chat_data["created_at"], datetime):
            self.created_at = datetime.fromtimestamp(chat_data["created_at"])
        
        else:
            self.created_at = chat_data["created_at"]
        
        self._set_style()
        self.get_pixmap()
        
        # Add DM to the DM dictionary.
        dm_list : DMListWidget = get_property("DMListWidget")
        dm_list.shown_dms[self.id] = self
        
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