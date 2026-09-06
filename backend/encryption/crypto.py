from cryptography.fernet import Fernet
import os

KEY_FILE=os.path.join(os.path.dirname(__file__),"secret.key")

def get_key():
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE,"wb") as f:f.write(Fernet.generate_key())
    with open(KEY_FILE,"rb") as f:return f.read()

def encrypt_password(value):
    return Fernet(get_key()).encrypt(value.encode()).decode()

def decrypt_password(value):
    return Fernet(get_key()).decrypt(value.encode()).decode()
