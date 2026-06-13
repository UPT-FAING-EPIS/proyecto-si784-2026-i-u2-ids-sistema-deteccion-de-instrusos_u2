@echo off
cd /d "%~dp0"

echo.
echo Iniciando IDS PRO Dashboard
echo Ubicacion del proyecto:
echo %CD%
echo.
echo Ejecutando:
echo   python run_dashboard.py
echo.
echo Dashboard:
echo   http://127.0.0.1:5000
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en PATH.
    echo Instala Python desde https://www.python.org/downloads/
    echo Marca la opcion "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

echo Verificando dependencias...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] No se pudieron instalar las dependencias.
    echo Revisa tu conexion a internet o ejecuta manualmente:
    echo   python -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

python run_dashboard.py

echo.
echo El dashboard se detuvo o no pudo iniciar.
echo La ventana queda abierta para revisar mensajes.
echo.

cmd /k
