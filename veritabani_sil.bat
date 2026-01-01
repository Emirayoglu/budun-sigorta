@echo off
echo ===================================
echo VERITABANI SIFIRLAMA
echo ===================================
echo.

if exist "sigorta_acente.db" (
    del "sigorta_acente.db"
    echo [OK] Veritabani silindi!
) else (
    echo [BILGI] Veritabani zaten yok.
)

echo.
echo Simdi programi calistirabilirsiniz.
echo.
pause

