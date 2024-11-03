from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
import json

#ecryption key
fernet = Fernet(settings.FERNET_KEY)

def encrypt_data(data):
    data = data.encode('utf-8')  # Chuyển chuỗi thành bytes
    return fernet.encrypt(data).decode('utf-8')

def decrypt_data(encrypted_value):
    try:
        encrypted_value = encrypted_value.encode('utf-8')  # Chuyển về bytes
        return fernet.decrypt(encrypted_value).decode('utf-8') 
    except InvalidToken:
        # Xử lý khi token không hợp lệ
        print("Giải mã không thành công: Token không hợp lệ.")
        return None  # Hoặc xử lý lỗi theo cách khác