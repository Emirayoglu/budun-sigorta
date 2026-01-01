@echo off
chcp 65001 > nul
echo ================================
echo BUDUN - Veritabani Temizleme
echo ================================
echo.
echo UYARI: Eski veritabani silinecek!
echo Tum verileriniz kaybolacak!
echo.
pause

if exist sigorta_acente.db (
    del sigorta_acente.db
    echo.
    echo [OK] Eski veritabani silindi.
    echo.
) else (
    echo.
    echo [!] Veritabani bulunamadi.
    echo.
)

echo Yeni veritabani otomatik olusturulacak.
echo Program baslatiliyor...
echo.
python main.py
