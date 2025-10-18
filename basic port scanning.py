import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f"Port {port} is open on {ip}")
    except Exception as e:
        pass

def network_scanner(network_range, ports_to_scan):
    try:
        network = ipaddress.ip_network(network_range)
        with ThreadPoolExecutor(max_workers=100) as executor:
            for ip in network.hosts():
                for port in ports_to_scan:
                    executor.submit(scan_port, str(ip), port)
    except ValueError:
        print("Invalid network range")

if __name__ == "__main__":
    network = input("Enter network range (e.g., 192.168.1.0/24): ")
    ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3389]
    network_scanner(network, ports)