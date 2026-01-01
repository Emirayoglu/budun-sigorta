-- BUDUN Sigorta Yönetim Sistemi - Supabase Tabloları
-- Bu SQL'i Supabase SQL Editor'de çalıştır

-- 1. Satışçılar Tablosu
CREATE TABLE IF NOT EXISTS satiscilar (
    id BIGSERIAL PRIMARY KEY,
    ad_soyad VARCHAR(200) NOT NULL UNIQUE,
    telefon VARCHAR(20),
    email VARCHAR(100),
    komisyon_orani DECIMAL(5,2) DEFAULT 15.00,
    durum VARCHAR(20) DEFAULT 'Aktif',
    kayit_tarihi TIMESTAMP DEFAULT NOW(),
    guncelleme_tarihi TIMESTAMP DEFAULT NOW()
);

-- 2. Müşteriler Tablosu
CREATE TABLE IF NOT EXISTS musteriler (
    id BIGSERIAL PRIMARY KEY,
    ad_soyad VARCHAR(200) NOT NULL,
    tc_no VARCHAR(11) UNIQUE,
    telefon VARCHAR(20),
    email VARCHAR(100),
    adres TEXT,
    kayit_tarihi TIMESTAMP DEFAULT NOW(),
    guncelleme_tarihi TIMESTAMP DEFAULT NOW()
);

-- 3. Poliçeler Tablosu
CREATE TABLE IF NOT EXISTS policeler (
    id BIGSERIAL PRIMARY KEY,
    musteri_id BIGINT NOT NULL REFERENCES musteriler(id) ON DELETE CASCADE,
    satisci_id BIGINT REFERENCES satiscilar(id) ON DELETE SET NULL,
    police_no VARCHAR(100) UNIQUE NOT NULL,
    sigorta_turu VARCHAR(50) NOT NULL,
    sirket VARCHAR(100) NOT NULL,
    baslangic_tarihi DATE NOT NULL,
    bitis_tarihi DATE NOT NULL,
    prim_tutari DECIMAL(12,2) DEFAULT 0,
    komisyon_tutari DECIMAL(12,2) DEFAULT 0,
    odeme_sekli VARCHAR(50) DEFAULT 'Nakit',
    aciklama TEXT,
    yenileme_durumu VARCHAR(50) DEFAULT 'Süreç devam ediyor',
    kayit_tarihi TIMESTAMP DEFAULT NOW(),
    guncelleme_tarihi TIMESTAMP DEFAULT NOW()
);

-- 4. Finans Kayıtları Tablosu
CREATE TABLE IF NOT EXISTS finans_kayitlari (
    id BIGSERIAL PRIMARY KEY,
    police_id BIGINT NOT NULL REFERENCES policeler(id) ON DELETE CASCADE,
    borc_tutari DECIMAL(12,2) DEFAULT 0,
    odenen_tutar DECIMAL(12,2) DEFAULT 0,
    kalan_borc DECIMAL(12,2) DEFAULT 0,
    kayit_tarihi TIMESTAMP DEFAULT NOW(),
    guncelleme_tarihi TIMESTAMP DEFAULT NOW()
);

-- İndeksler (Performans için)
CREATE INDEX IF NOT EXISTS idx_musteri_tc ON musteriler(tc_no);
CREATE INDEX IF NOT EXISTS idx_musteri_ad ON musteriler(ad_soyad);
CREATE INDEX IF NOT EXISTS idx_police_no ON policeler(police_no);
CREATE INDEX IF NOT EXISTS idx_police_musteri ON policeler(musteri_id);
CREATE INDEX IF NOT EXISTS idx_police_bitis ON policeler(bitis_tarihi);
CREATE INDEX IF NOT EXISTS idx_finans_police ON finans_kayitlari(police_id);

-- Varsayılan satışçı
INSERT INTO satiscilar (ad_soyad) VALUES ('Genel') ON CONFLICT DO NOTHING;

-- Başarılı mesajı
SELECT 'Tablolar başarıyla oluşturuldu! ✅' as sonuc;

