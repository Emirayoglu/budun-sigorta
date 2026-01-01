"""
Cloud Veritabanı Bağlantı Testi
Supabase bağlantısını test eder
"""

from database_cloud import CloudDatabase

def test_connection():
    print("=" * 50)
    print("🧪 BUDUN - Cloud Veritabanı Bağlantı Testi")
    print("=" * 50)
    print()
    
    try:
        # Veritabanına bağlan
        print("1️⃣ Veritabanına bağlanılıyor...")
        db = CloudDatabase()
        print("   ✅ Bağlantı başarılı!")
        print()
        
        # Tabloları kontrol et
        print("2️⃣ Tablolar kontrol ediliyor...")
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        print(f"   ✅ {len(tables)} tablo bulundu:")
        for table in tables:
            print(f"      - {table[0]}")
        print()
        
        # Test verisi ekle
        print("3️⃣ Test müşterisi ekleniyor...")
        success, message = db.musteri_ekle(
            ad_soyad="Test Müşteri",
            tc_no="12345678901",
            telefon="5551234567",
            email="test@test.com",
            adres="Test Adres"
        )
        
        if success:
            print(f"   ✅ {message}")
        else:
            print(f"   ℹ️  {message}")
        print()
        
        # Müşterileri listele
        print("4️⃣ Müşteriler listeleniyor...")
        musteriler = db.musterileri_getir()
        print(f"   ✅ Toplam {len(musteriler)} müşteri bulundu")
        if musteriler:
            for musteri in musteriler[:3]:  # İlk 3'ünü göster
                print(f"      - {musteri[1]} (TC: {musteri[2]})")
        print()
        
        cursor.close()
        db.put_connection(conn)
        
        # Başarılı
        print("=" * 50)
        print("🎉 TÜM TESTLER BAŞARILI!")
        print("=" * 50)
        print()
        print("✅ Cloud veritabanı hazır!")
        print("✅ Her yerden erişebilirsiniz")
        print("✅ Telefondan da kullanabilirsiniz")
        print()
        print("📱 Sonraki adım: Web arayüzü")
        print("   Komut: python web_app.py")
        print()
        
        db.close()
        return True
        
    except Exception as e:
        print()
        print("=" * 50)
        print("❌ HATA OLUŞTU!")
        print("=" * 50)
        print()
        print(f"Hata: {str(e)}")
        print()
        print("💡 Çözüm önerileri:")
        print("1. config.py dosyasını kontrol edin")
        print("2. Supabase connection string doğru mu?")
        print("3. Internet bağlantınız aktif mi?")
        print("4. psycopg2 kurulu mu? (pip install psycopg2-binary)")
        print()
        return False

if __name__ == "__main__":
    test_connection()


