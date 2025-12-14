#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║              SCANNER DE PORTS - OUTIL DE RECONNAISSANCE          ║
║                                                                  ║
║  ⚠️  USAGE ÉDUCATIF - SCANNER UNIQUEMENT VOS PROPRES SYSTÈMES ⚠️ ║
╚══════════════════════════════════════════════════════════════════╝
"""

import socket
import threading
from datetime import datetime
import sys

# Ports communs et leurs services
COMMON_PORTS = {
    21: "FTP - Transfert de fichiers",
    22: "SSH - Accès sécurisé",
    23: "Telnet - Accès non sécurisé ⚠️",
    25: "SMTP - Email sortant",
    53: "DNS - Noms de domaine",
    80: "HTTP - Web non sécurisé",
    110: "POP3 - Email",
    135: "RPC - Windows",
    139: "NetBIOS - Partage Windows",
    143: "IMAP - Email",
    443: "HTTPS - Web sécurisé",
    445: "SMB - Partage de fichiers Windows ⚠️",
    993: "IMAPS - Email sécurisé",
    995: "POP3S - Email sécurisé",
    1433: "MSSQL - Base de données",
    1521: "Oracle - Base de données",
    3306: "MySQL - Base de données",
    3389: "RDP - Bureau à distance Windows ⚠️",
    5432: "PostgreSQL - Base de données",
    5900: "VNC - Bureau à distance",
    6379: "Redis - Base de données",
    8080: "HTTP Proxy",
    8443: "HTTPS Alt",
    27017: "MongoDB - Base de données",
}

VULNERABILITIES = {
    21: "Brute force FTP, Anonymous login",
    22: "Brute force SSH, Anciennes versions vulnérables",
    23: "Telnet transmet en clair - DANGER!",
    80: "Injection SQL, XSS, Directory traversal",
    443: "Heartbleed, POODLE, anciennes versions TLS",
    445: "EternalBlue (WannaCry), MS17-010",
    3306: "Brute force MySQL, anciennes versions",
    3389: "BlueKeep (CVE-2019-0708) - CRITIQUE!",
    5900: "VNC sans authentification",
}

open_ports = []
lock = threading.Lock()

def scan_port(target, port, timeout=1):
    """Scanner un port spécifique"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        
        if result == 0:
            with lock:
                open_ports.append(port)
            return True
    except:
        pass
    return False

def get_banner(target, port, timeout=2):
    """Récupérer la bannière du service"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))
        
        # Envoyer une requête basique pour certains services
        if port in [80, 8080]:
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        else:
            sock.send(b"\r\n")
        
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner[:100] if banner else None
    except:
        return None

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              🔍 SCANNER DE PORTS - RECONNAISSANCE                ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Cet outil scanne les ports ouverts sur une cible.               ║
║  Les hackers l'utilisent pour trouver des vulnérabilités.        ║
║                                                                  ║
║  🎯 CE QUE FONT LES HACKERS:                                     ║
║     1. Scanner les ports ouverts                                 ║
║     2. Identifier les services                                   ║
║     3. Chercher des versions vulnérables                         ║
║     4. Exploiter les failles                                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Demander la cible
    print("🎯 Cibles suggérées (légales):")
    print("   - 127.0.0.1 (votre PC)")
    print("   - scanme.nmap.org (serveur de test officiel)")
    print("   - Votre routeur (ex: 192.168.1.1)")
    print()
    
    target = input("Entrez l'adresse IP ou le domaine: ").strip()
    if not target:
        target = "127.0.0.1"
    
    print(f"\n🔍 Résolution de {target}...")
    try:
        ip = socket.gethostbyname(target)
        print(f"✅ IP résolue: {ip}")
    except:
        print("❌ Impossible de résoudre cette adresse!")
        return
    
    print(f"\n🚀 Scan des ports communs sur {target} ({ip})...")
    print("   Cela peut prendre 30-60 secondes...\n")
    
    start_time = datetime.now()
    
    # Scanner avec threads
    threads = []
    ports_to_scan = list(COMMON_PORTS.keys())
    
    for port in ports_to_scan:
        t = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(t)
        t.start()
    
    # Attendre tous les threads
    for t in threads:
        t.join()
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Afficher les résultats
    print("\n" + "=" * 70)
    print(f"📊 RÉSULTATS DU SCAN - {target}")
    print("=" * 70)
    print(f"⏱️  Durée: {duration:.2f} secondes")
    print(f"🔢 Ports scannés: {len(ports_to_scan)}")
    print(f"✅ Ports ouverts: {len(open_ports)}")
    print("=" * 70 + "\n")
    
    if open_ports:
        print("🚪 PORTS OUVERTS:\n")
        print(f"{'PORT':<8} {'SERVICE':<35} {'VULNÉRABILITÉS'}")
        print("-" * 70)
        
        for port in sorted(open_ports):
            service = COMMON_PORTS.get(port, "Inconnu")
            vuln = VULNERABILITIES.get(port, "-")
            
            # Couleur pour les ports critiques
            if port in [23, 445, 3389]:
                prefix = "⚠️ "
            else:
                prefix = "   "
            
            print(f"{prefix}{port:<6} {service:<35} {vuln}")
        
        print("-" * 70)
        
        # Récupérer les bannières
        print("\n🏷️  BANNIÈRES DES SERVICES:\n")
        for port in sorted(open_ports):
            banner = get_banner(ip, port)
            if banner:
                print(f"   Port {port}: {banner[:60]}...")
    else:
        print("❌ Aucun port ouvert trouvé (ou tous filtrés par un firewall)")
    
    # Conseils de hacking
    print("\n" + "=" * 70)
    print("🎓 CE QUE FERAIT UN HACKER ENSUITE:")
    print("=" * 70)
    print("""
   1. Rechercher les CVE pour chaque service
      → Ex: searchsploit apache 2.4
      
   2. Utiliser des outils spécialisés
      → Nikto pour HTTP
      → Hydra pour brute force
      → Metasploit pour exploitation
      
   3. Tester les identifiants par défaut
      → admin:admin, root:root, etc.
      
   4. Chercher des fichiers sensibles
      → /robots.txt, /.git, /backup.sql
    """)

if __name__ == "__main__":
    main()
