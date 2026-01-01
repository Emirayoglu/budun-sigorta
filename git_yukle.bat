@echo off
echo ============================================================
echo              Git Otomatik Kurulum
echo ============================================================
echo.

echo [1/2] Git indiriliyor...
curl -L -o git-installer.exe https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe
echo       OK! Indirildi
echo.

echo [2/2] Git kuruluyor...
echo       Kurulum penceresi acilacak...
echo       Tum ayarlari VARSAYILAN birak, sadece NEXT tikla!
echo.
start /wait git-installer.exe

echo.
echo ============================================================
echo GIT KURULDU!
echo ============================================================
echo.
echo Simdi terminal'i KAPAT ve YENİDEN AC!
echo Sonra git komutlari calisacak.
echo.
pause


