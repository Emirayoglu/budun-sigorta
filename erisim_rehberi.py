"""
Basit Port Forwarding (Windows için)
Port yönlendirme yaparak internete aç
"""

import socket

def get_local_ip():
    """Yerel IP adresini bul"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

print("=" * 60)
print("📱 BUDUN Sigorta - Basit Erişim Rehberi")
print("=" * 60)
print()

local_ip = get_local_ip()

print("🏠 1. AYNI WiFi'DEN ERİŞİM (EN KOLAY)")
print("-" * 60)
print()
print("▶️ web_app.py çalıştır:")
print("   python web_app.py")
print()
print(f"▶️ Telefondan aç:")
print(f"   http://{local_ip}:5000")
print()
print("✅ PC ve telefon aynı WiFi'de olmalı!")
print()
print()

print("🌍 2. FARKLI WiFi'DEN ERİŞİM")
print("-" * 60)
print()
print("Seçenek A: Ngrok (Kayıt gerekli)")
print("  1. https://ngrok.com/signup adresinden kayıt ol")
print("  2. Token'ı al")
print("  3. ngrok config add-authtoken YOUR_TOKEN")
print("  4. ngrok http 5000")
print()
print("Seçenek B: Localtunnel (Kayıtsız)")
print("  1. Node.js yükle: https://nodejs.org/")
print("  2. npm install -g localtunnel")
print("  3. lt --port 5000")
print()
print("Seçenek C: Tailscale (En güvenli)")
print("  1. https://tailscale.com/ hesap aç")
print("  2. Hem PC hem telefona yükle")
print("  3. Otomatik bağlan")
print()
print()

print("💡 ÖNERİ:")
print("Aynı WiFi yöntemi en kolay ve hızlı!")
print("İnternetten erişim için modem ayarlarında")
print("port forwarding yapabilirsin (5000 → PC IP)")
print()


