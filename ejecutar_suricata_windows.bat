@echo off
setlocal

set "PROJECT_DIR=%~dp0"
set "SURICATA_EXE=C:\Program Files\Suricata\suricata.exe"
set "SURICATA_CONFIG=C:\Program Files\Suricata\suricata.yaml"
set "LOCAL_RULES=%PROJECT_DIR%suricata\local.rules"
set "LOG_DIR=%PROJECT_DIR%logs\suricata"
set "LOCAL_IP=192.168.1.11"

if not exist "%SURICATA_EXE%" (
    echo [ERROR] No se encontro Suricata en "%SURICATA_EXE%".
    pause
    exit /b 1
)

if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
)

echo [INFO] Iniciando Suricata IDS en Windows...
echo [INFO] Interfaz/IP: %LOCAL_IP%
echo [INFO] Logs: %LOG_DIR%
echo [INFO] Reglas: %LOCAL_RULES%
echo.

"%SURICATA_EXE%" -c "%SURICATA_CONFIG%" -S "%LOCAL_RULES%" -l "%LOG_DIR%" -i %LOCAL_IP% -k none

pause
