import os
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PublicKey, X25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
from typing import Dict, Tuple

def generate_keys(password: str) -> Tuple[bytes, bytes, bytes, bytes]: # salt, public_key, encrypted_private_key, nonce.
    """Generates a public and private key, where the private key is encrypted using the user's password.
    
    Args:
        password (str): User's password.
    
    Returns:
        tuple(bytes, bytes, bytes, bytes): salt, public_key, encrypted_private_key, nonce.
    """
    # ECDH Key pair.
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    private_bytes = private_key.private_bytes_raw()
    public_key = public_key.public_bytes_raw()
    
    # Key derived from user password.
    salt = os.urandom(16)
    kdf = Argon2id(
        salt = salt,
        length = 32,
        iterations = 4,
        memory_cost = 2**16,
        lanes = 1
    )
    
    key = kdf.derive(password.encode())
    
    # Encrypting private key.
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    
    encrypted_private_key = aesgcm.encrypt(nonce, private_bytes, None)
    
    return salt, public_key, encrypted_private_key, nonce

def encrypt_chat_key_for_all(
        sender_private_key: bytes,
        recipients_public_keys: dict[str, bytes]
) -> Tuple[bytes, Dict[str, Dict[str, str]]]:
    """
    Generates a random chat key and encrypts it for each recipient using ECDH.

    Args:
        sender_private_key (bytes): Sender's private key.
        recipients_public_keys (dict[str, bytes]): Dict of user_id -> public key bytes.

    Returns:
        tuple: (chat_key, {
            user_id -> {
                "encrypted_chat_key": hex-encoded string,
                "nonce": hex-encoded string
            }
        })
    """
    sender_private_key = X25519PrivateKey.from_private_bytes(sender_private_key)
    chat_key = os.urandom(32)
    encrypted_keys = {}

    for user_id, public_key_bytes in recipients_public_keys.items():
        recipient_pubkey = X25519PublicKey.from_public_bytes(public_key_bytes)

        # ECDH to derive shared secret
        shared_secret = sender_private_key.exchange(recipient_pubkey)

        # Derive AES key (you can use HKDF or hash)
        aes_key = hashlib.sha256(shared_secret).digest()

        # Encrypt the chat_key using AES-GCM
        nonce = os.urandom(12)
        aesgcm = AESGCM(aes_key)
        encrypted = aesgcm.encrypt(nonce, chat_key, None)

        encrypted_keys[user_id] = {
            "encrypted_chat_key": encrypted.hex(),
            "nonce": nonce.hex()
        }

    return chat_key, encrypted_keys

def decrypt_chat_key(
    recipient_private_key: bytes,
    sender_public_key: bytes,
    encrypted_chat_key: str,
    nonce: str
) -> bytes:
    """
    Decrypts an encrypted chat key using ECDH between the recipient and sender.

    Args:
        recipient_private_key (bytes): The recipient's private key (32 bytes).
        sender_public_key (bytes): The sender's public key (32 bytes).
        encrypted_chat_key (str): Hex-encoded AES-GCM encrypted chat key.
        nonce (str): Hex-encoded AES-GCM nonce used during encryption.

    Returns:
        bytes: The decrypted chat key (32 bytes).
    """
    private_key = X25519PrivateKey.from_private_bytes(recipient_private_key)
    public_key = X25519PublicKey.from_public_bytes(sender_public_key)

    # Derive shared secret with ECDH
    shared_secret = private_key.exchange(public_key)

    # Derive AES key from shared secret
    aes_key = hashlib.sha256(shared_secret).digest()

    # Decrypt the chat key
    aesgcm = AESGCM(aes_key)
    decrypted_chat_key = aesgcm.decrypt(
        bytes.fromhex(nonce),
        bytes.fromhex(encrypted_chat_key),
        None  # No associated data
    )

    return decrypted_chat_key

def decrypt_private_key(encrypted_private_key: bytes, password: str, salt: bytes, nonce: bytes) -> bytes:
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=4,
        memory_cost=2**16,
        lanes = 1
    )
    key = kdf.derive(password.encode())
    aesgcm = AESGCM(key)
    private_key = aesgcm.decrypt(nonce, encrypted_private_key, None)
    
    return private_key

def decrypt_message(encrypted: str, nonce: str, chat_key: bytes) -> str:
    aesgcm = AESGCM(chat_key)
    plaintext = aesgcm.decrypt(
        bytes.fromhex(nonce),
        bytes.fromhex(encrypted),
        None  # or associated_data if used
    )
    return plaintext.decode("utf-8")

def encrypt_message(plaintext: str, chat_key: bytes) -> dict:
    aesgcm = AESGCM(chat_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    return {
        "encrypted_message": ciphertext.hex(),
        "nonce": nonce.hex()
    }