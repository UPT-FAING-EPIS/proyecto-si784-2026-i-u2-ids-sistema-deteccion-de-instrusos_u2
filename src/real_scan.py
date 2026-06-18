import ipaddress
from pathlib import Path
import shutil
import subprocess
from datetime import datetime

from src.network_utils import detect_network_info


DEFAULT_PORT_RANGE = "1-100"
ALLOWED_PORT_RANGES = {
    "1-100",
    "1-1000",
    "22,23,53,80,443,3389",
    "31337,6667,9001",
}


def resolve_nmap_path() -> str:
    nmap_path = shutil.which("nmap") or shutil.which("nmap.exe")

    if nmap_path:
        return nmap_path

    common_paths = [
        Path("C:/Program Files/Nmap/nmap.exe"),
        Path("C:/Program Files (x86)/Nmap/nmap.exe"),
    ]

    for path in common_paths:
        if path.exists():
            return str(path)

    raise RuntimeError(
        "Nmap no esta instalado o no esta disponible. "
        "Instalalo desde https://nmap.org/download.html#windows "
        "o reinicia TrafficWatch despues de instalarlo."
    )


def run_local_nmap_scan(target: str = "", ports: str = DEFAULT_PORT_RANGE) -> dict:
    nmap_path = resolve_nmap_path()

    network_info = detect_network_info()
    network = ipaddress.ip_network(network_info.network, strict=False)
    clean_target = (target or network_info.gateway).strip()
    clean_ports = (ports or DEFAULT_PORT_RANGE).strip()

    if clean_ports not in ALLOWED_PORT_RANGES:
        raise ValueError(
            "Rango de puertos no permitido. Usa uno de: "
            + ", ".join(sorted(ALLOWED_PORT_RANGES))
        )

    try:
        target_ip = ipaddress.ip_address(clean_target)
    except ValueError as error:
        raise ValueError("El objetivo debe ser una IP valida de tu red local.") from error

    if target_ip not in network:
        raise ValueError(f"Objetivo fuera de la red local detectada: {network_info.network}")

    command = [
        nmap_path,
        "-Pn",
        "-p",
        clean_ports,
        str(target_ip),
    ]
    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )

    return {
        "started_at": started_at,
        "target": str(target_ip),
        "ports": clean_ports,
        "network": network_info.network,
        "gateway": network_info.gateway,
        "command": " ".join(command),
        "returncode": result.returncode,
        "stdout": result.stdout[-6000:],
        "stderr": result.stderr[-2000:],
    }
