"""
Bağlantı Testi - Basit Kontrol
"""
import socket
import requests

print("=" * 50)
print("🔍 Bağlantı Kontrolü")
print("=" * 50)
print()

# 1. Internet bağlantısı
print("1️⃣ Internet bağlantısı kontrol ediliyor...")
try:
    response = requests.get("https://www.google.com", timeout=5)
    print("   ✅ Internet bağlantısı OK!")
except:
    print("   ❌ Internet bağlantısı yok!")
print()

# 2. DNS çözümlemesi
print("2️⃣ Supabase DNS kontrol ediliyor...")
try:
    ip = socket.gethostbyname("db.iivinxqtiyrtznjqkzin.supabase.co")
    print(f"   ✅ DNS OK! IP: {ip}")
except socket.gaierror as e:
    print(f"   ❌ DNS hatası: {e}")
    print("   💡 VPN kullanıyor musun? Kapatmayı dene.")
    print("   💡 Firewall Supabase'i engelliyor olabilir.")
print()

# 3. Port kontrolü
print("3️⃣ Port 5432 kontrol ediliyor...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex(('db.iivinxqtiyrtznjqkzin.supabase.co', 5432))
    sock.close()
    
    if result == 0:
        print("   ✅ Port 5432 erişilebilir!")
    else:
        print("   ❌ Port 5432 kapalı veya erişilemiyor!")
        print("   💡 Firewall kontrolü gerekebilir")
except Exception as e:
    print(f"   ❌ Port test hatası: {e}")
print()

print("=" * 50)
print("Sonuç:")
print("=" * 50)


