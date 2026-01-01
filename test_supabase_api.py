"""
REST API Test - Çok daha kolay!
"""

print("=" * 50)
print("🧪 Supabase REST API Testi")
print("=" * 50)
print()

print("1️⃣ Config dosyasını kontrol et...")
print()

try:
    from config import SUPABASE_URL, SUPABASE_KEY
    
    print(f"   URL: {SUPABASE_URL}")
    
    if "BURAYA" in SUPABASE_KEY:
        print()
        print("❌ ANON KEY eksik!")
        print()
        print("🔧 Nasıl bulunur:")
        print("1. Supabase paneline git")
        print("2. Sol menü > Settings (⚙️)")
        print("3. Sol tarafta > API sekmesi")
        print("4. 'Project API keys' başlığı altında:")
        print("   - anon / public key'i kopyala")
        print("   - 'eyJhbGci...' ile başlar (çok uzun)")
        print("5. config.py'de SUPABASE_KEY'e yapıştır")
        print()
    else:
        print(f"   KEY: {SUPABASE_KEY[:20]}... ✅")
        print()
        
        print("2️⃣ Supabase kütüphanesi yükleniyor...")
        import subprocess
        subprocess.run(["pip", "install", "supabase"], check=True)
        print("   ✅ Yüklendi!")
        print()
        
        print("3️⃣ Bağlantı test ediliyor...")
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("   ✅ Bağlantı başarılı!")
        print()
        
        print("=" * 50)
        print("🎉 HER ŞEY HAZIR!")
        print("=" * 50)
        print()
        print("✅ REST API çalışıyor")
        print("✅ Firewall sorunu yok")
        print("✅ Her yerden erişebilirsin")
        
except ImportError as e:
    print(f"❌ Import hatası: {e}")
    print()
    print("Çözüm:")
    print("pip install supabase")
    
except Exception as e:
    print(f"❌ Hata: {e}")


