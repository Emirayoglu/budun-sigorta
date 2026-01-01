@echo off
chcp 65001 > nul
echo ================================
echo Sigorta Acente Yönetim Sistemi
echo ================================
echo.
echo Kutuphanelar kontrol ediliyor...
python -m pip install -r requirements.txt --quiet

echo.
echo Program baslatiliyor...
echo.
python main.py

pause

