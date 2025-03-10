from src.imports import *

class NetworkManager:
    def __init__(self):
        self.api_url = "https://fmp.n4gr.uk"
        
        token_data = self.get_session_token()
        self.token = token_data["token"]
        self.token_expiration = token_data["expiration_time"]
        
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
    def get_session_token(self) -> dict:
        endpoint = "/api/session/get"
        
        url = self.api_url + endpoint
        with requests.get(url) as response:
            response.raise_for_status()
            
            return response.json()
    
    def get_chat_data(self, chat_id: int) -> dict:
        endpoint = f"/api/chat/get/{chat_id}"

        url = self.api_url + endpoint
        with requests.get(url, headers = self.headers) as response:
            response.raise_for_status()
            
            return response.json()