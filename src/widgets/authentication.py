from src.shared.imports import *

# Third-party imports.
import srp

APIURL = "http://localhost:8080"

class Login(QObject):
    api : ApiClient
    reply_signal = Signal(object)
    
    def __init__(self, parent: QWidget, username: str, password: str):
        super().__init__(parent)
        self.username = username
        self.password = password
        
    @Decorators.api
    def run(self):
        self.usr = srp.User(self.username, self.password)
        username, A = self.usr.start_authentication()
        
        payload = {
            "username": username,
            "A": A.hex()
        }
        
        self.api.post(url = f"{APIURL}/post/challenge", payload = payload, connection = self._challenge_reply)

    @Decorators.api
    def _challenge_reply(self, data):
        data = json.loads(data)
        
        if "error" in data:
            login_panel : QWidget = get_property("LoginPanel")
            username_input : QLineEdit = login_panel.username_input
            
            username_input.set_error(f"{data['code']} - {data['error']}")
            
            return
        
        s = bytes.fromhex(data["s"])
        B = bytes.fromhex(data["B"])
        
        M = self.usr.process_challenge(s, B)

        payload = {
            "username": self.username,
            "M": M.hex()
        }
        
        self.api.post(url = f"{APIURL}/post/verify", payload = payload, connection = self._session_reply)
    
    def _session_reply(self, data):
        data = json.loads(data)
        
        if "error" in data:
            login_panel : QWidget = get_property("LoginPanel")
            password_input : QLineEdit = login_panel.password_input
            
            password_input.set_error(f"{data['code']} - {data['error']}")
            
            return

        HAMK = bytes.fromhex(data["HAMK"])

        self.usr.verify_session(HAMK)
        
        if self.usr.authenticated():
            print(True)
        
        else:
            print(False)

class Register(QObject):
    api : ApiClient
    
    def __init__(self, parent: QWidget, username: str, password: str):
        super().__init__(parent)
        self.username = username
        self.password = password
        
    @Decorators.api
    def run(self):
        salt, vkey = srp.create_salted_verification_key(self.username, self.password)
        
        payload = {
            "username": self.username,
            "salt": salt.hex(),
            "srp_verifier": vkey.hex()
        }
        
        self.api.post(f"{APIURL}/post/register", payload, self._registration_reply)
    
    def _registration_reply(self, data):
        data = json.loads(data)
        
        if "error" in data:
            panel : QWidget = get_property("RegisterPanel")
            username_input : QLineEdit = panel.username_input
            password_input : QLineEdit = panel.password_input
            
            username_input.set_error(f"{data['code']} - {data['error']}")

            return
        
        parent : QWidget = self.parent()
        parent._registration_complete()