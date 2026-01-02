# 📱 BUDUN Sigorta Yönetim Sistemi

Modern, kullanıcı dostu masaüstü sigorta yönetim uygulaması.

## ✨ Özellikler

### 👥 Müşteri Yönetimi
- ➕ Yeni müşteri ekleme
- 📝 Müşteri bilgilerini düzenleme
- 🔍 Müşteri arama ve filtreleme
- 📋 TC No, telefon, email, adres takibi

### 📋 Poliçe Yönetimi
- ➕ Yeni poliçe kaydı
- ✏️ Poliçe güncelleme
- 🗑️ Poliçe silme
- 🔍 Poliçe arama (müşteri, poliçe no, şirket)
- 📊 Tüm poliçe türleri: Kasko, Trafik, Konut, İşyeri, Sağlık, Hayat, Dask, Seyahat, Ferdi Kaza

### 🔄 Yenileme Takibi
- 📅 Bitiş tarihine göre otomatik yenileme listesi
- 🔴🟡🟢 Aciliyet durumları (30/60/120 gün)
- 📊 Takip durumu: Beklemede, Arandı, Teklif Verildi, Yenilendi, İptal
- 🎨 Renkli görsel göstergeler

### 💰 Finans / Borç Takibi
- 💵 Nakit poliçe takibi
- 📊 Ödenen / Kalan tutar hesaplama
- 📅 Ödeme tarihi takibi
- 🔴 Borçlu poliçe uyarıları

### 📊 Raporlama
- 📅 Tarih aralığına göre raporlar
- 👤 Satışçı bazlı raporlar
- 🏷️ Sigorta türüne göre filtreleme
- 💰 Toplam prim ve komisyon hesaplama
- 📈 Excel'e aktarma

### 🎯 Çapraz Satış
- 📋 Müşterinin mevcut poliçelerini görüntüleme
- ✅ Satış fırsatlarını belirleme
- 💡 Eksik sigorta türlerini önerme

### 👤 Satışçı Yönetimi
- ➕ Satışçı ekleme/düzenleme
- 💼 Komisyon oranı takibi
- 📊 Satışçı bazlı performans raporları

## 🚀 Kurulum ve Kullanım

### 📥 EXE Dosyasını Çalıştırma

1. **İndirme:**
   - `dist/BUDUN-Sigorta.exe` dosyasını istediğiniz konuma kopyalayın

2. **Çalıştırma:**
   - EXE dosyasına çift tıklayın
   - Program otomatik olarak açılacak
   - İlk çalıştırmada cloud veritabanına bağlanacak

3. **Cloud Veritabanı:**
   - ✅ Tüm veriler Supabase cloud'da saklanır
   - ✅ Her yerden aynı verilere erişim
   - ✅ Otomatik yedekleme
   - ✅ Çoklu cihaz senkronizasyonu

### 🛠️ Geliştirme (Python Kaynak Kodundan)

**Gereksinimler:**
```bash
Python 3.13+
PySide6
requests
```

**Kurulum:**
```bash
pip install PySide6 requests
```

**Çalıştırma:**
```bash
python main.py
```

**EXE Oluşturma:**
```bash
python build_exe.py
```

## 📁 Proje Yapısı

```
BUDUNv2/
├── main.py                     # Ana uygulama
├── database_supabase.py        # Cloud veritabanı işlemleri
├── config.py                   # Supabase bağlantı ayarları
├── build_exe.py                # EXE oluşturma script'i
├── dist/
│   └── BUDUN-Sigorta.exe      # Çalıştırılabilir dosya
└── README.md                   # Bu dosya
```

## 🔐 Güvenlik

- 🔒 Cloud veritabanı SSL ile şifrelenir
- 🔑 API anahtarları güvenli şekilde saklanır
- 👤 Kullanıcı verilerinin gizliliği korunur

## 🎨 Arayüz

- 🌈 Modern gradient tasarım
- 📱 Kullanıcı dostu menüler
- 🎯 Kolay navigasyon
- 📊 Görsel göstergeler ve renkli durumlar
- ⚡ Hızlı arama ve filtreleme

## 💾 Veritabanı

- ☁️ **Supabase PostgreSQL** - Cloud veritabanı
- 🔄 Otomatik senkronizasyon
- 📊 İlişkisel veri yapısı
- 🔍 Gelişmiş sorgulama özellikleri

## 📞 Destek

Sorun bildirmek veya öneride bulunmak için GitHub Issues kullanabilirsiniz.

## 📝 Lisans

Bu proje özel kullanım içindir.

---

**Geliştirici:** BUDUN Sigorta Ekibi
**Versiyon:** 2.0
**Son Güncelleme:** 2026
