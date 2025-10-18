import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import socket
import os
import platform
from tcp_port_scanner import tcp_scan
from udp_port_scanner import udp_scan

# Function for Ping Sweep
def ping_sweep(target):
    """Checks if the target is alive via ICMP ping."""
    param = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    response = os.system(f"ping {param} {target} >nul 2>&1")
    return "Alive" if response == 0 else "Unreachable"

# Function for Basic Vulnerability Scan (Example)
def check_vulnerabilities(port):
    """Returns known vulnerabilities based on common open ports."""
    vuln_db = {
        21: "FTP - Weak authentication",
        22: "SSH - Potential brute-force",
        23: "Telnet - Unencrypted communication",
        80: "HTTP - Possible outdated server",
        443: "HTTPS - Check for SSL vulnerabilities",
        3389: "RDP - Check for exposed access"
    }
    return vuln_db.get(port, "Unknown Risk")

# GUI Class
class NetworkScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Network Scanner")
        self.root.geometry("800x500")
        
        # Target IP
        tk.Label(root, text="Target IP/Range:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.target_entry = tk.Entry(root, width=40)
        self.target_entry.grid(row=0, column=1, padx=10, pady=5)

        # Ports Entry
        tk.Label(root, text="Ports (comma-separated):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ports_entry = tk.Entry(root, width=40)
        self.ports_entry.grid(row=1, column=1, padx=10, pady=5)

        # Scan Type
        tk.Label(root, text="Scan Type:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.scan_type = ttk.Combobox(root, values=["TCP Scan", "UDP Scan", "Ping Sweep", "All Scans"], state="readonly")
        self.scan_type.grid(row=2, column=1, padx=10, pady=5)
        self.scan_type.current(0)  # Default to TCP

        # Options: Banner & Vulnerability Check
        self.retrieve_banner = tk.BooleanVar()
        self.check_vuln = tk.BooleanVar()
        tk.Checkbutton(root, text="Retrieve Banners", variable=self.retrieve_banner).grid(row=3, column=1, sticky="w", padx=10)
        tk.Checkbutton(root, text="Check Vulnerabilities", variable=self.check_vuln).grid(row=4, column=1, sticky="w", padx=10)

        # Buttons
        self.scan_button = tk.Button(root, text="Start Scan", command=self.start_scan)
        self.scan_button.grid(row=5, column=0, pady=10)
        
        self.clear_button = tk.Button(root, text="Clear Results", command=self.clear_results)
        self.clear_button.grid(row=5, column=1, pady=10, sticky="w")

        self.save_button = tk.Button(root, text="Save Results", command=self.save_results)
        self.save_button.grid(row=5, column=1, pady=10, sticky="e")

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.grid(row=5, column=2, pady=10, padx=10)

        # Results Table
        columns = ("IP", "Port", "Service", "Banner", "Vulnerabilities")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_results(_col))
            self.tree.column(col, width=120)
        self.tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def start_scan(self):
        target = self.target_entry.get().strip()
        ports = self.ports_entry.get().strip()
        scan_type = self.scan_type.get()

        if not target:
            messagebox.showerror("Error", "Please enter a valid target.")
            return

        if scan_type in ["TCP Scan", "UDP Scan", "All Scans"] and not ports:
            messagebox.showerror("Error", "Please enter valid ports for TCP/UDP scan.")
            return

        try:
            ports = list(map(int, ports.split(","))) if ports else []
        except ValueError:
            messagebox.showerror("Error", "Invalid port format!")
            return

        self.tree.delete(*self.tree.get_children())  # Clear previous results

        def run_scan():
            results = {}

            if scan_type == "Ping Sweep":
                status = ping_sweep(target)
                self.tree.insert("", "end", values=(target, "-", "Ping", status, "-"))
                return

            if scan_type in ["TCP Scan", "All Scans"]:
                results["TCP"] = tcp_scan(target, ports, get_banners=self.retrieve_banner.get())

            if scan_type in ["UDP Scan", "All Scans"]:
                results["UDP"] = udp_scan(target, ports)

            for protocol, scan_results in results.items():
                for port, status in scan_results.items():
                    banner = status if self.retrieve_banner.get() else "Unknown"
                    vuln = check_vulnerabilities(port) if self.check_vuln.get() else "Not Checked"
                    self.tree.insert("", "end", values=(target, port, protocol, banner, vuln))

        threading.Thread(target=run_scan, daemon=True).start()

    def sort_results(self, col):
        """Sorts the results in the table."""
        items = [(self.tree.set(child, col), child) for child in self.tree.get_children()]
        items.sort(reverse=False)  # Change to True for descending order

        for index, (val, child) in enumerate(items):
            self.tree.move(child, "", index)

    def clear_results(self):
        """Clears the results from the table."""
        self.tree.delete(*self.tree.get_children())

    def save_results(self):
        """Saves the scan results to a file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                for row in self.tree.get_children():
                    f.write("\t".join(self.tree.item(row)["values"]) + "\n")
            messagebox.showinfo("Success", "Results saved successfully.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkScannerGUI(root)
    root.mainloop()
