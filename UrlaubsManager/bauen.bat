@echo off
echo ==============================================
echo  UrlaubsManager wird installiert und gebaut...
echo ==============================================
echo.
echo Installiere notwendige Pakete...
pip install paramiko pyinstaller

echo.
echo Baue die Anwendung...
python -m PyInstaller --noconfirm --onedir --windowed --name "UrlaubsManager" "urlaubsmanager.py"

echo.
echo ==============================================
echo Fertig! Das Programm liegt im Ordner "dist\UrlaubsManager"
echo ==============================================
pause
