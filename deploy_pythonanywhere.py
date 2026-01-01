"""
PythonAnywhere Deploy Script
En kolay cloud deployment yöntemi
"""

import os
import zipfile

print("=" * 60)
print("📦 PythonAnywhere İçin Paket Hazırlanıyor")
print("=" * 60)
print()

# Dosyaları listele
files_to_include = [
    'web_app.py',
    'database_supabase.py',
    'config.py',
    'requirements.txt',
    'templates/index.html'
]

print("1️⃣ Dosyalar kontrol ediliyor...")
for f in files_to_include:
    if os.path.exists(f):
        print(f"   ✅ {f}")
    else:
        print(f"   ❌ {f} bulunamadı!")

print()
print("2️⃣ ZIP dosyası oluşturuluyor...")

# ZIP oluştur
with zipfile.ZipFile('budun-pythonanywhere.zip', 'w') as zipf:
    for file in files_to_include:
        if os.path.exists(file):
            zipf.write(file)

print("   ✅ budun-pythonanywhere.zip hazır!")
print()

print("=" * 60)
print("🎉 PAKET HAZIR!")
print("=" * 60)
print()
print("📁 Dosya: budun-pythonanywhere.zip")
print()
print("Şimdi ne yapmalısın:")
print()
print("1️⃣ https://www.pythonanywhere.com adresine git")
print("   - Sign Up (Ücretsiz hesap)")
print()
print("2️⃣ Dashboard > Files")
print("   - Upload: budun-pythonanywhere.zip")
print("   - Unzip")
print()
print("3️⃣ Dashboard > Web")
print("   - Add a new web app")
print("   - Python 3.10")
print("   - Manual configuration")
print()
print("4️⃣ WSGI configuration:")
print("   - Edit /var/www/KULLANICI_wsgi.py")
print("   - İçeriği şununla değiştir:")
print()
print("   import sys")
print("   path = '/home/KULLANICI'")
print("   if path not in sys.path:")
print("       sys.path.append(path)")
print("   from web_app import app as application")
print()
print("5️⃣ Reload web app")
print()
print("6️⃣ Link:")
print("   https://KULLANICI.pythonanywhere.com")
print()
print("✅ 7/24 çalışır!")
print("✅ PC kapalı olsa bile!")
print("✅ Her yerden erişim!")
print()


