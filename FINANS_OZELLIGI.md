# 💰 FİNANS ÖZELLİĞİ

## Genel Bakış

Finans modülü, **Ödeme Şekli "Nakit"** olan poliçelerin borç takibini yapmak için tasarlanmıştır.

## Nasıl Çalışır?

### 1. Poliçe Girişi
- POLİÇE GİRİŞ sayfasında bir poliçe eklerken **Ödeme Şekli** kısmında **"Nakit"** seçilirse
- Bu poliçe otomatik olarak **FİNANS** sekmesindeki listeye eklenir
- Başlangıç borç tutarı = Prim Tutarı

### 2. Finans Listesi
FİNANS sekmesinde aşağıdaki bilgiler görüntülenir:
- **Poliçe No**
- **Müşteri Adı**
- **Telefon**
- **Poliçe Türü**
- **Sigorta Şirketi**
- **Prim Tutarı** (TL)
- **Borç Tutarı** (TL)
- **Ödenen Tutar** (TL)
- **Kalan Borç** (TL) - Renk kodlu:
  - 🔴 Kırmızı: Borç var
  - 🟢 Yeşil: Borç tamamlandı
- **Kayıt Tarihi**

### 3. Borç Güncelleme
- Bir poliçenin üzerine **çift tıklayın**
- Açılan pencerede:
  - Poliçe detaylarını görüntüleyin
  - Ödeme tutarı girin
  - **Hızlı Ödeme** butonları ile:
    - Tamamını Öde
    - Yarısını Öde
  - Yeni kalan borç otomatik hesaplanır
  - KAYDET butonuna basın

### 4. Borç Arttırma/Azaltma
- **Arttırma:** Pozitif tutar girerek ek borç ekleyebilirsiniz
- **Azaltma:** Ödeme tutarı girerek borcu düşürebilirsiniz
- **Fazla Ödeme:** Kalan borçtan fazla ödeme girerseniz uyarı alırsınız

## Özellikler

✅ **Otomatik Kayıt:** Nakit poliçeler otomatik finans listesine eklenir
✅ **Renk Kodlu:** Borç durumu görsel olarak anlaşılır
✅ **Hızlı Ödeme:** Tek tıkla tam veya yarım ödeme
✅ **Canlı Hesaplama:** Ödeme girerken yeni borç otomatik hesaplanır
✅ **Detaylı İzleme:** Her poliçenin ödeme geçmişi takip edilir

## Veritabanı

Yeni bir tablo eklendi: `finans_kayitlari`

**Alanlar:**
- `police_id`: Poliçe referansı
- `borc_tutari`: Toplam borç
- `odenen_tutar`: Toplam ödenen
- `kalan_borc`: Kalan borç
- `guncelleme_tarihi`: Son güncelleme tarihi

## Kullanım Senaryosu

### Örnek:
1. Müşteri bir Kasko poliçesi yaptırıyor
2. Prim: 5,000 TL
3. Ödeme şekli: **Nakit** seçiliyor
4. Poliçe kaydediliyor
5. → FİNANS sekmesinde görünür (Borç: 5,000 TL)
6. Müşteri 2,000 TL ödeme yapıyor
7. Finans detay penceresinden 2,000 TL giriyoruz
8. → Kalan borç: 3,000 TL (Kırmızı)
9. Müşteri kalan 3,000 TL'yi ödüyor
10. → Kalan borç: 0 TL (Yeşil) ✓

## Notlar

⚠️ **ÖNEMLİ:** 
- Sadece **Nakit** ödeme şekli seçilen poliçeler finans listesinde görünür
- Müşteri Kartı veya Havale ile yapılan poliçeler finans takibine girmez
- Ödeme tutarı kalan borçtan fazla ise uyarı verilir
- Borç sıfırlandığında satır yeşil renge döner

## Güncelleme

Veritabanını sıfırlamak için eski `sigorta_acente.db` dosyasını silin ve programı yeniden başlatın.

