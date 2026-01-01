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
                {'id': m[0], 'ad_soyad': m[1], 'tc_no': m[2]}
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
                {'id': s[0], 'ad_soyad': s[1]}
                for s in satiscilar
            ]
        })
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


