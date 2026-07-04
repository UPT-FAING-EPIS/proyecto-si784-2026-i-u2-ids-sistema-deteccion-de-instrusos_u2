---
name: trafficwatch-ids-review
description: Skill específica para revisar, implementar, probar y documentar TrafficWatch IDS, un sistema académico de detección de intrusos con Python, Flask, Scapy, dashboard web, respuesta activa controlada, Suricata/IPS, scripts de Windows y despliegue demo en Render. Úsala para cambios en reglas IDS, alertas, tráfico clasificado, dashboard, red local, bloqueo temporal, APIs Flask, pruebas, empaquetado, documentación o compatibilidad Render/local.
---

# TrafficWatch IDS Review

## Propósito

Usa esta skill para trabajar dentro del repositorio TrafficWatch IDS con contexto de seguridad, red local, dashboard, despliegue académico y compatibilidad Windows/Render.

La prioridad es mantener el sistema útil para laboratorio, demostrable en Render y seguro para pruebas controladas. No conviertas funciones de simulación o defensa en acciones ofensivas ni automatices acciones de red sin autorización explícita del usuario.

## Cuándo Usarla

Activa esta skill cuando la solicitud mencione o afecte:

- Reglas de detección IDS, clasificación de tráfico, falsos positivos o umbrales.
- Alertas, incidentes, historial, exportación CSV/JSON o agregación del dashboard.
- Botones del dashboard, JavaScript, estilos, navegación o consumo de APIs.
- Bloqueo temporal de IP, Firewall de Windows, respuesta activa o modo prueba.
- Red local, escaneo de equipos, laboratorio de 100 equipos, Nmap, Scapy o Suricata.
- Ejecución local en Windows, empaquetado, instaladores o scripts `.bat`/`.ps1`.
- Despliegue en Render, PostgreSQL, variables de entorno o limitaciones de hosting.
- Pruebas automatizadas, documentación académica, README o informes.

## Primer Paso

1. Lee `README.md`, `config.json` y los archivos directamente relacionados con la solicitud.
2. Revisa `tests/` antes de modificar detección, almacenamiento, respuesta activa, APIs o dashboard.
3. Verifica si el cambio aplica a ejecución local, demo Render o ambos.
4. Trata `logs/` como datos de ejecución. No dependas de logs reales versionados ni los conviertas en fixtures.
5. Antes de tocar red, firewall, instaladores o capturas reales, confirma que el usuario lo pidió explícitamente.

## Mapa Del Proyecto

- `main.py`: arranque local del IDS. Carga configuración, detecta red, inicia captura y actualiza estado.
- `src/analyzer.py`: reglas IDS para escaneo de puertos, ICMP flood, SYN flood, fuerza bruta, alta frecuencia, puertos sospechosos y puertos raros.
- `src/alert_manager.py`: creación de alertas, cooldown, categorías, persistencia y metadatos de respuesta.
- `src/storage.py`: lectura/escritura JSON con límite de registros y tolerancia a corrupción.
- `src/network_utils.py`: detección de red en Windows y comandos sugeridos.
- `src/network_scanner.py`: escaneo controlado de red local para inventario del dashboard.
- `src/response_actions.py`: respuesta activa con Firewall de Windows y bloqueo temporal conservador.
- `src/real_scan.py`: validación de objetivos y construcción/uso controlado de escaneos reales.
- `src/suricata_integration.py`: estado de Suricata, eventos EVE, reglas, planes IPS y comandos sugeridos.
- `web/app.py`: rutas Flask, APIs, simulación, incidentes, exportaciones, red local, Suricata, IPS y Render.
- `web/templates/dashboard.html`: dashboard principal, navegación, tablas, botones y consumo de APIs.
- `web/templates/attack_lab.html`: laboratorio controlado para simulaciones.
- `suricata/local.rules`: reglas locales de Suricata.
- `config.json`: umbrales, rutas de logs, ventana de incidentes, límites de red, Suricata y respuesta activa.
- `tests/`: pruebas de analizador, alertas, almacenamiento, red, APIs y respuesta activa.
- Scripts Windows: `INICIAR_TRAFFICWATCH.bat`, `setup_windows.ps1`, instalador, empaquetado y ayudantes de administrador.
- `render.yaml` y `runtime.txt`: despliegue de demostración en Render.

## Reglas De Trabajo

- Prefiere cambios pequeños, claros y enfocados.
- Mantén umbrales y límites configurables en `config.json`; evita constantes rígidas de seguridad.
- Conserva nombres de alerta consistentes entre analizador, simulador, dashboard, respuesta activa, Suricata y pruebas.
- Agrega o actualiza pruebas cuando cambies reglas IDS, formatos de alerta, respuesta activa, APIs o comportamiento del dashboard.
- Mantén separación estricta:
  - Local Windows: captura real, Scapy, firewall, Suricata, Nmap y escaneo de red.
  - Render: dashboard, simulaciones, historial, gráficos y demostraciones seguras.
- No ejecutes escaneos reales, captura de paquetes, Suricata, Nmap, cambios de firewall, instaladores o scripts de administrador salvo solicitud explícita.
- Si una función puede bloquear una IP, debe ser manual, visible para el usuario, temporal, reversible y validada.
- Para laboratorios grandes, evita una fila por paquete cuando sea mejor agrupar por incidente, IP, tipo, puerto y ventana temporal.
- Conserva textos en español del dashboard y documentación, salvo que la tarea pida traducción.
- No agregues al commit archivos generados, `dist/`, `build/`, `__pycache__/`, logs reales, capturas locales ni rutas específicas de una máquina.

## Seguridad Y Alcance Permitido

Este proyecto es defensivo y académico. Es correcto ayudar con:

- Simulaciones controladas dentro de laboratorio autorizado.
- Detección, visualización, clasificación y explicación de eventos.
- Bloqueo temporal defensivo desde el equipo donde corre el IDS.
- Mejoras de escalabilidad para redes locales autorizadas.
- Validaciones que eviten acciones peligrosas por accidente.

Evita:

- Instrucciones para atacar terceros o evadir defensas.
- Automatizar bloqueos masivos sin confirmación.
- Ejecutar comandos que cambien firewall/red sin autorización explícita.
- Convertir pruebas de laboratorio en herramientas ofensivas reutilizables contra redes externas.

## Flujo Recomendado Por Tipo De Tarea

### Cambios En Detección

1. Revisa `src/analyzer.py`, `config.json` y pruebas relacionadas.
2. Verifica que el tipo de alerta exista o se refleje en dashboard/simulador/exportaciones.
3. Cuida cooldown y agrupación para no generar ruido excesivo.
4. Prueba con casos pequeños y deterministas.

### Cambios En Dashboard

1. Revisa `web/templates/dashboard.html` y los endpoints usados en `web/app.py`.
2. Asegura que el JavaScript soporte campos faltantes o respuestas vacías.
3. Mantén actualización automática sin duplicar filas innecesariamente.
4. Verifica renderizado con `app.test_client()` cuando baste.

### Cambios En Respuesta Activa

1. Revisa `src/response_actions.py`, `web/app.py`, `config.json` y pruebas.
2. Mantén duración configurable y por defecto conservadora para laboratorio.
3. Valida IPs, evita rangos peligrosos y registra la acción de forma comprensible.
4. No ejecutes firewall real si solo necesitas probar construcción de comandos.

### Cambios En Red Local

1. Limita el alcance a la red local detectada o configurada.
2. Usa timeouts, caché y límite de hosts/trabajadores.
3. Para laboratorios de hasta 100 equipos, prioriza escaneo acotado, resultados cacheados y reintentos controlados.
4. No dependas de nombres DNS/reverse lookup para que el dashboard funcione.

### Cambios En Render

1. Recuerda que Render no puede capturar tráfico real ni modificar firewall local.
2. Usa variables de entorno y rutas portables.
3. Evita depender de Windows, Npcap, Suricata local o permisos de administrador.
4. Mantén simulaciones y vistas demo funcionales.

## Validación

Usa la validación más específica posible:

```powershell
python -m json.tool config.json
python -m compileall src web
python -m pytest
```

Pruebas enfocadas útiles:

```powershell
python -m pytest tests/test_traffic_classification.py
python -m pytest tests/test_alert_manager.py
python -m pytest tests/test_response_actions.py
python -m pytest tests/test_network_utils.py
```

Prueba rápida para dashboard/API:

```powershell
python -c "from web.app import app; c=app.test_client(); assert c.get('/').status_code == 200; assert c.get('/api/status').status_code == 200; print('OK')"
```

Si `pytest` no está instalado, informa el bloqueo y ejecuta al menos:

```powershell
python -m json.tool config.json
python -m compileall src web
```

## Checklist De Revisión

Antes de terminar, revisa:

- ¿El cambio rompe `config.json` o introduce claves no documentadas?
- ¿Los tipos de alerta siguen coincidiendo entre backend, frontend, simulador y pruebas?
- ¿El dashboard tolera listas vacías, campos nulos y errores de API?
- ¿La agrupación de incidentes evita ruido sin ocultar eventos importantes?
- ¿La respuesta activa sigue siendo manual, temporal y reversible?
- ¿Render sigue funcionando aunque no existan herramientas locales de red?
- ¿Las pruebas no dependen de red real, logs reales ni permisos de administrador?
- ¿No se agregaron archivos generados o datos locales al commit?

## Respuesta Al Usuario

Al finalizar una tarea, explica en español:

- Qué se revisó o cambió.
- Qué validación se ejecutó y su resultado.
- Si aplica, qué queda pendiente para probar en Windows, red local o Render.
- Si hubo una decisión de seguridad, explícalala de forma simple y práctica.
