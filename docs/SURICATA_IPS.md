# Integracion Suricata IPS

TrafficWatch puede integrarse con Suricata leyendo el archivo `eve.json`.

## Flujo propuesto

```text
Red -> Suricata IDS/IPS -> eve.json -> TrafficWatch Dashboard
```

Suricata escribe eventos en formato EVE JSON. El dashboard lee `logs/suricata/eve.json`,
normaliza alertas y muestra firma, severidad, accion, IP origen, IP destino y protocolo.

## Archivos agregados

- `src/suricata_integration.py`: lector y normalizador de eventos EVE.
- `suricata/local.rules`: reglas locales de ejemplo para modo IPS.
- `config.json`: seccion `suricata` con rutas de `eve.json` y `local.rules`.
- Dashboard: pestana `Suricata IPS`.

## Configuracion en el proyecto

```json
"suricata": {
    "enabled": true,
    "eve_log_file": "logs/suricata/eve.json",
    "local_rules_file": "suricata/local.rules",
    "max_alerts": 100
}
```

## Modo IDS vs IPS

En modo IDS, Suricata observa trafico y genera alertas.

En modo IPS/inline, Suricata puede aplicar acciones como `drop` o `reject`.
El bloqueo real depende de que el trafico pase por Suricata en linea.

## Windows

El instalador Windows probado instala Suricata en:

```text
C:\Program Files\Suricata\suricata.exe
```

Comando validado para capturar trafico y escribir eventos en el dashboard:

```powershell
& "C:\Program Files\Suricata\suricata.exe" -c "C:\Program Files\Suricata\suricata.yaml" -S "suricata\local.rules" -l "logs\suricata" -i 192.168.1.11 -k none
```

Tambien puedes ejecutar:

```text
ejecutar_suricata_windows.bat
```

Esta build de Windows funciona para IDS/captura con Npcap. En la verificacion local no
incluye `NFQueue` ni `WinDivert`, por lo que no puede hacer bloqueo IPS inline real en
Windows. Para bloqueo real usa Linux/NFQUEUE, WinDivert con una build compatible, o una
respuesta activa con firewall/DNS.

## Linux con NFQUEUE, ejemplo conceptual

```bash
sudo iptables -I FORWARD -j NFQUEUE --queue-num 0
sudo suricata -c /etc/suricata/suricata.yaml -q 0
```

En el dashboard, la pestana `Suricata IPS` puede generar un plan de laboratorio
para una interfaz especifica, por ejemplo `eth0`:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -I FORWARD -i eth0 -j NFQUEUE --queue-num 0
sudo iptables -I FORWARD -o eth0 -j NFQUEUE --queue-num 0
sudo suricata -c /etc/suricata/suricata.yaml -q 0 -l /var/log/suricata
```

Comandos de reversa:

```bash
sudo iptables -D FORWARD -i eth0 -j NFQUEUE --queue-num 0
sudo iptables -D FORWARD -o eth0 -j NFQUEUE --queue-num 0
```

Usa estos comandos primero en laboratorio. En IPS/inline, una regla mal escrita
puede bloquear trafico valido o cortar conectividad.

## Reglas locales

Agregar `suricata/local.rules` al `suricata.yaml` real:

```yaml
rule-files:
  - local.rules
```

Ejemplo de regla IPS:

```text
drop tcp any any -> $HOME_NET 22 (msg:"TrafficWatch IPS posible fuerza bruta SSH"; flags:S; threshold:type threshold, track by_src, count 8, seconds 30; sid:9000001; rev:1;)
```

## Bloqueo de YouTube

Suricata puede detectar dominios en TLS SNI o HTTP Host, pero YouTube usa HTTPS,
QUIC y CDNs compartidos. Para una politica estable conviene combinar:

- Suricata para deteccion y evidencia.
- DNS filtering para dominios.
- Firewall o router para aplicar politica.

Dominios sugeridos:

```text
youtube.com
www.youtube.com
m.youtube.com
googlevideo.com
ytimg.com
youtubei.googleapis.com
```

## Fuentes oficiales

- Suricata EVE JSON: https://docs.suricata.io/en/latest/output/eve/eve-json-output.html
- Acciones `drop` y `reject` en IPS: https://docs.suricata.io/en/latest/configuration/suricata-yaml.html
- Formato EVE y campos de accion/veredicto: https://docs.suricata.io/en/latest/output/eve/eve-json-format.html
