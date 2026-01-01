"""
Supabase REST API Veritabanı Sınıfı - REQUESTS VERSİYONU
Supabase Python kütüphanesi yerine direkt REST API
"""

import requests
import os
from datetime import datetime

class SupabaseDB:
    """
    Supabase REST API ile veritabanı işlemleri (requests kütüphanesi ile)
    """
    
    def __init__(self):
        self.supabase_url = os.environ.get('SUPABASE_URL')
        self.supabase_key = os.environ.get('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            from config import SUPABASE_URL, SUPABASE_KEY
            self.supabase_url = SUPABASE_URL
            self.supabase_key = SUPABASE_KEY
        
        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        
        # Geriye uyumluluk için dummy cursor
        self._cursor = self.FakeCursor()
        self._connection = None
        print("OK Supabase REST API'ye baglandi (requests)")
    
    class FakeCursor:
        def execute(self, *args, **kwargs):
            pass
        def fetchall(self):
            return []
        def fetchone(self):
            return None
    
    @property
    def cursor(self):
        return self._cursor
    
    @property  
    def connection(self):
        return self._connection
    
    def _get(self, table, filters=None, select="*", order=None, limit=None):
        """GET isteği"""
        url = f"{self.supabase_url}/rest/v1/{table}"
        params = {'select': select}
        
        if filters:
            for key, value in filters.items():
                params[key] = f'eq.{value}'
        
        if order:
            params['order'] = order
            
        if limit:
            params['limit'] = limit
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"GET Hatası: {response.status_code} - {response.text}")
            return []
    
    def _post(self, table, data):
        """POST isteği"""
        url = f"{self.supabase_url}/rest/v1/{table}"
        response = requests.post(url, headers=self.headers, json=data)
        
        print(f"POST {table}: Status {response.status_code}")
        
        if response.status_code in [200, 201]:
            return True, "Başarılı"
        else:
            error_msg = f"Hata: {response.status_code} - {response.text}"
            print(error_msg)
            return False, error_msg
    
    def _patch(self, table, filters, data):
        """PATCH isteği"""
        url = f"{self.supabase_url}/rest/v1/{table}"
        params = {}
        for key, value in filters.items():
            params[key] = f'eq.{value}'
        
        response = requests.patch(url, headers=self.headers, params=params, json=data)
        
        if response.status_code == 200:
            return True, "Güncellendi"
        else:
            return False, f"Hata: {response.text}"
    
    def _delete(self, table, filters):
        """DELETE isteği"""
        url = f"{self.supabase_url}/rest/v1/{table}"
        params = {}
        for key, value in filters.items():
            params[key] = f'eq.{value}'
        
        response = requests.delete(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return True, "Silindi"
        else:
            return False, f"Hata: {response.text}"
    
    def get_policeler(self):
        """Tüm poliçeleri getir"""
        return self._get('policeler', order='kayit_tarihi.desc')
    
    def police_listesi_getir(self):
        """Poliçe listesini getir (formatlanmış)"""
        policeler = self._get('policeler', order='kayit_tarihi.desc')
        
        result = []
        for p in policeler:
            # Müşteri bilgisi
            musteri_id = p.get('musteri_id')
            if musteri_id:
                musteri = self._get('musteriler', filters={'id': musteri_id})
                musteri_ad = musteri[0]['ad_soyad'] if musteri else 'Bilinmiyor'
            else:
                musteri_ad = 'Bilinmiyor'
            
            # Satışçı bilgisi
            satisci_id = p.get('satisci_id')
            if satisci_id:
                satisci = self._get('satiscilar', filters={'id': satisci_id})
                satisci_ad = satisci[0]['ad_soyad'] if satisci else '-'
            else:
                satisci_ad = '-'
            
            result.append((
                musteri_ad,
                p.get('police_no'),
                p.get('sigorta_turu'),
                p.get('sirket'),
                p.get('baslangic_tarihi'),
                p.get('bitis_tarihi'),
                p.get('prim_tutari'),
                p.get('komisyon_tutari'),
                satisci_ad
            ))
        
        return result
    
    def musteri_ekle(self, ad_soyad, tc_no='', telefon='', email='', adres=''):
        """Yeni müşteri ekle"""
        data = {
            'ad_soyad': ad_soyad,
            'tc_no': tc_no,
            'telefon': telefon,
            'email': email,
            'adres': adres
        }
        return self._post('musteriler', data)
    
    def police_ekle(self, musteri_id, police_no, sigorta_turu, sirket, baslangic, bitis, 
                    prim=0, komisyon=0, aciklama='', satisci_id=None, odeme_sekli='Nakit'):
        """Yeni poliçe ekle"""
        data = {
            'musteri_id': musteri_id,
            'police_no': police_no,
            'sigorta_turu': sigorta_turu,
            'sirket': sirket,
            'baslangic_tarihi': baslangic,
            'bitis_tarihi': bitis,
            'prim_tutari': prim,
            'komisyon_tutari': komisyon,
            'aciklama': aciklama,
            'satisci_id': satisci_id,
            'odeme_sekli': odeme_sekli
        }
        return self._post('policeler', data)
    
    def musterileri_getir(self):
        """Tüm müşterileri getir - DICT FORMAT"""
        musteriler = self._get('musteriler', order='ad_soyad.asc')
        return musteriler  # Direkt dict listesi dön
    
    def satiscilari_getir(self):
        """Aktif satışçıları getir"""
        satiscilar = self._get('satiscilar', filters={'durum': 'Aktif'}, order='ad_soyad.asc')
        return [(s['id'], s['ad_soyad'], s.get('komisyon_orani', 0)) for s in satiscilar]
    
    def police_detay_getir(self, police_id):
        """Poliçe detaylarını getir"""
        police = self._get('policeler', filters={'id': police_id})
        if police:
            return police[0]
        return None
    
    def police_guncelle(self, police_id, **kwargs):
        """Poliçe güncelle"""
        return self._patch('policeler', {'id': police_id}, kwargs)
    
    def police_sil(self, police_id):
        """Poliçe sil"""
        return self._delete('policeler', {'id': police_id})
    
    def satisci_ekle(self, ad_soyad, telefon='', email='', komisyon_orani=0):
        """Yeni satışçı ekle"""
        data = {
            'ad_soyad': ad_soyad,
            'telefon': telefon,
            'email': email,
            'komisyon_orani': komisyon_orani,
            'durum': 'Aktif'
        }
        return self._post('satiscilar', data)
    
    def yenileme_durumu_guncelle(self, police_id, yenilendi_mi):
        """Yenileme durumunu güncelle"""
        return self._patch('policeler', {'id': police_id}, {'yenilendi_mi': yenilendi_mi})
    
    def nakit_policeleri_getir(self):
        """Nakit ödeme şekilli poliçeleri getir"""
        return self._get('policeler', filters={'odeme_sekli': 'Nakit'}, order='kayit_tarihi.desc')
    
    def finans_kayitlari_getir(self):
        """Finans kayıtlarını getir"""
        return self._get('finans_kayitlari', order='kayit_tarihi.desc')
    
    def finans_guncelle(self, police_id, odendi_mi, odeme_tarihi=None):
        """Finans durumunu güncelle"""
        data = {'odendi_mi': odendi_mi}
        if odeme_tarihi:
            data['odeme_tarihi'] = odeme_tarihi
        return self._patch('finans_kayitlari', {'police_id': police_id}, data)
    
    def finans_detay_getir(self, finans_id):
        """Finans detayını getir"""
        finans = self._get('finans_kayitlari', filters={'id': finans_id})
        if finans:
            return finans[0]
        return None
    
    def capraz_satis_policeleri_getir(self, musteri_id=None):
        """Müşterinin mevcut poliçelerini getir. musteri_id None ise tüm poliçeleri getir."""
        if musteri_id:
            return self._get('policeler', filters={'musteri_id': musteri_id})
        else:
            return self._get('policeler', order='kayit_tarihi.desc')
    
    def capraz_satis_onerileri_getir(self, sigorta_turu):
        """Çapraz satış önerileri"""
        oneriler = {
            "Trafik": ["Kasko", "Ferdi Kaza"],
            "Kasko": ["Trafik", "Ferdi Kaza", "Seyahat"],
            "Konut": ["Dask", "Ferdi Kaza", "Hayat"],
            "İşyeri": ["Dask", "Ferdi Kaza", "Hayat", "Sağlık"],
            "Sağlık": ["Hayat", "Ferdi Kaza"],
            "Hayat": ["Sağlık", "Ferdi Kaza"],
            "Seyahat": ["Kasko", "Sağlık"],
            "Dask": ["Konut", "Deprem"],
        }
        return oneriler.get(sigorta_turu, [])
    
    def yenileme_policeleri_getir(self, baslangic_tarih, bitis_tarih):
        """Belirli tarih aralığındaki poliçeleri getir (yenileme için)"""
        policeler = self._get('policeler', order='bitis_tarihi.asc')
        
        # Tarih filtreleme - DICT FORMAT
        filtered = []
        for p in policeler:
            bitis = p.get('bitis_tarihi')
            if bitis and baslangic_tarih <= bitis.split('T')[0] <= bitis_tarih:
                # Direkt dict olarak dön
                filtered.append(p)
        
        return filtered
    
    def musteri_police_detay_getir(self, police_id):
        """Poliçe ve müşteri bilgilerini birlikte getir (çapraz satış için)"""
        police = self._get('policeler', filters={'id': police_id})
        if not police:
            return None
        
        p = police[0]
        musteri = self._get('musteriler', filters={'id': p.get('musteri_id')})
        
        if musteri:
            m = musteri[0]
            return (p.get('musteri_id'), m.get('ad_soyad'), m.get('tc_no'), m.get('telefon'))
        
        return None
    
    def close(self):
        """Bağlantıyı kapat (dummy)"""
        pass
