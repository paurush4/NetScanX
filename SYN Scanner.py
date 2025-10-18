import socket
from concurrent.futures import ThreadPoolExecutor

def tcp_scan(target_ip, ports):
    open_ports = {}

    def scan_port(port):
        try:
            with socket.create_connection((target_ip, port), timeout=1):
                print(f"[+] Port {port} is open!")  # Debugging
                open_ports[port] = "Open"
        except (socket.timeout, ConnectionRefusedError, OSError):
            open_ports[port] = "Closed"

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(scan_port, ports)

    return open_ports
