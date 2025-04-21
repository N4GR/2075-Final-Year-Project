import rsa
from rsa.key import PrivateKey, PublicKey
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64
import hashlib

def generate_rsa_keypair() -> tuple[PublicKey, PrivateKey]:
    public_key, private_key = rsa.newkeys(2048)
    
    return public_key, private_key

def encrypt_private_key(private_key: PrivateKey, password: str) -> tuple[bytes, bytes, bytes]:
    # Create a key derived from password.
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = salt,
        iterations = 100_000,
        backend = default_backend()
    )
    
    key = kdf.derive(password.encode())
    
    # Convert the key to bytes.
    private_key_bytes = private_key.save_pkcs1()
    
    # Pad private key bytes to make its size a multiple of the block size.
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(private_key_bytes) + padder.finalize()
    
    # Initialise AES Cipher for encryption. (AES CBC mode)
    iv = os.urandom(16) # Initialisation vector.
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend = default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the private key.
    encrypted_private_key = encryptor.update(padded_data) + encryptor.finalize()
    
    return salt, iv, encrypted_private_key

def decrypt_private_key(encrypted_private_key: bytes, password: str, salt: bytes, iv: bytes) -> PrivateKey:
    # Derive the key from the same password, salt and method.
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = salt,
        iterations = 100_000,
        backend = default_backend()
    )
    key = kdf.derive(password.encode())
    
    # Initialise AES cipher for decryption.
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend = default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the private key.
    decrypted_data = decryptor.update(encrypted_private_key) + decryptor.finalize()
    
    # Unpad the decrypted private key.
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    # Load the private key from the bytes object.
    private_key = PrivateKey.load_pkcs1(unpadded_data)
    
    return private_key

def generate_shared_secret(shared_secret: bytes, public_key: bytes) -> bytes:
    public_key = PublicKey.load_pkcs1(public_key)
        
    encrypted_shared_secret = rsa.encrypt(shared_secret, public_key)
    
    return encrypted_shared_secret

def decrypt_shared_secret(encrypted_shared_secret: bytes, private_key: PrivateKey):
    return rsa.decrypt(encrypted_shared_secret, private_key)

def encrypt_message(message: str, shared_secret: bytes) -> tuple[bytes, bytes]:
    message = message.encode()
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(shared_secret), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    # Pad message to block size.
    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message) + padder.finalize()
    
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    
    return iv, ciphertext

def decrypt_message(iv: bytes, ciphertext: bytes, shared_secret: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(shared_secret), modes.CBC(iv))
    decryptor = cipher.decryptor()
    
    padded_message = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    message = unpadder.update(padded_message) + unpadder.finalize()
    
    return message.decode("utf-8")