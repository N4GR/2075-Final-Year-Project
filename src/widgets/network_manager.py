from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtCore import QUrl, QObject, QJsonDocument, QTimer
from PySide6.QtWidgets import QMessageBox

from logging import Logger
import json
from typing import Callable


from src.shared.decorators import Decorators

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
        if timer:
            timer.stop()
            timer.deleteLater()
        
        if error == QNetworkReply.NetworkError.ConnectionRefusedError:
            return
        
        # Get the connection and call it with the data.
        connection = self._connections.pop(reply, Callable)
        if connection:
            connection(data)
    
    def post(self, url: str, payload: dict, connection: Callable = None):
        self.log.info(f"Sending POST request to [{url}]")
        
        request = QNetworkRequest(QUrl(url))
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        
        json_data = QJsonDocument.fromVariant(payload).toJson()
        
        reply = self.network_manager.post(request, json_data)
        
        if connection:
            self._connections[reply] = connection
            
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.setInterval(self.timeout)
            timer.timeout.connect(lambda : self._on_timeout(reply))
            timer.start()
                        
            self._timers[reply] = timer
    
    def _on_timeout(self, reply: QNetworkReply):
        timer = self._timers[reply]
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