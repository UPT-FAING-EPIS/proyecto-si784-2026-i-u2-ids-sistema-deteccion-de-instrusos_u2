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

# Informe de Factibilidad

Version: **2.1**

| Version | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:--:|:--:|:--:|:--:|:--:|:--|
| 1.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-04-05 | Version inicial |
| 2.0 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-06-09 | Actualizacion segun implementacion final |
| 2.1 | APO, ECA | APO, ECA | P. Cuadros Q. | 2026-07-04 | Actualizacion segun codigo actual, Render, Suricata IPS y respuesta activa controlada |

## 1. Descripcion del proyecto

**TrafficWatch IDS** es un sistema basico de deteccion de intrusos orientado al monitoreo de trafico de red en Windows. El sistema captura paquetes con **Scapy**, analiza el trafico mediante reglas configurables, clasifica eventos y genera alertas visibles en un dashboard web construido con **Flask**.

El proyecto se ejecuta principalmente en un entorno local o de laboratorio. Tambien cuenta con una demostracion web en **Render**, pensada para mostrar el dashboard, simulaciones, historial y graficos sin realizar captura real de red ni acciones de firewall en el entorno remoto.

## 2. Alcance actual

La version actual incluye:

- Captura de paquetes en tiempo real.
- Deteccion automatica de interfaz, IP local, gateway y red.
- Reglas IDS para escaneo de puertos, SYN flood, ICMP flood, fuerza bruta, alta frecuencia de conexiones, puertos sospechosos y puertos raros.
- Cooldown de alertas repetidas para reducir ruido.
- Clasificacion de trafico entrante, saliente, local, gateway y externo.
- Dashboard web con secciones de alertas, historial, graficos, estado del IDS, trafico clasificado y reglas IDS.
- Agrupacion de alertas repetidas como incidentes para mejorar lectura del dashboard.
- Laboratorio web `/attack-lab` para generar eventos remotos controlados.
- Escaneo controlado de dispositivos de la red local.
- Ejecucion local validada de Nmap con rangos de puertos permitidos.
- Integracion con Suricata EVE, reglas locales, eventos de demostracion y planes IPS.
- Politicas IPS sugeridas, incluyendo comandos de firewall y reglas Suricata para escenarios autorizados.
- Respuesta activa manual para bloqueo temporal de IPs asociadas a fuerza bruta SSH.
- Despliegue de demostracion en Render mediante `render.yaml`, `runtime.txt` y Gunicorn.
- Empaquetado e instalador para Windows.
- Exportacion de alertas en JSON/CSV.
- Exportacion de trafico clasificado en JSON/CSV.
- Scripts de automatizacion para Windows.

Fuera de alcance:

- Bloqueo masivo o automatico de trafico sin confirmacion.
- Uso ofensivo contra redes externas o no autorizadas.
- Operacion real de captura, Nmap, Suricata o Firewall de Windows desde Render.
- Operacion como IDS empresarial de alta demanda.

Por ello, el sistema debe considerarse principalmente un **IDS academico**, con funciones de apoyo IPS y respuesta activa solo en modo controlado, local y autorizado.

## 3. Riesgos

| Riesgo | Descripcion | Mitigacion |
|---|---|---|
| Falsos positivos | Trafico legitimo puede activar alertas. | Uso de cooldown, umbrales configurables y pruebas controladas. |
| Permisos insuficientes | Scapy requiere permisos de administrador para capturar paquetes. | Uso de `abrir_powershell_admin.bat`. |
| Dependencia de Nmap | Las pruebas de escaneo requieren Nmap instalado. | `setup_windows.ps1` verifica e intenta instalar Nmap con winget. |
| Dependencia de Npcap/Scapy | La captura real necesita soporte de captura en Windows. | Instalacion guiada y ejecucion local como administrador. |
| Limitaciones de Render | Render no accede a la red local del usuario ni al Firewall de Windows. | Separar funciones demo de funciones locales reales. |
| Respuesta activa | Un bloqueo mal aplicado podria afectar conectividad. | Bloqueo manual, temporal, validado por IP y documentado como funcion local. |
| Ruido en red | Muchas conexiones normales pueden generar registros. | Limite de registros de trafico y reglas diferenciadas. |
| Uso indebido | El sistema podria usarse fuera de redes autorizadas. | Documentacion de uso etico y enfoque academico. |

## 4. Factibilidad tecnica

El proyecto es tecnicamente viable porque utiliza herramientas gratuitas, conocidas y disponibles en Windows:

| Tecnologia | Uso |
|---|---|
| Python | Lenguaje principal del sistema. |
| Scapy | Captura y analisis de paquetes. |
| Flask | Dashboard web local. |
| Nmap | Generacion de trafico de prueba autorizado. |
| Suricata | Lectura de eventos EVE, reglas locales y planes IPS de laboratorio. |
| Windows Firewall | Bloqueo temporal local y manual en escenarios autorizados. |
| Gunicorn/Render | Publicacion del dashboard como demostracion web. |
| PowerShell/CMD | Automatizacion de ejecucion en Windows. |
| JSON/CSV | Persistencia y exportacion de registros. |

El sistema cuenta con archivos de arranque para simplificar la ejecucion:

- `setup_windows.ps1`: verifica Python, pip, dependencias y Nmap.
- `abrir_cmd_proyecto.bat`: inicia el dashboard.
- `abrir_powershell_admin.bat`: inicia el IDS como administrador.
- `abrir_powershell_pruebas.bat`: abre consola de pruebas.
- `INICIAR_TRAFFICWATCH.bat`: facilita el inicio del dashboard empaquetado.
- `CREAR_EJECUTABLE_WINDOWS.bat` y `CREAR_INSTALADOR_WINDOWS.bat`: generan entregables para Windows.
- `render.yaml`: permite publicar el dashboard de demostracion en Render.

**Resultado:** Factibilidad tecnica alta.

## 5. Factibilidad economica

El proyecto no requiere licencias comerciales. Los costos se limitan al uso de equipos personales, energia, internet y tiempo de desarrollo.

| Concepto | Costo estimado |
|---|---:|
| Herramientas de software | S/. 0.00 |
| Equipo de desarrollo propio | S/. 0.00 |
| Internet y energia | S/. 130.00 |
| Tiempo de desarrollo academico | S/. 1600.00 |
| Materiales y documentacion | S/. 275.00 |
| **Total estimado** | **S/. 2005.00** |

Frente a herramientas comerciales de monitoreo y seguridad, TrafficWatch IDS representa una alternativa de bajo costo para aprendizaje y pruebas.

**Resultado:** Factibilidad economica alta.

## 6. Factibilidad operativa

El sistema es operable por estudiantes con conocimientos basicos de redes y Windows. La ejecucion se simplifico mediante archivos `.bat`, instalador, ejecutable Windows y dashboard web. El usuario puede iniciar dashboard, IDS y pruebas sin escribir comandos complejos.

Orden recomendado:

1. `abrir_cmd_proyecto.bat`
2. `abrir_powershell_admin.bat`
3. `abrir_powershell_pruebas.bat`

El dashboard permite interpretar los resultados mediante tablas, filtros, graficos, estado del IDS, historial, incidentes agrupados, trafico clasificado, Attack Lab, Suricata IPS y politicas generadas. En Render, el usuario puede revisar la demo sin permisos de administrador; las funciones reales de red se mantienen en la maquina local.

**Resultado:** Factibilidad operativa alta.

## 7. Factibilidad legal

El proyecto utiliza tecnologias open-source y se orienta a redes propias, laboratorios academicos o entornos autorizados. Las pruebas con Nmap, Suricata, Attack Lab y simuladores deben ejecutarse solo con autorizacion. La respuesta activa se mantiene como funcion defensiva, manual, temporal y local.

Los datos almacenados son tecnicos:

- Direcciones IP.
- Puertos.
- Protocolos.
- Flags TCP.
- Tipos de alerta.

**Resultado:** Factibilidad legal alta si se respeta el uso etico.

## 8. Factibilidad social y ambiental

El proyecto tiene impacto social positivo porque fortalece el aprendizaje practico en ciberseguridad, redes y calidad de software. Al ser software, no genera residuos fisicos ni requiere infraestructura adicional.

**Resultado:** Factibilidad social y ambiental alta.

## 9. Conclusiones

TrafficWatch IDS es viable desde el punto de vista tecnico, economico, operativo, legal, social y ambiental. La version actual cumple con el objetivo academico de capturar trafico, analizar patrones sospechosos, generar alertas, conservar evidencias, mostrar resultados mediante un dashboard local y ofrecer una demostracion web compatible con Render.

Se recomienda su uso en redes propias o laboratorios autorizados, manteniendo claramente su alcance como IDS academico con apoyo de respuesta activa e IPS solo bajo condiciones controladas.
