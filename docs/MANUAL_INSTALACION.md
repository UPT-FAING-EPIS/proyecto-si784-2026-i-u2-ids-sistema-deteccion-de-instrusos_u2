# Manual de Instalacion

## Proyecto

**TrafficWatch IDS**  
Version del documento: **1.0**  
Fecha: **2026-07-04**

## 1. Objetivo

Explicar las formas de instalar y ejecutar TrafficWatch IDS en Windows y en Render. El sistema tiene funciones completas en entorno local y una demo web limitada en Render.

## 2. Modos de instalacion

| Modo | Recomendado para | Incluye |
|---|---|---|
| Local con Python | Desarrollo y pruebas completas | Dashboard, IDS, Scapy, Nmap, Suricata opcional, respuesta activa. |
| Ejecutable Windows | Uso simple sin abrir VS Code | Dashboard empaquetado y laboratorio web. |
| Instalador Windows | Entrega a otro usuario | Accesos directos, dependencias opcionales y configuracion inicial. |
| Render | Demostracion web publica | Dashboard, simulaciones, historial y graficos demo. |

## 3. Requisitos

### 3.1 Requisitos generales

- Windows 10/11.
- Conexion a Internet para instalar dependencias.
- Permisos de administrador para captura real y firewall.
- Git, si se desea clonar el repositorio.

### 3.2 Requisitos para modo local

- Python 3.9 o superior.
- Dependencias de `requirements.txt`.
- Npcap para captura real con Scapy.
- Nmap para escaneos reales.
- Suricata opcional para laboratorio IPS.

### 3.3 Requisitos para Render

- Repositorio en GitHub.
- Cuenta en Render.
- Archivos:
  - `render.yaml`
  - `runtime.txt`
  - `requirements.txt`

## 4. Instalacion local con Python

### Paso 1: Obtener el proyecto

Opcion A: clonar con Git.

```powershell
git clone https://github.com/UPT-FAING-EPIS/proyecto-si784-2026-i-u1-ids.git
cd proyecto-si784-2026-i-u1-ids
```

Opcion B: descargar ZIP desde GitHub y descomprimirlo.

### Paso 2: Crear entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### Paso 3: Instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 4: Crear carpetas de logs

El sistema las crea automaticamente, pero se puede preparar manualmente:

```powershell
mkdir logs
mkdir logs\suricata
```

### Paso 5: Ejecutar dashboard

```powershell
python run_dashboard.py
```

Abrir en el navegador:

```text
http://127.0.0.1:5000/
```

Laboratorio web:

```text
http://127.0.0.1:5000/attack-lab
```

### Paso 6: Ejecutar IDS real

Abrir PowerShell como administrador:

```powershell
python main.py
```

La captura real requiere permisos de administrador y Npcap.

## 5. Instalacion automatizada en Windows

Desde la carpeta del proyecto:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\INSTALAR_TRAFFICWATCH_WINDOWS.ps1
```

El instalador:

- Verifica Python.
- Crea `.venv`.
- Instala dependencias.
- Crea carpetas de logs.
- Crea accesos directos.
- Revisa Nmap y Suricata.
- Pregunta por herramientas opcionales.

Despues de instalar:

```text
INICIAR_TRAFFICWATCH.bat
```

## 6. Uso rapido con scripts

Orden recomendado:

1. Ejecutar `abrir_cmd_proyecto.bat`.
2. Ejecutar `abrir_powershell_admin.bat`.
3. Ejecutar `abrir_powershell_pruebas.bat`.

Descripcion:

| Script | Funcion |
|---|---|
| `abrir_cmd_proyecto.bat` | Inicia el dashboard Flask. |
| `abrir_powershell_admin.bat` | Abre IDS con permisos de administrador. |
| `abrir_powershell_pruebas.bat` | Abre consola para pruebas. |
| `setup_windows.ps1` | Verifica dependencias. |
| `INICIAR_TRAFFICWATCH.bat` | Inicia el dashboard en instalacion Windows. |
| `ejecutar_suricata_windows.bat` | Ayuda con ejecucion local de Suricata. |

## 7. Crear ejecutable Windows

Para generar ejecutable:

```powershell
CREAR_EJECUTABLE_WINDOWS.bat
```

Salida esperada:

```text
dist/TrafficWatchIDS/TrafficWatchIDS.exe
```

## 8. Crear instalador Windows

Para generar instalador:

```powershell
CREAR_INSTALADOR_WINDOWS.bat
```

Salida esperada:

```text
installer_output/TrafficWatchIDS_Setup.exe
```

El instalador usa la configuracion de:

```text
installer/TrafficWatchIDS.iss
```

## 9. Instalacion de Npcap

Npcap es necesario para captura real con Scapy.

1. Descargar desde:

```text
https://npcap.com/#download
```

2. Instalar con permisos de administrador.
3. Reiniciar la terminal o el equipo si es necesario.
4. Ejecutar nuevamente `python main.py` como administrador.

## 10. Instalacion de Nmap

Nmap es necesario para pruebas reales de escaneo.

Descarga:

```text
https://nmap.org/download.html#windows
```

Tambien puede instalarse mediante los scripts del proyecto si `winget` esta disponible.

## 11. Configuracion de Suricata

Suricata es opcional. El dashboard puede:

- Leer `logs/suricata/eve.json`.
- Mostrar estado de reglas locales.
- Generar evento demo.
- Construir comandos y reglas IPS.

Archivo de reglas:

```text
suricata/local.rules
```

Archivo EVE:

```text
logs/suricata/eve.json
```

## 12. Despliegue en Render

Render se usa solo para demo web.

### Archivos requeridos

```text
render.yaml
runtime.txt
requirements.txt
```

### Configuracion

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn web.app:app --bind 0.0.0.0:$PORT
```

Variable:

```text
TRAFFICWATCH_DEPLOYMENT=render
```

### Limitaciones en Render

Render no puede:

- Capturar trafico real de la red del usuario.
- Ejecutar Nmap real contra la red local.
- Operar Suricata real en la red local.
- Modificar Windows Firewall.

Render si puede:

- Mostrar dashboard.
- Generar simulaciones.
- Mostrar historial demo.
- Mostrar graficos.
- Abrir Attack Lab en modo demostracion.

## 13. Verificacion

Validaciones recomendadas:

```powershell
python -m json.tool config.json
python -m compileall src web
python -m pytest
```

Prueba rapida del dashboard:

```powershell
python -c "from web.app import app; c=app.test_client(); assert c.get('/').status_code == 200; assert c.get('/api/status').status_code == 200; print('OK')"
```

## 14. Problemas frecuentes

| Problema | Causa probable | Solucion |
|---|---|---|
| Scapy no captura | Falta administrador o Npcap | Ejecutar PowerShell como administrador e instalar Npcap. |
| Nmap no funciona | Nmap no instalado o no esta en PATH | Instalar Nmap y reiniciar terminal. |
| Dashboard no abre | Flask no esta corriendo | Ejecutar `python run_dashboard.py`. |
| Otra PC no entra | Firewall bloquea puerto 5000 | Permitir acceso en red privada. |
| Suricata no muestra alertas | No existe `eve.json` | Generar evento demo o configurar Suricata real. |
| Render no captura trafico | Limitacion del hosting | Usar Render solo como demostracion. |

