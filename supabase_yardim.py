"""
Alternatif: Kolay Bağlantı Yöntemi
Supabase REST API kullanarak daha kolay bağlantı
"""

# Bu yöntem daha kolay olabilir!
# Sadece 2 bilgi lazım: PROJECT_URL ve ANON_KEY

SUPABASE_URL = "https://[PROJECT-REF].supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Bu bilgileri bulma:
# 1. Supabase > Settings > API
# 2. Project URL'i kopyala
# 3. anon/public key'i kopyala

# Bu yöntemle PostgreSQL kurulumuna gerek yok!
# REST API üzerinden çalışır

print("""
🔍 Supabase'de Bağlantı Bilgilerini Bulma

Adım 1: Sol menüde ⚙️ Settings (Project Settings)
Adım 2: Sol tarafta "API" sekmesine tıkla
Adım 3: Göreceksin:
   - Project URL: https://xyz.supabase.co
   - anon public key: eyJhbGci...

Bu iki bilgiyi config.py'e yapıştır!

Alternatif olarak "Database" sekmesine git:
   - Connection String'i bul
   - URI formatını kopyala

Sorun devam ediyorsa, proje ekran görüntüsü gönder!
""")


