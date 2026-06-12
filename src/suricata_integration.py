import json
from datetime import datetime
from pathlib import Path
from typing import Iterable


DEFAULT_EVE_LOG_FILE = "logs/suricata/eve.json"
DEFAULT_LOCAL_RULES_FILE = "suricata/local.rules"


def read_suricata_alerts(eve_log_file: str, max_events: int = 100) -> list:
    path = Path(eve_log_file)

    if not path.exists():
        return []

    events = []

    for event in _read_eve_events(path):
        if event.get("event_type") != "alert":
            continue

        events.append(normalize_suricata_alert(event))

    return events[-max(1, int(max_events or 100)):]


def get_suricata_status(eve_log_file: str, local_rules_file: str) -> dict:
    eve_path = Path(eve_log_file)
    rules_path = Path(local_rules_file)
    alerts = read_suricata_alerts(str(eve_path), max_events=500)
    blocked_alerts = [
        alert for alert in alerts
        if str(alert.get("action", "")).lower() in {"blocked", "drop", "reject"}
        or str(alert.get("verdict", "")).lower() in {"drop", "reject"}
    ]

    return {
        "eve_log_file": str(eve_path),
        "eve_log_exists": eve_path.exists(),
        "local_rules_file": str(rules_path),
        "local_rules_exists": rules_path.exists(),
        "total_alerts": len(alerts),
        "blocked_alerts": len(blocked_alerts),
        "last_alert": alerts[-1] if alerts else None,
    }


def append_demo_suricata_alert(eve_log_file: str) -> dict:
    path = Path(eve_log_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    event = build_demo_suricata_event()

    with open(path, "a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")

    return normalize_suricata_alert(event)


def build_firewall_block_command(ip_address: str) -> dict:
    clean_ip = str(ip_address or "").strip()

    if not clean_ip:
        raise ValueError("IP requerida para generar el bloqueo.")

    rule_name = f"TrafficWatch IDS Block {clean_ip}"

    return {
        "ip": clean_ip,
        "windows_powershell": (
            f'New-NetFirewallRule -DisplayName "{rule_name}" '
            f'-Direction Inbound -RemoteAddress {clean_ip} -Action Block'
        ),
        "linux_iptables": f"sudo iptables -I INPUT -s {clean_ip} -j DROP",
        "suricata_drop_rule": (
            f'drop ip {clean_ip} any -> any any '
            f'(msg:"TrafficWatch IPS bloqueo IP {clean_ip}"; sid:9000101; rev:1;)'
        ),
    }


def build_youtube_policy_commands() -> dict:
    domains = [
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "googlevideo.com",
        "ytimg.com",
        "youtubei.googleapis.com",
    ]

    return {
        "domains": domains,
        "note": (
            "YouTube usa HTTPS, QUIC y CDNs de Google. Suricata puede alertar "
            "por SNI/TLS o HTTP, pero el bloqueo mas estable suele hacerse con DNS "
            "filtering o firewall perimetral."
        ),
        "suricata_example_rules": [
            (
                'drop tls any any -> any any '
                '(msg:"TrafficWatch IPS politica YouTube TLS"; '
                'tls.sni; content:"youtube.com"; nocase; sid:9000201; rev:1;)'
            ),
            (
                'drop tls any any -> any any '
                '(msg:"TrafficWatch IPS politica GoogleVideo TLS"; '
                'tls.sni; content:"googlevideo.com"; nocase; sid:9000202; rev:1;)'
            ),
        ],
        "dns_policy_list": "\n".join(domains),
    }


def build_youtube_block_for_ip(ip_address: str) -> dict:
    clean_ip = str(ip_address or "").strip()

    if not clean_ip:
        raise ValueError("IP requerida para generar la politica de YouTube.")

    domains = [
        "youtube.com",
        "googlevideo.com",
        "ytimg.com",
        "youtubei.googleapis.com",
    ]
    base_sid = 9000300
    suricata_rules = []

    for index, domain in enumerate(domains, start=1):
        suricata_rules.append(
            f'drop tls {clean_ip} any -> any any '
            f'(msg:"TrafficWatch IPS bloquear YouTube {domain} para {clean_ip}"; '
            f'tls.sni; content:"{domain}"; nocase; sid:{base_sid + index}; rev:1;)'
        )

    suricata_rules.append(
        f'drop http {clean_ip} any -> any any '
        f'(msg:"TrafficWatch IPS bloquear YouTube HTTP para {clean_ip}"; '
        f'http.host; content:"youtube.com"; nocase; sid:{base_sid + 20}; rev:1;)'
    )

    suricata_rules.append(
        f'drop udp {clean_ip} any -> any 443 '
        f'(msg:"TrafficWatch IPS bloquear QUIC hacia YouTube por politica para {clean_ip}"; '
        f'sid:{base_sid + 30}; rev:1;)'
    )

    return {
        "ip": clean_ip,
        "domains": domains,
        "suricata_rules": suricata_rules,
        "suricata_rules_text": "\n\n".join(suricata_rules),
        "note": (
            "Estas reglas bloquean intentos identificables por TLS SNI o HTTP Host "
            "desde la IP indicada. Para hacerlo mas fuerte, combina con bloqueo DNS "
            "de youtube.com, googlevideo.com, ytimg.com y youtubei.googleapis.com."
        ),
    }


def build_inline_ips_plan(interface: str = "eth0", queue_num: int = 0) -> dict:
    clean_interface = str(interface or "eth0").strip()

    if not clean_interface:
        raise ValueError("Interfaz requerida para generar el modo IPS/inline.")

    queue = int(queue_num or 0)

    if queue < 0:
        raise ValueError("El numero de cola NFQUEUE no puede ser negativo.")

    return {
        "mode": "NFQUEUE",
        "interface": clean_interface,
        "queue_num": queue,
        "requirements": [
            "Linux con Suricata instalado.",
            "Trafico pasando por el equipo Suricata, por ejemplo router, gateway o laboratorio con forwarding.",
            "Permisos root para iptables/nftables y Suricata.",
            "Reglas Suricata con acciones drop o reject.",
        ],
        "enable_commands": [
            "sudo sysctl -w net.ipv4.ip_forward=1",
            f"sudo iptables -I FORWARD -i {clean_interface} -j NFQUEUE --queue-num {queue}",
            f"sudo iptables -I FORWARD -o {clean_interface} -j NFQUEUE --queue-num {queue}",
            f"sudo suricata -c /etc/suricata/suricata.yaml -q {queue} -l /var/log/suricata",
        ],
        "disable_commands": [
            f"sudo iptables -D FORWARD -i {clean_interface} -j NFQUEUE --queue-num {queue}",
            f"sudo iptables -D FORWARD -o {clean_interface} -j NFQUEUE --queue-num {queue}",
        ],
        "suricata_yaml_hint": (
            "outputs:\n"
            "  - eve-log:\n"
            "      enabled: yes\n"
            "      filetype: regular\n"
            "      filename: eve.json\n\n"
            "rule-files:\n"
            "  - local.rules\n\n"
            "action-order:\n"
            "  - pass\n"
            "  - drop\n"
            "  - reject\n"
            "  - alert"
        ),
        "notes": (
            "NFQUEUE envia paquetes del firewall a Suricata. Si una regla usa drop/reject "
            "y Suricata esta en modo IPS, el paquete puede bloquearse. Pruebalo primero "
            "en laboratorio porque una regla incorrecta puede cortar conectividad."
        ),
    }


def normalize_suricata_alert(event: dict) -> dict:
    alert = event.get("alert", {}) or {}
    verdict = event.get("verdict", {}) or {}
    final_action = verdict.get("action") or alert.get("action") or "allowed"

    return {
        "timestamp": event.get("timestamp", ""),
        "signature": alert.get("signature", "SIN_FIRMA"),
        "category": alert.get("category", "DESCONOCIDO"),
        "severity": alert.get("severity", ""),
        "action": alert.get("action", "allowed"),
        "verdict": final_action,
        "protocol": event.get("proto", ""),
        "source_ip": event.get("src_ip", ""),
        "source_port": event.get("src_port", ""),
        "destination_ip": event.get("dest_ip", ""),
        "destination_port": event.get("dest_port", ""),
        "sid": alert.get("signature_id", ""),
        "raw": event,
    }


def build_demo_suricata_event() -> dict:
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "event_type": "alert",
        "src_ip": "10.10.10.44",
        "src_port": 52122,
        "dest_ip": "192.168.1.33",
        "dest_port": 22,
        "proto": "TCP",
        "alert": {
            "action": "blocked",
            "signature_id": 9000001,
            "rev": 1,
            "signature": "TrafficWatch IPS demo fuerza bruta SSH",
            "category": "Attempted Administrator Privilege Gain",
            "severity": 1,
        },
        "verdict": {
            "action": "drop",
        },
    }


def _read_eve_events(path: Path) -> Iterable[dict]:
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return
