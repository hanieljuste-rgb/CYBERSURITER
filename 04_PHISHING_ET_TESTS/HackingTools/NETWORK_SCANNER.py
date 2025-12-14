#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║     ███╗   ██╗███████╗████████╗██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗              ║
║     ████╗  ██║██╔════╝╚══██╔══╝██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝              ║
║     ██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝               ║
║     ██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗               ║
║     ██║ ╚████║███████╗   ██║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗              ║
║     ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝              ║
║                                                                                  ║
║                    🔍 SCANNER RÉSEAU AVANCÉ v2.0 🔍                              ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import socket
import subprocess
import threading
import time
import json
import re
import os
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

OUTPUT_DIR = Path(r"C:\Users\davis\OneDrive\Bureau\HACKING\02_EXTRACTION_DONNEES\SCANS_RESEAU")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Couleurs terminal
class C:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Ports communs avec services et vulnérabilités
PORTS_DATABASE = {
    21: {"service": "FTP", "vuln": "Anonymous login, Brute force", "risk": "HIGH"},
    22: {"service": "SSH", "vuln": "Brute force, anciennes versions", "risk": "MEDIUM"},
    23: {"service": "Telnet", "vuln": "Pas de chiffrement!", "risk": "CRITICAL"},
    25: {"service": "SMTP", "vuln": "Open relay, spam", "risk": "MEDIUM"},
    53: {"service": "DNS", "vuln": "Zone transfer, amplification", "risk": "MEDIUM"},
    80: {"service": "HTTP", "vuln": "XSS, SQLi, traversal", "risk": "HIGH"},
    110: {"service": "POP3", "vuln": "Mots de passe en clair", "risk": "HIGH"},
    135: {"service": "RPC", "vuln": "MS exploits", "risk": "HIGH"},
    139: {"service": "NetBIOS", "vuln": "Enumeration, null sessions", "risk": "HIGH"},
    143: {"service": "IMAP", "vuln": "Mots de passe en clair", "risk": "MEDIUM"},
    443: {"service": "HTTPS", "vuln": "Heartbleed, POODLE", "risk": "LOW"},
    445: {"service": "SMB", "vuln": "EternalBlue, WannaCry", "risk": "CRITICAL"},
    1433: {"service": "MSSQL", "vuln": "Brute force, default creds", "risk": "HIGH"},
    1521: {"service": "Oracle", "vuln": "TNS Listener attacks", "risk": "HIGH"},
    3306: {"service": "MySQL", "vuln": "Brute force, root sans mdp", "risk": "HIGH"},
    3389: {"service": "RDP", "vuln": "BlueKeep CVE-2019-0708", "risk": "CRITICAL"},
    5432: {"service": "PostgreSQL", "vuln": "Brute force", "risk": "MEDIUM"},
    5900: {"service": "VNC", "vuln": "Pas d'auth, brute force", "risk": "HIGH"},
    6379: {"service": "Redis", "vuln": "Pas d'auth par défaut", "risk": "CRITICAL"},
    8080: {"service": "HTTP-Proxy", "vuln": "Proxy ouvert", "risk": "MEDIUM"},
    8443: {"service": "HTTPS-Alt", "vuln": "Interface admin", "risk": "MEDIUM"},
    27017: {"service": "MongoDB", "vuln": "Pas d'auth par défaut", "risk": "CRITICAL"},
}

# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    """Affiche la bannière"""
    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                     🔍 NETWORK SCANNER AVANCÉ v2.0 🔍                        ║
╚══════════════════════════════════════════════════════════════════════════════╝{C.END}
    """)

def get_local_ip():
    """Obtient l'IP locale"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_network_range():
    """Calcule la plage réseau"""
    ip = get_local_ip()
    parts = ip.split('.')
    return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"

def resolve_hostname(ip):
    """Résout le nom d'hôte"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "N/A"

def get_mac_address(ip):
    """Obtient l'adresse MAC via ARP"""
    try:
        result = subprocess.run(
            f'arp -a {ip}',
            shell=True, capture_output=True, text=True, timeout=5
        )
        match = re.search(r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}', result.stdout)
        if match:
            return match.group(0)
    except:
        pass
    return "N/A"

def get_mac_vendor(mac):
    """Identifie le fabricant via les 3 premiers octets MAC"""
    vendors = {
        "00:50:56": "VMware",
        "00:0c:29": "VMware",
        "08:00:27": "VirtualBox",
        "52:54:00": "QEMU/KVM",
        "b8:27:eb": "Raspberry Pi",
        "dc:a6:32": "Raspberry Pi",
        "00:1a:79": "TECNO",
        "ac:cf:23": "TECNO",
        "44:d9:e7": "Ubiquiti",
        "00:11:32": "Synology",
        "00:26:ab": "D-Link",
        "c8:3a:35": "Tenda",
        "e4:f4:c6": "Xiaomi",
        "64:cc:2e": "Xiaomi",
        "30:b4:9e": "TP-Link",
        "50:c7:bf": "TP-Link",
        "00:23:68": "Apple",
        "3c:06:30": "Apple",
        "88:66:5a": "Apple",
        "fc:fc:48": "Apple",
        "5c:f5:da": "Apple",
        "94:65:2d": "OnePlus",
        "a0:8c:fd": "Huawei",
        "48:db:50": "Huawei",
        "88:53:2e": "Intel",
        "00:1e:67": "Intel",
        "5c:e0:c5": "Samsung",
        "8c:71:f8": "Samsung",
        "00:15:5d": "Microsoft (Hyper-V)",
    }
    
    if mac and mac != "N/A":
        prefix = mac[:8].lower().replace("-", ":")
        for vendor_prefix, vendor_name in vendors.items():
            if prefix.startswith(vendor_prefix.lower()):
                return vendor_name
    return "Inconnu"

# ═══════════════════════════════════════════════════════════════════════════════
# SCAN DE PORTS
# ═══════════════════════════════════════════════════════════════════════════════

def scan_port(ip, port, timeout=1):
    """Scanne un port spécifique"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def get_banner(ip, port, timeout=2):
    """Récupère la bannière du service"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        
        # Envoyer une requête basique pour certains services
        if port == 80 or port == 8080:
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        elif port == 21:
            pass  # FTP envoie sa bannière automatiquement
        elif port == 22:
            pass  # SSH envoie sa bannière automatiquement
        else:
            sock.send(b"\r\n")
        
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner[:100] if banner else "N/A"
    except:
        return "N/A"

def scan_host_ports(ip, ports=None, timeout=1, get_banners=False):
    """Scanne tous les ports d'un hôte"""
    if ports is None:
        ports = list(PORTS_DATABASE.keys())
    
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_port = {executor.submit(scan_port, ip, port, timeout): port for port in ports}
        
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                if future.result():
                    port_info = PORTS_DATABASE.get(port, {"service": "Unknown", "vuln": "N/A", "risk": "LOW"})
                    banner = get_banner(ip, port) if get_banners else "N/A"
                    open_ports.append({
                        "port": port,
                        "service": port_info["service"],
                        "vuln": port_info["vuln"],
                        "risk": port_info["risk"],
                        "banner": banner
                    })
            except:
                pass
    
    return sorted(open_ports, key=lambda x: x["port"])

def full_port_scan(ip, start=1, end=1024, timeout=0.5):
    """Scan complet de tous les ports"""
    open_ports = []
    total = end - start + 1
    
    print(f"\n    {C.CYAN}🔍 Scan de {ip} ports {start}-{end}...{C.END}")
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, ip, port, timeout): port for port in range(start, end + 1)}
        done = 0
        
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            done += 1
            
            # Progress bar
            if done % 100 == 0:
                pct = int(done / total * 100)
                bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
                print(f"\r    [{bar}] {pct}% ({done}/{total})", end="", flush=True)
            
            try:
                if future.result():
                    service = PORTS_DATABASE.get(port, {}).get("service", "Unknown")
                    open_ports.append({"port": port, "service": service})
            except:
                pass
    
    print(f"\r    {C.GREEN}✓ Scan terminé - {len(open_ports)} ports ouverts{C.END}          ")
    return sorted(open_ports, key=lambda x: x["port"])

# ═══════════════════════════════════════════════════════════════════════════════
# SCAN DU RÉSEAU LOCAL
# ═══════════════════════════════════════════════════════════════════════════════

def ping_host(ip, timeout=1):
    """Vérifie si un hôte est en ligne"""
    try:
        result = subprocess.run(
            f'ping -n 1 -w {timeout * 1000} {ip}',
            shell=True, capture_output=True, text=True, timeout=timeout + 2
        )
        return "TTL=" in result.stdout
    except:
        return False

def scan_network(network_range=None, timeout=1):
    """Scanne tout le réseau local"""
    if network_range is None:
        local_ip = get_local_ip()
        parts = local_ip.split('.')
        network_range = f"{parts[0]}.{parts[1]}.{parts[2]}"
    else:
        network_range = network_range.rsplit('.', 1)[0]
    
    print(f"\n    {C.CYAN}🌐 Scan du réseau {network_range}.0/24...{C.END}\n")
    
    hosts = []
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_ip = {
            executor.submit(ping_host, f"{network_range}.{i}", timeout): f"{network_range}.{i}" 
            for i in range(1, 255)
        }
        
        for i, future in enumerate(as_completed(future_to_ip)):
            ip = future_to_ip[future]
            
            # Progress
            pct = int((i + 1) / 254 * 100)
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            print(f"\r    [{bar}] {pct}%", end="", flush=True)
            
            try:
                if future.result():
                    hostname = resolve_hostname(ip)
                    mac = get_mac_address(ip)
                    vendor = get_mac_vendor(mac)
                    
                    hosts.append({
                        "ip": ip,
                        "hostname": hostname,
                        "mac": mac,
                        "vendor": vendor
                    })
            except:
                pass
    
    print(f"\r    {C.GREEN}✓ Scan terminé - {len(hosts)} hôtes trouvés{C.END}          \n")
    return sorted(hosts, key=lambda x: [int(p) for p in x["ip"].split('.')])

def deep_scan_network():
    """Scan approfondi du réseau avec ports"""
    hosts = scan_network()
    
    print(f"\n    {C.CYAN}🔍 Scan des ports sur {len(hosts)} hôtes...{C.END}\n")
    
    for i, host in enumerate(hosts):
        print(f"    [{i+1}/{len(hosts)}] {host['ip']} ({host['vendor']})...")
        host['ports'] = scan_host_ports(host['ip'], timeout=0.5)
        
        if host['ports']:
            print(f"        {C.GREEN}→ {len(host['ports'])} ports ouverts{C.END}")
    
    return hosts

# ═══════════════════════════════════════════════════════════════════════════════
# DÉTECTION DE VULNÉRABILITÉS
# ═══════════════════════════════════════════════════════════════════════════════

def check_vulnerabilities(host_data):
    """Analyse les vulnérabilités d'un hôte"""
    vulns = []
    
    for port_info in host_data.get('ports', []):
        port = port_info['port']
        risk = port_info.get('risk', 'LOW')
        
        if risk in ['HIGH', 'CRITICAL']:
            vulns.append({
                'port': port,
                'service': port_info['service'],
                'risk': risk,
                'description': port_info.get('vuln', 'N/A')
            })
    
    return vulns

def vulnerability_report(hosts):
    """Génère un rapport de vulnérabilités"""
    print(f"\n{C.RED}{'═' * 70}{C.END}")
    print(f"{C.BOLD}{C.RED}⚠️  RAPPORT DE VULNÉRABILITÉS{C.END}")
    print(f"{C.RED}{'═' * 70}{C.END}\n")
    
    critical_count = 0
    high_count = 0
    
    for host in hosts:
        vulns = check_vulnerabilities(host)
        
        if vulns:
            print(f"    {C.YELLOW}📌 {host['ip']}{C.END} ({host.get('vendor', 'N/A')})")
            
            for v in vulns:
                if v['risk'] == 'CRITICAL':
                    color = C.RED
                    critical_count += 1
                else:
                    color = C.YELLOW
                    high_count += 1
                
                print(f"        {color}[{v['risk']}]{C.END} Port {v['port']} ({v['service']})")
                print(f"              → {v['description']}")
            print()
    
    print(f"\n    {C.RED}🔴 CRITIQUES: {critical_count}{C.END}")
    print(f"    {C.YELLOW}🟡 HAUTES: {high_count}{C.END}")
    
    return critical_count, high_count

# ═══════════════════════════════════════════════════════════════════════════════
# SCAN WiFi
# ═══════════════════════════════════════════════════════════════════════════════

def scan_wifi_networks():
    """Scanne les réseaux WiFi disponibles"""
    print(f"\n    {C.CYAN}📡 Scan des réseaux WiFi...{C.END}\n")
    
    try:
        result = subprocess.run(
            'netsh wlan show networks mode=bssid',
            shell=True, capture_output=True, text=True
        )
        
        networks = []
        current_network = {}
        
        for line in result.stdout.split('\n'):
            line = line.strip()
            
            if line.startswith('SSID') and ':' in line and 'BSSID' not in line:
                if current_network:
                    networks.append(current_network)
                current_network = {'ssid': line.split(':', 1)[1].strip()}
            elif 'Type' in line and ':' in line:
                current_network['type'] = line.split(':', 1)[1].strip()
            elif 'Authentification' in line or 'Authentication' in line:
                current_network['auth'] = line.split(':', 1)[1].strip()
            elif 'Chiffrement' in line or 'Encryption' in line or 'Cipher' in line:
                current_network['encryption'] = line.split(':', 1)[1].strip()
            elif 'BSSID' in line:
                current_network['bssid'] = line.split(':', 1)[1].strip()
            elif 'Signal' in line:
                signal = line.split(':', 1)[1].strip().replace('%', '')
                current_network['signal'] = int(signal) if signal.isdigit() else 0
            elif 'Canal' in line or 'Channel' in line:
                current_network['channel'] = line.split(':', 1)[1].strip()
        
        if current_network:
            networks.append(current_network)
        
        # Trier par signal
        networks.sort(key=lambda x: x.get('signal', 0), reverse=True)
        
        return networks
    except Exception as e:
        print(f"    {C.RED}Erreur: {e}{C.END}")
        return []

def display_wifi_networks(networks):
    """Affiche les réseaux WiFi"""
    print(f"\n    {C.CYAN}{'═' * 70}{C.END}")
    print(f"    {C.BOLD}📡 RÉSEAUX WIFI DÉTECTÉS ({len(networks)}){C.END}")
    print(f"    {C.CYAN}{'═' * 70}{C.END}\n")
    
    for i, net in enumerate(networks, 1):
        ssid = net.get('ssid', 'N/A')
        signal = net.get('signal', 0)
        auth = net.get('auth', 'N/A')
        channel = net.get('channel', 'N/A')
        
        # Barre de signal
        bars = "█" * (signal // 20) + "░" * (5 - signal // 20)
        
        # Couleur selon sécurité
        if 'Open' in auth or 'Ouvert' in auth:
            sec_color = C.RED
            sec_icon = "🔓"
        elif 'WEP' in auth:
            sec_color = C.YELLOW
            sec_icon = "⚠️"
        elif 'WPA3' in auth:
            sec_color = C.GREEN
            sec_icon = "🔒"
        else:
            sec_color = C.CYAN
            sec_icon = "🔐"
        
        print(f"    {C.WHITE}[{i:2d}]{C.END} {ssid[:25]:<25} [{bars}] {signal}%")
        print(f"         {sec_color}{sec_icon} {auth}{C.END} | Canal: {channel}")
        print()

def get_saved_wifi_passwords():
    """Récupère les mots de passe WiFi enregistrés"""
    print(f"\n    {C.CYAN}🔑 Récupération des mots de passe WiFi enregistrés...{C.END}\n")
    
    passwords = []
    
    try:
        # Lister les profils
        result = subprocess.run(
            'netsh wlan show profiles',
            shell=True, capture_output=True, text=True
        )
        
        profiles = re.findall(r':\s*(.+)', result.stdout)
        profiles = [p.strip() for p in profiles if p.strip()]
        
        for profile in profiles:
            try:
                detail = subprocess.run(
                    f'netsh wlan show profile name="{profile}" key=clear',
                    shell=True, capture_output=True, text=True
                )
                
                # Chercher le mot de passe
                key_match = re.search(r'(Contenu de la cl|Key Content)\s*:\s*(.+)', detail.stdout)
                auth_match = re.search(r'(Authentification|Authentication)\s*:\s*(.+)', detail.stdout)
                
                passwords.append({
                    'ssid': profile,
                    'password': key_match.group(2).strip() if key_match else 'N/A',
                    'auth': auth_match.group(2).strip() if auth_match else 'N/A'
                })
            except:
                pass
        
        return passwords
    except Exception as e:
        print(f"    {C.RED}Erreur: {e}{C.END}")
        return []

# ═══════════════════════════════════════════════════════════════════════════════
# EXPORT ET RAPPORTS
# ═══════════════════════════════════════════════════════════════════════════════

def export_scan_results(data, filename=None):
    """Exporte les résultats en JSON"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = OUTPUT_DIR / f"scan_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n    {C.GREEN}✓ Résultats exportés: {filename}{C.END}")
    return filename

def generate_html_report(hosts, filename=None):
    """Génère un rapport HTML"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = OUTPUT_DIR / f"rapport_{timestamp}.html"
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Rapport de Scan Réseau</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a2e; color: #eee; }
            h1 { color: #00ff88; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #333; padding: 10px; text-align: left; }
            th { background: #16213e; color: #00ff88; }
            tr:hover { background: #0f3460; }
            .critical { color: #ff4444; font-weight: bold; }
            .high { color: #ff8800; }
            .medium { color: #ffff00; }
            .low { color: #00ff88; }
        </style>
    </head>
    <body>
        <h1>🔍 Rapport de Scan Réseau</h1>
        <p>Date: """ + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + """</p>
        <h2>Hôtes découverts</h2>
        <table>
            <tr><th>IP</th><th>Hostname</th><th>MAC</th><th>Vendor</th><th>Ports ouverts</th></tr>
    """
    
    for host in hosts:
        ports_str = ", ".join([str(p['port']) for p in host.get('ports', [])])
        html += f"""
            <tr>
                <td>{host['ip']}</td>
                <td>{host.get('hostname', 'N/A')}</td>
                <td>{host.get('mac', 'N/A')}</td>
                <td>{host.get('vendor', 'N/A')}</td>
                <td>{ports_str or 'Aucun'}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n    {C.GREEN}✓ Rapport HTML: {filename}{C.END}")
    return filename

# ═══════════════════════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def show_menu():
    """Affiche le menu"""
    local_ip = get_local_ip()
    
    print(f"""
    {C.CYAN}┌────────────────────────────────────────────────────────────────────┐
    │  💻 IP Locale: {local_ip:<20}                              │
    │  🌐 Réseau: {get_network_range():<23}                              │
    ├────────────────────────────────────────────────────────────────────┤
    │  {C.BOLD}🔍 SCAN RÉSEAU{C.END}{C.CYAN}                                                   │
    ├────────────────────────────────────────────────────────────────────┤
    │  [1] Scanner le réseau local (découverte d'hôtes)                  │
    │  [2] Scan approfondi (hôtes + ports)                               │
    │  [3] Scanner les ports d'une IP spécifique                         │
    │  [4] Scan complet de ports (1-65535)                               │
    ├────────────────────────────────────────────────────────────────────┤
    │  {C.BOLD}📡 WIFI{C.END}{C.CYAN}                                                          │
    ├────────────────────────────────────────────────────────────────────┤
    │  [5] Scanner les réseaux WiFi                                      │
    │  [6] Récupérer mots de passe WiFi enregistrés                      │
    ├────────────────────────────────────────────────────────────────────┤
    │  {C.BOLD}📊 RAPPORTS{C.END}{C.CYAN}                                                      │
    ├────────────────────────────────────────────────────────────────────┤
    │  [7] Rapport de vulnérabilités                                     │
    │  [8] Exporter en JSON                                              │
    │  [9] Générer rapport HTML                                          │
    ├────────────────────────────────────────────────────────────────────┤
    │  [0] Quitter                                                       │
    └────────────────────────────────────────────────────────────────────┘{C.END}
    """)

def main():
    """Fonction principale"""
    print_banner()
    
    hosts_data = []
    
    while True:
        show_menu()
        choice = input(f"\n    {C.GREEN}👉 Choix: {C.END}").strip()
        
        try:
            if choice == "1":
                hosts_data = scan_network()
                for host in hosts_data:
                    print(f"    {C.GREEN}✓{C.END} {host['ip']:<15} {host['hostname'][:20]:<20} {host['mac']:<17} {host['vendor']}")
            
            elif choice == "2":
                hosts_data = deep_scan_network()
                for host in hosts_data:
                    print(f"\n    {C.YELLOW}{host['ip']}{C.END} ({host['vendor']})")
                    for p in host.get('ports', []):
                        print(f"        Port {p['port']}: {p['service']}")
            
            elif choice == "3":
                ip = input("    IP à scanner: ").strip()
                ports = scan_host_ports(ip, get_banners=True)
                print(f"\n    {C.CYAN}Ports ouverts sur {ip}:{C.END}")
                for p in ports:
                    risk_color = C.RED if p['risk'] == 'CRITICAL' else C.YELLOW if p['risk'] == 'HIGH' else C.GREEN
                    print(f"    {risk_color}[{p['risk']}]{C.END} {p['port']:<6} {p['service']:<12} {p['banner'][:40]}")
            
            elif choice == "4":
                ip = input("    IP à scanner: ").strip()
                ports = full_port_scan(ip, 1, 65535)
                for p in ports:
                    print(f"    Port {p['port']}: {p['service']}")
            
            elif choice == "5":
                networks = scan_wifi_networks()
                display_wifi_networks(networks)
            
            elif choice == "6":
                passwords = get_saved_wifi_passwords()
                print(f"\n    {C.CYAN}🔑 Mots de passe WiFi enregistrés:{C.END}\n")
                for p in passwords:
                    print(f"    {C.YELLOW}{p['ssid']}{C.END}")
                    print(f"        Mot de passe: {C.GREEN}{p['password']}{C.END}")
                    print(f"        Sécurité: {p['auth']}\n")
            
            elif choice == "7":
                if not hosts_data:
                    print(f"    {C.YELLOW}Lancez d'abord un scan (option 2){C.END}")
                else:
                    vulnerability_report(hosts_data)
            
            elif choice == "8":
                if hosts_data:
                    export_scan_results(hosts_data)
                else:
                    print(f"    {C.YELLOW}Aucune donnée à exporter{C.END}")
            
            elif choice == "9":
                if hosts_data:
                    generate_html_report(hosts_data)
                else:
                    print(f"    {C.YELLOW}Aucune donnée pour le rapport{C.END}")
            
            elif choice == "0":
                print(f"\n    {C.YELLOW}👋 Au revoir!{C.END}\n")
                break
            
            else:
                print(f"    {C.RED}Option invalide{C.END}")
        
        except KeyboardInterrupt:
            print(f"\n    {C.YELLOW}Interrompu{C.END}")
        except Exception as e:
            print(f"    {C.RED}Erreur: {e}{C.END}")
        
        input(f"\n    {C.CYAN}⏎ Entrée pour continuer...{C.END}")

if __name__ == "__main__":
    main()
