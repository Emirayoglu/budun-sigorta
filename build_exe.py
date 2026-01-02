# BUDUN Sigorta Yönetim Sistemi - EXE Oluşturma Script
# PyInstaller ile tek dosya EXE

import subprocess
import sys
import os

print("=" * 60)
print("BUDUN - EXE Olusturma Basliyor")
print("=" * 60)
print()

# 1. PyInstaller'ı yükle
print("1. PyInstaller yukleniyor...")
subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
print("   OK PyInstaller yuklendi!")
print()

# 2. EXE oluştur
print("2. EXE dosyasi olusturuluyor...")
print("   Bu birkac dakika surebilir...")
print()

# PyInstaller komutu (İkonsuz)
cmd = [
    "pyinstaller",
    "--name=BUDUN-Sigorta",
    "--onefile",  # Tek dosya
    "--windowed",  # Console penceresi gösterme
    "--add-data=config.py;.",  # Config dosyasını dahil et
    "--hidden-import=requests",
    "--hidden-import=database_supabase",
    "main.py"
]

try:
    subprocess.run(cmd, check=True)
    print()
    print("=" * 60)
    print("EXE BASARIYLA OLUSTURULDU!")
    print("=" * 60)
    print()
    print("Konum: dist/BUDUN-Sigorta.exe")
    print()
    print("OK Bu dosyayi istedigin bilgisayara kopyalayabilirsin")
    print("OK Cloud baglantisi otomatik calisacak")
    print("OK Tum veriler senkronize olacak")
    print()
    print("Not: config.py icindeki Supabase bilgileri EXE'ye gomuldu")
    print()
    
except subprocess.CalledProcessError:
    print()
    print("EXE olusturma hatasi!")
    print()
    print("Manuel komut:")
    print(' '.join(cmd))


