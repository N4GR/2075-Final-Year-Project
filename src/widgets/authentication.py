from src.shared.imports import *

# Third-party imports.
import srp
import hashlib

@Decorators.autolog
@Decorators.api
@Decorators.property
class SRPRegister(QObject):
    log : logging.Logger
    api : ApiClient
    
    error_signal = Signal(dict)
    
    def __init__(self, parent: QWidget, username: str, password: str, profile_src: str):
        super().__init__(parent)
        self.username = username
        self.password = password
        self.profile_src = profile_src
    
    def register(self):
        salt, vkey = srp.create_salted_verification_key(self.username, self.password)
        
        self.api.post(
            API_SRP_REGISTER,
            {
                "username": self.username,
                "salt": salt.hex(),
                "srp_verifier": vkey.hex()
            },
            self._register_reply
        )
    
    def _register_reply(self, data):
        data : dict = json.loads(data)
        
        if "error" in data:
            self.log.info(f"{data['code']} - {data['error']}")
            self.error_signal.emit(data)
            
            return
        
        access_token = data.get("access_token")
        access_token_expiry = data.get("access_token_expiry")
        
        set_property("AccessToken", access_token)
        set_property("AccessTokenExpiry", access_token_expiry)

@Decorators.autolog
@Decorators.api
@Decorators.property
class SRPLogin(QObject):
    log : logging.Logger
    api : ApiClient
    
    error_signal = Signal(dict)
    
    def __init__(self, parent: QWidget, username: str, password: str):
        super().__init__(parent)
        self.username = username
        self.password = password
        
        self.user : srp.User = None
    
    def login(self):
        self.user = srp.User(self.username, self.password)
        username, A = self.user.start_authentication()
        
        self.api.post(
            API_SRP_START,
            {
                "username": username,
                "A": A.hex()
            },
            self._handle_challenge
        )
    
    def _handle_challenge(self, data):
        data : dict = json.loads(data)
        
        if "error" in data:
            self.log.info(f"{data['code']} - {data['error']}")
            self.error_signal.emit(data)
            
            return
        
        salt_hex = data.get("salt")
        b_hex = data.get("B")
        
        if not salt_hex:
            self.log.info(f"Salt hex not received.")
            
            return
        
        if not b_hex:
            self.log.info(f"B hex not received.")
            
            return
        
        salt = bytes.fromhex(salt_hex)
        B = bytes.fromhex(b_hex)
        
        # Process challenge.
        M = self.user.process_challenge(salt, B)
        
        self.api.post(
            API_SRP_VERIFY,
            {
                "username": self.username,
                "M": M.hex()
            },
            self._verify_reply
        )
        
    def _verify_reply(self, data):
        data : dict = json.loads(data)
        
        if "error" in data:
            self.log.info(f"{data['code']} - {data['error']}")
            self.error_signal.emit(data)
            
            return
        
        hamk_hex = data.get("HAMK")
        access_token = data.get("access_token")
        access_token_expiry = data.get("access_token_expiry")
        refresh_token = data.get("refresh_token")
        refresh_token_expiry = data.get("refresh_token_expiry")
        
        fields = {
            "hamk_hex": hamk_hex,
            "access_token": access_token,
            "access_token_expiry": access_token_expiry,
            "refresh_token": refresh_token,
            "refresh_token_expiry": refresh_token_expiry
        }
        
        for name, value in fields.items():
            if not value:
                self.log.info(f"Missing {name} from verification reply.")
                
                return
        
        HAMK = bytes.fromhex(hamk_hex)
        self.user.verify_session(HAMK)
        
        if self.user.authenticated():
            self.log.info(f"Server verified client verification request with HAMK: [{hamk_hex}]")
        
        else:
            self.log.info(f"Client or server failed verification with HAMK: [{hamk_hex}]")
            
            return
        
        set_property("AccessToken", access_token)
        set_property("AccessTokenExpiry", access_token_expiry)
        
        self.log.info(f"Setting keyring service with name 'metaphrast' and username 'refresh_token'")
        keyring.set_password("metaphrast", "refresh_token", refresh_token)

@Decorators.autolog
class Login(QObject):
    log : logging.Logger
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
        
        self.api.post(url = API_CHALLENGE, payload = payload, connection = self._challenge_reply)

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
        
        self.api.post(url = API_VERIFY, payload = payload, connection = self._session_reply)
    
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
            self.log.info(f"Client account and server verified with HAMK: {HAMK.hex()}")
        
        else:
            self.log.info(f"Client account or server failed verification with HAMK: {HAMK.hex()}")
            
            return
        
        # Store tokens in a keyring and application property.
        refresh_token = data["refresh_token"]
        refresh_expiry_date = data["refresh_token_expiry"]
        access_token = data["access_token"]
        access_token_expiry = data["access_token_expiry"]

        set_property("AccessToken", access_token)
        set_property("AccessTokenExpiry", access_token_expiry)
        
        keyring.set_password("metaphrast", "refresh_token", refresh_token)
        
        self.log.info("Saved access_token to keyring: metaphrast under the name refresh_token")
                
        return

@Decorators.autolog
class Register(QObject):
    log : logging.Logger
    api : ApiClient
    
    def __init__(self, parent: QWidget, username: str, password: str, profile_src: str):
        """Registers the user into the database.

        Args:
            parent (QWidget): Parent of the QObject.
            username (str): Username of the user.
            password (str): Password of the user.
            profile_src (str): Profile picture absolute path to upload.
        """
        super().__init__(parent)
        self.username = username
        self.password = password
        self.profile_src = profile_src
        
    @Decorators.api
    def run(self):
        salt, vkey = srp.create_salted_verification_key(self.username, self.password)
        
        payload = {
            "username": self.username,
            "salt": salt.hex(),
            "srp_verifier": vkey.hex()
        }
        
        self.api.post(API_REGISTER, payload, self._registration_reply)
    
    @Decorators.api
    def _registration_reply(self, data):
        data = json.loads(data)
        
        panel : QWidget = get_property("RegisterPanel")
        username_input : QLineEdit = panel.username_input
        password_input : QLineEdit = panel.password_input
        
        if "error" in data:
            self.log.info(f"Registration error: [{data['code']}] - [{data['error']}]")
            
            username_input.set_error(f"{data['code']} - {data['error']}")
            return
        
        access_token = data.get("access_token")
        if not access_token:
            self.log.info("Didn't receive access token, registration failed.")
            
            username_input.set_error(f"Failed to retrieve access token.")
            return
        
        set_property("AccessToken", access_token)
        
        # Upload profile picture.
        self.log.info(f"Beginning upload of [{self.profile_src}]")
        
        self.api.upload_file(API_FILE_UPLOAD, self.profile_src, self.username, self._upload_progress, self._upload_reply)
    
    def _upload_progress(self, bytes_sent: int, bytes_total: int):
        """Called on file upload progress."""
        kb_sent = round(bytes_sent / 1024, 2)
        kb_total = round(bytes_total / 1024, 2)
        
        if kb_sent <= 0 or kb_total <= 0:
            return
        
        profile_upload : QWidget = get_property("ProfileUpload")
        progress_label : QLabel = profile_upload.file_upload_progress_label
        
        
        uploaded_str = f"{kb_sent}/{kb_total}KB"
        self.log.info(f"Uploaded [{uploaded_str}] of [{self.profile_src}]")
        progress_label.setText(uploaded_str)
    
    def _upload_reply(self, data):
        data = json.loads(data)
        
        if "error" in data:
            login_panel : QWidget = get_property("LoginPanel")
            password_input : QLineEdit = login_panel.password_input
            
            password_input.set_error(f"{data['code']} - {data['error']}")
            
            return
        
        self.log.info(f"Upload complete of [{self.profile_src}]")
        
        parent : QWidget = self.parent()
        parent._registration_complete()