@echo off
echo ============================================================
echo           Railway CLI ile Otomatik Deploy
echo ============================================================
echo.

echo [1/2] Railway CLI kuruluyor...
npm install -g @railway/cli
echo       OK!
echo.

echo [2/2] Railway'e login oluyor...
railway login
echo.

echo [3/3] Deploy basliyor...
railway init
railway up
echo.

echo ============================================================
echo DEPLOY TAMAMLANDI!
echo Link'i railway dashboard'dan gorebilirsin
echo https://railway.app/dashboard
echo ============================================================
pause


