import socket
from concurrent.futures import ThreadPoolExecutor

def get_service_banner(ip, port, timeout=2):
    """Attempts to retrieve a service banner from an open port."""
    try:
        with socket.create_connection((ip, port), timeout) as s:
            s.sendall(b'GET / HTTP/1.1\r\n\r\n')
            banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            return banner.split('\n')[0] if banner else "No banner"
    except (socket.timeout, ConnectionRefusedError, OSError):
        return None

def tcp_scan(target_ip, ports, get_banners=False, max_threads=10):
    """Scans the given ports on the target IP and retrieves banners if requested."""
    print(f"Scanning IP: {target_ip} on Ports: {ports}")

    open_ports = {}  # Dictionary to store open ports and banners (if retrieved)

    def scan_port(port):
        """Checks if a port is open and retrieves its banner if requested."""
        try:
            with socket.create_connection((target_ip, port), timeout=1):
                banner = get_service_banner(target_ip, port) if get_banners else None
                open_ports[port] = banner
        except (socket.timeout, ConnectionRefusedError, OSError):
            pass  # Port is closed or unreachable

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(scan_port, ports)

    return open_ports
