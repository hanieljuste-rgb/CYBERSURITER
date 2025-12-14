#!/usr/bin/env python3
"""
📡 Network Scanner - Scanner de réseau local
Auteur: Formation Cybersécurité
Usage: python network_scanner.py
⚠️ À utiliser uniquement sur VOTRE propre réseau !
"""

import subprocess
import socket
import concurrent.futures
import ipaddress
import re
import os

class NetworkScanner:
    def __init__(self):
        self.local_ip = self.get_local_ip()
        self.network = self.get_network()
    
    def get_local_ip(self):
        """Obtient l'IP locale"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def get_network(self):
        """Obtient le réseau local (ex: 192.168.1.0/24)"""
        parts = self.local_ip.split('.')
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    
    def ping(self, ip):
        """Ping une IP"""
        try:
            # Windows ping
            result = subprocess.run(
                ['ping', '-n', '1', '-w', '500', str(ip)],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def scan_port(self, ip, port, timeout=1):
        """Scan un port spécifique"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((str(ip), port))
            sock.close()
            return result == 0
        except:
            return False
    
    def get_hostname(self, ip):
        """Obtient le hostname d'une IP"""
        try:
            return socket.gethostbyaddr(str(ip))[0]
        except:
            return "Unknown"
    
    def scan_network(self):
        """Scan tout le réseau local"""
        print(f"\n🔍 Scan du réseau: {self.network}")
        print(f"📍 Votre IP: {self.local_ip}")
        print("-" * 50)
        
        network = ipaddress.IPv4Network(self.network, strict=False)
        active_hosts = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(self.ping, ip): ip for ip in network.hosts()}
            
            for future in concurrent.futures.as_completed(futures):
                ip = futures[future]
                if future.result():
                    hostname = self.get_hostname(ip)
                    active_hosts.append((str(ip), hostname))
                    print(f"  ✅ {ip} - {hostname}")
        
        return active_hosts
    
    def scan_ports(self, ip, ports=None):
        """Scan les ports d'une IP"""
        if ports is None:
            # Ports courants
            ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 
                     443, 445, 993, 995, 1433, 3306, 3389, 5555, 8080, 8443]
        
        print(f"\n🔍 Scan des ports de {ip}")
        print("-" * 50)
        
        open_ports = []
        
        port_names = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 135: "RPC",
            139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            993: "IMAPS", 995: "POP3S", 1433: "MSSQL", 3306: "MySQL",
            3389: "RDP", 5555: "ADB", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt"
        }
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.scan_port, ip, port): port for port in ports}
            
            for future in concurrent.futures.as_completed(futures):
                port = futures[future]
                if future.result():
                    service = port_names.get(port, "Unknown")
                    open_ports.append((port, service))
                    print(f"  ✅ Port {port}/tcp - {service} - OUVERT")
        
        return open_ports
    
    def get_arp_table(self):
        """Obtient la table ARP (adresses MAC)"""
        try:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            return result.stdout
        except:
            return "Erreur lors de la lecture de la table ARP"
    
    def get_wifi_networks(self):
        """Liste les réseaux Wi-Fi disponibles"""
        try:
            result = subprocess.run(
                ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
                capture_output=True,
                text=True
            )
            return result.stdout
        except:
            return "Erreur lors du scan Wi-Fi"


def menu():
    """Menu interactif"""
    scanner = NetworkScanner()
    
    while True:
        print("\n" + "="*50)
        print("📡 NETWORK SCANNER - Menu Principal")
        print("="*50)
        print(f"📍 Votre IP: {scanner.local_ip}")
        print(f"🌐 Réseau: {scanner.network}")
        print("="*50)
        print("1. 🔍 Scanner le réseau (trouver les appareils)")
        print("2. 🔓 Scanner les ports d'une IP")
        print("3. 📋 Voir la table ARP (adresses MAC)")
        print("4. 📶 Lister les réseaux Wi-Fi")
        print("5. 🎯 Scan complet (réseau + ports)")
        print("0. ❌ Quitter")
        print("="*50)
        
        choice = input("Choix: ").strip()
        
        if choice == '1':
            hosts = scanner.scan_network()
            print(f"\n📊 {len(hosts)} appareils trouvés sur le réseau")
        
        elif choice == '2':
            ip = input("IP à scanner (ex: 192.168.1.1): ").strip()
            scanner.scan_ports(ip)
        
        elif choice == '3':
            print("\n📋 Table ARP:")
            print(scanner.get_arp_table())
        
        elif choice == '4':
            print("\n📶 Réseaux Wi-Fi disponibles:")
            print(scanner.get_wifi_networks())
        
        elif choice == '5':
            hosts = scanner.scan_network()
            if hosts:
                print("\n🎯 Scan des ports pour chaque hôte...")
                for ip, hostname in hosts:
                    scanner.scan_ports(ip)
        
        elif choice == '0':
            print("👋 Au revoir!")
            break
        
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    print("⚠️  AVERTISSEMENT: Utilisez ce scanner uniquement sur votre propre réseau!")
    print("    Scanner un réseau sans autorisation est ILLÉGAL.")
    input("    Appuyez sur Entrée pour continuer...")
    menu()
