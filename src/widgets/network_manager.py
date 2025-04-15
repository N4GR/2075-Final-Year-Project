from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtCore import Signal, QUrl, QByteArray, QObject

from logging import Logger
import json

from src.shared.decorators import Decorators

@Decorators.autolog
class ApiClient(QObject):
    request_finished = Signal(object)
    log : Logger
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ApiClient, cls).__new__(cls)
        
        return cls._instance
    
    def __init__(self, parent = None):
        if hasattr(self, "_instantialised") and self._instantialised:
            return
        
        super().__init__(parent)
        
        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self._handle_response)

        self._callback = None
        self._instantialised = True
    
    def _handle_response(self, reply: QNetworkReply):
        http_status = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        error = reply.error()
        error_string = reply.errorString()
        
        self.log.debug(f"HTTP Status: {http_status}, Qt Error: {error}, Message: {error_string}")
        
        data = reply.readAll().data().decode()
        self.log.debug(f"Raw response: {data}")
        
        try:
            json_data = json.loads(data)
        
        except json.JSONDecodeError as e:
            json_data = {"error": "Invalid JSON", "details": str(e), "raw": data}
            
            return
        
        if http_status == 200:
            self.request_finished.emit(json_data)
        
        if self._callback:
            self._callback(json_data)
        
        reply.deleteLater()
    
    def post(self, endpoint: str, payload: dict, callback = None):
        self._callback = callback
        
        url = QUrl(endpoint)
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        
        data = QByteArray(json.dumps(payload).encode("utf-8"))
        self.network_manager.post(request, data)