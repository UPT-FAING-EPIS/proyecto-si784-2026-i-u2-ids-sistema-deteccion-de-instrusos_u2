# Estandares de Programacion

## Proyecto

**TrafficWatch IDS**  
Version del documento: **1.0**  
Fecha: **2026-07-04**

## 1. Objetivo

Definir reglas de codificacion, organizacion, seguridad y validacion para mantener TrafficWatch IDS consistente, mantenible y seguro para un entorno academico de ciberseguridad defensiva.

## 2. Principios generales

- Mantener cambios pequenos, claros y enfocados.
- Priorizar codigo legible sobre abstracciones innecesarias.
- Respetar la separacion entre ejecucion local real y demostracion web en Render.
- No ejecutar acciones reales de red, firewall, Nmap o Suricata sin autorizacion explicita.
- Mantener las reglas IDS configurables desde `config.json`.
- Evitar subir logs reales, capturas, builds o rutas especificas de una computadora.

## 3. Organizacion del proyecto

| Carpeta/archivo | Uso |
|---|---|
| `main.py` | Entrada local del IDS. |
| `src/` | Logica principal: captura, analisis, alertas, red, respuesta activa y Suricata. |
| `web/` | Dashboard Flask, APIs y templates HTML. |
| `tests/` | Pruebas automatizadas. |
| `docs/` | Documentacion academica y manuales. |
| `suricata/` | Reglas locales de Suricata. |
| `installer/` | Archivos de instalador Windows. |
| `logs/` | Datos de ejecucion generados localmente. No versionar logs reales. |

## 4. Estilo Python

### 4.1 Nombres

| Elemento | Estilo | Ejemplo |
|---|---|---|
| Variables | `snake_case` | `source_ip` |
| Funciones | `snake_case` | `scan_local_network()` |
| Clases | `PascalCase` | `AlertStorage` |
| Constantes | `UPPER_SNAKE_CASE` | `DEFAULT_PORT_RANGE` |
| Archivos | `snake_case.py` | `network_scanner.py` |

### 4.2 Reglas de codigo

- Usar funciones cortas con una responsabilidad clara.
- Preferir diccionarios simples para estructuras JSON del dashboard.
- Validar entradas de usuario con `ipaddress`, listas permitidas o conversiones controladas.
- Capturar excepciones esperadas y devolver mensajes claros al dashboard.
- No silenciar errores importantes sin registrar o devolver informacion util.
- Evitar rutas absolutas de una maquina local.
- Usar `Path` para rutas de archivos.

Ejemplo recomendado:

```python
try:
    source_ip = str(ipaddress.ip_address(raw_ip.strip()))
except ValueError:
    return jsonify({"status": "error", "message": "Ingresa una IP valida."}), 400
```

## 5. Estandar de configuracion

- Todo umbral IDS debe estar en `config.json`.
- No fijar directamente en codigo valores como cantidad de paquetes, ventanas de tiempo o puertos configurables.
- Al agregar una regla nueva, documentar:
  - Campo en `config.json`.
  - Tipo de alerta generado.
  - Evidencia usada.
  - Prueba automatizada o prueba manual.

Ejemplo de regla:

```json
"icmp_flood": {
    "enabled": true,
    "time_window_seconds": 5,
    "packet_threshold": 20
}
```

## 6. Estandar de alertas

Toda alerta debe mantener una estructura compatible con el dashboard:

```json
{
    "timestamp": "2026-07-04 10:15:20",
    "level": "ALTO",
    "category": "IDS",
    "type": "FUERZA_BRUTA_SSH",
    "source_ip": "192.168.1.50",
    "target_ip": "192.168.1.33",
    "target_port": 22,
    "evidence_count": 8,
    "description": "Intentos repetidos hacia SSH"
}
```

Reglas:

- `type` debe ser consistente entre analizador, simulador, dashboard y pruebas.
- `level` debe usar `BAJO`, `MEDIO` o `ALTO`.
- `description` debe ser legible para usuario final.
- Si hay respuesta activa, usar `response_action`.
- Evitar guardar datos sensibles innecesarios.

## 7. Estandar de APIs Flask

- Las rutas deben devolver JSON en APIs `/api/*`.
- En errores, devolver:

```json
{
    "status": "error",
    "message": "Descripcion del problema"
}
```

- Usar codigos HTTP adecuados:
  - `200` para exito.
  - `400` para entrada invalida.
  - `404` para tipo no soportado.
  - `429` para operacion ocupada.
  - `500` para fallas internas controladas.
- El JavaScript debe tolerar listas vacias y campos faltantes.
- No asumir que `logs/` tiene datos previos.

## 8. Estandar de frontend

- Mantener textos en espanol.
- No romper las secciones existentes del dashboard.
- Toda nueva vista debe tener:
  - Boton o entrada clara.
  - Estado de carga o mensaje de resultado.
  - Manejo de error.
  - Consumo de API existente o nueva ruta documentada.
- Evitar duplicar filas durante actualizaciones automaticas.
- No depender de campos obligatorios si el backend puede devolver `null`.

## 9. Seguridad

- No agregar funciones ofensivas.
- No escanear redes externas.
- No ejecutar Nmap real sin accion explicita del usuario.
- No ejecutar Suricata real ni modificar firewall sin autorizacion.
- La respuesta activa debe ser:
  - Manual o recomendada por defecto.
  - Temporal.
  - Validada por IP.
  - Reversible.
  - Registrada en alertas.
- Render debe mantenerse como demo sin captura real ni firewall local.

## 10. Pruebas

Usar pruebas enfocadas segun el cambio:

```powershell
python -m pytest tests/test_traffic_classification.py
python -m pytest tests/test_alert_manager.py
python -m pytest tests/test_response_actions.py
python -m pytest tests/test_network_utils.py
python -m pytest tests/test_storage.py
```

Para validacion general:

```powershell
python -m json.tool config.json
python -m compileall src web
python -m pytest
```

Para dashboard/API:

```powershell
python -c "from web.app import app; c=app.test_client(); assert c.get('/').status_code == 200; assert c.get('/api/status').status_code == 200; print('OK')"
```

## 11. Documentacion

Cuando se agregue una funcion nueva, revisar si corresponde actualizar:

- `README.md`
- `docs/FD03-Informe-Especificación Requerimientos.md`
- `docs/FD04-Informe-Arquitectura de Software.md`
- `docs/FD05-Informe-Proyecto Final.md`
- `docs/DICCIONARIO_DATOS.md`
- `docs/MANUAL_USUARIO.md`

La documentacion debe distinguir:

- Funcion local real.
- Funcion demo en Render.
- Funcion simulada.
- Funcion que requiere administrador.

## 12. Git y repositorio

- No subir `logs/`, `dist/`, `build/`, `__pycache__/`, instaladores generados ni capturas locales.
- Hacer commits con mensajes claros.
- Antes de subir:

```powershell
git status
git diff
```

Mensaje recomendado:

```text
docs: actualizar manuales del proyecto
```

