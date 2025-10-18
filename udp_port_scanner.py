import socket
from concurrent.futures import ThreadPoolExecutor

def udp_scan(ip, ports, max_threads=50):
    results = {}

    def scan_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.settimeout(1)
                s.sendto(b'\x00'*8, (ip, port))
                
                try:
                    data, addr = s.recvfrom(1024)
                    results[port] = "Open"
                except socket.timeout:
                    results[port] = "Filtered"  # UDP may not always respond
                
        except Exception as e:
            results[port] = "Closed"  # If an error occurs

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(scan_port, ports)
    
    return results  # ✅ Returning a dictionary instead of a list
