"""
Cloudflared ile Otomatik İnternet Erişimi
Token yok, kayıt yok, direkt çalışır!
"""

import subprocess
import sys
import os
import urllib.request
import zipfile
import platform

print("=" * 60)
print("🌍 BUDUN - İnternet Erişimi Kuruluyor")
print("=" * 60)
print()

# Cloudflared indir ve yükle
print("1️⃣ Cloudflared indiriliyor...")

system = platform.system()
machine = platform.machine()

if system == "Windows":
    if "64" in machine or "x86_64" in machine or "AMD64" in machine:
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
        filename = "cloudflared.exe"
    else:
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-386.exe"
        filename = "cloudflared.exe"
else:
    print("❌ Bu script şu an sadece Windows için!")
    sys.exit(1)

# İndir
if not os.path.exists(filename):
    print(f"   İndiriliyor: {url}")
    try:
        urllib.request.urlretrieve(url, filename)
        print("   ✅ İndirildi!")
    except Exception as e:
        print(f"   ❌ İndirme hatası: {e}")
        print()
        print("Manuel indirme:")
        print(f"   {url}")
        print("   İndirdikten sonra bu klasöre kopyala")
        sys.exit(1)
else:
    print("   ✅ Zaten indirilmiş!")

print()
print("2️⃣ İnternet tüneli açılıyor...")
print()
print("⏳ Web uygulamanın çalıştığından emin ol!")
print("   (Başka bir terminalde: python web_app.py)")
print()

# Cloudflared başlat
print("=" * 60)
print("🚀 Tünel açılıyor...")
print("=" * 60)
print()

try:
    subprocess.run([filename, "tunnel", "--url", "http://localhost:5000"])
except KeyboardInterrupt:
    print()
    print("👋 Tünel kapatıldı!")


