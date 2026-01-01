"""
Ngrok ile internete aç
Her yerden erişim için
"""

from pyngrok import ngrok
import os

print("🌍 İnternet Bağlantısı Açılıyor...")
print()

# Ngrok token (ilk kullanımda gerekli)
# Token almak için: https://dashboard.ngrok.com/get-started/setup
# ngrok_token = "YOUR_TOKEN_HERE"
# ngrok.set_auth_token(ngrok_token)

# Web uygulamasını internete aç
public_url = ngrok.connect(5000)

print("=" * 60)
print("🎉 İNTERNETTEN ERİŞİM HAZIR!")
print("=" * 60)
print()
print(f"🌍 İnternet Adresi: {public_url}")
print()
print("✅ Bu adresi herhangi bir cihazdan aç!")
print("✅ Internet üzerinden her yerden erişebilirsin")
print("✅ Telefon, tablet, başka PC - hepsi tamam!")
print()
print("💡 web_app.py'yi çalıştırmayı unutma!")
print()


