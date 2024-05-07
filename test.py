import base64
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        # Tạo và lưu trữ khóa mã hóa một cách an toàn.
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt_password(self, password: str) -> str:
        # Mã hóa mật khẩu và chuyển kết quả đã mã hóa thành chuỗi base64.
        encrypted = self.cipher_suite.encrypt(password.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt_password(self, encrypted_password: str) -> str:
        # Chuyển đổi chuỗi base64 trở lại thành bytes, sau đó giải mã.
        encrypted = base64.urlsafe_b64decode(encrypted_password.encode())
        return self.cipher_suite.decrypt(encrypted).decode()

# Sử dụng lớp để mã hóa và giải mã mật khẩu.
if __name__ == "__main__":
    password_manager = PasswordManager()
    password = "example_password"
    encrypted = password_manager.encrypt_password(password)
    print("Encrypted:", encrypted, type(encrypted))
    decrypted = password_manager.decrypt_password(encrypted)
    print("Decrypted:", decrypted, type(decrypted))
    
    encrypted2 = password_manager.encrypt_password("example_password")
    print("Encrypted:", encrypted2, type(encrypted2))
    decrypted2 = password_manager.decrypt_password(encrypted2)
    print("Decrypted:", decrypted2, type(decrypted2))
    
