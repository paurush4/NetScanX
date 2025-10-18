# NetScanX - Network Scanning Tool

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A modular Python-based network scanner with GUI interface for network discovery, port scanning, and vulnerability assessment.

## 🚀 Features

- **TCP/UDP Port Scanning** - Multi-threaded port scanning with 60% performance optimization
- **SYN Scanning** - Half-open connection scanning
- **ICMP Ping Sweep** - Network-wide host discovery
- **Banner Grabbing** - Service identification and version detection
- **Vulnerability Detection** - Basic CVE checks for common services
- **GUI Interface** - User-friendly Tkinter interface
- **Export Results** - Save scan results to text files
- **Real-time Monitoring** - Live scan progress and sortable results

## 📋 Installation

```bash
git clone https://github.com/yourusername/NetScanX.git
cd NetScanX
pip install requests
python gui.py
```

## 💻 Usage

1. **Launch the application**
   ```bash
   python gui.py
   ```

2. **Configure scan**
   - Enter target IP or network range (e.g., `192.168.1.1` or `192.168.1.0/24`)
   - Specify ports (comma-separated: `21,22,80,443`)
   - Select scan type: TCP, UDP, Ping Sweep, or All Scans
   - Enable Banner Grabbing and/or Vulnerability Checks

3. **Start scan and view results**
   - Click "Start Scan"
   - Results appear in real-time
   - Save results using "Save Results" button

## 📁 Project Structure

```
NetScanX/
├── gui.py                  # Main GUI application
├── tcp_port_scanner.py     # TCP scanning module
├── udp_port_scanner.py     # UDP scanning module
├── SYN Scanner.py          # SYN scanning module
├── ping_sweep.py           # ICMP ping sweep
├── vulnerbility.py         # Vulnerability checks
└── basic port scanning.py  # Basic scanner utility
```

## 🎯 Key Features

- **Multi-threaded Architecture** - Concurrent scanning for optimal performance
- **Network Range Support** - CIDR notation (192.168.1.0/24)
- **Vulnerability Database** - Checks for vsftpd 2.3.4, Apache 2.4.49 vulnerabilities
- **Interactive Results** - Sortable table with IP, Port, Service, Banner, Vulnerabilities

## ⚠️ Legal Notice

**For authorized security testing only.** Only scan networks you own or have explicit permission to test. Unauthorized scanning may be illegal.

## 🛠️ Requirements

- Python 3.8+
- tkinter (included with Python)
- requests library

## 👨‍💻 Author

**Aman Paurush**
- Email: amanpaurush5015@gmail.com
- LinkedIn: [linkedin.com/in/aman-paurush](https://linkedin.com/in/aman-paurush/)
- GitHub: [github.com/paurush4](https://github.com/paurush4)

## 📄 License

MIT License - Educational and authorized security testing purposes only.

---

**🔒 Built for Network Security | ⚡ Performance Optimized**
