# Supabase Veritabanı Bağlantı Ayarları
# Bu dosyayı .gitignore'a eklemeyi unutmayın!

# Adım 1: supabase.com'da hesap aç
# Adım 2: New Project oluştur
# Adım 3: Settings > Database > Connection String (URI) kopyala
# Adım 4: Aşağıdaki satıra yapıştır

# ============================================
# Supabase Bağlantı Ayarları
# ============================================

# PostgreSQL Direkt Bağlantı (Şu an çalışmıyor - DNS sorunu)
SUPABASE_DB_URL = "postgresql://postgres:249448.Emir@db.iivinxqtiyrtznjqkzin.supabase.co:5432/postgres"

# REST API Bağlantı (ÖNERİLEN - Daha kolay!) ✅ HAZIR
SUPABASE_URL = "https://iivinxqtiyrtznjqkzin.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlpdmlueHF0aXlydHpuanFremluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcyODA3NjMsImV4cCI6MjA4Mjg1Njc2M30.IiBTk5HsudUt4wB3sgiJTwgV6MzfBnZ0YZYftuee5_4"

# Alternatif - Ayrı parametreler
SUPABASE_CONFIG = {
    'host': 'db.[PROJE-ID].supabase.co',
    'database': 'postgres',
    'user': 'postgres',
    'password': '[SIFRENIZ]',
    'port': 5432
}

# Web App Ayarları
SECRET_KEY = "your-secret-key-here-change-this"  # Flask için
DEBUG = True  # Geliştirme modunda True, production'da False

# Uygulama Ayarları
APP_NAME = "BUDUN Sigorta Yönetim Sistemi"
APP_VERSION = "2.0"

