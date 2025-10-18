import requests

def check_vulnerabilities(ip, port, service_info):
    vulnerabilities = []
    
    # Example checks (very basic)
    if port == 21 and "vsftpd" in service_info:
        if "2.3.4" in service_info:
            vulnerabilities.append("vsftpd 2.3.4 backdoor (CVE-2011-2523)")
    
    if port == 80 or port == 443:
        try:
            response = requests.get(f"http://{ip}:{port}", timeout=3)
            headers = response.headers
            
            if "Apache/2.4.49" in headers.get('Server', ''):
                vulnerabilities.append("Apache 2.4.49 Path Traversal (CVE-2021-41773)")
        except:
            pass
    
    return vulnerabilities