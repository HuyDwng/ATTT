from cryptography.fernet import Fernet
from django.conf import settings
import json

#ecryption key
fernet = Fernet(settings.FERNET_KEY)

# def encrypt_data(data):
#     return fernet.encrypt(data.encode()).decode()

# def decrypt_data(encrypted_data):
#     return fernet.decrypt(encrypted_data.encode()).decode()


def encrypt_data(data):
    # Chuyển đổi dữ liệu thành chuỗi JSON
    json_data = json.dumps(data, default=str)
    encrypted_data = fernet.encrypt(json_data.encode())
    return encrypted_data.decode()  # Trả về dữ liệu đã mã hóa dưới dạng chuỗi

def decrypt_data(encrypted_data):
    decrypted_data = fernet.decrypt(encrypted_data.encode()).decode()
    return json.loads(decrypted_data)