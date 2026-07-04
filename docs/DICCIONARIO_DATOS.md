# Diccionario de Datos

## Proyecto

**TrafficWatch IDS**  
Version del documento: **1.0**  
Fecha: **2026-07-04**

## 1. Objetivo

Este documento describe las estructuras de datos principales usadas por TrafficWatch IDS. El sistema almacena informacion en archivos JSON dentro de `logs/`, usa `config.json` como archivo de configuracion y expone datos mediante APIs Flask.

Los archivos de `logs/` son datos de ejecucion. No deben usarse como codigo fuente ni subirse al repositorio con informacion real de red.

## 2. Archivos de datos

| Archivo | Tipo | Responsable | Descripcion |
|---|---|---|---|
| `config.json` | Objeto JSON | Usuario/desarrollador | Configuracion general, reglas IDS, Suricata, escaneo y respuesta activa. |
| `logs/alerts.json` | Lista JSON | `src/alert_manager.py`, `web/app.py` | Historial de alertas IDS, simulaciones y acciones de respuesta. |
| `logs/traffic.json` | Lista JSON | `src/analyzer.py`, `web/app.py` | Ultimos eventos de trafico clasificado. |
| `logs/status.json` | Objeto JSON | `src/status_manager.py` | Estado operativo del IDS local. |
| `logs/policies.json` | Lista JSON | `web/app.py` | Politicas IPS generadas desde el dashboard. |
| `logs/suricata/eve.json` | JSON por linea | Suricata / demo | Eventos EVE reales o de demostracion. |
| `suricata/local.rules` | Texto | Usuario/desarrollador | Reglas locales de Suricata. |

## 3. Entidad Alerta

Archivo principal: `logs/alerts.json`  
Formato: lista de objetos.

| Campo | Tipo | Obligatorio | Ejemplo | Descripcion |
|---|---|:--:|---|---|
| `timestamp` | string | Si | `2026-07-04 10:15:20` | Fecha y hora de generacion. |
| `level` | string | Si | `ALTO` | Nivel de severidad: `BAJO`, `MEDIO`, `ALTO`. |
| `category` | string | No | `SIMULACION_LOCAL` | Categoria general de la alerta. |
| `type` | string | Si | `FUERZA_BRUTA_SSH` | Tipo de alerta IDS. |
| `source_ip` | string | Si | `192.168.1.50` | IP origen del evento. |
| `target_ip` | string | No | `192.168.1.33` | IP destino o recurso afectado. |
| `target_port` | int/string/null | No | `22` | Puerto objetivo o etiqueta de servicio. |
| `evidence_count` | int | No | `8` | Cantidad de eventos que sustentan la alerta. |
| `description` | string | Si | `8 intentos hacia SSH...` | Explicacion legible del evento. |
| `response_action` | object/null | No | `{...}` | Accion recomendada o aplicada por respuesta activa. |
| `duration_seconds` | int | No | `3` | Duracion declarada en eventos de laboratorio. |
| `mode` | string | No | `CONTROLADO` | Modo de prueba de laboratorio. |

Tipos principales de alerta:

| Tipo | Origen | Descripcion |
|---|---|---|
| `ESCANEO_DE_PUERTOS` | `src/analyzer.py` | Una IP accede a varios puertos en una ventana corta. |
| `SYN_FLOOD` | `src/analyzer.py` | Exceso de paquetes TCP SYN desde una misma IP. |
| `ICMP_FLOOD` | `src/analyzer.py` | Exceso de paquetes ICMP desde una misma IP. |
| `PUERTO_SOSPECHOSO` | `src/analyzer.py` | Conexion hacia puertos sensibles configurados. |
| `PUERTO_RARO` | `src/analyzer.py` | Conexion hacia puertos poco comunes configurados. |
| `ALTA_FRECUENCIA_CONEXIONES` | `src/analyzer.py` | Muchas conexiones TCP desde una misma IP. |
| `FUERZA_BRUTA_FTP` | `src/analyzer.py` | Intentos repetidos hacia FTP. |
| `FUERZA_BRUTA_SSH` | `src/analyzer.py` | Intentos repetidos hacia SSH. |
| `FUERZA_BRUTA_TELNET` | `src/analyzer.py` | Intentos repetidos hacia Telnet. |
| `FUERZA_BRUTA_RDP` | `src/analyzer.py` | Intentos repetidos hacia RDP. |
| `ESCANEO_REAL_NMAP` | `web/app.py` | Escaneo Nmap solicitado desde el dashboard. |
| `TRAFICO_REAL_LAB_*` | `web/app.py` | Trafico remoto controlado desde Attack Lab. |
| `POLITICA_BLOQUEO_YOUTUBE` | `web/app.py` | Politica IPS generada para una IP. |
| `BLOQUEO_TEMPORAL_SSH` | `web/app.py` | Bloqueo temporal aplicado a una IP con alerta SSH. |

## 4. Entidad Trafico Clasificado

Archivo principal: `logs/traffic.json`  
Formato: lista de objetos.  
Limite actual: `20` registros en el dashboard.

| Campo | Tipo | Obligatorio | Ejemplo | Descripcion |
|---|---|:--:|---|---|
| `timestamp` | string | Si | `2026-07-04 10:15:20` | Fecha y hora del evento. |
| `direction` | string | Si | `LOCAL` | Clasificacion: `ENTRANTE`, `SALIENTE`, `LOCAL`, `GATEWAY`, `EXTERNO`, `REMOTO_LAB`, `DESCONOCIDO`. |
| `protocol` | string | Si | `TCP` | Protocolo detectado: `TCP`, `ICMP`, `IP`, `HTTP`. |
| `source_ip` | string | Si | `192.168.1.20` | IP origen. |
| `destination_ip` | string | Si | `192.168.1.1` | IP destino. |
| `source_port` | int/null | No | `50421` | Puerto origen si aplica. |
| `destination_port` | int/null | No | `80` | Puerto destino si aplica. |
| `flags` | string | No | `S` | Flags TCP o etiqueta de laboratorio. |

## 5. Entidad Estado IDS

Archivo principal: `logs/status.json`  
Formato: objeto JSON.

| Campo | Tipo | Ejemplo | Descripcion |
|---|---|---|---|
| `ids_active` | boolean | `true` | Indica si el IDS esta activo. |
| `started_at` | string | `2026-07-04 10:00:00` | Hora de inicio del IDS. |
| `last_heartbeat` | string | `2026-07-04 10:01:00` | Ultima actualizacion de vida. |
| `stopped_at` | string | `2026-07-04 10:30:00` | Hora de parada, si aplica. |
| `interface` | string | `Wi-Fi` | Interfaz usada por Scapy. |
| `local_ip` | string | `192.168.1.33` | IP local detectada. |
| `gateway` | string | `192.168.1.1` | Puerta de enlace. |
| `network` | string | `192.168.1.0/24` | Red detectada. |
| `heartbeat_age_seconds` | int/null | `4` | Calculado por `/api/status`. |
| `last_alert` | object/null | `{...}` | Ultima alerta registrada. |
| `last_traffic` | object/null | `{...}` | Ultimo trafico clasificado. |

## 6. Entidad Politica IPS

Archivo principal: `logs/policies.json`  
Formato: lista de objetos.

| Campo | Tipo | Ejemplo | Descripcion |
|---|---|---|---|
| `timestamp` | string | `2026-07-04 10:15:20` | Fecha de generacion. |
| `type` | string | `BLOQUEO_YOUTUBE` | Tipo de politica. |
| `target_ip` | string | `192.168.1.50` | IP a la que se aplicaria la politica. |
| `domains` | list[string] | `["youtube.com"]` | Dominios asociados. |
| `status` | string | `GENERADA_PENDIENTE_DE_APLICAR` | Estado de la politica. |
| `apply_at` | string | `Gateway, router...` | Lugar sugerido de aplicacion. |
| `note` | string | `Estas reglas...` | Observacion de uso. |
| `suricata_rules` | list[string] | `["drop tls ..."]` | Reglas Suricata generadas. |

## 7. Entidad Suricata Normalizada

Origen: `logs/suricata/eve.json`  
Funcion: `normalize_suricata_alert()`.

| Campo | Tipo | Ejemplo | Descripcion |
|---|---|---|---|
| `timestamp` | string | `2026-07-04T10:15:20` | Fecha del evento EVE. |
| `signature` | string | `TrafficWatch IPS demo fuerza bruta SSH` | Firma de Suricata. |
| `category` | string | `Attempted Administrator Privilege Gain` | Categoria Suricata. |
| `severity` | int/string | `1` | Severidad de Suricata. |
| `action` | string | `blocked` | Accion declarada por la alerta. |
| `verdict` | string | `drop` | Accion final o veredicto. |
| `protocol` | string | `TCP` | Protocolo. |
| `source_ip` | string | `10.10.10.44` | IP origen. |
| `source_port` | int/string | `52122` | Puerto origen. |
| `destination_ip` | string | `192.168.1.33` | IP destino. |
| `destination_port` | int/string | `22` | Puerto destino. |
| `sid` | int/string | `9000001` | Signature ID. |
| `raw` | object | `{...}` | Evento EVE original. |

## 8. Entidad Respuesta Activa

Campo embebido: `response_action`.

| Campo | Tipo | Ejemplo | Descripcion |
|---|---|---|---|
| `action` | string | `BLOQUEO_TEMPORAL_IP` | Tipo de accion. |
| `status` | string | `RECOMENDADO` | Estado: `RECOMENDADO`, `NO_APLICADO`, `BLOQUEO_APLICADO`. |
| `reason` | string | `Alerta FUERZA_BRUTA_SSH...` | Motivo. |
| `source_ip` | string | `192.168.1.50` | IP afectada. |
| `duration_minutes` | int | `2` | Duracion del bloqueo. |
| `block_until` | string | `2026-07-04 10:17:20` | Fecha estimada de desbloqueo. |
| `windows_rule_name` | string | `TrafficWatch IDS Auto Block ...` | Nombre de regla Windows Firewall. |
| `windows_block_command` | string | `New-NetFirewallRule ...` | Comando de bloqueo. |
| `windows_unblock_command` | string | `Remove-NetFirewallRule ...` | Comando de desbloqueo. |
| `note` | string | `Ejecuta el comando...` | Instruccion de seguridad. |

## 9. Configuracion Principal

Archivo: `config.json`.

| Seccion | Campo | Tipo | Descripcion |
|---|---|---|---|
| General | `interface` | string | Interfaz para captura; `auto` usa deteccion automatica. |
| Red | `network.auto_detect` | boolean | Habilita deteccion automatica de red. |
| Red | `network.scan_target` | string | Objetivo sugerido para pruebas, normalmente `gateway`. |
| Escaneo | `network_scan.timeout_ms` | int | Timeout por host. |
| Escaneo | `network_scan.max_hosts` | int | Maximo de hosts a revisar. |
| Escaneo | `network_scan.max_workers` | int | Hilos paralelos maximos. |
| Escaneo | `network_scan.cache_seconds` | int | Cache de resultados. |
| Dashboard | `dashboard.incident_window_seconds` | int | Ventana para agrupar incidentes. |
| Logs | `log_file` | string | Ruta de alertas. |
| Logs | `status_file` | string | Ruta de estado. |
| Alertas | `alert_cooldown_seconds` | int | Tiempo para evitar alertas repetidas. |
| Trafico | `traffic_monitor.enabled` | boolean | Activa registro de trafico. |
| Trafico | `traffic_monitor.max_records` | int | Limite de trafico guardado. |
| Suricata | `suricata.eve_log_file` | string | Ruta EVE JSON. |
| Suricata | `suricata.local_rules_file` | string | Ruta de reglas locales. |
| Respuesta | `active_response.enabled` | boolean | Activa generacion de respuesta. |
| Respuesta | `active_response.auto_block_enabled` | boolean | Permite intentar bloqueo automatico. |
| Respuesta | `active_response.block_minutes` | int | Duracion del bloqueo. |

## 10. APIs Principales

| Ruta | Metodo | Devuelve/recibe |
|---|---|---|
| `/api/alerts` | GET | Lista de alertas. |
| `/api/incidents` | GET | Lista de incidentes agrupados. |
| `/api/traffic` | GET | Lista de trafico clasificado. |
| `/api/status` | GET | Estado operativo enriquecido. |
| `/api/charts` | GET | Datos agregados para graficos. |
| `/api/network/devices` | GET/POST | Dispositivos activos de red local. |
| `/api/real-scan/nmap` | POST | Resultado de Nmap local validado. |
| `/api/suricata/status` | GET | Estado de EVE y reglas locales. |
| `/api/suricata/alerts` | GET | Alertas Suricata normalizadas. |
| `/api/suricata/demo-alert` | POST | Evento demo Suricata. |
| `/api/ips/policies` | GET | Politicas IPS guardadas. |
| `/api/firewall/block-ssh-ip` | POST | Bloqueo temporal SSH validado. |
| `/api/simulate/<attack_type>` | POST | Alerta simulada local. |
| `/api/remote-attack/<attack_type>` | POST | Alerta remota simulada. |
| `/api/remote-lab-traffic/<traffic_type>` | POST | Trafico remoto controlado. |

