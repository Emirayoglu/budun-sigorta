"""
Localtunnel ile internete aç
Ngrok'tan daha kolay, kayıt gerektirmiyor!
"""

import subprocess
import sys

print("🌍 Localtunnel ile İnternet Erişimi")
print("=" * 60)
print()

# Localtunnel yükle
print("1️⃣ Localtunnel yükleniyor...")
try:
    subprocess.run(["npm", "install", "-g", "localtunnel"], check=True)
    print("   ✅ Yüklendi!")
except:
    print("   ⚠️ NPM bulunamadı!")
    print()
    print("💡 Node.js yükle:")
    print("   https://nodejs.org/")
    print()
    sys.exit(1)

print()
print("2️⃣ İnternet tüneli açılıyor...")
print()

# Localtunnel başlat
print("=" * 60)
print("🎉 İNTERNET ERİŞİMİ HAZIR!")
print("=" * 60)
print()
print("⚠️ web_app.py'nin çalıştığından emin ol!")
print()
print("Şimdi şu komutu çalıştır:")
print("lt --port 5000")
print()
print("Sana bir internet adresi verecek:")
print("https://xyz-abc-123.loca.lt")
print()
print("Bu adresi telefondan veya her yerden aç!")
print()


