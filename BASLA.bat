@echo off
echo ============================================================
echo           BUDUN Sigorta - Internet Erisimi
echo ============================================================
echo.

REM Cloudflared indir (yoksa)
if not exist cloudflared.exe (
    echo [1/3] Cloudflared indiriliyor...
    curl -L -o cloudflared.exe https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe
    echo       OK! Indirildi
    echo.
) else (
    echo [1/3] Cloudflared zaten var - ATLA
    echo.
)

REM Web uygulamasını başlat
echo [2/3] Web uygulamasi baslatiliyor...
start "BUDUN Web App" cmd /k python web_app.py
timeout /t 3 > nul
echo       OK! Web app calisiyor
echo.

REM İnternet tünelini aç
echo [3/3] Internet tuneli aciliyor...
echo.
echo ============================================================
echo   INTERNET ADRESI ASAGIDA GORUNECEK!
echo   https://xyz-abc.trycloudflare.com gibi
echo ============================================================
echo.
cloudflared.exe tunnel --url http://localhost:5000

pause


