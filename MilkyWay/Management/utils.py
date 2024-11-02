from cryptography.fernet import Fernet
from django.conf import settings


#ecryption key
fernet = Fernet(settings.FERNET_KEY)

def encrypt_data(data):
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    return fernet.decrypt(encrypted_data.encode()).decode()
