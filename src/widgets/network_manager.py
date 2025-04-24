from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest, QHttpMultiPart, QHttpPart
from PySide6.QtCore import QUrl, QObject, QJsonDocument, QTimer, QFile, QIODevice
from PySide6.QtWidgets import QMessageBox

from logging import Logger
from typing import Callable

from src.shared.decorators import Decorators
from src.shared.objects import *
from src.shared.funcs import *
from src.shared.globals import *

@Decorators.autolog
class ApiClient(QObject):
    log : Logger
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.timeout = 5000
        
        self.network_manager = QNetworkAccessManager(parent)
        self.network_manager.finished.connect(self._reply)

        self._connections : dict[QNetworkReply, Callable] = {}
        self._timers : dict[QNetworkReply, QTimer] = {}
    
    def _reply(self, reply: QNetworkReply):
        data = reply.readAll().data().decode()
        error = reply.error()
        reply_url = reply.url().toString()
        
        self.log.info(f"Reply from [{reply_url}]")
        
        # Delete the timer.
        timer = self._timers.pop(reply, QTimer)
        if timer and isinstance(timer, QTimer):
            timer.deleteLater()
        
        if error == QNetworkReply.NetworkError.ConnectionRefusedError:
            return
        
        # Get the connection and call it with the data.
        connection : Callable = self._connections.pop(reply)
        if connection:
            connection(data)
    
    def add_timer(self, reply: QNetworkReply):
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.setInterval(self.timeout)
        timer.timeout.connect(lambda : self._on_timeout(reply))
        timer.start()
                    
        self._timers[reply] = timer
        
        return timer
    
    def post(self, url: str, payload: dict, connection: Callable = None, auth: bool = False):
        self.log.info(f"Sending POST request to [{url}]")
        
        request = QNetworkRequest(QUrl(url))
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        
        json_data = QJsonDocument.fromVariant(payload).toJson()
        
        if auth:
            access_token = get_property("AccessToken")
            request.setRawHeader(b"Authorization", f"Bearer {access_token}".encode())
        
        reply = self.network_manager.post(request, json_data)
        
        if connection:
            self._connections[reply] = connection
            self.add_timer(reply)
    
    def upload_file(
            self,
            url: str,
            file_src: str,
            username: str,
            progress_connection: Callable = None,
            reply_connection: Callable = None
        ):
        request = QNetworkRequest(QUrl(url))
        
        access_token = get_property("AccessToken")
        if not access_token:
            self.log.info("Couldn't get property: AccessToken")
            
            return
        
        request.setRawHeader(b"Authorization", f"Bearer {access_token}".encode())
        
        file = QFile(file_src)
        if not file.open(QIODevice.OpenModeFlag.ReadOnly):
            self.log.info(f"Couldn't open file [{file_src}]")
            
            return
        
        multipart = QHttpMultiPart(QHttpMultiPart.ContentType.FormDataType)
        
        # File part.
        file_part = QHttpPart()
        file_part.setHeader(
            QNetworkRequest.KnownHeaders.ContentDispositionHeader,
            f'form-data; name="file"; filename="{os.path.basename(file.fileName())}"'
        )
        file_part.setBodyDevice(file)
        file.setParent(multipart)
        
        multipart.append(file_part)
        
        # Username part.
        username_part = QHttpPart()
        username_part.setHeader(
            QNetworkRequest.KnownHeaders.ContentDispositionHeader,
            'form-data; name="username"'
        )
        username_part.setBody(username.encode())
        
        multipart.append(username_part)
            
        reply = self.network_manager.post(request, multipart)
        multipart.setParent(reply)
        
        if reply_connection:
            self._connections[reply] = reply_connection
            self.add_timer(reply)
        
        if progress_connection:
            reply.uploadProgress.connect(progress_connection)
        
        reply.errorOccurred.connect(lambda err: self.log.info(f"Upload error: {err} [{file_src}]"))
    
    def _on_timeout(self, reply: QNetworkReply):
        timer = self._timers.get(reply)
        if not timer:
            return
        
        timer.deleteLater()
        timer_seconds = int(self.timeout / 1000)
        
        reply_url = reply.url().toString()
        
        self.log.info(f"Request timed out to [{reply_url}] after {timer_seconds} seconds.")
        
        popup = QMessageBox(self.parent())
        popup.setWindowTitle("API Network Timeout")
        popup.setText(f"API timed out after {timer_seconds} seconds.")
        popup.setIcon(QMessageBox.Icon.Warning)
        popup.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
        
        popup.exec()
    
    def get(self, url: str, connection: Callable, auth: bool = False):
        self.log.info(f"Sending GET request to [{url}]")
        request = QNetworkRequest(QUrl(url))
        
        if auth:
            access_token = get_property("AccessToken")
            request.setRawHeader(b"Authorization", f"Bearer {access_token}".encode())
        
        reply = self.network_manager.get(request)
        
        self._connections[reply] = connection
        self.add_timer(reply)