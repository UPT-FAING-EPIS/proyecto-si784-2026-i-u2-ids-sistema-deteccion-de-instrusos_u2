![Logo](../media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingenieria de Sistemas**

**Proyecto TrafficWatch IDS**

Curso: **Calidad y Pruebas de Software**

Docente: **MAG. Patrick Cuadros Quiroga**

Integrantes:

- **Edgar Diego Chara Apaza (2019065026)**
- **Abel Fernando Pacompia Ortiz (2023076797)**

**Tacna - Peru**

**2026**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

# Documento de Vision

Version: **2.1**

| Version | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:--:|:--:|:--:|:--:|:--:|:--|
| 1.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-04-14 | Version inicial |
| 2.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-06-09 | Actualizacion segun implementacion final |
| 2.1 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-07-04 | Actualizacion segun dashboard actual, Render, Suricata IPS y respuesta activa |

## 1. Introduccion

### 1.1 Proposito

Este documento describe la vision del sistema **TrafficWatch IDS**, una herramienta academica para monitoreo de trafico de red y deteccion de comportamientos sospechosos en tiempo real.

El documento sirve como referencia para comprender el problema, los usuarios, el alcance, las capacidades actuales y las restricciones del producto.

### 1.2 Alcance

TrafficWatch IDS esta orientado a redes locales, equipos personales y laboratorios academicos en Windows. El sistema permite capturar trafico, analizar paquetes mediante reglas IDS y visualizar alertas en un dashboard web local. Tambien cuenta con una demostracion en Render para mostrar la interfaz, simulaciones, historial y graficos sin ejecutar captura real de red.

La version actual incluye:

- Dashboard web.
- Historial de alertas.
- Filtros y paginacion.
- Graficos.
- Exportacion JSON/CSV.
- Estado operativo del IDS.
- Trafico clasificado.
- Incidentes agrupados.
- Attack Lab para trafico remoto controlado.
- Escaneo controlado de red local.
- Escaneo Nmap local validado.
- Integracion con Suricata EVE, reglas locales y planes IPS.
- Politicas IPS sugeridas y guardadas.
- Respuesta activa manual con Windows Firewall para escenarios autorizados.
- Despliegue de demostracion en Render.
- Scripts de arranque automatico.

No incluye bloqueo masivo ni mitigacion automatica sin confirmacion. Las funciones de respuesta activa son locales, temporales, defensivas y dependen de permisos del sistema operativo.

### 1.3 Definiciones

| Termino | Definicion |
|---|---|
| IDS | Sistema de deteccion de intrusos que alerta sobre actividad sospechosa. |
| IPS | Sistema de prevencion de intrusos que puede bloquear trafico. |
| Scapy | Libreria Python para captura y analisis de paquetes. |
| Flask | Framework web usado para el dashboard. |
| Nmap | Herramienta usada para pruebas autorizadas de escaneo. |
| Suricata | Motor IDS/IPS usado como referencia para eventos EVE, reglas y planes IPS. |
| Render | Plataforma usada para publicar una demo web del dashboard. |
| Attack Lab | Vista web para generar eventos controlados desde otro equipo o navegador. |
| Respuesta activa | Accion defensiva manual o recomendada, como bloqueo temporal de una IP. |
| Gateway | Puerta de enlace de la red local. |
| Alerta | Registro generado por una regla IDS. |

## 2. Posicionamiento

### 2.1 Oportunidad

Muchas redes academicas o pequenas no cuentan con herramientas simples para observar trafico y comprender eventos sospechosos. Las soluciones comerciales pueden ser costosas o complejas para estudiantes.

TrafficWatch IDS ofrece una alternativa gratuita, didactica y ejecutable en Windows para aprender conceptos de IDS, redes, pruebas de software, respuesta activa controlada y despliegue web de demostracion.

### 2.2 Problema

La falta de monitoreo dificulta identificar escaneos de puertos, intentos repetidos de conexion, trafico inusual o accesos hacia puertos sensibles. Esto genera desconocimiento sobre lo que ocurre en la red local.

TrafficWatch IDS aborda este problema capturando paquetes, clasificando trafico, generando alertas interpretables, agrupando incidentes y ofreciendo vistas de apoyo para laboratorio, Render, Suricata y politicas IPS.

## 3. Interesados y usuarios

| Actor | Descripcion | Necesidad |
|---|---|---|
| Estudiante | Usuario principal del sistema. | Ejecutar pruebas y comprender alertas. |
| Desarrollador | Mantiene y mejora el proyecto. | Modificar reglas, dashboard y scripts. |
| Docente | Evalua el proyecto academico. | Ver evidencias, documentacion y resultados. |
| Analista de red principiante | Interpreta trafico local. | Observar eventos y exportar informacion. |
| Usuario de demo web | Revisa el dashboard publicado en Render. | Explorar simulaciones sin ejecutar captura real. |

## 4. Vista general del producto

### 4.1 Perspectiva

El producto funciona como una aplicacion local con dos procesos principales:

- **IDS:** captura y analiza paquetes con permisos de administrador.
- **Dashboard:** muestra informacion en `http://127.0.0.1:5000`.

Ambos procesos pueden ejecutarse mediante archivos `.bat`. El dashboard tambien puede publicarse como demo en Render usando Gunicorn, con funciones reales de red limitadas o simuladas.

### 4.2 Capacidades

| Capacidad | Descripcion |
|---|---|
| Captura de paquetes | Observa trafico en tiempo real con Scapy. |
| Deteccion por reglas | Evalua patrones configurados en `config.json`. |
| Alertas | Guarda eventos en `logs/alerts.json`. |
| Trafico clasificado | Guarda ultimos paquetes en `logs/traffic.json`. |
| Estado IDS | Mantiene informacion en `logs/status.json`. |
| Dashboard | Presenta tablas, incidentes, historial, graficos, estado, reglas, Suricata y exportaciones. |
| Attack Lab | Permite generar eventos remotos controlados para laboratorio. |
| Escaneo local | Lista dispositivos activos y ejecuta Nmap con validaciones. |
| Suricata/IPS | Lee EVE JSON, genera eventos demo, reglas drop y planes inline. |
| Respuesta activa | Recomienda o aplica bloqueo temporal local con Windows Firewall bajo confirmacion. |
| Pruebas guiadas | Genera ejemplos segun red detectada. |
| Demo Render | Permite demostrar el dashboard sin capturar trafico real. |

## 5. Caracteristicas del producto

### 5.1 Reglas IDS

La version actual detecta:

- `ESCANEO_DE_PUERTOS`
- `SYN_FLOOD`
- `ICMP_FLOOD`
- `PUERTO_SOSPECHOSO`
- `PUERTO_RARO`
- `ALTA_FRECUENCIA_CONEXIONES`
- `FUERZA_BRUTA_FTP`
- `FUERZA_BRUTA_SSH`
- `FUERZA_BRUTA_TELNET`
- `FUERZA_BRUTA_RDP`

### 5.2 Dashboard

El dashboard incluye:

- Resumen de alertas.
- Tipos de trafico.
- Trafico clasificado.
- Estado IDS.
- Graficos.
- Historial con filtros.
- Reglas IDS.
- Incidentes agrupados.
- Escaneo de red local.
- Escaneo Nmap local validado.
- Vista Suricata IPS.
- Politicas IPS.
- Boton de bloqueo temporal para alertas SSH validas.

### 5.3 Automatizacion

Archivos principales:

- `setup_windows.ps1`
- `INSTALAR_TRAFFICWATCH_WINDOWS.ps1`
- `INICIAR_TRAFFICWATCH.bat`
- `CREAR_EJECUTABLE_WINDOWS.bat`
- `CREAR_INSTALADOR_WINDOWS.bat`
- `abrir_cmd_proyecto.bat`
- `abrir_powershell_admin.bat`
- `abrir_powershell_pruebas.bat`
- `ejecutar_suricata_windows.bat`
- `simular_fuerza_bruta.py`

## 6. Restricciones

- El IDS principal requiere permisos de administrador.
- Nmap debe estar instalado para pruebas de escaneo.
- Npcap es necesario para captura real con Scapy.
- Suricata es opcional y solo se usa realmente en entorno local preparado.
- El sistema esta enfocado en Windows.
- El dashboard es local y no tiene autenticacion.
- La respuesta activa no debe ejecutarse automaticamente sin autorizacion.
- Render es solo demostracion; no captura red local, no ejecuta Nmap real, no opera Suricata real y no modifica Windows Firewall.
- Debe usarse solo en redes autorizadas.

## 7. Calidad esperada

| Atributo | Descripcion |
|---|---|
| Usabilidad | Uso simplificado mediante `.bat` y dashboard. |
| Mantenibilidad | Codigo modular separado por captura, analisis, alertas, storage y web. |
| Auditabilidad | Logs en JSON y exportacion CSV. |
| Configurabilidad | Reglas y umbrales en `config.json`. |
| Seguridad operativa | Separacion entre funciones locales reales y demo Render. |
| Portabilidad limitada | Ejecucion completa enfocada en Windows; demo web portable en Render. |

## 8. Conclusion

TrafficWatch IDS cumple la vision de una herramienta academica para monitoreo y deteccion basica de intrusiones. La version actual es mas completa que el prototipo inicial, ya que incorpora dashboard avanzado, incidentes, graficos, exportaciones, clasificacion de trafico, estado operativo, reglas IDS ampliadas, Attack Lab, Suricata IPS, politicas de respuesta y despliegue de demostracion en Render.
