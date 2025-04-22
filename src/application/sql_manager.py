# Python imports.
import sqlite3
from collections import namedtuple
from logging import Logger
from uuid import UUID
from datetime import datetime

# Local imports.
from src.shared.decorators import Decorators
from src.shared.funcs import path

@Decorators.property
@Decorators.autolog
class SQLManager:
    log : Logger
    
    def __init__(self):
        self._connection = sqlite3.connect(path("/data/metaphrast.sqlite"), autocommit = True)
        self._connection.row_factory = self.named_tuple_factory
        
        self._cursor = self._connection.cursor()
    
    @staticmethod
    def named_tuple_factory(cursor: sqlite3.Cursor, row: sqlite3.Row):
        fields = [col[0] for col in cursor.description]
        Row = namedtuple("Row", fields)
        
        return Row(*row)
    
    def add_chat(self, chat_id: str, sender_id: str, recipient_id: str, created_at: str):
        """Adds a chat to the chats table.
        
        Args:
            chat_id (str): Chat ID from UUID hex.
            sender_id (str): Sender ID from UUID hex.
            recipient_id (str): Recipient ID from UUID hex.
        """
        self._cursor.execute("""
            INSERT INTO chats (
                chat_id, sender_id, recipient_id,
                created_at
            ) VALUES (
                ?, ?, ?, ?
            )
        """, (chat_id, sender_id, recipient_id, created_at))
    
    def get_chat(self, chat_id: str) -> dict[str, UUID] | None:
        """Gets a chat from the SQLManager using the chat id.
        
        Args:
            chat_id (str): Chat ID in the chats database.
        
        Returns:
            dict[str, UUID] | None: Dictionary of returned values.
                {"chat_id": UUID, "sender_id": UUID, "recipient_id": UUID}
        """
        self._cursor.execute("SELECT * FROM chats WHERE chat_id = ?", (chat_id,))
        fetch = self._cursor.fetchone()
        
        if not fetch:
            return None
        
        return {
            "chat_id": UUID(fetch.chat_id),
            "sender_id": UUID(fetch.sender_id),
            "recipient_id": UUID(fetch.recipient_id)
        }
    
    def add_message(
            self,
            message_id: str,
            chat_id: str,
            sender_id: str,
            encrypted_message: bytes,
            iv: bytes,
            encrypted_shared_secret_for_sender: bytes,
            encrypted_shared_secret_for_recipient: bytes,
            sent_at: str
    ):
        """Adds a message to the messages table.
        
        Args:
            message_id (str): Message ID as a UUID str hex.
            chat_id (str): Chat ID as UUID str hex.
            sender_id (str): Sender ID as UUID str hex.
            encrypted_message (bytes): Encrypted message as bytes object.
            iv: IV as bytes object.
            encrypted_shared_secret_for_sender (bytes): Encrypted secret for sender.
            encrypted_shared_secret_for_recipient (bytes): Encrypted secret for recipient.
            sent_at (str): Timestamp string from datetime object.
        """
        self._cursor.execute("""
            INSERT INTO messages (
                message_id, chat_id, sender_id,
                encrypted_message, iv, sent_at,
                encrypted_shared_secret_for_sender,
                encrypted_shared_secret_for_recipient
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            message_id, chat_id, sender_id, encrypted_message,
            iv, sent_at, encrypted_shared_secret_for_sender,
            encrypted_shared_secret_for_recipient
        ))
    
    def get_message(self, message_id: str) -> dict:
        self._cursor.execute("""
            SELECT * FROM messages
            WHERE message_id = ?
        """, (message_id,))
        
        fetch = self._cursor.fetchone()
        if not fetch: return None
        
        return {
            "message_id": fetch.message_id,
            "chat_id": fetch.chat_id,
            "sender_id": fetch.sender_id,
            "encrypted_message": fetch.encrypted_message,
            "iv": fetch.iv,
            "encrypted_shared_secret_for_sender": fetch.encrypted_shared_secret_for_sender,
            "encrypted_shared_secret_for_recipient": fetch.encrypted_shared_secret_for_recipient,
            "sent_at": fetch.sent_at
        }
    
    def get_messages(self, chat_id: str):
        self._cursor.execute("""
            SELECT * FROM messages
            WHERE chat_id = ?
            ORDER BY sent_at ASC
        """, (chat_id,))
        
        fetch = self._cursor.fetchall()
        if not fetch: return None
        
        fixed_fetch : list[dict] = []
        for item in fetch:
            fixed_fetch.append({
                "message_id": UUID(item.message_id),
                "chat_id": UUID(item.chat_id),
                "sender_id": UUID(item.sender_id),
                "encrypted_message": item.encrypted_message,
                "iv": item.iv,
                "encrypted_shared_secret_for_sender": item.encrypted_shared_secret_for_sender,
                "encrypted_shared_secret_for_recipient": item.encrypted_shared_secret_for_recipient,
                "sent_at": datetime.fromtimestamp(float(item.sent_at))
            })
        
        return fixed_fetch
    
    def get_profile(self, user_id: UUID = None, username: str = None) -> dict[str, UUID | str | bytes]:
        field = "user_id" if user_id else "username"
        data = user_id.hex if user_id else username
        
        query = f"""
            SELECT * FROM profiles
            WHERE {field} = ?
        """
        
        self._cursor.execute(query, (data,))
        fetch = self._cursor.fetchone()
        if not fetch: return None
        
        return {
            "user_id": UUID(fetch.user_id),
            "username": fetch.username,
            "profile": fetch.profile,
        }
    
    def add_profile(self, user_id: UUID, username: str, profile: bytes):
        self._cursor.execute("""
            INSERT INTO profiles (
                user_id, profile, username
            ) VALUES (
                ?, ?, ?
            )
        """, (user_id.hex, profile, username))
    
    def get_all_chats(self) -> list[dict[str, str]]:
        self._cursor.execute("SELECT * FROM chats")
        fetch = self._cursor.fetchall()
        
        if not fetch: return None
        
        fetching : list[dict[str, str]] = []
        for item in fetch:
            fetching.append({
                "chat_id": item.chat_id,
                "sender_id": item.sender_id,
                "recipient_id": item.recipient_id,
                "created_at": item.created_at
            })
        
        return fetching