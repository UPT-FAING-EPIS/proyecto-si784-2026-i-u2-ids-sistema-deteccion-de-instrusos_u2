# Manual de Usuario

## Proyecto

**TrafficWatch IDS**  
Version del documento: **1.0**  
Fecha: **2026-07-04**

## 1. Objetivo

Guiar al usuario en el uso de TrafficWatch IDS para monitorear trafico, revisar alertas, usar el dashboard, ejecutar pruebas controladas, consultar Suricata IPS y entender las diferencias entre modo local y demo Render.

## 2. Recomendaciones de seguridad

- Usar el sistema solo en redes propias, laboratorios academicos o entornos autorizados.
- No escanear redes de terceros.
- No ejecutar Nmap, Suricata ni cambios de firewall sin permiso.
- Ejecutar captura real solo en una PC autorizada.
- Recordar que Render es demo; no captura la red local del usuario.

## 3. Formas de uso

| Modo | URL principal | Uso |
|---|---|---|
| Local | `http://127.0.0.1:5000/` | Uso completo desde la misma PC. |
| Red local | `http://<IP-DE-LA-PC>:5000/` | Acceso desde otro equipo autorizado. |
| Attack Lab | `http://<IP-DE-LA-PC>:5000/attack-lab` | Generar eventos remotos controlados. |
| Render | URL publica de Render | Demo web sin captura real. |

## 4. Inicio recomendado

### Paso 1: Iniciar dashboard

Ejecutar:

```text
abrir_cmd_proyecto.bat
```

O manualmente:

```powershell
python run_dashboard.py
```

Abrir:

```text
http://127.0.0.1:5000/
```

### Paso 2: Iniciar IDS real

Ejecutar como administrador:

```text
abrir_powershell_admin.bat
```

O manualmente en PowerShell administrador:

```powershell
python main.py
```

### Paso 3: Abrir consola de pruebas

```text
abrir_powershell_pruebas.bat
```

## 5. Secciones del dashboard

| Seccion | Funcion |
|---|---|
| Dashboard | Muestra resumen e incidentes activos. |
| Tipos de trafico | Explica trafico entrante, saliente, local y gateway. |
| Trafico clasificado | Lista ultimos paquetes observados. |
| Estado IDS | Muestra si el IDS esta activo, red, gateway e interfaz. |
| Graficos | Presenta alertas por tipo, nivel, minuto y top IPs. |
| Historial | Permite revisar, filtrar, paginar y exportar alertas. |
| Reglas IDS | Resume las reglas de deteccion disponibles. |
| Escaneo de red | Lista dispositivos activos detectados en la red local. |
| Suricata IPS | Muestra eventos EVE, reglas, comandos y politicas IPS. |

## 6. Interpretar alertas

Campos importantes:

| Campo | Significado |
|---|---|
| Fecha | Momento del evento. |
| Nivel | Severidad: `BAJO`, `MEDIO`, `ALTO`. |
| Tipo | Regla que genero la alerta. |
| IP origen | Equipo que genero el evento. |
| IP destino | Equipo o recurso afectado. |
| Puerto | Servicio o puerto relacionado. |
| Descripcion | Explicacion resumida del evento. |
| Respuesta | Accion recomendada o aplicada. |

Tipos comunes:

| Tipo | Interpretacion |
|---|---|
| `ESCANEO_DE_PUERTOS` | Una IP intento acceder a muchos puertos. |
| `SYN_FLOOD` | Muchos paquetes SYN desde una IP. |
| `ICMP_FLOOD` | Muchos paquetes ICMP desde una IP. |
| `FUERZA_BRUTA_SSH` | Intentos repetidos contra SSH. |
| `PUERTO_RARO` | Conexion hacia puerto poco comun. |
| `ALTA_FRECUENCIA_CONEXIONES` | Muchas conexiones TCP en poco tiempo. |

## 7. Historial

En la seccion Historial se puede:

- Revisar alertas anteriores.
- Filtrar por IP.
- Filtrar por tipo.
- Cambiar paginas.
- Exportar alertas.
- Borrar historial.

Exportaciones disponibles:

```text
/api/export/alerts.json
/api/export/alerts.csv
```

## 8. Trafico clasificado

La seccion muestra los ultimos eventos registrados en `logs/traffic.json`.

Clasificaciones:

| Direccion | Significado |
|---|---|
| `ENTRANTE` | Trafico hacia el equipo local desde fuera de la red local. |
| `SALIENTE` | Trafico desde el equipo local hacia fuera de la red local. |
| `LOCAL` | Trafico entre equipos de la misma red. |
| `GATEWAY` | Trafico relacionado con la puerta de enlace. |
| `EXTERNO` | Trafico no clasificado como local. |
| `REMOTO_LAB` | Trafico controlado desde Attack Lab. |

## 9. Estado IDS

La seccion Estado IDS muestra:

- Si el IDS esta activo.
- Interfaz usada.
- IP local.
- Gateway.
- Red detectada.
- Ultima alerta.
- Ultimo trafico.
- Edad del ultimo latido.

Si `ids_active` aparece inactivo, revisar que `python main.py` siga ejecutandose como administrador.

## 10. Graficos

La seccion Graficos ayuda a identificar:

- Tipos de alerta mas frecuentes.
- Niveles de severidad.
- Alertas por minuto.
- IPs con mas actividad sospechosa.

## 11. Escaneo de red

La seccion de escaneo de red permite detectar dispositivos activos.

Antes de usar:

- Confirmar que se esta en una red autorizada.
- Evitar redes de terceros.
- Respetar limites de `config.json`.

El resultado muestra:

- IP.
- MAC si esta disponible.
- Hostname si se habilita resolucion.
- Rol: este equipo, gateway o dispositivo.
- Estado.

## 12. Escaneo Nmap local

El dashboard permite ejecutar Nmap de forma validada.

Rangos permitidos:

```text
1-100
1-1000
22,23,53,80,443,3389
31337,6667,9001
```

Reglas:

- El objetivo debe ser una IP valida.
- El objetivo debe pertenecer a la red local detectada.
- Nmap debe estar instalado.
- Usar solo contra equipos autorizados.

## 13. Attack Lab

URL:

```text
http://<IP-DE-LA-PC>:5000/attack-lab
```

Sirve para que otro equipo autorizado genere eventos controlados.

Acciones disponibles:

- Simular escaneo.
- Generar trafico equivalente a fuerza bruta.
- Generar rafagas controladas.
- Generar trafico hacia puerto raro.
- Generar alta frecuencia de conexiones.

El sistema registra la IP del equipo que realizo la solicitud.

## 14. Suricata IPS

La vista Suricata IPS permite:

- Consultar estado de `logs/suricata/eve.json`.
- Ver alertas EVE normalizadas.
- Generar una alerta demo.
- Crear comandos de bloqueo.
- Crear reglas Suricata `drop`.
- Generar planes IPS inline con NFQUEUE.
- Guardar politicas IPS.

Importante:

- La vista puede funcionar en modo demo.
- Suricata real debe configurarse localmente.
- Las reglas generadas no deben aplicarse sin revisar.

## 15. Respuesta activa

El dashboard puede mostrar el boton:

```text
Bloquear 2 min
```

Este boton solo aplica para alertas SSH validas:

- `FUERZA_BRUTA_SSH`
- `TRAFICO_REAL_LAB_FUERZA_BRUTA_SSH`

Condiciones:

- Debe existir una alerta SSH registrada para esa IP.
- El usuario debe confirmar la accion.
- TrafficWatch debe ejecutarse con permisos suficientes.
- El bloqueo afecta solo a la PC donde corre TrafficWatch.
- La accion es temporal.

## 16. Uso en Render

Render sirve para demostracion.

Puede:

- Mostrar dashboard.
- Ejecutar simulaciones.
- Mostrar graficos.
- Mostrar historial demo.
- Abrir Attack Lab.

No puede:

- Capturar paquetes reales de tu red.
- Ejecutar Nmap real en tu red local.
- Ejecutar Suricata real sobre tu red.
- Modificar Windows Firewall.

## 17. Pruebas sugeridas

Ver ejemplos segun red detectada:

```powershell
python -m src.network_utils
```

Escaneo de puertos:

```powershell
nmap -p 1-100 <gateway>
```

Fuerza bruta simulada:

```powershell
python simular_fuerza_bruta.py --port 21 --count 10
python simular_fuerza_bruta.py --port 22 --count 10
python simular_fuerza_bruta.py --port 3389 --count 10
```

Alta frecuencia:

```powershell
python simular_fuerza_bruta.py --port 80 --count 120 --delay 0.01
```

Puerto raro:

```powershell
nmap -p 31337 <gateway>
```

## 18. Exportacion de evidencias

Alertas:

```text
/api/export/alerts.json
/api/export/alerts.csv
```

Trafico:

```text
/api/export/traffic.json
/api/export/traffic.csv
```

Los archivos exportados pueden usarse como evidencia academica, evitando incluir datos sensibles de terceros.

## 19. Cierre del sistema

Para detener:

1. Cerrar la ventana donde corre `python main.py`.
2. Cerrar la ventana donde corre `python run_dashboard.py`.
3. Verificar que no queden terminales de prueba ejecutandose.

## 20. Problemas frecuentes

| Problema | Posible causa | Solucion |
|---|---|---|
| No aparecen alertas | El IDS no esta capturando | Ejecutar `python main.py` como administrador. |
| Dashboard vacio | No hay logs aun | Ejecutar pruebas controladas. |
| No abre localhost | Dashboard apagado | Ejecutar `python run_dashboard.py`. |
| Otra PC no entra | Firewall bloquea puerto 5000 | Permitir acceso en red privada. |
| Boton de bloqueo falla | Falta administrador o no es Windows | Ejecutar con permisos y revisar mensaje. |
| Nmap falla | No esta instalado o objetivo invalido | Instalar Nmap y usar IP local autorizada. |
| Suricata sin alertas | No existe `eve.json` | Generar evento demo o configurar Suricata. |

