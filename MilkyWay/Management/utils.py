from cryptography.fernet import Fernet,InvalidToken
from django.conf import settings
import json

#ecryption key
fernet = Fernet(settings.FERNET_KEY)

def encrypt_data(data):
    json_data = json.dumps(data, ensure_ascii=False)
    encrypted_data = fernet.encrypt(json_data.encode('utf-8'))
    return encrypted_data.decode('utf-8')

def decrypt_data(encrypted_value):
    try:
        decrypted_data = fernet.decrypt(encrypted_value.encode('utf-8')).decode('utf-8')
        return json.loads(decrypted_data)
    except InvalidToken:
        return None