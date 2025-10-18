import os
import platform
import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-w', '1', str(host)]
    try:
        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return host if output.returncode == 0 else None
    except:
        return None

def icmp_sweep(network_range, max_threads=100):
    live_hosts = []
    network = ipaddress.ip_network(network_range)
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(ping, network.hosts())
    
    for result in results:
        if result is not None:
            live_hosts.append(str(result))
    
    return live_hosts