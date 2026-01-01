# GÜVENLİ Config Yönetimi
# Hassas bilgileri korumak için

import os
from cryptography.fernet import Fernet

class SecureConfig:
    """
    Supabase bilgilerini şifreleyerek sakla
    EXE'ye gömülse bile güvenli
    """
    
    # Şifreleme anahtarı (ilk çalıştırmada oluştur)
    KEY_FILE = "secure.key"
    
    @staticmethod
    def generate_key():
        """Yeni şifreleme anahtarı oluştur"""
        key = Fernet.generate_key()
        with open(SecureConfig.KEY_FILE, 'wb') as f:
            f.write(key)
        return key
    
    @staticmethod
    def load_key():
        """Mevcut anahtarı yükle"""
        if not os.path.exists(SecureConfig.KEY_FILE):
            return SecureConfig.generate_key()
        
        with open(SecureConfig.KEY_FILE, 'rb') as f:
            return f.read()
    
    @staticmethod
    def encrypt_config(url, key):
        """Config bilgilerini şifrele"""
        fernet = Fernet(SecureConfig.load_key())
        
        encrypted_url = fernet.encrypt(url.encode())
        encrypted_key = fernet.encrypt(key.encode())
        
        return encrypted_url, encrypted_key
    
    @staticmethod
    def decrypt_config(encrypted_url, encrypted_key):
        """Config bilgilerini çöz"""
        fernet = Fernet(SecureConfig.load_key())
        
        url = fernet.decrypt(encrypted_url).decode()
        key = fernet.decrypt(encrypted_key).decode()
        
        return url, key

# Kullanım:
# from secure_config import SecureConfig
# url, key = SecureConfig.decrypt_config(ENCRYPTED_URL, ENCRYPTED_KEY)


