"""
Supabase REST API Veritabanı Sınıfı - TAM VERSİYON
Tüm Database fonksiyonlarının Supabase uyumlu hali
"""

from supabase import create_client, Client
from datetime import datetime

class SupabaseDB:
    """
    Supabase REST API ile veritabanı işlemleri
    SQLite Database sınıfı ile aynı fonksiyonlar
    """
    
    def __init__(self):
        from config import SUPABASE_URL, SUPABASE_KEY
        
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Geriye uyumluluk için dummy cursor ve connection
        self._cursor = self.FakeCursor()
        self._connection = None
        print("✅ Supabase'e bağlandı (REST API)")
    
    # Geriye uyumluluk için fake cursor sınıfı
    class FakeCursor:
        def execute(self, *args, **kwargs):
            pass
        def fetchall(self):
            return []
        def fetchone(self):
            return None
    
    @property
    def cursor(self):
        """Fake cursor - geriye uyumluluk için"""
        return self._cursor
    
    @property  
    def connection(self):
        """Fake connection - geriye uyumluluk için"""
        return self._connection
    
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
    
    def capraz_satis_policeleri_getir(self):
        """Çapraz satış için tüm poliçeleri müşteri bilgileriyle getir"""
        try:
            result = self.supabase.table('policeler')\
                .select('id, police_no, musteriler(ad_soyad, telefon, tc_no), sigorta_turu, sirket, baslangic_tarihi, bitis_tarihi, prim_tutari, kayit_tarihi')\
                .execute()
            
            # Tuple formatına dönüştür
            formatted = []
            for p in result.data:
                musteri = p.get('musteriler', {})
                formatted.append((
                    p['id'],
                    p['police_no'],
                    musteri.get('ad_soyad', '-'),
                    musteri.get('telefon', '-'),
                    musteri.get('tc_no', '-'),
                    p['sigorta_turu'],
                    p['sirket'],
                    p['baslangic_tarihi'],
                    p['bitis_tarihi'],
                    p['prim_tutari'],
                    p['kayit_tarihi']
                ))
            return formatted
        except Exception as e:
            print(f"Hata: {e}")
            return []
    
    def musteri_ekle(self, ad_soyad, tc_no, telefon, email, adres):
        """Yeni müşteri ekle"""
        try:
            data = {
                "ad_soyad": ad_soyad,
                "tc_no": tc_no,
                "telefon": telefon,
                "email": email,
                "adres": adres
            }
            
            result = self.supabase.table('musteriler').insert(data).execute()
            return True, "Müşteri başarıyla eklendi"
        except Exception as e:
            if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                return False, "Bu TC No zaten kayıtlı!"
            return False, f"Hata: {str(e)}"
    
    def police_ekle(self, musteri_id, police_no, sigorta_turu, sirket, 
                    baslangic_tarihi, bitis_tarihi, prim_tutari, 
                    komisyon_tutari, aciklama, satisci_id=None, odeme_sekli='Nakit'):
        """Yeni poliçe ekle"""
        try:
            data = {
                "musteri_id": musteri_id,
                "satisci_id": satisci_id,
                "police_no": police_no,
                "sigorta_turu": sigorta_turu,
                "sirket": sirket,
                "baslangic_tarihi": baslangic_tarihi,
                "bitis_tarihi": bitis_tarihi,
                "prim_tutari": float(prim_tutari) if prim_tutari else 0,
                "komisyon_tutari": float(komisyon_tutari) if komisyon_tutari else 0,
                "odeme_sekli": odeme_sekli,
                "aciklama": aciklama
            }
            
            result = self.supabase.table('policeler').insert(data).execute()
            
            # Nakit ise finans kaydı oluştur
            if odeme_sekli == 'Nakit' and result.data:
                police_id = result.data[0]['id']
                finans_data = {
                    "police_id": police_id,
                    "borc_tutari": float(prim_tutari) if prim_tutari else 0,
                    "odenen_tutar": 0,
                    "kalan_borc": float(prim_tutari) if prim_tutari else 0
                }
                self.supabase.table('finans_kayitlari').insert(finans_data).execute()
            
            return True, "Poliçe başarıyla eklendi"
        except Exception as e:
            if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                return False, "Bu poliçe numarası zaten kayıtlı!"
            return False, f"Hata: {str(e)}"
    
    def musterileri_getir(self):
        """Tüm müşterileri getir"""
        try:
            result = self.supabase.table('musteriler')\
                .select('id, ad_soyad, tc_no')\
                .order('ad_soyad')\
                .execute()
            
            return [(m['id'], m['ad_soyad'], m['tc_no']) for m in result.data]
        except Exception as e:
            print(f"Hata: {e}")
            return []
    
    def satiscilari_getir(self):
        """Aktif satışçıları getir"""
        try:
            result = self.supabase.table('satiscilar')\
                .select('id, ad_soyad')\
                .eq('aktif', True)\
                .order('ad_soyad')\
                .execute()
            
            return [(s['id'], s['ad_soyad']) for s in result.data]
        except Exception as e:
            print(f"Hata: {e}")
            return []
    
    def satisci_ekle(self, ad_soyad):
        """Yeni satışçı ekle"""
        try:
            self.supabase.table('satiscilar').insert({'ad_soyad': ad_soyad}).execute()
            return True, "Satışçı başarıyla eklendi"
        except Exception as e:
            if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                return False, "Bu satışçı zaten kayıtlı!"
            return False, f"Hata: {str(e)}"
    
    def police_guncelle(self, police_id, police_no, sigorta_turu, sirket,
                        baslangic_tarihi, bitis_tarihi, prim_tutari, 
                        komisyon_tutari, aciklama, satisci_id=None):
        """Poliçe bilgilerini güncelle"""
        try:
            data = {
                "police_no": police_no,
                "sigorta_turu": sigorta_turu,
                "sirket": sirket,
                "baslangic_tarihi": baslangic_tarihi,
                "bitis_tarihi": bitis_tarihi,
                "prim_tutari": float(prim_tutari) if prim_tutari else 0,
                "komisyon_tutari": float(komisyon_tutari) if komisyon_tutari else 0,
                "aciklama": aciklama,
                "satisci_id": satisci_id
            }
            
            self.supabase.table('policeler').update(data).eq('id', police_id).execute()
            return True, "Poliçe başarıyla güncellendi"
        except Exception as e:
            if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                return False, "Bu poliçe numarası başka bir kayıtta kullanılıyor!"
            return False, f"Hata: {str(e)}"
    
    def police_sil(self, police_id):
        """Poliçe sil"""
        try:
            self.supabase.table('policeler').delete().eq('id', police_id).execute()
            return True, "Poliçe başarıyla silindi"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def police_detay_getir(self, police_no):
        """Poliçe detaylarını getir"""
        try:
            result = self.supabase.table('policeler')\
                .select('*, musteriler(ad_soyad, tc_no, telefon, email), satiscilar(ad_soyad)')\
                .eq('police_no', police_no)\
                .execute()
            
            if not result.data:
                return None
            
            p = result.data[0]
            musteri = p.get('musteriler', {})
            satisci = p.get('satiscilar', {})
            
            # Tuple formatına dönüştür
            return (
                p['id'],
                p['police_no'],
                p['sigorta_turu'],
                p['sirket'],
                p['baslangic_tarihi'],
                p['bitis_tarihi'],
                p['prim_tutari'],
                p['komisyon_tutari'],
                p['aciklama'],
                musteri.get('ad_soyad', '-'),
                musteri.get('tc_no', '-'),
                musteri.get('telefon', '-'),
                musteri.get('email', '-'),
                p.get('satisci_id'),
                satisci.get('ad_soyad', '-') if satisci else '-'
            )
        except Exception as e:
            print(f"Hata: {e}")
            return None
    
    def yenileme_durumu_guncelle(self, police_no, durum):
        """Poliçenin yenileme durumunu güncelle"""
        try:
            self.supabase.table('policeler')\
                .update({'yenileme_durumu': durum})\
                .eq('police_no', police_no)\
                .execute()
            return True, "Durum güncellendi"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def nakit_policeleri_getir(self):
        """Ödeme şekli 'Nakit' olan poliçeleri getir"""
        try:
            result = self.supabase.table('policeler')\
                .select('id, police_no, musteriler(ad_soyad, telefon), sigorta_turu, sirket, prim_tutari, finans_kayitlari(borc_tutari, odenen_tutar, kalan_borc), kayit_tarihi')\
                .eq('odeme_sekli', 'Nakit')\
                .order('kayit_tarihi', desc=True)\
                .execute()
            
            formatted = []
            for p in result.data:
                musteri = p.get('musteriler', {})
                finans_list = p.get('finans_kayitlari', [])
                finans = finans_list[0] if finans_list else {}
                
                formatted.append((
                    p['id'],
                    p['police_no'],
                    musteri.get('ad_soyad', '-'),
                    musteri.get('telefon', '-'),
                    p['sigorta_turu'],
                    p['sirket'],
                    p['prim_tutari'],
                    finans.get('borc_tutari', 0),
                    finans.get('odenen_tutar', 0),
                    finans.get('kalan_borc', 0),
                    p['kayit_tarihi']
                ))
            return formatted
        except Exception as e:
            print(f"Hata: {e}")
            return []
    
    def finans_guncelle(self, police_id, odenen_tutar):
        """Finans kaydını güncelle"""
        try:
            # Mevcut finans kaydını al
            result = self.supabase.table('finans_kayitlari')\
                .select('*')\
                .eq('police_id', police_id)\
                .execute()
            
            if result.data:
                finans = result.data[0]
                yeni_odenen = finans['odenen_tutar'] + float(odenen_tutar)
                kalan_borc = finans['borc_tutari'] - yeni_odenen
                
                self.supabase.table('finans_kayitlari')\
                    .update({
                        'odenen_tutar': yeni_odenen,
                        'kalan_borc': kalan_borc
                    })\
                    .eq('police_id', police_id)\
                    .execute()
            else:
                # Finans kaydı yoksa oluştur
                police_result = self.supabase.table('policeler')\
                    .select('prim_tutari')\
                    .eq('id', police_id)\
                    .execute()
                
                if police_result.data:
                    prim = police_result.data[0]['prim_tutari']
                    kalan = prim - float(odenen_tutar)
                    
                    self.supabase.table('finans_kayitlari').insert({
                        'police_id': police_id,
                        'borc_tutari': prim,
                        'odenen_tutar': float(odenen_tutar),
                        'kalan_borc': kalan
                    }).execute()
            
            return True, "Finans kaydı güncellendi"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def finans_detay_getir(self, police_id):
        """Poliçenin finans detaylarını getir"""
        try:
            result = self.supabase.table('policeler')\
                .select('police_no, musteriler(ad_soyad), sigorta_turu, sirket, prim_tutari, finans_kayitlari(borc_tutari, odenen_tutar, kalan_borc)')\
                .eq('id', police_id)\
                .execute()
            
            if not result.data:
                return None
            
            p = result.data[0]
            musteri = p.get('musteriler', {})
            finans_list = p.get('finans_kayitlari', [])
            finans = finans_list[0] if finans_list else {}
            
            return (
                p['police_no'],
                musteri.get('ad_soyad', '-'),
                p['sigorta_turu'],
                p['sirket'],
                p['prim_tutari'],
                finans.get('borc_tutari', 0),
                finans.get('odenen_tutar', 0),
                finans.get('kalan_borc', 0)
            )
        except Exception as e:
            print(f"Hata: {e}")
            return None
    
    def police_listesi_getir(self):
        """Tüm poliçeleri getir (main.py için)"""
        try:
            result = self.supabase.table('policeler')\
                .select('musteriler(ad_soyad), police_no, sigorta_turu, sirket, baslangic_tarihi, bitis_tarihi, prim_tutari, komisyon_tutari, satiscilar(ad_soyad)')\
                .order('kayit_tarihi', desc=True)\
                .execute()
            
            formatted = []
            for p in result.data:
                musteri = p.get('musteriler', {})
                satisci = p.get('satiscilar', {})
                
                formatted.append((
                    musteri.get('ad_soyad', '-'),
                    p['police_no'],
                    p['sigorta_turu'],
                    p['sirket'],
                    p['baslangic_tarihi'],
                    p['bitis_tarihi'],
                    p['prim_tutari'],
                    p['komisyon_tutari'],
                    satisci.get('ad_soyad', '-') if satisci else '-'
                ))
            return formatted
        except Exception as e:
            print(f"Hata: {e}")
            return []
    
    def close(self):
        """Bağlantıyı kapat (REST API'de gerek yok)"""
        pass
