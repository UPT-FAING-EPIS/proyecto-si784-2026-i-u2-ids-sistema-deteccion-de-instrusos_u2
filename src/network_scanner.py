import ipaddress
import platform
import re
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.network_utils import detect_network_info


MAX_PING_SWEEP_HOSTS = 254


def scan_local_network(timeout_ms: int = 180, resolve_names: bool = True) -> dict:
    network_info = detect_network_info()
    network = ipaddress.ip_network(network_info.network, strict=False)
    hosts = list(network.hosts())
    arp_entries = _read_arp_table()
    active_ips = set(arp_entries.keys())
    ping_sweep_used = len(hosts) <= MAX_PING_SWEEP_HOSTS

    if ping_sweep_used:
        active_ips.update(_ping_sweep(hosts, timeout_ms=timeout_ms))

    arp_entries = _read_arp_table()
    active_ips.update(arp_entries.keys())
    devices = []

    for ip_address in sorted(active_ips, key=_ip_sort_key):
        if ipaddress.ip_address(ip_address) not in network:
            continue

        devices.append({
            "ip": ip_address,
            "mac": arp_entries.get(ip_address, ""),
            "hostname": _resolve_hostname(ip_address) if resolve_names else "",
            "role": _device_role(ip_address, network_info),
            "status": "Activo",
        })

    return {
        "interface": network_info.interface,
        "local_ip": network_info.ip_address,
        "gateway": network_info.gateway,
        "network": network_info.network,
        "ping_sweep_used": ping_sweep_used,
        "device_count": len(devices),
        "devices": devices,
    }


def _ping_sweep(hosts, timeout_ms: int) -> set:
    active_ips = set()
    workers = min(64, max(4, len(hosts)))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(_ping_host, str(host), timeout_ms): str(host)
            for host in hosts
        }

        for future in as_completed(futures):
            ip_address = futures[future]

            try:
                if future.result():
                    active_ips.add(ip_address)
            except OSError:
                continue

    return active_ips


def _ping_host(ip_address: str, timeout_ms: int) -> bool:
    if platform.system() == "Windows":
        command = ["ping", "-n", "1", "-w", str(timeout_ms), ip_address]
    else:
        timeout_seconds = max(1, int(timeout_ms / 1000))
        command = ["ping", "-c", "1", "-W", str(timeout_seconds), ip_address]

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

    return result.returncode == 0


def _read_arp_table() -> dict:
    result = subprocess.run(
        ["arp", "-a"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return {}

    entries = {}
    pattern = re.compile(
        r"(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+"
        r"(?P<mac>[0-9a-fA-F]{2}(?:[:-][0-9a-fA-F]{2}){5})"
    )

    for match in pattern.finditer(result.stdout):
        entries[match.group("ip")] = match.group("mac").replace("-", ":").lower()

    return entries


def _resolve_hostname(ip_address: str) -> str:
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
    except (socket.herror, socket.gaierror, OSError):
        return ""

    return hostname


def _device_role(ip_address: str, network_info) -> str:
    if ip_address == network_info.ip_address:
        return "Este equipo"

    if ip_address == network_info.gateway:
        return "Gateway"

    return "Dispositivo"


def _ip_sort_key(ip_address: str):
    return tuple(int(part) for part in ip_address.split("."))
