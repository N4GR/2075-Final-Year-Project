from src.shared.imports import *

@Decorators.autolog
class MessageListener(QThread):
    log : logging.Logger
    
    on_message_signal = Signal(dict)
    on_error_signal = Signal(dict)
    
    def __init__(self):
        """A Qobject intended to be used as a QThread to listen for incoming messages."""
        super().__init__()

    def run(self):
        self.username = get_property("Username")
        self.access_token = get_property("AccessToken")
        
        self.sio = socketio.Client(True, 10, 1)

        self.sio.on("connect", self._on_connect)
        self.sio.on("disconnect", self._on_disconnect)
        self.sio.on("get_message", self._on_message_reply)
        
        self.sio.connect(
            API_URL + f"?username={self.username}",
            headers = {"Authorization": f"Bearer {self.access_token}"}
        )
    
    def _on_connect(self):
        self.log.info(f"Socket connected: {API_URL}?={self.username}")
        
    def _on_disconnect(self):
        self.log.info(f"Socket disconnected: {API_URL}?={self.username}")
    
    def send_message(self, data: dict):
        self.sio.emit("send_message", data)
    
    def _on_message_reply(self, data: dict):
        """Socket message when a user sends a message."""
        self.on_message_signal.emit(data)
        
