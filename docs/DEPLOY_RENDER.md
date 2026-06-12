# Despliegue en Render

TrafficWatch IDS puede publicarse en Render como dashboard web.

## Que funciona en Render

- Dashboard Flask.
- Simulador de alertas.
- Historial, filtros, graficos y exportaciones.
- Vista Suricata IPS en modo demostracion.
- Reglas y comandos sugeridos para laboratorio.

## Que no funciona en Render

Render corre en la nube. Por eso no puede:

- Capturar la red Wi-Fi local del usuario.
- Usar Npcap.
- Ejecutar Suricata Windows.
- Bloquear YouTube o IPs de una red local.
- Escanear dispositivos de tu LAN real.

Para captura real, ejecuta `main.py`, Suricata o el lanzador Windows en una maquina dentro de tu red.

## Archivos de despliegue

- `render.yaml`: configuracion del servicio web.
- `runtime.txt`: version de Python.
- `requirements.txt`: dependencias, incluyendo `gunicorn`.

## Configuracion automatica con render.yaml

Al conectar el repositorio, Render puede leer:

```yaml
buildCommand: pip install -r requirements.txt
startCommand: gunicorn web.app:app --bind 0.0.0.0:$PORT
```

## Pasos en Render

1. Sube el proyecto a GitHub.
2. Entra a https://render.com/.
3. Selecciona `New` > `Web Service`.
4. Conecta tu repositorio.
5. Usa estos valores si Render no los detecta:

```text
Runtime: Python
Build Command: pip install -r requirements.txt
Start Command: gunicorn web.app:app --bind 0.0.0.0:$PORT
```

6. Crea el servicio.
7. Al terminar, Render entregara una URL parecida a:

```text
https://trafficwatch-ids.onrender.com
```

## Nota sobre logs

En planes gratuitos, los archivos escritos en disco pueden perderse cuando el servicio
se reinicia o redepliega. Para una demo esta bien; para produccion conviene usar una
base de datos o un disco persistente.
