"""
Serveo - SSH Tunnel (En basit!)
Hiçbir kurulum gerektirmez
"""

import subprocess
import sys

print("=" * 60)
print("🌍 Serveo ile İnternet Erişimi")
print("=" * 60)
print()
print("✅ Hiçbir kurulum gerektirmez!")
print("✅ Token gerektirmez!")
print("✅ Kayıt gerektirmez!")
print()

print("⏳ Web uygulamanın çalıştığından emin ol!")
print("   (Başka terminalde: python web_app.py)")
print()
input("Hazır olunca ENTER'a bas...")
print()

print("=" * 60)
print("🚀 Tünel açılıyor...")
print("=" * 60)
print()
print("📱 Birkaç saniye sonra internet adresi göreceksin!")
print("   http://serveo.net/xyz gibi bir adres")
print()

try:
    # SSH ile serveo tüneli
    subprocess.run([
        "ssh",
        "-R", "80:localhost:5000",
        "serveo.net"
    ])
except KeyboardInterrupt:
    print()
    print("👋 Tünel kapatıldı!")
except FileNotFoundError:
    print("❌ SSH bulunamadı!")
    print()
    print("💡 Windows için:")
    print("   Settings > Apps > Optional Features")
    print("   'OpenSSH Client' yükle")
    print()
    print("VEYA BASLA.bat kullan (daha kolay!)")


