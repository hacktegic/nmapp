from enum import Enum
import xml.etree.ElementTree as ET
from typing import Dict, List


class NmapOriginalFormat(Enum):
    NORMAL = 1
    XML = 2
    GREPABLE = 3
    LOOKS_INVALID = 10


def detect_format(nmap_original_output: str) -> NmapOriginalFormat:
    if nmap_original_output.find("Starting Nmap ") >= 0:
        return NmapOriginalFormat.NORMAL
    if nmap_original_output.find("<!DOCTYPE nmaprun>") >= 0:
        return NmapOriginalFormat.XML
    if nmap_original_output.find("# Nmap ") >= 0:
        return NmapOriginalFormat.GREPABLE
    return NmapOriginalFormat.LOOKS_INVALID


def reformat_to_markdown(nmap_original_output: str) -> str:
    if detect_format(nmap_original_output) == NmapOriginalFormat.LOOKS_INVALID:
        raise ValueError("The provided input looks invalid")
    nmap_open_ports = {}
    if detect_format(nmap_original_output) == NmapOriginalFormat.NORMAL:
        raise NotImplementedError("Only XML input is supported for now")
    if detect_format(nmap_original_output) == NmapOriginalFormat.XML:
        nmap_open_ports = reformat_xml_to_dict(nmap_original_output)
    if detect_format(nmap_original_output) == NmapOriginalFormat.GREPABLE:
        raise NotImplementedError("Only XML input is supported for now")
    return reformat_dict_to_markdown(nmap_open_ports)


def reformat_xml_to_dict(nmap_original_output: str) -> dict:
    """Parse Nmap XML output and return a dict of address -> sorted list of open ports (ints)."""
    try:
        root = ET.fromstring(nmap_original_output)
    except ET.ParseError as exc:
        raise ValueError(f"Failed to parse XML input: {exc}")

    hosts_ports: Dict[str, set] = {}

    for host in root.findall("host"):
        addrs = [a.get("addr") for a in host.findall("address") if a.get("addr")]
        if not addrs:
            continue

        # Sort addresses
        addrs.sort()

        # Join into a comma-separated string
        addr = ",".join(addrs)

        # find ports
        ports_elem = host.find("ports")
        if ports_elem is None:
            continue

        for port in ports_elem.findall("port"):
            state = port.find("state")
            if state is None:
                continue
            if state.get("state") != "open":
                continue
            portid = port.get("portid")
            if not portid:
                continue
            try:
                port_int = int(portid)
            except ValueError:
                continue
            hosts_ports.setdefault(addr, set()).add(port_int)

    result: Dict[str, List[int]] = {}
    for addr in sorted(hosts_ports.keys()):
        result[addr] = sorted(hosts_ports[addr])

    return result


def reformat_dict_to_markdown(nmap_open_ports: dict) -> str:
    """Convert dict of address -> list of ports to deterministic markdown.

    Each host is rendered as a level-2 heading (## <address>) followed by a list of ports,
    one per line prefixed with '- '. Hosts are rendered in ascending key order and ports in
    ascending numeric order.
    """
    if not nmap_open_ports:
        return ""

    lines: List[str] = []
    # ensure deterministic order
    for addr in sorted(nmap_open_ports.keys()):
        lines.append(f"## {addr}")
        ports = nmap_open_ports.get(addr) or []
        # If ports is a set or other iterable, convert to sorted list of ints
        try:
            ports_list = sorted(int(p) for p in ports)
        except Exception:
            # fallback: represent as strings
            ports_list = sorted(ports)
        for p in ports_list:
            lines.append(f"- {p}")
        # blank line between hosts
        lines.append("")

    # remove trailing blank line
    if lines and lines[-1] == "":
        lines = lines[:-1]

    return "\n".join(lines)
