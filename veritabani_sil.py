import os

# Veritabanı dosyası
db_file = "sigorta_acente.db"

if os.path.exists(db_file):
    os.remove(db_file)
    print("✅ Veritabanı silindi!")
else:
    print("ℹ️  Veritabanı zaten yok.")

print("\n🚀 Şimdi programı çalıştırın:")
print("   python main.py")
input("\nDevam etmek için Enter'a basın...")

