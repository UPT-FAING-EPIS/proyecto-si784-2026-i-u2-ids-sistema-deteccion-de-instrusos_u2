<center>

[comment]: <img src="./media/media/image1.png" style="width:1.088in;height:1.46256in" alt="escudo.png" />

![./media/media/image1.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto *TrafficWatch IDS***

Curso: *CALIDAD Y PRUEBAS DE SOFTWARE*

Docente: *MAG.PATRICK CUADROS QUIROGA*

Integrantes:

***Edgar Diego Chara Apaza        (2019065026)***

***Abel Fernando Pacompía Ortiz   (2023076797)***


**Tacna – Perú**

***2026***

**  
**
</center>
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|MPV|ELV|ARV|04/04/2026|Versión Original|












**Sistema *Desarrollo de un sistema de detección de intrusos (IDS) para monitoreo de tráfico de red***

**Documento de Visión**

**Versión *{1.0}***
**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|MPV|ELV|ARV|04/04/20260|Versión Original|


<div style="page-break-after: always; visibility: hidden">\pagebreak</div>


**INDICE GENERAL**
#
[1.	Introducción](#_Toc52661346)

1.1	Propósito

1.2	Alcance

1.3	Definiciones, Siglas y Abreviaturas

1.4	Referencias

1.5	Visión General

[2.	Posicionamiento](#_Toc52661347)

2.1	Oportunidad de negocio

2.2	Definición del problema

[3.	Descripción de los interesados y usuarios](#_Toc52661348)

3.1	Resumen de los interesados

3.2	Resumen de los usuarios

3.3	Entorno de usuario

3.4	Perfiles de los interesados

3.5	Perfiles de los Usuarios

3.6	Necesidades de los interesados y usuarios

[4.	Vista General del Producto](#_Toc52661349)

4.1	Perspectiva del producto

4.2	Resumen de capacidades

4.3	Suposiciones y dependencias

4.4	Costos y precios

4.5	Licenciamiento e instalación

[5.	Características del producto](#_Toc52661350)

[6.	Restricciones](#_Toc52661351)

[7.	Rangos de calidad](#_Toc52661352)

[8.	Precedencia y Prioridad](#_Toc52661353)

[9.	Otros requerimientos del producto](#_Toc52661354)

b) Estandares legales

c) Estandares de comunicación	](#_toc394513800)37

d) Estandaraes de cumplimiento de la plataforma	](#_toc394513800)42

e) Estandaraes de calidad y seguridad	](#_toc394513800)42

[CONCLUSIONES](#_Toc52661355)

[RECOMENDACIONES](#_Toc52661356)

[BIBLIOGRAFIA](#_Toc52661357)

[WEBGRAFIA](#_Toc52661358)


<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

**<u>Informe de Visión</u>**

1. <span id="_Toc52661346" class="anchor"></span>**Introducción**

        1.1	Propósito
   
El presente documento de visión tiene como propósito describir de manera general el sistema TrafficWatch IDS, un sistema de detección de intrusos (IDS) orientado al monitoreo del tráfico de red. Este documento define el alcance del sistema, los problemas que busca resolver, los actores involucrados y las necesidades que se pretenden satisfacer.

Asimismo, sirve como base para la planificación, desarrollo y validación del sistema, permitiendo al equipo de trabajo y a los interesados comprender claramente los objetivos del proyecto.


    1.2	Alcance

El sistema TrafficWatch IDS está orientado al monitoreo de redes locales en entornos académicos o de pequeña escala, permitiendo identificar actividades sospechosas mediante el análisis del tráfico de red en tiempo real.

El sistema incluirá funcionalidades como:

- Captura de paquetes de red
- Análisis de tráfico mediante reglas simples
- Detección de comportamientos anómalos
- Generación de alertas


        1.3	Definiciones, Siglas y Abreviaturas

- IDS (Intrusion Detection System): Sistema que permite detectar actividades sospechosas en una red.
- Tráfico de red: Conjunto de datos que circulan por una red informática.
- Paquete: Unidad básica de información transmitida en una red.
- IP: Dirección que identifica un dispositivo en la red.
- Puerto: Punto lógico de comunicación en un sistema.
- Scapy: Librería de Python para manipulación y análisis de paquetes de red.


        1.4	Referencias

- Documentación oficial de Python
- Documentación de la librería Scapy
- Material del curso de Calidad y Pruebas de Software
- Documentación interna del proyecto


        1.5	Visión General

El documento está organizado en secciones que describen el contexto del proyecto, los problemas identificados, los usuarios involucrados y las características generales del sistema. Primero se presenta el posicionamiento del sistema, seguido de la descripción de los interesados y usuarios, permitiendo tener una visión clara del propósito y utilidad del sistema IDS.


<div style="page-break-after: always; visibility: hidden">\pagebreak</div>



2. <span id="_Toc52661347" class="anchor"></span>**Posicionamiento**

        2.1	Oportunidad de negocio

En la actualidad, la seguridad informática se ha convertido en una necesidad fundamental debido al incremento de ataques en redes. Sin embargo, muchas instituciones educativas y pequeñas organizaciones no cuentan con herramientas accesibles para monitorear su red.

Las soluciones comerciales de seguridad suelen ser costosas y complejas, lo que limita su implementación en entornos académicos.

El desarrollo de TrafficWatch IDS representa una oportunidad para ofrecer una solución accesible, educativa y funcional que permita:
- Mejorar la seguridad en redes locales
- Facilitar el aprendizaje en ciberseguridad
- Reducir costos al utilizar software open-source



        2.2	Definición del problema

Actualmente, muchas redes no cuentan con mecanismos adecuados para detectar intrusiones en tiempo real.

Esto genera problemas como:
- Accesos no autorizados sin detección
- Falta de control sobre el tráfico de red
- Dificultad para identificar ataques
- Dependencia de herramientas costosas

¿Cómo detectar actividades sospechosas en una red sin utilizar soluciones complejas o costosas?
El proyecto propone resolver este problema mediante un sistema IDS básico, capaz de monitorear tráfico y generar alertas de manera eficiente.



<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

3. <span id="_Toc52661348" class="anchor"></span>**Vista General del Producto**

        3.1	Resumen de los interesados

Los interesados del proyecto son aquellas personas o grupos que se ven afectados por el desarrollo o el resultado del sistema, aunque no necesariamente lo utilicen de forma directa:

| Nombre                 | Descripción                                                                 | Responsabilidades |
|------------------------|-----------------------------------------------------------------------------|------------------|
| Equipo de desarrollo   | Estudiantes encargados de diseñar e implementar el sistema IDS.            | Diseño, desarrollo, pruebas y mantenimiento del sistema. |
| Docente del curso      | Profesor encargado de supervisar y evaluar el proyecto.                    | Evaluar avances, validar resultados y guiar el desarrollo. |
| Institución académica  | Universidad donde se desarrolla el proyecto.                               | Brindar entorno académico y recursos básicos para el desarrollo. |
| Comunidad técnica      | Personas interesadas en seguridad informática y software open-source.      | Analizar, reutilizar o mejorar el sistema desarrollado. |



    3.2	Resumen de los usuarios

Los usuarios directos del sistema son aquellos que interactuarán con el IDS para monitorear el tráfico de red y detectar posibles amenazas:

| Nombre              | Descripción                                                                 | Responsabilidades | Comentarios |
|--------------------|-----------------------------------------------------------------------------|------------------|------------|
| Estudiante usuario | Persona que utiliza el sistema con fines académicos.                        | Ejecutar el sistema y analizar las alertas generadas. | Usuario principal del sistema. |
| Desarrollador      | Persona que implementa y mejora el sistema IDS.                             | Configurar reglas, optimizar el sistema y realizar pruebas. | Usuario técnico. |
| Analista de red    | Usuario con conocimientos básicos de redes.                                 | Interpretar el tráfico de red y validar alertas. | Uso intermedio. |




    3.3	Entorno de usuario
    
El sistema será utilizado en un entorno académico controlado:

| Elemento           | Descripción |
|--------------------|------------|
| Hardware           | Laptops o PCs con mínimo 4GB RAM |
| Sistema operativo  | Windows o Linux (Linux recomendado) |
| Red                | LAN o Wi-Fi |
| Herramientas       | Python, VS Code, Scapy |
| Tipo de entorno    | Académico y de pruebas |



    3.4	Perfiles de los interesados

| Interesado         | Perfil |
|-------------------|-------|
| Docente           | Profesional encargado de evaluar el proyecto y asegurar el cumplimiento académico. |
| Institución       | Organización que promueve el desarrollo de proyectos tecnológicos. |
| Comunidad técnica | Grupo interesado en software open-source. |


    3.5	Perfiles de los Usuarios

| Usuario           | Perfil |
|------------------|-------|
| Estudiante       | Usuario con conocimientos básicos de redes que utiliza el sistema con fines educativos. |
| Desarrollador    | Usuario técnico que implementa y mejora el sistema. |
| Analista de red  | Usuario que interpreta el tráfico y evalúa amenazas. |



    3.6	Necesidades de los interesados y usuarios

| Tipo de necesidad | Descripción |
|------------------|------------|
| Seguridad        | Detectar intrusiones y actividades sospechosas en la red. |
| Simplicidad      | Sistema fácil de usar e implementar. |
| Accesibilidad    | Uso de herramientas gratuitas y open-source. |
| Monitoreo        | Visualización del tráfico en tiempo real. |



<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

4. <span id="_Toc52661349" class="anchor"></span>**Estudio de
    Factibilidad**

    4.1	Perspectiva del producto

    4.2	Resumen de capacidades

    4.3	Suposiciones y dependencias

    4.4	Costos y precios

    4.5	Licenciamiento e instalación

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

5. <span id="_Toc52661350" class="anchor"></span>**Características del producto**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

6. <span id="_Toc52661351" class="anchor"></span>**Restricciones**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

7. <span id="_Toc52661352" class="anchor"></span>**Rangos de Calidad**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

8. <span id="_Toc52661353" class="anchor"></span>**Precedencia y Prioridad**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

9. <span id="_Toc52661354" class="anchor"></span>**Otros requerimientos del producto**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

<span id="_Toc52661355" class="anchor"></span>**CONCLUSIONES**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

<span id="_Toc52661356" class="anchor"></span>**RECOMENDACIONES**

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

<span id="_Toc52661357" class="anchor"></span>**BIBLIOGRAFIA**

- Sommerville, I. (2011). *Ingeniería de software* (9ª ed.). Pearson Educación.

- Stallings, W. (2017). *Seguridad informática: principios y práctica*. Pearson.

- Kurose, J., & Ross, K. (2017). *Redes de computadoras: un enfoque descendente* (7ª ed.). Pearson.


<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

<span id="_Toc52661358" class="anchor"></span>**WEBGRAFIA**
- Python Software Foundation. (2026). *Python Documentation*.  
  https://docs.python.org/3/

- Scapy Project. (2026). *Scapy Documentation*.  
  https://scapy.readthedocs.io/

- OWASP Foundation. (2026). *Open Web Application Security Project*.  
  https://owasp.org/

- Cisco Networking Academy. (2026). *Introducción a la Ciberseguridad*.  
  https://www.netacad.com/

- NIST. (2026). *Guide to Intrusion Detection and Prevention Systems*.  
  https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-94.pdf

- GeeksforGeeks. (2026). *Intrusion Detection System (IDS)*.  
  https://www.geeksforgeeks.org/intrusion-detection-system-ids/

- IBM Security. (2026). *What is an Intrusion Detection System (IDS)?*  
  https://www.ibm.com/topics/intrusion-detection-system

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>
