#!/usr/bin/env python3
"""
📡 Module de Scanning - Ports & Réseaux
Scanner de ports et découverte réseau
"""

import os
import sys
import socket
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
    B = '\033[94m'; M = '\033[95m'; C = '\033[96m'
    W = '\033[97m'; X = '\033[0m'; BOLD = '\033[1m'

def banner():
    print(f"""
{C.C}{C.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║              📡 MODULE SCANNING - PORTS & RÉSEAUX             ║
╠═══════════════════════════════════════════════════════════════╣
║  Découverte réseau et scan de ports - Usage légal uniquement  ║
╚═══════════════════════════════════════════════════════════════╝
{C.X}
{C.Y}⚠️ Scannez UNIQUEMENT vos propres systèmes ou avec autorisation !{C.X}
""")

def menu():
    print(f"""
{C.BOLD}═══════════════════════════════════════════════════════════════
                        OUTILS DE SCAN
═══════════════════════════════════════════════════════════════{C.X}

  {C.C}[1]{C.X}  Port Scanner - Scan rapide des ports
  {C.C}[2]{C.X}  Service Detection - Détection des services
  {C.C}[3]{C.X}  Network Discovery - Découverte du réseau local
  {C.C}[4]{C.X}  Ping Sweep - Hôtes actifs sur le réseau
  {C.C}[5]{C.X}  Banner Grabbing - Récupération des bannières
  {C.C}[6]{C.X}  Nmap Guide - Comment utiliser Nmap
  {C.C}[7]{C.X}  Scan Votre Réseau Local
  
  {C.R}[0]{C.X}  Retour au menu principal
""")

# Ports communs avec leurs services
COMMON_PORTS = {
    21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
    80: 'HTTP', 110: 'POP3', 135: 'MSRPC', 139: 'NetBIOS', 
    143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 993: 'IMAPS',
    995: 'POP3S', 1433: 'MSSQL', 1521: 'Oracle', 3306: 'MySQL',
    3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC', 6379: 'Redis',
    8080: 'HTTP-Proxy', 8443: 'HTTPS-Alt', 27017: 'MongoDB'
}

def port_scan(target, ports=None):
    """Scan des ports d'une cible"""
    print(f"\n{C.C}═══ PORT SCANNER ═══{C.X}\n")
    
    if not target:
        target = input(f"{C.Y}Entrez l'IP ou le domaine cible : {C.X}").strip()
    
    if not ports:
        port_range = input(f"{C.Y}Ports à scanner (ex: 1-1000 ou 22,80,443) [défaut: communs] : {C.X}").strip()
        
        if not port_range:
            ports = list(COMMON_PORTS.keys())
        elif '-' in port_range:
            start, end = map(int, port_range.split('-'))
            ports = range(start, end + 1)
        elif ',' in port_range:
            ports = [int(p.strip()) for p in port_range.split(',')]
        else:
            ports = [int(port_range)]
    
    print(f"\n{C.G}[+] Scan de {target} - {len(list(ports))} ports{C.X}")
    print(f"{C.C}[*] Démarré à {datetime.now().strftime('%H:%M:%S')}{C.X}\n")
    
    open_ports = []
    
    def scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            sock.close()
            
            if result == 0:
                service = COMMON_PORTS.get(port, 'Unknown')
                return (port, service)
        except:
            pass
        return None
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(scan_port, ports)
        
        for result in results:
            if result:
                port, service = result
                open_ports.append(result)
                print(f"  {C.G}[OPEN]{C.X} Port {port}/tcp - {service}")
    
    print(f"\n{C.C}[*] Scan terminé - {len(open_ports)} ports ouverts trouvés{C.X}")
    return open_ports

def banner_grab(target, port):
    """Récupère la bannière d'un service"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((target, port))
        
        # Envoyer une requête basique
        if port in [80, 8080, 443, 8443]:
            sock.send(b'HEAD / HTTP/1.1\r\nHost: ' + target.encode() + b'\r\n\r\n')
        else:
            sock.send(b'\r\n')
        
        banner = sock.recv(1024).decode('utf-8', errors='ignore')
        sock.close()
        return banner.strip()[:200]
    except:
        return None

def service_detection():
    """Détection des services avec banner grabbing"""
    print(f"\n{C.C}═══ SERVICE DETECTION ═══{C.X}\n")
    target = input(f"{C.Y}Entrez l'IP ou le domaine cible : {C.X}").strip()
    
    print(f"\n{C.G}[+] Détection des services sur {target}...{C.X}\n")
    
    # Scan des ports communs d'abord
    open_ports = []
    for port in COMMON_PORTS.keys():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((target, port)) == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
    
    # Banner grabbing
    print(f"  {'PORT':<10}{'SERVICE':<15}{'BANNER'}")
    print(f"  {'-'*60}")
    
    for port in open_ports:
        service = COMMON_PORTS.get(port, 'Unknown')
        banner = banner_grab(target, port)
        banner_short = banner[:40] + '...' if banner and len(banner) > 40 else banner or 'N/A'
        print(f"  {C.G}{port:<10}{service:<15}{C.X}{banner_short}")

def network_discovery():
    """Découverte des hôtes sur le réseau local"""
    print(f"\n{C.C}═══ NETWORK DISCOVERY ═══{C.X}\n")
    
    # Obtenir l'IP locale
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"{C.G}[+] Votre IP locale : {local_ip}{C.X}")
    
    # Déterminer le sous-réseau
    ip_parts = local_ip.split('.')
    subnet = '.'.join(ip_parts[:3])
    
    print(f"{C.C}[*] Scan du sous-réseau {subnet}.0/24...{C.X}\n")
    
    active_hosts = []
    
    def ping_host(ip):
        param = '-n' if os.name == 'nt' else '-c'
        command = ['ping', param, '1', '-w', '500', ip]
        try:
            result = subprocess.run(command, capture_output=True, timeout=2)
            if result.returncode == 0:
                return ip
        except:
            pass
        return None
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        ips = [f"{subnet}.{i}" for i in range(1, 255)]
        results = executor.map(ping_host, ips)
        
        for result in results:
            if result:
                active_hosts.append(result)
                try:
                    hostname = socket.gethostbyaddr(result)[0]
                except:
                    hostname = "N/A"
                print(f"  {C.G}[ALIVE]{C.X} {result} - {hostname}")
    
    print(f"\n{C.C}[*] {len(active_hosts)} hôtes actifs trouvés{C.X}")

def scan_local_network():
    """Scan complet du réseau local"""
    print(f"\n{C.C}═══ SCAN RÉSEAU LOCAL ═══{C.X}\n")
    
    # ARP table
    print(f"{C.Y}[*] Table ARP actuelle :{C.X}\n")
    subprocess.run(['arp', '-a'], shell=True)
    
    print(f"\n{C.Y}[*] Connexions actives :{C.X}\n")
    subprocess.run(['netstat', '-an'], shell=True)

def nmap_guide():
    """Guide d'utilisation de Nmap"""
    guide = f"""
{C.C}{C.BOLD}═══ GUIDE NMAP ═══{C.X}

{C.Y}Nmap est l'outil de scan de référence. Installez-le depuis nmap.org{C.X}

{C.BOLD}Scans de base:{C.X}
  {C.G}nmap 192.168.1.1{C.X}              - Scan basique
  {C.G}nmap -sV 192.168.1.1{C.X}          - Détection de versions
  {C.G}nmap -O 192.168.1.1{C.X}           - Détection OS
  {C.G}nmap -A 192.168.1.1{C.X}           - Scan agressif (tout)

{C.BOLD}Scans de ports:{C.X}
  {C.G}nmap -p 22,80,443 target{C.X}      - Ports spécifiques
  {C.G}nmap -p 1-1000 target{C.X}         - Plage de ports
  {C.G}nmap -p- target{C.X}               - Tous les ports (65535)
  {C.G}nmap --top-ports 100 target{C.X}   - Top 100 ports

{C.BOLD}Types de scans:{C.X}
  {C.G}nmap -sT target{C.X}   - TCP Connect (bruyant)
  {C.G}nmap -sS target{C.X}   - SYN Scan (furtif, root requis)
  {C.G}nmap -sU target{C.X}   - UDP Scan
  {C.G}nmap -sn target{C.X}   - Ping Scan (découverte)

{C.BOLD}Découverte réseau:{C.X}
  {C.G}nmap -sn 192.168.1.0/24{C.X}       - Scan de tout le sous-réseau

{C.BOLD}Scripts NSE:{C.X}
  {C.G}nmap --script vuln target{C.X}     - Scan de vulnérabilités
  {C.G}nmap --script http-enum target{C.X} - Énumération HTTP

{C.BOLD}Sauvegarde:{C.X}
  {C.G}nmap -oN scan.txt target{C.X}      - Sortie normale
  {C.G}nmap -oX scan.xml target{C.X}      - Sortie XML
"""
    print(guide)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    
    while True:
        menu()
        choice = input(f"\n{C.C}Choisissez une option : {C.X}").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            port_scan(None)
        elif choice == '2':
            service_detection()
        elif choice == '3':
            network_discovery()
        elif choice == '4':
            network_discovery()  # Même fonction
        elif choice == '5':
            target = input(f"{C.Y}IP cible : {C.X}").strip()
            port = int(input(f"{C.Y}Port : {C.X}").strip())
            banner = banner_grab(target, port)
            print(f"\n{C.G}Banner:{C.X}\n{banner}")
        elif choice == '6':
            nmap_guide()
        elif choice == '7':
            scan_local_network()
        else:
            print(f"\n{C.R}[!] Option invalide{C.X}")
        
        input(f"\n{C.Y}Appuyez sur Entrée pour continuer...{C.X}")

if __name__ == "__main__":
    main()
