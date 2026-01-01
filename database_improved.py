import sqlite3
import os
from datetime import datetime
import json

class DatabaseImproved:
    def __init__(self, db_name="sigorta_acente.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.create_indexes()
    
    def connect(self):
        """Veritabanına bağlan - WAL mode ile performans artışı"""
        self.connection = sqlite3.connect(
            self.db_name,
            check_same_thread=False  # Çoklu kullanıcı için
        )
        # WAL mode - daha hızlı ve concurrent erişim
        self.connection.execute('PRAGMA journal_mode=WAL')
        # Foreign key kontrolünü etkinleştir
        self.connection.execute('PRAGMA foreign_keys=ON')
        self.cursor = self.connection.cursor()
    
    def create_tables(self):
        """Gerekli tabloları oluştur - İyileştirilmiş versiyon"""
        
        # Satışçılar tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS satiscilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad_soyad TEXT NOT NULL UNIQUE,
                telefon TEXT,
                email TEXT,
                aktif INTEGER DEFAULT 1,
                kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Müşteriler tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS musteriler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad_soyad TEXT NOT NULL,
                tc_no TEXT UNIQUE,
                telefon TEXT,
                email TEXT,
                adres TEXT,
                dogum_tarihi DATE,
                notlar TEXT,
                kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Poliçeler tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS policeler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                musteri_id INTEGER NOT NULL,
                satisci_id INTEGER,
                police_no TEXT UNIQUE NOT NULL,
                sigorta_turu TEXT NOT NULL,
                sirket TEXT NOT NULL,
                baslangic_tarihi DATE NOT NULL,
                bitis_tarihi DATE NOT NULL,
                prim_tutari REAL DEFAULT 0,
                komisyon_tutari REAL DEFAULT 0,
                komisyon_orani REAL DEFAULT 0,
                odeme_sekli TEXT DEFAULT 'Nakit',
                taksit_sayisi INTEGER DEFAULT 1,
                aciklama TEXT,
                yenileme_durumu TEXT DEFAULT 'Süreç devam ediyor',
                durum TEXT DEFAULT 'Aktif',
                kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (musteri_id) REFERENCES musteriler (id) ON DELETE CASCADE,
                FOREIGN KEY (satisci_id) REFERENCES satiscilar (id) ON DELETE SET NULL
            )
        ''')
        
        # Finans kayıtları tablosu (İyileştirilmiş)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS finans_kayitlari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                police_id INTEGER NOT NULL,
                borc_tutari REAL DEFAULT 0,
                odenen_tutar REAL DEFAULT 0,
                kalan_borc REAL DEFAULT 0,
                son_odeme_tarihi DATE,
                kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (police_id) REFERENCES policeler (id) ON DELETE CASCADE
            )
        ''')
        
        # YENİ: Ödeme geçmişi tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS odeme_gecmisi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                finans_kayit_id INTEGER NOT NULL,
                police_id INTEGER NOT NULL,
                odeme_tutari REAL NOT NULL,
                odeme_tarihi DATE NOT NULL,
                odeme_sekli TEXT DEFAULT 'Nakit',
                aciklama TEXT,
                kullanici TEXT,
                kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (finans_kayit_id) REFERENCES finans_kayitlari (id) ON DELETE CASCADE,
                FOREIGN KEY (police_id) REFERENCES policeler (id) ON DELETE CASCADE
            )
        ''')
        
        # YENİ: Sistem logları
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sistem_loglari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                islem_tipi TEXT NOT NULL,
                tablo_adi TEXT,
                kayit_id INTEGER,
                aciklama TEXT,
                kullanici TEXT,
                kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # YENİ: Ayarlar tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ayarlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                anahtar TEXT UNIQUE NOT NULL,
                deger TEXT,
                aciklama TEXT,
                guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Varsayılan satışçı ekle
        self.cursor.execute("SELECT COUNT(*) FROM satiscilar")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO satiscilar (ad_soyad) VALUES ('Genel')")
        
        self.connection.commit()
    
    def create_indexes(self):
        """Performans için indeksler oluştur"""
        indexes = [
            # Müşteriler
            "CREATE INDEX IF NOT EXISTS idx_musteri_tc ON musteriler(tc_no)",
            "CREATE INDEX IF NOT EXISTS idx_musteri_ad ON musteriler(ad_soyad)",
            "CREATE INDEX IF NOT EXISTS idx_musteri_telefon ON musteriler(telefon)",
            
            # Poliçeler
            "CREATE INDEX IF NOT EXISTS idx_police_no ON policeler(police_no)",
            "CREATE INDEX IF NOT EXISTS idx_police_musteri ON policeler(musteri_id)",
            "CREATE INDEX IF NOT EXISTS idx_police_satisci ON policeler(satisci_id)",
            "CREATE INDEX IF NOT EXISTS idx_police_bitis ON policeler(bitis_tarihi)",
            "CREATE INDEX IF NOT EXISTS idx_police_tur ON policeler(sigorta_turu)",
            "CREATE INDEX IF NOT EXISTS idx_police_sirket ON policeler(sirket)",
            
            # Finans
            "CREATE INDEX IF NOT EXISTS idx_finans_police ON finans_kayitlari(police_id)",
            
            # Ödeme geçmişi
            "CREATE INDEX IF NOT EXISTS idx_odeme_finans ON odeme_gecmisi(finans_kayit_id)",
            "CREATE INDEX IF NOT EXISTS idx_odeme_police ON odeme_gecmisi(police_id)",
            "CREATE INDEX IF NOT EXISTS idx_odeme_tarih ON odeme_gecmisi(odeme_tarihi)",
            
            # Loglar
            "CREATE INDEX IF NOT EXISTS idx_log_tarih ON sistem_loglari(kayit_tarihi)",
            "CREATE INDEX IF NOT EXISTS idx_log_tablo ON sistem_loglari(tablo_adi)",
        ]
        
        for index_sql in indexes:
            try:
                self.cursor.execute(index_sql)
            except sqlite3.OperationalError:
                pass  # İndeks zaten varsa devam et
        
        self.connection.commit()
    
    def log_ekle(self, islem_tipi, tablo_adi=None, kayit_id=None, aciklama=None, kullanici="Sistem"):
        """İşlem logu ekle"""
        try:
            self.cursor.execute('''
                INSERT INTO sistem_loglari (islem_tipi, tablo_adi, kayit_id, aciklama, kullanici)
                VALUES (?, ?, ?, ?, ?)
            ''', (islem_tipi, tablo_adi, kayit_id, aciklama, kullanici))
            self.connection.commit()
        except Exception as e:
            print(f"Log ekleme hatası: {e}")
    
    def backup_olustur(self, backup_klasoru="backups"):
        """Veritabanı yedeği oluştur"""
        try:
            if not os.path.exists(backup_klasoru):
                os.makedirs(backup_klasoru)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dosya = os.path.join(backup_klasoru, f"backup_{timestamp}.db")
            
            # Backup al
            backup_conn = sqlite3.connect(backup_dosya)
            self.connection.backup(backup_conn)
            backup_conn.close()
            
            self.log_ekle("BACKUP", aciklama=f"Yedek oluşturuldu: {backup_dosya}")
            return True, f"Yedek başarıyla oluşturuldu: {backup_dosya}"
        except Exception as e:
            return False, f"Yedek oluşturma hatası: {str(e)}"
    
    def istatistikler_getir(self):
        """Genel istatistikler"""
        stats = {}
        
        # Toplam kayıtlar
        self.cursor.execute("SELECT COUNT(*) FROM musteriler")
        stats['toplam_musteri'] = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM policeler")
        stats['toplam_police'] = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM policeler WHERE durum = 'Aktif'")
        stats['aktif_police'] = self.cursor.fetchone()[0]
        
        # Toplam primler
        self.cursor.execute("SELECT SUM(prim_tutari) FROM policeler")
        stats['toplam_prim'] = self.cursor.fetchone()[0] or 0
        
        self.cursor.execute("SELECT SUM(komisyon_tutari) FROM policeler")
        stats['toplam_komisyon'] = self.cursor.fetchone()[0] or 0
        
        # Finans durumu
        self.cursor.execute("SELECT SUM(kalan_borc) FROM finans_kayitlari")
        stats['toplam_alacak'] = self.cursor.fetchone()[0] or 0
        
        return stats
    
    # Eski fonksiyonları koru (geriye uyumluluk için)
    def capraz_satis_onerileri_getir(self, sigorta_turu):
        """Bir sigorta türü için çapraz satış önerilerini getir"""
        capraz_satis = {
            "Trafik": ["Kasko", "Ferdi Kaza"],
            "Kasko": ["Trafik", "Ferdi Kaza", "Seyahat"],
            "Konut": ["Dask", "Ferdi Kaza", "Hayat"],
            "İşyeri": ["Dask", "Ferdi Kaza", "Hayat", "Sağlık"],
            "Sağlık": ["Hayat", "Ferdi Kaza"],
            "Hayat": ["Sağlık", "Ferdi Kaza"],
            "Dask": ["Konut", "Ferdi Kaza"],
            "Seyahat": ["Trafik", "Ferdi Kaza"],
            "Ferdi Kaza": ["Kasko", "Trafik", "Konut", "İşyeri", "Sağlık", "Hayat", "Dask", "Seyahat"]
        }
        return capraz_satis.get(sigorta_turu, [])
    
    def musteri_ekle(self, ad_soyad, tc_no, telefon, email, adres):
        """Yeni müşteri ekle"""
        try:
            self.cursor.execute('''
                INSERT INTO musteriler (ad_soyad, tc_no, telefon, email, adres)
                VALUES (?, ?, ?, ?, ?)
            ''', (ad_soyad, tc_no, telefon, email, adres))
            self.connection.commit()
            self.log_ekle("EKLE", "musteriler", self.cursor.lastrowid, f"Yeni müşteri: {ad_soyad}")
            return True, "Müşteri başarıyla eklendi"
        except sqlite3.IntegrityError:
            return False, "Bu TC No zaten kayıtlı!"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def police_ekle(self, musteri_id, police_no, sigorta_turu, sirket, 
                    baslangic_tarihi, bitis_tarihi, prim_tutari, 
                    komisyon_tutari, aciklama, satisci_id=None, odeme_sekli='Nakit'):
        """Yeni poliçe ekle"""
        try:
            self.cursor.execute('''
                INSERT INTO policeler (musteri_id, satisci_id, police_no, sigorta_turu, 
                                      sirket, baslangic_tarihi, bitis_tarihi,
                                      prim_tutari, komisyon_tutari, odeme_sekli, aciklama)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (musteri_id, satisci_id, police_no, sigorta_turu, sirket, 
                  baslangic_tarihi, bitis_tarihi, prim_tutari, 
                  komisyon_tutari, odeme_sekli, aciklama))
            
            police_id = self.cursor.lastrowid
            
            # Eğer ödeme şekli Nakit ise, finans kaydı oluştur
            if odeme_sekli == 'Nakit':
                self.cursor.execute('''
                    INSERT INTO finans_kayitlari (police_id, borc_tutari, odenen_tutar, kalan_borc)
                    VALUES (?, ?, 0, ?)
                ''', (police_id, prim_tutari, prim_tutari))
            
            self.connection.commit()
            self.log_ekle("EKLE", "policeler", police_id, f"Yeni poliçe: {police_no}")
            return True, "Poliçe başarıyla eklendi"
        except sqlite3.IntegrityError:
            return False, "Bu poliçe numarası zaten kayıtlı!"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    # Diğer tüm fonksiyonlar aynı şekilde devam eder...
    # (Tüm eski Database class fonksiyonlarını buraya kopyalayın)
    
    def close(self):
        """Veritabanı bağlantısını kapat"""
        if self.connection:
            self.connection.close()


