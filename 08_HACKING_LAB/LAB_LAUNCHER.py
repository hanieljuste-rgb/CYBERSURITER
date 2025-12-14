#!/usr/bin/env python3
"""
🔐 HACKING LAB LAUNCHER
Environnement d'apprentissage légal de la cybersécurité

⚠️ USAGE LÉGAL UNIQUEMENT - Éducation et recherche personnelle
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from datetime import datetime

# Couleurs pour le terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██╗  ██╗ █████╗  ██████╗██╗  ██╗    ██╗      █████╗ ██████╗ ║
    ║   ██║  ██║██╔══██╗██╔════╝██║ ██╔╝    ██║     ██╔══██╗██╔══██╗║
    ║   ███████║███████║██║     █████╔╝     ██║     ███████║██████╔╝║
    ║   ██╔══██║██╔══██║██║     ██╔═██╗     ██║     ██╔══██║██╔══██╗║
    ║   ██║  ██║██║  ██║╚██████╗██║  ██╗    ███████╗██║  ██║██████╔╝║
    ║   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚═════╝ ║
    ║                                                               ║
    ║          🔐 Environnement d'Apprentissage Légal 🔐           ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}
    {Colors.YELLOW}⚠️  AVERTISSEMENT : Usage éducatif uniquement !{Colors.RESET}
    {Colors.GREEN}✓ Testez uniquement sur VOS systèmes ou avec autorisation{Colors.RESET}
    """
    print(banner)

def print_menu():
    menu = f"""
{Colors.BOLD}╔═══════════════════════════════════════════════════════════════╗
║                    MODULES D'APPRENTISSAGE                     ║
╠═══════════════════════════════════════════════════════════════╣{Colors.RESET}
║                                                               ║
║  {Colors.CYAN}[1]{Colors.RESET}  🔍 Reconnaissance & OSINT                            ║
║  {Colors.CYAN}[2]{Colors.RESET}  📡 Scanning de Ports & Réseaux                       ║
║  {Colors.CYAN}[3]{Colors.RESET}  💉 Exploitation & Vulnérabilités                     ║
║  {Colors.CYAN}[4]{Colors.RESET}  🚪 Post-Exploitation & Persistence                   ║
║  {Colors.CYAN}[5]{Colors.RESET}  🌐 Hacking Web (SQL, XSS, CSRF...)                   ║
║  {Colors.CYAN}[6]{Colors.RESET}  📶 Sécurité WiFi (votre réseau)                      ║
║  {Colors.CYAN}[7]{Colors.RESET}  🔐 Cryptographie & Password Cracking                 ║
║  {Colors.CYAN}[8]{Colors.RESET}  🔬 Analyse Forensique                                ║
║  {Colors.CYAN}[9]{Colors.RESET}  🦠 Analyse de Malwares (Sandbox)                     ║
║  {Colors.CYAN}[10]{Colors.RESET} 🏁 CTF Practice (Exercices)                          ║
║                                                               ║
║  {Colors.YELLOW}[11]{Colors.RESET} 🛠️  Installer les Outils                            ║
║  {Colors.YELLOW}[12]{Colors.RESET} 🖥️  Lancer Machine Virtuelle Vulnérable              ║
║  {Colors.YELLOW}[13]{Colors.RESET} 📚 Ressources & Tutoriels                           ║
║                                                               ║
║  {Colors.RED}[0]{Colors.RESET}  ❌ Quitter                                           ║
║                                                               ║
{Colors.BOLD}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(menu)

def show_legal_notice():
    notice = f"""
{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                    ⚖️ NOTICE LÉGALE ⚖️                        ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  En utilisant ce lab, vous acceptez de :                      ║
║                                                               ║
║  ✓ N'utiliser ces outils qu'à des fins éducatives            ║
║  ✓ Ne tester QUE sur vos propres systèmes                    ║
║  ✓ Obtenir une autorisation ÉCRITE avant tout test           ║
║  ✓ Ne jamais causer de dommage à des tiers                   ║
║  ✓ Respecter les lois de votre pays                          ║
║                                                               ║
║  Le non-respect de ces règles peut entraîner :               ║
║  • Des poursuites pénales                                    ║
║  • Des amendes importantes                                   ║
║  • Des peines d'emprisonnement                               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(notice)
    input(f"{Colors.YELLOW}Appuyez sur Entrée pour accepter et continuer...{Colors.RESET}")

def run_module(module_num):
    """Lance le module sélectionné"""
    base_path = Path(__file__).parent
    
    modules = {
        1: ("01_RECON", "recon_tools.py"),
        2: ("02_SCANNING", "scanner.py"),
        3: ("03_EXPLOITATION", "exploit_lab.py"),
        4: ("04_POST_EXPLOITATION", "post_exploit.py"),
        5: ("05_WEB_HACKING", "web_hacking_lab.py"),
        6: ("06_WIRELESS", "wireless_lab.py"),
        7: ("07_CRYPTO", "crypto_lab.py"),
        8: ("08_FORENSICS", "forensics_lab.py"),
        9: ("09_MALWARE_ANALYSIS", "malware_sandbox.py"),
        10: ("10_CTF_PRACTICE", "ctf_challenges.py"),
    }
    
    if module_num in modules:
        folder, script = modules[module_num]
        script_path = base_path / folder / script
        
        if script_path.exists():
            print(f"\n{Colors.GREEN}[+] Lancement du module {folder}...{Colors.RESET}\n")
            subprocess.run([sys.executable, str(script_path)])
        else:
            print(f"\n{Colors.YELLOW}[!] Module en cours de développement : {script_path}{Colors.RESET}")
            print(f"{Colors.CYAN}[i] Consultez le README du dossier {folder} pour plus d'infos.{Colors.RESET}\n")
            input("Appuyez sur Entrée pour continuer...")

def install_tools():
    """Installe les outils de hacking légaux"""
    print(f"\n{Colors.CYAN}[*] Installation des outils de cybersécurité...{Colors.RESET}\n")
    
    tools = [
        "requests",      # HTTP requests
        "beautifulsoup4", # Web scraping
        "scapy",         # Packet manipulation
        "pycryptodome",  # Cryptography
        "paramiko",      # SSH
        "python-nmap",   # Nmap wrapper
        "dnspython",     # DNS queries
        "whois",         # WHOIS lookups
        "shodan",        # Shodan API
        "colorama",      # Colors
    ]
    
    for tool in tools:
        print(f"{Colors.YELLOW}[*] Installation de {tool}...{Colors.RESET}")
        subprocess.run([sys.executable, "-m", "pip", "install", tool, "-q"])
    
    print(f"\n{Colors.GREEN}[✓] Installation terminée !{Colors.RESET}\n")
    input("Appuyez sur Entrée pour continuer...")

def show_resources():
    """Affiche les ressources d'apprentissage"""
    resources = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                   📚 RESSOURCES D'APPRENTISSAGE                ║
╠═══════════════════════════════════════════════════════════════╣{Colors.RESET}
║                                                               ║
║  {Colors.GREEN}PLATEFORMES DE PRACTICE (LÉGALES) :{Colors.RESET}                       ║
║  • TryHackMe.com      - Parcours guidés pour débutants        ║
║  • HackTheBox.com     - CTF et machines réalistes             ║
║  • OverTheWire.org    - Wargames en ligne                     ║
║  • PicoCTF.org        - CTF éducatif                          ║
║  • VulnHub.com        - VMs vulnérables à télécharger         ║
║  • PortSwigger Academy - Sécurité web                         ║
║                                                               ║
║  {Colors.YELLOW}CERTIFICATIONS :{Colors.RESET}                                         ║
║  • CompTIA Security+  - Niveau débutant                       ║
║  • CEH                - Certified Ethical Hacker              ║
║  • OSCP               - Offensive Security (avancé)           ║
║  • eJPT               - eLearnSecurity Junior                 ║
║                                                               ║
║  {Colors.MAGENTA}MACHINES VIRTUELLES VULNÉRABLES :{Colors.RESET}                       ║
║  • Metasploitable 2/3 - Practice Metasploit                   ║
║  • DVWA               - Damn Vulnerable Web App               ║
║  • OWASP WebGoat      - Sécurité web                          ║
║  • Kioptrix           - Série de VMs                          ║
║  • Mr. Robot          - Thème série TV                        ║
║                                                               ║
{Colors.BOLD}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(resources)
    input(f"\n{Colors.CYAN}Appuyez sur Entrée pour continuer...{Colors.RESET}")

def launch_vulnerable_vm():
    """Guide pour lancer une VM vulnérable"""
    guide = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║              🖥️ LANCER UNE VM VULNÉRABLE                       ║
╠═══════════════════════════════════════════════════════════════╣{Colors.RESET}
║                                                               ║
║  {Colors.GREEN}Option 1 : Docker (Recommandé){Colors.RESET}                            ║
║  ─────────────────────────────────────────────────────────────║
║  # DVWA (Damn Vulnerable Web App)                             ║
║  docker run -d -p 80:80 vulnerables/web-dvwa                  ║
║                                                               ║
║  # OWASP Juice Shop                                           ║
║  docker run -d -p 3000:3000 bkimminich/juice-shop             ║
║                                                               ║
║  {Colors.YELLOW}Option 2 : VirtualBox/VMware{Colors.RESET}                              ║
║  ─────────────────────────────────────────────────────────────║
║  1. Télécharger depuis VulnHub.com                            ║
║  2. Importer l'OVA dans VirtualBox                            ║
║  3. Configurer le réseau en "Host-Only"                       ║
║  4. Démarrer et scanner avec nmap                             ║
║                                                               ║
║  {Colors.MAGENTA}Option 3 : WSL2 + Docker{Colors.RESET}                                 ║
║  ─────────────────────────────────────────────────────────────║
║  1. Activer WSL2 sur Windows                                  ║
║  2. Installer Docker Desktop                                  ║
║  3. Lancer les conteneurs vulnérables                         ║
║                                                               ║
{Colors.BOLD}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(guide)
    
    choice = input(f"\n{Colors.CYAN}Voulez-vous que je vérifie si Docker est installé ? (o/n) : {Colors.RESET}")
    if choice.lower() == 'o':
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"\n{Colors.GREEN}[✓] Docker est installé : {result.stdout}{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}[!] Docker n'est pas installé.{Colors.RESET}")
            print(f"{Colors.CYAN}[i] Téléchargez-le sur : https://www.docker.com/products/docker-desktop{Colors.RESET}")
    
    input(f"\n{Colors.CYAN}Appuyez sur Entrée pour continuer...{Colors.RESET}")

def main():
    clear_screen()
    print_banner()
    show_legal_notice()
    
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        try:
            choice = input(f"\n{Colors.CYAN}Choisissez un module [0-13] : {Colors.RESET}")
            
            if choice == '0':
                print(f"\n{Colors.GREEN}[+] Merci d'avoir utilisé le Hacking Lab !{Colors.RESET}")
                print(f"{Colors.YELLOW}[!] N'oubliez pas : Hackez de manière éthique et légale !{Colors.RESET}\n")
                break
            elif choice == '11':
                install_tools()
            elif choice == '12':
                launch_vulnerable_vm()
            elif choice == '13':
                show_resources()
            elif choice.isdigit() and 1 <= int(choice) <= 10:
                run_module(int(choice))
            else:
                print(f"\n{Colors.RED}[!] Option invalide. Choisissez entre 0 et 13.{Colors.RESET}")
                input("Appuyez sur Entrée pour continuer...")
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}[!] Interruption détectée. Au revoir !{Colors.RESET}\n")
            break

if __name__ == "__main__":
    main()
