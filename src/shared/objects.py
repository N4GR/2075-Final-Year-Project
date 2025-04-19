from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    profile_picture: bytes = None