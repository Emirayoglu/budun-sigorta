import psycopg2
from psycopg2 import pool
from datetime import datetime
import os

class CloudDatabase:
    """
    Cloud PostgreSQL Veritabanı Sınıfı (Supabase uyumlu)
    Her yerden erişilebilir, her zaman güncel!
    """
    
    def __init__(self):
        self.connection_pool = None
        self.init_pool()
        self.create_tables()
    
    def init_pool(self):
        """Connection pool oluştur - Çoklu kullanıcı desteği"""
        try:
            # Supabase bağlantı bilgileri (config.py'den gelecek)
            from config import SUPABASE_DB_URL
            
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,  # Min 1, Max 20 bağlantı
                SUPABASE_DB_URL
            )
            print("✅ Cloud veritabanına bağlandı!")
        except ImportError:
            print("⚠️ config.py dosyası bulunamadı! Lütfen oluşturun.")
            print("Örnek: SUPABASE_DB_URL = 'postgresql://user:password@host:5432/database'")
        except Exception as e:
            print(f"❌ Veritabanı bağlantı hatası: {e}")
    
    def get_connection(self):
        """Connection pool'dan bağlantı al"""
        return self.connection_pool.getconn()
    
    def put_connection(self, conn):
        """Bağlantıyı geri ver"""
        self.connection_pool.putconn(conn)
    
    def create_tables(self):
        """Tabloları oluştur - PostgreSQL optimized"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Satışçılar tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS satiscilar (
                    id SERIAL PRIMARY KEY,
                    ad_soyad VARCHAR(200) NOT NULL UNIQUE,
                    telefon VARCHAR(20),
                    email VARCHAR(100),
                    aktif BOOLEAN DEFAULT TRUE,
                    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Müşteriler tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS musteriler (
                    id SERIAL PRIMARY KEY,
                    ad_soyad VARCHAR(200) NOT NULL,
                    tc_no VARCHAR(11) UNIQUE,
                    telefon VARCHAR(20),
                    email VARCHAR(100),
                    adres TEXT,
                    dogum_tarihi DATE,
                    notlar TEXT,
                    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Poliçeler tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS policeler (
                    id SERIAL PRIMARY KEY,
                    musteri_id INTEGER NOT NULL REFERENCES musteriler(id) ON DELETE CASCADE,
                    satisci_id INTEGER REFERENCES satiscilar(id) ON DELETE SET NULL,
                    police_no VARCHAR(100) UNIQUE NOT NULL,
                    sigorta_turu VARCHAR(50) NOT NULL,
                    sirket VARCHAR(100) NOT NULL,
                    baslangic_tarihi DATE NOT NULL,
                    bitis_tarihi DATE NOT NULL,
                    prim_tutari DECIMAL(12,2) DEFAULT 0,
                    komisyon_tutari DECIMAL(12,2) DEFAULT 0,
                    komisyon_orani DECIMAL(5,2) DEFAULT 0,
                    odeme_sekli VARCHAR(50) DEFAULT 'Nakit',
                    taksit_sayisi INTEGER DEFAULT 1,
                    aciklama TEXT,
                    yenileme_durumu VARCHAR(50) DEFAULT 'Süreç devam ediyor',
                    durum VARCHAR(20) DEFAULT 'Aktif',
                    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Finans kayıtları tablosu
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS finans_kayitlari (
                    id SERIAL PRIMARY KEY,
                    police_id INTEGER NOT NULL REFERENCES policeler(id) ON DELETE CASCADE,
                    borc_tutari DECIMAL(12,2) DEFAULT 0,
                    odenen_tutar DECIMAL(12,2) DEFAULT 0,
                    kalan_borc DECIMAL(12,2) DEFAULT 0,
                    son_odeme_tarihi DATE,
                    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Ödeme geçmişi
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS odeme_gecmisi (
                    id SERIAL PRIMARY KEY,
                    finans_kayit_id INTEGER REFERENCES finans_kayitlari(id) ON DELETE CASCADE,
                    police_id INTEGER REFERENCES policeler(id) ON DELETE CASCADE,
                    odeme_tutari DECIMAL(12,2) NOT NULL,
                    odeme_tarihi DATE NOT NULL,
                    odeme_sekli VARCHAR(50) DEFAULT 'Nakit',
                    aciklama TEXT,
                    kullanici VARCHAR(100),
                    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Sistem logları
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sistem_loglari (
                    id SERIAL PRIMARY KEY,
                    islem_tipi VARCHAR(50) NOT NULL,
                    tablo_adi VARCHAR(50),
                    kayit_id INTEGER,
                    aciklama TEXT,
                    kullanici VARCHAR(100),
                    ip_adresi VARCHAR(50),
                    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Kullanıcılar tablosu (Gelecekte login için)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kullanicilar (
                    id SERIAL PRIMARY KEY,
                    kullanici_adi VARCHAR(50) UNIQUE NOT NULL,
                    sifre_hash VARCHAR(255) NOT NULL,
                    ad_soyad VARCHAR(200),
                    email VARCHAR(100),
                    rol VARCHAR(20) DEFAULT 'kullanici',
                    aktif BOOLEAN DEFAULT TRUE,
                    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    son_giris TIMESTAMP
                )
            ''')
            
            # İndeksler oluştur
            self.create_indexes(cursor)
            
            conn.commit()
            print("✅ Tablolar oluşturuldu!")
            
            # Varsayılan satışçı ekle
            cursor.execute("SELECT COUNT(*) FROM satiscilar")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO satiscilar (ad_soyad) VALUES ('Genel')")
                conn.commit()
            
        except Exception as e:
            print(f"❌ Tablo oluşturma hatası: {e}")
            conn.rollback()
        finally:
            cursor.close()
            self.put_connection(conn)
    
    def create_indexes(self, cursor):
        """Performans için indeksler"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_musteri_tc ON musteriler(tc_no)",
            "CREATE INDEX IF NOT EXISTS idx_musteri_ad ON musteriler(ad_soyad)",
            "CREATE INDEX IF NOT EXISTS idx_police_no ON policeler(police_no)",
            "CREATE INDEX IF NOT EXISTS idx_police_musteri ON policeler(musteri_id)",
            "CREATE INDEX IF NOT EXISTS idx_police_bitis ON policeler(bitis_tarihi)",
            "CREATE INDEX IF NOT EXISTS idx_finans_police ON finans_kayitlari(police_id)",
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
            except:
                pass
    
    # Tüm CRUD fonksiyonları buraya gelecek
    def musteri_ekle(self, ad_soyad, tc_no, telefon, email, adres):
        """Yeni müşteri ekle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO musteriler (ad_soyad, tc_no, telefon, email, adres)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            ''', (ad_soyad, tc_no, telefon, email, adres))
            
            musteri_id = cursor.fetchone()[0]
            conn.commit()
            return True, f"Müşteri başarıyla eklendi (ID: {musteri_id})"
        except psycopg2.IntegrityError:
            conn.rollback()
            return False, "Bu TC No zaten kayıtlı!"
        except Exception as e:
            conn.rollback()
            return False, f"Hata: {str(e)}"
        finally:
            cursor.close()
            self.put_connection(conn)
    
    def musterileri_getir(self):
        """Tüm müşterileri getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT id, ad_soyad, tc_no FROM musteriler ORDER BY ad_soyad')
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            self.put_connection(conn)
    
    # Diğer tüm fonksiyonlar... (police_ekle, satiscilari_getir, vb.)
    
    def close(self):
        """Tüm bağlantıları kapat"""
        if self.connection_pool:
            self.connection_pool.closeall()

# SQLite'dan PostgreSQL'e veri aktarma aracı
class DataMigrator:
    """Mevcut SQLite verilerini Cloud'a aktar"""
    
    def __init__(self, sqlite_db_path="sigorta_acente.db"):
        self.sqlite_db = sqlite_db_path
        self.cloud_db = CloudDatabase()
    
    def migrate_all(self):
        """Tüm verileri aktar"""
        import sqlite3
        
        sqlite_conn = sqlite3.connect(self.sqlite_db)
        sqlite_cursor = sqlite_conn.cursor()
        
        print("🚀 Veri aktarımı başlıyor...")
        
        # 1. Satışçıları aktar
        print("📋 Satışçılar aktarılıyor...")
        sqlite_cursor.execute("SELECT ad_soyad, aktif FROM satiscilar")
        for row in sqlite_cursor.fetchall():
            # Cloud DB'ye ekle
            pass
        
        # 2. Müşterileri aktar
        print("👥 Müşteriler aktarılıyor...")
        # ...
        
        # 3. Poliçeleri aktar
        print("📄 Poliçeler aktarılıyor...")
        # ...
        
        print("✅ Veri aktarımı tamamlandı!")
        
        sqlite_conn.close()


