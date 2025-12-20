import subprocess
import xml.etree.ElementTree as ET
import requests
import socket

def get_opened_ports_via_nmap(host):
    xml_out = subprocess.check_output(["nmap", "-Pn", "-p-", "--open", "-T4", "-oX", "-", host])
    root = ET.fromstring(xml_out)
    ports = set()
    for host in root.findall("host"):
        ports_el = host.find("ports")
        if ports_el is None:
            continue
        for p in ports_el.findall("port"):
            state = p.find("state")
            if state is not None and state.get("state") == "open":
                ports.add(int(p.get("portid")))
    return ports

def test_only_allowed_ports_open(host, opened_ports):
    opened_ports = get_opened_ports_via_nmap(host)
    print("Opened ports: " + str(sorted(opened_ports)))
    print("Expected ports: " + str(sorted(opened_ports)))
    extra = opened_ports - opened_ports
    missing = opened_ports - opened_ports
    assert not extra, f"Extra ports: {sorted(extra)}"
    assert not missing, f"Missing ports: {sorted(missing)}"

def test_https_ports_for_200(host, https_ports_ok):
    for https_port in https_ports_ok:
        print(f"Checking port {https_port}...")
        resp = requests.get(f"https://{host}:{https_port}", verify=False)
        print(f"Port {https_port} returned status code {resp.status_code}")
        assert resp.status_code == 200, f"Port {https_port} returned status code {resp.status_code}, expected 200"

def test_ssh_port(host, ssh_port):
    with socket.create_connection((host, ssh_port), timeout=3) as sock:
        banner = sock.recv(1024).decode(errors="ignore")
    print(f"SSH banner on {host}:{ssh_port}: {banner!r}")
    assert banner.startswith("SSH-"), f"Wrong banner on port {ssh_port}: {banner!r}"
