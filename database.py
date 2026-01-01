import sqlite3
import os

class Database:
    def __init__(self, db_name="sigorta_acente.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Veritabanına bağlan"""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
    
    def create_tables(self):
        """Gerekli tabloları oluştur"""
        # Satışçılar tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS satiscilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad_soyad TEXT NOT NULL UNIQUE,
                aktif INTEGER DEFAULT 1,
                kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                prim_tutari REAL,
                komisyon_tutari REAL,
                odeme_sekli TEXT DEFAULT 'Nakit',
                aciklama TEXT,
                yenileme_durumu TEXT DEFAULT 'Süreç devam ediyor',
                kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (musteri_id) REFERENCES musteriler (id),
                FOREIGN KEY (satisci_id) REFERENCES satiscilar (id)
            )
        ''')
        
        # Finans kayıtları tablosu (Nakit ödeme borç takibi)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS finans_kayitlari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                police_id INTEGER NOT NULL,
                borc_tutari REAL DEFAULT 0,
                odenen_tutar REAL DEFAULT 0,
                kalan_borc REAL DEFAULT 0,
                guncelleme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (police_id) REFERENCES policeler (id) ON DELETE CASCADE
            )
        ''')
        
        # Varsayılan satışçı ekle
        self.cursor.execute("SELECT COUNT(*) FROM satiscilar")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO satiscilar (ad_soyad) VALUES ('Genel')")
        
        self.connection.commit()
    
    def capraz_satis_onerileri_getir(self, sigorta_turu):
        """Bir sigorta türü için çapraz satış önerilerini getir"""
        # Çapraz satış eşleştirmeleri (sektör standartları)
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
    
    def capraz_satis_policeleri_getir(self):
        """Çapraz satış için tüm poliçeleri müşteri bilgileriyle getir"""
        self.cursor.execute('''
            SELECT 
                p.id,
                p.police_no,
                m.ad_soyad as musteri_adi,
                m.telefon,
                m.tc_no,
                p.sigorta_turu,
                p.sirket,
                p.baslangic_tarihi,
                p.bitis_tarihi,
                p.prim_tutari,
                p.kayit_tarihi
            FROM policeler p
            JOIN musteriler m ON p.musteri_id = m.id
            ORDER BY p.kayit_tarihi DESC
        ''')
        return self.cursor.fetchall()
    
    def musteri_ekle(self, ad_soyad, tc_no, telefon, email, adres):
        """Yeni müşteri ekle"""
        try:
            self.cursor.execute('''
                INSERT INTO musteriler (ad_soyad, tc_no, telefon, email, adres)
                VALUES (?, ?, ?, ?, ?)
            ''', (ad_soyad, tc_no, telefon, email, adres))
            self.connection.commit()
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
            return True, "Poliçe başarıyla eklendi"
        except sqlite3.IntegrityError:
            return False, "Bu poliçe numarası zaten kayıtlı!"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def musterileri_getir(self):
        """Tüm müşterileri getir"""
        self.cursor.execute('SELECT id, ad_soyad, tc_no FROM musteriler ORDER BY ad_soyad')
        return self.cursor.fetchall()
    
    def satiscilari_getir(self):
        """Aktif satışçıları getir"""
        self.cursor.execute('SELECT id, ad_soyad FROM satiscilar WHERE aktif = 1 ORDER BY ad_soyad')
        return self.cursor.fetchall()
    
    def satisci_ekle(self, ad_soyad):
        """Yeni satışçı ekle"""
        try:
            self.cursor.execute('INSERT INTO satiscilar (ad_soyad) VALUES (?)', (ad_soyad,))
            self.connection.commit()
            return True, "Satışçı başarıyla eklendi"
        except sqlite3.IntegrityError:
            return False, "Bu satışçı zaten kayıtlı!"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def police_guncelle(self, police_id, police_no, sigorta_turu, sirket,
                        baslangic_tarihi, bitis_tarihi, prim_tutari, 
                        komisyon_tutari, aciklama, satisci_id=None):
        """Poliçe bilgilerini güncelle"""
        try:
            self.cursor.execute('''
                UPDATE policeler 
                SET police_no = ?, sigorta_turu = ?, sirket = ?,
                    baslangic_tarihi = ?, bitis_tarihi = ?,
                    prim_tutari = ?, komisyon_tutari = ?, aciklama = ?,
                    satisci_id = ?
                WHERE id = ?
            ''', (police_no, sigorta_turu, sirket, baslangic_tarihi, 
                  bitis_tarihi, prim_tutari, komisyon_tutari, aciklama, 
                  satisci_id, police_id))
            self.connection.commit()
            return True, "Poliçe başarıyla güncellendi"
        except sqlite3.IntegrityError:
            return False, "Bu poliçe numarası başka bir kayıtta kullanılıyor!"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def police_sil(self, police_id):
        """Poliçe sil"""
        try:
            self.cursor.execute('DELETE FROM policeler WHERE id = ?', (police_id,))
            self.connection.commit()
            return True, "Poliçe başarıyla silindi"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def police_detay_getir(self, police_no):
        """Poliçe detaylarını getir"""
        self.cursor.execute('''
            SELECT p.id, p.police_no, p.sigorta_turu, p.sirket,
                   p.baslangic_tarihi, p.bitis_tarihi, p.prim_tutari,
                   p.komisyon_tutari, p.aciklama, m.ad_soyad, m.tc_no,
                   m.telefon, m.email, p.satisci_id, s.ad_soyad as satisci_adi
            FROM policeler p
            JOIN musteriler m ON p.musteri_id = m.id
            LEFT JOIN satiscilar s ON p.satisci_id = s.id
            WHERE p.police_no = ?
        ''', (police_no,))
        return self.cursor.fetchone()
    
    def yenileme_durumu_guncelle(self, police_no, durum):
        """Poliçenin yenileme durumunu güncelle"""
        try:
            self.cursor.execute('''
                UPDATE policeler 
                SET yenileme_durumu = ?
                WHERE police_no = ?
            ''', (durum, police_no))
            self.connection.commit()
            return True, "Durum güncellendi"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def nakit_policeleri_getir(self):
        """Ödeme şekli 'Nakit' olan poliçeleri getir"""
        self.cursor.execute('''
            SELECT 
                p.id,
                p.police_no,
                m.ad_soyad as musteri_adi,
                m.telefon,
                p.sigorta_turu,
                p.sirket,
                p.prim_tutari,
                f.borc_tutari,
                f.odenen_tutar,
                f.kalan_borc,
                p.kayit_tarihi
            FROM policeler p
            JOIN musteriler m ON p.musteri_id = m.id
            LEFT JOIN finans_kayitlari f ON p.id = f.police_id
            WHERE p.odeme_sekli = 'Nakit'
            ORDER BY p.kayit_tarihi DESC
        ''')
        return self.cursor.fetchall()
    
    def finans_guncelle(self, police_id, odenen_tutar):
        """Finans kaydını güncelle"""
        try:
            # Önce mevcut bilgileri al
            self.cursor.execute('''
                SELECT borc_tutari, odenen_tutar
                FROM finans_kayitlari
                WHERE police_id = ?
            ''', (police_id,))
            
            result = self.cursor.fetchone()
            if result:
                borc_tutari, mevcut_odenen = result
                yeni_odenen = mevcut_odenen + odenen_tutar
                kalan_borc = borc_tutari - yeni_odenen
                
                self.cursor.execute('''
                    UPDATE finans_kayitlari
                    SET odenen_tutar = ?,
                        kalan_borc = ?,
                        guncelleme_tarihi = CURRENT_TIMESTAMP
                    WHERE police_id = ?
                ''', (yeni_odenen, kalan_borc, police_id))
            else:
                # Finans kaydı yoksa oluştur
                self.cursor.execute('''
                    SELECT prim_tutari FROM policeler WHERE id = ?
                ''', (police_id,))
                prim_tutari = self.cursor.fetchone()[0]
                kalan_borc = prim_tutari - odenen_tutar
                
                self.cursor.execute('''
                    INSERT INTO finans_kayitlari (police_id, borc_tutari, odenen_tutar, kalan_borc)
                    VALUES (?, ?, ?, ?)
                ''', (police_id, prim_tutari, odenen_tutar, kalan_borc))
            
            self.connection.commit()
            return True, "Finans kaydı güncellendi"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def finans_detay_getir(self, police_id):
        """Poliçenin finans detaylarını getir"""
        self.cursor.execute('''
            SELECT 
                p.police_no,
                m.ad_soyad as musteri_adi,
                p.sigorta_turu,
                p.sirket,
                p.prim_tutari,
                f.borc_tutari,
                f.odenen_tutar,
                f.kalan_borc
            FROM policeler p
            JOIN musteriler m ON p.musteri_id = m.id
            LEFT JOIN finans_kayitlari f ON p.id = f.police_id
            WHERE p.id = ?
        ''', (police_id,))
        return self.cursor.fetchone()
    
    def close(self):
        """Veritabanı bağlantısını kapat"""
        if self.connection:
            self.connection.close()

