# BUDUN Sigorta Yönetim Sistemi - Cloud Kurulum Rehberi

## 🚀 Hızlı Başlangıç (15 Dakika)

### Adım 1: Supabase Hesabı Oluştur (2 dk)

1. https://supabase.com adresine git
2. "Start your project" butonuna tık
3. GitHub ile giriş yap (veya email)
4. ✅ Ücretsiz!

### Adım 2: Yeni Proje Oluştur (3 dk)

1. "New Project" butonuna tık
2. Bilgileri doldur:
   - **Name**: BUDUN-Sigorta
   - **Database Password**: Güçlü bir şifre belirle (kaydet!)
   - **Region**: Europe (Frankfurt) - En yakın
3. "Create new project" tıkla
4. ⏳ 2-3 dakika bekle (proje hazırlanıyor)

### Adım 3: Bağlantı Bilgilerini Al (1 dk)

1. Sol menüden **Settings** (⚙️) tıkla
2. **Database** sekmesine git
3. "Connection string" bölümünde **URI** seçeneğini bul
4. 📋 Kopyala butonu ile kopyala

Örnek görünüm:
```
postgresql://postgres:YOUR-PASSWORD@db.abcdefgh.supabase.co:5432/postgres
```

### Adım 4: Config Dosyasını Düzenle (2 dk)

1. `config.py` dosyasını aç
2. Kopyaladığın connection string'i yapıştır:

```python
SUPABASE_DB_URL = "postgresql://postgres:YOUR-PASSWORD@db.abcdefgh.supabase.co:5432/postgres"
```

3. Kaydet!

### Adım 5: Gerekli Paketleri Yükle (3 dk)

```bash
pip install psycopg2-binary flask flask-cors
```

### Adım 6: İlk Çalıştırma (2 dk)

```bash
python test_cloud_connection.py
```

Görmen gereken:
```
✅ Cloud veritabanına bağlandı!
✅ Tablolar oluşturuldu!
✅ Test başarılı!
```

---

## 📱 Telefonda Kullanım

### Web Uygulaması ile (Önerilenl)

Sonraki adımda Flask web uygulaması hazırlayacağız:
- Tarayıcıdan erişim
- Responsive tasarım
- Her cihazdan kullanım

```bash
python web_app.py
```

Sonra telefondan:
```
http://BILGISAYAR-IP:5000
```

### Internet Üzerinden Erişim (Ngrok)

```bash
pip install pyngrok
python web_app.py --public
```

Sonra herhangi bir internet bağlantısından:
```
https://abc123.ngrok.io
```

---

## 🔧 Sorun Giderme

### "ModuleNotFoundError: No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### "Could not connect to server"
- Internet bağlantınızı kontrol edin
- Supabase şifrenizi config.py'de doğru yazdığınızdan emin olun
- Supabase projenizin "aktif" olduğunu kontrol edin

### "SSL Connection Error"
Connection string'e ekleyin:
```python
SUPABASE_DB_URL = "postgresql://...?sslmode=require"
```

---

## 📊 Veri Aktarımı

Mevcut SQLite verilerini Cloud'a aktarmak için:

```bash
python migrate_to_cloud.py
```

Bu komut:
- ✅ Tüm müşterileri aktarır
- ✅ Tüm poliçeleri aktarır
- ✅ Tüm finansal kayıtları aktarır
- ✅ Yedek oluşturur

---

## 🎯 Sonraki Adımlar

1. ✅ Cloud veritabanı hazır
2. 🔄 Mevcut verileri aktar
3. 🌐 Web arayüzü hazırla (Flask)
4. 📱 Telefonda test et
5. 🚀 Kullanmaya başla!

---

## 💡 Avantajlar

- ✅ **Her yerden erişim**: PC, telefon, tablet
- ✅ **Her zaman güncel**: Gerçek zamanlı senkronizasyon
- ✅ **Otomatik yedekleme**: Supabase her şeyi yedekler
- ✅ **Çoklu kullanıcı**: 10 kişi aynı anda kullanabilir
- ✅ **Ücretsiz**: 500MB veri + sınırsız API
- ✅ **Güvenli**: SSL şifrelemeli bağlantı

---

## 📞 Destek

Sorun mu yaşıyorsun? Hemen söyle, birlikte çözelim!


