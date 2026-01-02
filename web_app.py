"""
BUDUN Sigorta - Web Uygulaması
Telefon ve tarayıcıdan erişim için Flask web arayüzü
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from database_supabase import SupabaseDB
from datetime import datetime, date

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'budun-sigorta-secret-key'

# Veritabanı bağlantısı
db = SupabaseDB()

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

@app.route('/api/policeler', methods=['GET'])
def get_policeler():
    """Tüm poliçeleri getir"""
    try:
        policeler = db.police_listesi_getir()
        return jsonify({
            'success': True,
            'data': [
                {
                    'musteri': p[0],
                    'police_no': p[1],
                    'sigorta_turu': p[2],
                    'sirket': p[3],
                    'baslangic': p[4],
                    'bitis': p[5],
                    'prim': float(p[6]) if p[6] else 0,
                    'komisyon': float(p[7]) if p[7] else 0,
                    'satisci': p[8]
                }
                for p in policeler
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/musteriler', methods=['GET'])
def get_musteriler():
    """Tüm müşterileri getir"""
    try:
        musteriler = db.musterileri_getir()
        return jsonify({
            'success': True,
            'data': [
                {'id': m.get('id'), 'ad_soyad': m.get('ad_soyad'), 'tc_no': m.get('tc_no', '')}
                for m in musteriler
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/musteri/ekle', methods=['POST'])
def musteri_ekle():
    """Yeni müşteri ekle"""
    try:
        data = request.get_json()
        success, message = db.musteri_ekle(
            data['ad_soyad'],
            data.get('tc_no', ''),
            data.get('telefon', ''),
            data.get('email', ''),
            data.get('adres', '')
        )
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/police/ekle', methods=['POST'])
def police_ekle():
    """Yeni poliçe ekle"""
    try:
        data = request.get_json()
        success, message = db.police_ekle(
            data['musteri_id'],
            data['police_no'],
            data['sigorta_turu'],
            data['sirket'],
            data['baslangic_tarihi'],
            data['bitis_tarihi'],
            data.get('prim_tutari', 0),
            data.get('komisyon_tutari', 0),
            data.get('aciklama', ''),
            data.get('satisci_id'),
            data.get('odeme_sekli', 'Nakit')
        )
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/satiscilar', methods=['GET'])
def get_satiscilar():
    """Aktif satışçıları getir"""
    try:
        satiscilar = db.satiscilari_getir()
        return jsonify({
            'success': True,
            'data': [
                {'id': s.get('id'), 'ad_soyad': s.get('ad_soyad'), 'komisyon_orani': s.get('komisyon_orani', 0)}
                for s in satiscilar
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/police/<police_no>', methods=['GET'])
def get_police_detay(police_no):
    """Poliçe detayını getir"""
    try:
        police = db.police_no_ile_getir(police_no)
        if police:
            return jsonify({'success': True, 'data': police})
        return jsonify({'success': False, 'error': 'Poliçe bulunamadı'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/police/<int:police_id>', methods=['PUT'])
def police_guncelle(police_id):
    """Poliçe güncelle"""
    try:
        data = request.get_json()
        success, message = db.police_guncelle(
            police_id,
            data.get('police_no'),
            data.get('sigorta_turu'),
            data.get('sirket'),
            data.get('baslangic_tarihi'),
            data.get('bitis_tarihi'),
            data.get('prim_tutari'),
            data.get('komisyon_tutari'),
            data.get('aciklama'),
            data.get('satisci_id'),
            data.get('odeme_sekli')
        )
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/police/<int:police_id>', methods=['DELETE'])
def police_sil(police_id):
    """Poliçe sil"""
    try:
        success, message = db.police_sil(police_id)
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/yenilemeler', methods=['GET'])
def get_yenilemeler():
    """Yenileme poliçelerini getir"""
    try:
        from datetime import datetime, timedelta
        
        # Bugünden 90 gün önceden 120 gün sonraya kadar olan poliçeleri getir
        bugun = datetime.now().date()
        baslangic = (bugun - timedelta(days=90)).strftime("%Y-%m-%d")
        bitis = (bugun + timedelta(days=120)).strftime("%Y-%m-%d")
        
        policeler = db.yenileme_policeleri_getir(baslangic, bitis)
        
        # Her poliçe için kalan gün ve müşteri bilgisi ekle
        result = []
        for p in policeler:
            bitis_str = p.get('bitis_tarihi', '')
            if bitis_str:
                bitis_tarih = datetime.strptime(bitis_str.split('T')[0], "%Y-%m-%d").date()
                kalan_gun = (bitis_tarih - bugun).days
                
                # Müşteri adını al
                musteri_id = p.get('musteri_id')
                musteri_ad = '-'
                if musteri_id:
                    musteriler = db.musterileri_getir()
                    for m in musteriler:
                        if m.get('id') == musteri_id:
                            musteri_ad = m.get('ad_soyad', '-')
                            break
                
                p['kalan_gun'] = kalan_gun
                p['musteri_ad'] = musteri_ad
                result.append(p)
        
        return jsonify({'success': True, 'data': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/yenileme/<int:police_id>', methods=['PUT'])
def yenileme_guncelle(police_id):
    """Yenileme durumunu güncelle"""
    try:
        data = request.get_json()
        yeni_durum = data.get('yenileme_durumu')
        success, message = db.yenileme_durumu_guncelle(police_id, yeni_durum)
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/finans', methods=['GET'])
def get_finans():
    """Nakit poliçeleri getir"""
    try:
        policeler = db.nakit_policeleri_getir()
        return jsonify({'success': True, 'data': policeler})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/finans/<int:police_id>', methods=['PUT'])
def finans_guncelle(police_id):
    """Finans durumu güncelle"""
    try:
        data = request.get_json()
        success, message = db.finans_guncelle(
            police_id,
            data.get('odenen_tutar'),
            data.get('odeme_tarihi')
        )
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/raporlar', methods=['POST'])
def raporlar():
    """Rapor oluştur"""
    try:
        data = request.get_json()
        bas_tarih = data.get('baslangic_tarihi')
        bit_tarih = data.get('bitis_tarihi')
        satisci_id = data.get('satisci_id')
        sigorta_turu = data.get('sigorta_turu')
        
        # Tüm poliçeleri al
        policeler = db.police_listesi_getir()
        
        # Filtreleme mantığı buraya eklenecek (şimdilik tümünü dön)
        return jsonify({'success': True, 'data': policeler})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/capraz-satis/<int:musteri_id>', methods=['GET'])
def capraz_satis(musteri_id):
    """Müşterinin mevcut poliçelerini getir"""
    try:
        policeler = db.musteri_police_detay_getir(musteri_id)
        return jsonify({'success': True, 'data': policeler})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_local_ip():
    """Yerel IP adresini bul"""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    local_ip = get_local_ip()
    
    print("=" * 60)
    print("🌐 BUDUN Sigorta Web Uygulaması")
    print("=" * 60)
    print()
    print("✅ Server başlatılıyor...")
    print()
    print(f"📡 Port: {port}")
    print(f"📱 TELEFONDAN ERİŞİM:")
    print(f"   http://{local_ip}:{port}")
    print()
    print("💻 BU BILGISAYARDAN:")
    print(f"   http://localhost:{port}")
    print()
    print("🔄 Server'ı durdurmak için: CTRL+C")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=port, debug=False)


