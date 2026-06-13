@echo off
setlocal

set "PROJECT_DIR=%~dp0"
set "DASHBOARD_URL=http://127.0.0.1:5000"
set "SURICATA_EXE=C:\Program Files\Suricata\suricata.exe"
set "SURICATA_CONFIG=C:\Program Files\Suricata\suricata.yaml"
set "SURICATA_RULES=%PROJECT_DIR%suricata\local.rules"
set "SURICATA_LOGS=%PROJECT_DIR%logs\suricata"
set "SURICATA_INTERFACE=192.168.1.11"

cd /d "%PROJECT_DIR%"

echo ==========================================
echo  TrafficWatch IDS
echo ==========================================
echo.
echo Iniciando dashboard...

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python no esta disponible en PATH.
    echo Instala Python o abre el proyecto desde una terminal donde python funcione.
    pause
    exit /b 1
)

echo Verificando dependencias Python...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias.
    echo Ejecuta manualmente: python -m pip install -r requirements.txt
    pause
    exit /b 1
)

start "TrafficWatch Dashboard" /D "%PROJECT_DIR%" cmd /k python run_dashboard.py

if exist "%SURICATA_EXE%" (
    if not exist "%SURICATA_LOGS%" mkdir "%SURICATA_LOGS%"
    echo Iniciando Suricata IDS...
    start "TrafficWatch Suricata" /D "%PROJECT_DIR%" cmd /k ""%SURICATA_EXE%" -c "%SURICATA_CONFIG%" -S "%SURICATA_RULES%" -l "%SURICATA_LOGS%" -i %SURICATA_INTERFACE% -k none"
) else (
    echo [AVISO] Suricata no esta instalado en C:\Program Files\Suricata.
)

echo Abriendo navegador...
timeout /t 3 /nobreak >nul
start "" "%DASHBOARD_URL%"

echo.
echo Listo. Dashboard: %DASHBOARD_URL%
echo Laboratorio remoto: revisa la ventana del dashboard para ver la URL /attack-lab
echo Puedes cerrar esta ventana.
timeout /t 5 /nobreak >nul
