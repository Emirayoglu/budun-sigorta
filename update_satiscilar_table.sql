-- Supabase satiscilar tablosunu güncelle
-- Bu SQL'i Supabase SQL Editor'de çalıştır

-- Önce mevcut tabloyu sil (VERİLER SİLİNECEK!)
DROP TABLE IF EXISTS satiscilar CASCADE;

-- Yeni tabloyu oluştur
CREATE TABLE satiscilar (
    id BIGSERIAL PRIMARY KEY,
    ad_soyad VARCHAR(200) NOT NULL UNIQUE,
    telefon VARCHAR(20),
    email VARCHAR(100),
    komisyon_orani DECIMAL(5,2) DEFAULT 15.00,
    durum VARCHAR(20) DEFAULT 'Aktif',
    kayit_tarihi TIMESTAMP DEFAULT NOW(),
    guncelleme_tarihi TIMESTAMP DEFAULT NOW()
);

-- Varsayılan satışçı ekle
INSERT INTO satiscilar (ad_soyad, telefon, durum, komisyon_orani) 
VALUES ('Varsayılan Satışçı', '05551234567', 'Aktif', 15.00);

-- Başarılı mesajı
SELECT 'Satiscilar tablosu guncellendi!' as sonuc;



