#!/usr/bin/env python3
"""
🔍 Module de Reconnaissance & OSINT
Collecte d'informations légales sur des cibles (avec autorisation)
"""

import os
import sys
import socket
import subprocess
from pathlib import Path

# Couleurs
class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
    B = '\033[94m'; M = '\033[95m'; C = '\033[96m'
    W = '\033[97m'; X = '\033[0m'; BOLD = '\033[1m'

def banner():
    print(f"""
{C.C}{C.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║           🔍 MODULE RECONNAISSANCE & OSINT                    ║
╠═══════════════════════════════════════════════════════════════╣
║  Collecte d'informations publiques de manière légale          ║
╚═══════════════════════════════════════════════════════════════╝
{C.X}
{C.Y}⚠️ Utilisez uniquement sur des cibles autorisées !{C.X}
""")

def menu():
    print(f"""
{C.BOLD}═══════════════════════════════════════════════════════════════
                        OUTILS DISPONIBLES
═══════════════════════════════════════════════════════════════{C.X}

  {C.C}[1]{C.X}  DNS Lookup - Résolution de noms de domaine
  {C.C}[2]{C.X}  WHOIS Lookup - Informations sur un domaine
  {C.C}[3]{C.X}  IP Geolocation - Localisation d'une IP
  {C.C}[4]{C.X}  Subdomain Finder - Recherche de sous-domaines
  {C.C}[5]{C.X}  Email Harvester - Collecte d'emails publics
  {C.C}[6]{C.X}  Social Media Search - Recherche sur réseaux sociaux
  {C.C}[7]{C.X}  Google Dorking Guide - Recherches avancées
  {C.C}[8]{C.X}  HTTP Headers - Analyse des en-têtes HTTP
  
  {C.R}[0]{C.X}  Retour au menu principal
""")

def dns_lookup():
    """Résolution DNS d'un domaine"""
    print(f"\n{C.C}═══ DNS LOOKUP ═══{C.X}\n")
    domain = input(f"{C.Y}Entrez le domaine (ex: google.com) : {C.X}").strip()
    
    if not domain:
        print(f"{C.R}[!] Domaine invalide{C.X}")
        return
    
    print(f"\n{C.G}[+] Résolution DNS pour {domain}:{C.X}\n")
    
    try:
        # Résolution A (IPv4)
        ip = socket.gethostbyname(domain)
        print(f"  {C.C}IPv4 (A):{C.X} {ip}")
        
        # Résolution complète
        results = socket.getaddrinfo(domain, None)
        ips_v6 = set()
        for result in results:
            if result[0] == socket.AF_INET6:
                ips_v6.add(result[4][0])
        
        for ip6 in ips_v6:
            print(f"  {C.C}IPv6 (AAAA):{C.X} {ip6}")
            
    except socket.gaierror as e:
        print(f"{C.R}[!] Erreur: {e}{C.X}")
    
    # Essayer nslookup pour plus de détails
    print(f"\n{C.Y}[*] Détails nslookup:{C.X}")
    subprocess.run(['nslookup', domain], shell=True)

def whois_lookup():
    """WHOIS lookup d'un domaine"""
    print(f"\n{C.C}═══ WHOIS LOOKUP ═══{C.X}\n")
    domain = input(f"{C.Y}Entrez le domaine : {C.X}").strip()
    
    try:
        import whois
        w = whois.whois(domain)
        print(f"\n{C.G}[+] Informations WHOIS pour {domain}:{C.X}\n")
        print(f"  {C.C}Registrar:{C.X} {w.registrar}")
        print(f"  {C.C}Création:{C.X} {w.creation_date}")
        print(f"  {C.C}Expiration:{C.X} {w.expiration_date}")
        print(f"  {C.C}Serveurs DNS:{C.X} {w.name_servers}")
        print(f"  {C.C}Status:{C.X} {w.status}")
    except ImportError:
        print(f"{C.Y}[!] Module 'whois' non installé. Installation...{C.X}")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'python-whois'])
        print(f"{C.G}[+] Relancez la commande.{C.X}")
    except Exception as e:
        print(f"{C.R}[!] Erreur: {e}{C.X}")

def ip_geolocation():
    """Géolocalisation d'une IP"""
    print(f"\n{C.C}═══ IP GEOLOCATION ═══{C.X}\n")
    ip = input(f"{C.Y}Entrez l'adresse IP : {C.X}").strip()
    
    try:
        import requests
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        
        if data['status'] == 'success':
            print(f"\n{C.G}[+] Géolocalisation de {ip}:{C.X}\n")
            print(f"  {C.C}Pays:{C.X} {data.get('country', 'N/A')}")
            print(f"  {C.C}Région:{C.X} {data.get('regionName', 'N/A')}")
            print(f"  {C.C}Ville:{C.X} {data.get('city', 'N/A')}")
            print(f"  {C.C}Code postal:{C.X} {data.get('zip', 'N/A')}")
            print(f"  {C.C}FAI:{C.X} {data.get('isp', 'N/A')}")
            print(f"  {C.C}Organisation:{C.X} {data.get('org', 'N/A')}")
            print(f"  {C.C}Coordonnées:{C.X} {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
        else:
            print(f"{C.R}[!] Impossible de géolocaliser cette IP{C.X}")
    except ImportError:
        print(f"{C.Y}[!] Module 'requests' non installé.{C.X}")
    except Exception as e:
        print(f"{C.R}[!] Erreur: {e}{C.X}")

def http_headers():
    """Analyse des en-têtes HTTP"""
    print(f"\n{C.C}═══ HTTP HEADERS ANALYSIS ═══{C.X}\n")
    url = input(f"{C.Y}Entrez l'URL (avec https://) : {C.X}").strip()
    
    if not url.startswith('http'):
        url = 'https://' + url
    
    try:
        import requests
        response = requests.head(url, allow_redirects=True, timeout=10)
        
        print(f"\n{C.G}[+] En-têtes HTTP pour {url}:{C.X}\n")
        
        security_headers = [
            'X-Frame-Options',
            'X-XSS-Protection', 
            'X-Content-Type-Options',
            'Strict-Transport-Security',
            'Content-Security-Policy',
            'X-Permitted-Cross-Domain-Policies',
            'Referrer-Policy'
        ]
        
        print(f"  {C.BOLD}En-têtes généraux:{C.X}")
        print(f"  {C.C}Server:{C.X} {response.headers.get('Server', 'Non divulgué')}")
        print(f"  {C.C}Content-Type:{C.X} {response.headers.get('Content-Type', 'N/A')}")
        print(f"  {C.C}Status Code:{C.X} {response.status_code}")
        
        print(f"\n  {C.BOLD}En-têtes de sécurité:{C.X}")
        for header in security_headers:
            value = response.headers.get(header, None)
            if value:
                print(f"  {C.G}✓ {header}:{C.X} {value}")
            else:
                print(f"  {C.R}✗ {header}:{C.X} Manquant")
                
    except Exception as e:
        print(f"{C.R}[!] Erreur: {e}{C.X}")

def google_dorking_guide():
    """Guide des Google Dorks"""
    guide = f"""
{C.C}{C.BOLD}═══ GOOGLE DORKING GUIDE ═══{C.X}

{C.Y}Les Google Dorks sont des recherches avancées pour trouver des informations publiques.{C.X}
{C.R}⚠️ N'utilisez pas ces techniques pour accéder à des données non autorisées !{C.X}

{C.BOLD}Opérateurs de base:{C.X}
  {C.C}site:example.com{C.X}        - Rechercher sur un site spécifique
  {C.C}filetype:pdf{C.X}            - Rechercher un type de fichier
  {C.C}intitle:"mot"{C.X}           - Mot dans le titre
  {C.C}inurl:"mot"{C.X}             - Mot dans l'URL
  {C.C}intext:"mot"{C.X}            - Mot dans le contenu
  {C.C}"phrase exacte"{C.X}         - Recherche exacte

{C.BOLD}Exemples légaux:{C.X}
  {C.G}site:github.com filetype:py password{C.X}
      → Trouver des scripts Python contenant "password" sur GitHub
  
  {C.G}site:pastebin.com "api key"{C.X}
      → Trouver des clés API exposées publiquement
  
  {C.G}site:linkedin.com "security engineer" "Paris"{C.X}
      → Recherche de profils (OSINT légal)

{C.BOLD}Ressources:{C.X}
  • Google Hacking Database: https://www.exploit-db.com/google-hacking-database
  • OSINT Framework: https://osintframework.com
"""
    print(guide)

def subdomain_finder():
    """Recherche de sous-domaines"""
    print(f"\n{C.C}═══ SUBDOMAIN FINDER ═══{C.X}\n")
    domain = input(f"{C.Y}Entrez le domaine principal : {C.X}").strip()
    
    common_subdomains = [
        'www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'test',
        'staging', 'api', 'app', 'mobile', 'shop', 'store',
        'cdn', 'static', 'images', 'img', 'media', 'video',
        'vpn', 'remote', 'portal', 'login', 'secure', 'ssl',
        'webmail', 'email', 'smtp', 'pop', 'imap', 'ns1', 'ns2',
        'dns', 'mx', 'gateway', 'proxy', 'firewall', 'backup'
    ]
    
    print(f"\n{C.G}[+] Recherche de sous-domaines pour {domain}...{C.X}\n")
    found = []
    
    for sub in common_subdomains:
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            print(f"  {C.G}[✓]{C.X} {subdomain} → {ip}")
            found.append((subdomain, ip))
        except socket.gaierror:
            pass
    
    print(f"\n{C.C}[*] {len(found)} sous-domaines trouvés.{C.X}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    
    while True:
        menu()
        choice = input(f"\n{C.C}Choisissez une option : {C.X}").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            dns_lookup()
        elif choice == '2':
            whois_lookup()
        elif choice == '3':
            ip_geolocation()
        elif choice == '4':
            subdomain_finder()
        elif choice == '5':
            print(f"\n{C.Y}[!] Email Harvester - À implémenter avec theHarvester{C.X}")
        elif choice == '6':
            print(f"\n{C.Y}[!] Utilisez https://namechk.com pour rechercher des usernames{C.X}")
        elif choice == '7':
            google_dorking_guide()
        elif choice == '8':
            http_headers()
        else:
            print(f"\n{C.R}[!] Option invalide{C.X}")
        
        input(f"\n{C.Y}Appuyez sur Entrée pour continuer...{C.X}")

if __name__ == "__main__":
    main()
