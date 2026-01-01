# Sigorta Acente Yönetim Sistemi

## Kurulum

### 1. Python Kurulumu
Python 3.8 veya üzeri sürüm gereklidir.
- [Python'u buradan indirin](https://www.python.org/downloads/)

### 2. Gerekli Kütüphaneleri Kurun

```bash
pip install -r requirements.txt
```

### 3. Programı Çalıştırın

```bash
python main.py
```

## Mevcut Özellikler (v0.1)

✅ Müşteri bilgileri girişi
✅ Poliçe bilgileri girişi
✅ Veritabanına kaydetme
✅ Modern ve kullanıcı dostu arayüz

## Yapılacaklar

- [ ] Poliçe listeleme ve görüntüleme
- [ ] Yenileme hatırlatmaları
- [ ] Raporlama ve filtreleme
- [ ] Finans takibi
- [ ] Excel/PDF export

## Veritabanı Yapısı

Program SQLite veritabanı kullanır. `sigorta_acente.db` dosyası otomatik oluşturulur.

### Tablolar:
- **musteriler**: Müşteri bilgileri
- **policeler**: Poliçe kayıtları

## Notlar

- TC No alanı benzersiz olmalıdır
- Poliçe numarası benzersiz olmalıdır
- Tarih formatı: GG.AA.YYYY

