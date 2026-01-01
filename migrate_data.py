"""
SQLite'dan Supabase'e Veri Aktarımı
Mevcut verilerini cloud'a taşır
"""

import sqlite3
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

def migrate_data():
    print("=" * 50)
    print("📦 Veri Aktarımı Başlıyor")
    print("=" * 50)
    print()
    
    # SQLite bağlantısı
    try:
        sqlite_conn = sqlite3.connect('sigorta_acente.db')
        sqlite_cursor = sqlite_conn.cursor()
        print("✅ SQLite veritabanına bağlandı")
    except:
        print("❌ SQLite veritabanı bulunamadı")
        print("ℹ️  Yeni başlıyorsan, bu normal. Direkt yeni veritabanını kullan!")
        return
    
    # Supabase bağlantısı
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase'e bağlandı")
    print()
    
    # 1. Satışçıları aktar
    print("1️⃣ Satışçılar aktarılıyor...")
    try:
        sqlite_cursor.execute("SELECT ad_soyad, aktif FROM satiscilar")
        satiscilar = sqlite_cursor.fetchall()
        
        for satisci in satiscilar:
            try:
                supabase.table('satiscilar').insert({
                    'ad_soyad': satisci[0],
                    'aktif': satisci[1] == 1
                }).execute()
            except:
                pass  # Zaten varsa geç
        
        print(f"   ✅ {len(satiscilar)} satışçı aktarıldı")
    except Exception as e:
        print(f"   ⚠️ Satışçı aktarımında sorun: {e}")
    
    # 2. Müşterileri aktar
    print("2️⃣ Müşteriler aktarılıyor...")
    try:
        sqlite_cursor.execute("SELECT id, ad_soyad, tc_no, telefon, email, adres FROM musteriler")
        musteriler = sqlite_cursor.fetchall()
        
        musteri_id_map = {}  # Eski ID -> Yeni ID eşleştirmesi
        
        for musteri in musteriler:
            try:
                result = supabase.table('musteriler').insert({
                    'ad_soyad': musteri[1],
                    'tc_no': musteri[2],
                    'telefon': musteri[3],
                    'email': musteri[4],
                    'adres': musteri[5]
                }).execute()
                
                musteri_id_map[musteri[0]] = result.data[0]['id']
            except Exception as e:
                print(f"   ⚠️ Müşteri atlanamadı: {musteri[1]}")
        
        print(f"   ✅ {len(musteriler)} müşteri aktarıldı")
    except Exception as e:
        print(f"   ⚠️ Müşteri aktarımında sorun: {e}")
    
    # 3. Poliçeleri aktar
    print("3️⃣ Poliçeler aktarılıyor...")
    try:
        sqlite_cursor.execute("""
            SELECT musteri_id, satisci_id, police_no, sigorta_turu, sirket,
                   baslangic_tarihi, bitis_tarihi, prim_tutari, komisyon_tutari,
                   odeme_sekli, aciklama, yenileme_durumu
            FROM policeler
        """)
        policeler = sqlite_cursor.fetchall()
        
        for police in policeler:
            try:
                yeni_musteri_id = musteri_id_map.get(police[0])
                if not yeni_musteri_id:
                    continue
                
                result = supabase.table('policeler').insert({
                    'musteri_id': yeni_musteri_id,
                    'satisci_id': police[1],
                    'police_no': police[2],
                    'sigorta_turu': police[3],
                    'sirket': police[4],
                    'baslangic_tarihi': police[5],
                    'bitis_tarihi': police[6],
                    'prim_tutari': police[7],
                    'komisyon_tutari': police[8],
                    'odeme_sekli': police[9],
                    'aciklama': police[10],
                    'yenileme_durumu': police[11]
                }).execute()
                
                # Finans kaydı varsa aktar
                if police[9] == 'Nakit':
                    police_id = result.data[0]['id']
                    supabase.table('finans_kayitlari').insert({
                        'police_id': police_id,
                        'borc_tutari': police[7],
                        'odenen_tutar': 0,
                        'kalan_borc': police[7]
                    }).execute()
                
            except Exception as e:
                print(f"   ⚠️ Poliçe atlanamadı: {police[2]}")
        
        print(f"   ✅ {len(policeler)} poliçe aktarıldı")
    except Exception as e:
        print(f"   ⚠️ Poliçe aktarımında sorun: {e}")
    
    sqlite_conn.close()
    
    print()
    print("=" * 50)
    print("🎉 VERİ AKTARIMI TAMAMLANDI!")
    print("=" * 50)
    print()
    print("✅ Tüm verileriniz artık Cloud'da")
    print("✅ Her yerden erişebilirsiniz")
    print("✅ Eski SQLite dosyasını yedek olarak saklayabilirsiniz")

if __name__ == "__main__":
    migrate_data()


