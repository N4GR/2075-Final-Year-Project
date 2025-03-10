import requests

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
    
    def get_chat_data(self) -> dict:
        # EXAMPLE FUNCTION.
        return {
            "Members": [
                {
                    "username": "Karl",
                    "id": 1
                },
                {
                    "username": "Kenny",
                    "id": 2
                },
                {
                    "username": "Kerry",
                    "id": 3
                }
            ],
            "Messages": [
                {
                    "text": "Hello Kenny!",
                    "author_id": 1
                },
                {
                    "text": "Hey Kenny, how are you?",
                    "author_id": 2
                },
                {
                    "text": "Sup guys, did you see the game last night?",
                    "author_id": 3
                },
                {
                    "text": "Yeahhhh, it was crazy dude! Also, doing pretty good Ken, hbu?",
                    "author_id": 1
                }
            ]
        }
    
    def ___get_chat_data(self, chat_id: int) -> dict:
        endpoint = f"/api/chat/get/{chat_id}"

        url = self.api_url + endpoint
        with requests.get(url, headers = self.headers) as response:
            response.raise_for_status()
            
            return response.json()