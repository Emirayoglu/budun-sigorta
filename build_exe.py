# BUDUN Sigorta Yönetim Sistemi - EXE Oluşturma Script
# PyInstaller ile tek dosya EXE

import subprocess
import sys
import os

print("=" * 60)
print("📦 BUDUN - EXE Oluşturma Başlıyor")
print("=" * 60)
print()

# 1. PyInstaller'ı yükle
print("1️⃣ PyInstaller yükleniyor...")
subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
print("   ✅ PyInstaller yüklendi!")
print()

# 2. EXE oluştur
print("2️⃣ EXE dosyası oluşturuluyor...")
print("   ⏳ Bu birkaç dakika sürebilir...")
print()

# PyInstaller komutu (İkonsuz)
cmd = [
    "pyinstaller",
    "--name=BUDUN-Sigorta",
    "--onefile",  # Tek dosya
    "--windowed",  # Console penceresi gösterme
    "--add-data=config.py;.",  # Config dosyasını dahil et
    "--hidden-import=supabase",
    "--hidden-import=psycopg2",
    "--hidden-import=database_supabase",
    "main.py"
]

try:
    subprocess.run(cmd, check=True)
    print()
    print("=" * 60)
    print("🎉 EXE BAŞARIYLA OLUŞTURULDU!")
    print("=" * 60)
    print()
    print("📁 Konum: dist/BUDUN-Sigorta.exe")
    print()
    print("✅ Bu dosyayı istediğin bilgisayara kopyalayabilirsin")
    print("✅ Cloud bağlantısı otomatik çalışacak")
    print("✅ Tüm veriler senkronize olacak")
    print()
    print("💡 Not: config.py içindeki Supabase bilgileri EXE'ye gömüldü")
    print()
    
except subprocess.CalledProcessError:
    print()
    print("❌ EXE oluşturma hatası!")
    print()
    print("Manuel komut:")
    print(' '.join(cmd))

