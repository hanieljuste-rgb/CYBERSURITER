#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║     ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗                      ║
║     ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝                      ║
║        ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║                         ║
║        ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║                         ║
║        ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║                         ║
║        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝                         ║
║                                                                                  ║
║                    🔥 HACKING TOOLKIT CENTRAL v2.0 🔥                            ║
║                                                                                  ║
║              Centre de commande pour tous les outils de hacking                  ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

BASE_DIR = Path(r"C:\Users\davis\OneDrive\Bureau\HACKING")

# Chemins des outils
TOOLS = {
    'phone_controller': BASE_DIR / "01_CONTROLE_TELEPHONE" / "MEGA_PHONE_CONTROLLER.py",
    'wave_transfert': BASE_DIR / "01_CONTROLE_TELEPHONE" / "WAVE_AUTO_TRANSFERT.py",
    'network_scanner': BASE_DIR / "04_PHISHING_ET_TESTS" / "HackingTools" / "NETWORK_SCANNER.py",
    'password_cracker': BASE_DIR / "04_PHISHING_ET_TESTS" / "HackingTools" / "PASSWORD_CRACKER.py",
    'port_scanner': BASE_DIR / "04_PHISHING_ET_TESTS" / "HackingTools" / "port_scanner.py",
    'wifi_cracker': BASE_DIR / "04_PHISHING_ET_TESTS" / "HackingTools" / "wifi_cracker_demo.py",
    'phishing_server': BASE_DIR / "04_PHISHING_ET_TESTS" / "PhishingDemo" / "phishing_server.py",
}

# Couleurs
class C:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def clear_screen():
    """Efface l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Affiche la bannière principale"""
    clear_screen()
    print(f"""
{C.RED}╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║  {C.WHITE}██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗                          {C.RED}║
║  {C.WHITE}██║  ██║██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝                          {C.RED}║
║  {C.WHITE}███████║███████║██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗                         {C.RED}║
║  {C.WHITE}██╔══██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║                         {C.RED}║
║  {C.WHITE}██║  ██║██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝                         {C.RED}║
║  {C.WHITE}╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝                          {C.RED}║
║                                                                                  ║
║                    {C.CYAN}🔥 TOOLKIT CENTRAL v2.0 🔥{C.RED}                                   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝{C.END}
    """)

def run_tool(tool_path, title=""):
    """Lance un outil Python"""
    if not tool_path.exists():
        print(f"\n    {C.RED}✗ Outil non trouvé: {tool_path}{C.END}")
        return False
    
    print(f"\n    {C.CYAN}🚀 Lancement de {title or tool_path.name}...{C.END}")
    print(f"    {C.DIM}Chemin: {tool_path}{C.END}\n")
    
    try:
        subprocess.run([sys.executable, str(tool_path)], cwd=str(tool_path.parent))
        return True
    except KeyboardInterrupt:
        print(f"\n    {C.YELLOW}Outil fermé{C.END}")
        return True
    except Exception as e:
        print(f"\n    {C.RED}Erreur: {e}{C.END}")
        return False

def check_tools():
    """Vérifie la disponibilité des outils"""
    print(f"\n    {C.CYAN}🔍 Vérification des outils...{C.END}\n")
    
    all_ok = True
    
    for name, path in TOOLS.items():
        if path.exists():
            print(f"    {C.GREEN}✓{C.END} {name:<20} {C.DIM}{path.name}{C.END}")
        else:
            print(f"    {C.RED}✗{C.END} {name:<20} {C.RED}MANQUANT{C.END}")
            all_ok = False
    
    return all_ok

def system_info():
    """Affiche les informations système"""
    import platform
    import socket
    
    print(f"\n{C.CYAN}{'═' * 60}{C.END}")
    print(f"{C.BOLD}{C.CYAN}💻 INFORMATIONS SYSTÈME{C.END}")
    print(f"{C.CYAN}{'═' * 60}{C.END}\n")
    
    print(f"    {C.WHITE}OS:{C.END} {platform.system()} {platform.release()}")
    print(f"    {C.WHITE}Machine:{C.END} {platform.machine()}")
    print(f"    {C.WHITE}Hostname:{C.END} {socket.gethostname()}")
    
    # IP locale
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"    {C.WHITE}IP Locale:{C.END} {local_ip}")
    except:
        pass
    
    print(f"    {C.WHITE}Python:{C.END} {platform.python_version()}")
    print(f"    {C.WHITE}Date:{C.END} {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

def quick_actions_menu():
    """Menu des actions rapides"""
    print(f"""
    {C.YELLOW}┌────────────────────────────────────────────────────────────────────┐
    │                     ⚡ ACTIONS RAPIDES ⚡                          │
    ├────────────────────────────────────────────────────────────────────┤
    │  [A] Scanner mon réseau local                                      │
    │  [B] Voir mots de passe WiFi enregistrés                          │
    │  [C] Capturer écran téléphone                                      │
    │  [D] Générer mot de passe sécurisé                                │
    │  [E] Vérifier force d'un mot de passe                             │
    │  [R] Retour au menu principal                                      │
    └────────────────────────────────────────────────────────────────────┘{C.END}
    """)

def show_main_menu():
    """Affiche le menu principal"""
    print(f"""
    {C.CYAN}┌────────────────────────────────────────────────────────────────────┐
    │  {C.BOLD}📱 CONTRÔLE TÉLÉPHONE{C.END}{C.CYAN}                                            │
    ├────────────────────────────────────────────────────────────────────┤
    │  [1] 📱 MEGA Phone Controller (contrôle complet)                   │
    │  [2] 💸 Wave Auto Transfert (automatisation)                       │
    ├────────────────────────────────────────────────────────────────────┤
    │  {C.BOLD}🌐 RÉSEAU & SÉCURITÉ{C.END}{C.CYAN}                                             │
    ├────────────────────────────────────────────────────────────────────┤
    │  [3] 🔍 Network Scanner (scan réseau avancé)                       │
    │  [4] 🔓 Password Cracker (crack de hash)                           │
    │  [5] 🚪 Port Scanner (scan de ports)                               │
    │  [6] 📡 WiFi Cracker Demo (éducatif)                               │
    ├────────────────────────────────────────────────────────────────────┤
    │  {C.BOLD}🎣 PHISHING & TESTS{C.END}{C.CYAN}                                              │
    ├────────────────────────────────────────────────────────────────────┤
    │  [7] 🎣 Phishing Server (serveur de phishing)                      │
    ├────────────────────────────────────────────────────────────────────┤
    │  {C.BOLD}🔧 UTILITAIRES{C.END}{C.CYAN}                                                   │
    ├────────────────────────────────────────────────────────────────────┤
    │  [8] ⚡ Actions rapides                                            │
    │  [9] 🔍 Vérifier les outils                                        │
    │  [10] 💻 Infos système                                             │
    ├────────────────────────────────────────────────────────────────────┤
    │  [0] 🚪 Quitter                                                    │
    └────────────────────────────────────────────────────────────────────┘{C.END}
    """)

# ═══════════════════════════════════════════════════════════════════════════════
# ACTIONS RAPIDES
# ═══════════════════════════════════════════════════════════════════════════════

def quick_network_scan():
    """Scan rapide du réseau"""
    print(f"\n    {C.CYAN}🌐 Scan rapide du réseau local...{C.END}\n")
    
    try:
        import socket
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        # Obtenir IP locale
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        network = '.'.join(local_ip.split('.')[:3])
        
        def ping(ip):
            result = subprocess.run(
                f'ping -n 1 -w 500 {ip}',
                shell=True, capture_output=True, text=True
            )
            return "TTL=" in result.stdout
        
        hosts = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(ping, f"{network}.{i}"): i for i in range(1, 255)}
            
            for future in as_completed(futures):
                i = futures[future]
                if future.result():
                    hosts.append(f"{network}.{i}")
        
        print(f"    {C.GREEN}✓ {len(hosts)} hôtes trouvés:{C.END}\n")
        for host in sorted(hosts, key=lambda x: int(x.split('.')[-1])):
            marker = " (MOI)" if host == local_ip else ""
            print(f"    {C.WHITE}• {host}{C.YELLOW}{marker}{C.END}")
        
    except Exception as e:
        print(f"    {C.RED}Erreur: {e}{C.END}")

def quick_wifi_passwords():
    """Affiche les mots de passe WiFi"""
    print(f"\n    {C.CYAN}📡 Mots de passe WiFi enregistrés...{C.END}\n")
    
    try:
        import re
        
        # Lister les profils
        result = subprocess.run(
            'netsh wlan show profiles',
            shell=True, capture_output=True, text=True
        )
        
        profiles = re.findall(r':\s*(.+)', result.stdout)
        profiles = [p.strip() for p in profiles if p.strip()]
        
        for profile in profiles:
            detail = subprocess.run(
                f'netsh wlan show profile name="{profile}" key=clear',
                shell=True, capture_output=True, text=True
            )
            
            key_match = re.search(r'(Contenu de la cl|Key Content)\s*:\s*(.+)', detail.stdout)
            password = key_match.group(2).strip() if key_match else "N/A"
            
            print(f"    {C.WHITE}📶 {profile}{C.END}")
            print(f"       {C.GREEN}🔑 {password}{C.END}\n")
        
    except Exception as e:
        print(f"    {C.RED}Erreur: {e}{C.END}")

def quick_phone_screenshot():
    """Capture d'écran rapide du téléphone"""
    print(f"\n    {C.CYAN}📱 Capture d'écran du téléphone...{C.END}\n")
    
    ADB = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
    DEVICE = "100.88.242.60:5555"
    OUTPUT = BASE_DIR / "02_EXTRACTION_DONNEES" / "TECNO_CK6" / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    try:
        subprocess.run(f'"{ADB}" -s {DEVICE} shell screencap -p /sdcard/screen.png', shell=True)
        subprocess.run(f'"{ADB}" -s {DEVICE} pull /sdcard/screen.png "{OUTPUT}"', shell=True)
        subprocess.run(f'"{ADB}" -s {DEVICE} shell rm /sdcard/screen.png', shell=True)
        
        print(f"    {C.GREEN}✓ Capture sauvegardée: {OUTPUT}{C.END}")
    except Exception as e:
        print(f"    {C.RED}Erreur: {e}{C.END}")

def quick_generate_password():
    """Génère un mot de passe sécurisé"""
    import secrets
    import string
    
    length = 16
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    
    password = ''.join(secrets.choice(chars) for _ in range(length))
    
    print(f"\n    {C.GREEN}🔐 Mot de passe généré:{C.END}")
    print(f"\n    {C.BOLD}{C.CYAN}{password}{C.END}\n")

def quick_check_password():
    """Vérifie la force d'un mot de passe"""
    import string
    
    password = input(f"\n    {C.WHITE}Mot de passe à vérifier: {C.END}").strip()
    
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 2
    
    if score <= 2:
        strength = f"{C.RED}FAIBLE{C.END}"
    elif score <= 4:
        strength = f"{C.YELLOW}MOYEN{C.END}"
    elif score <= 6:
        strength = f"{C.GREEN}FORT{C.END}"
    else:
        strength = f"{C.GREEN}TRÈS FORT{C.END}"
    
    print(f"\n    Force: {strength} ({score}/7)")

# ═══════════════════════════════════════════════════════════════════════════════
# BOUCLE PRINCIPALE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Fonction principale"""
    
    while True:
        print_banner()
        show_main_menu()
        
        choice = input(f"\n    {C.GREEN}👉 Choix: {C.END}").strip().lower()
        
        try:
            if choice == "1":
                run_tool(TOOLS['phone_controller'], "MEGA Phone Controller")
            
            elif choice == "2":
                run_tool(TOOLS['wave_transfert'], "Wave Auto Transfert")
            
            elif choice == "3":
                run_tool(TOOLS['network_scanner'], "Network Scanner")
            
            elif choice == "4":
                run_tool(TOOLS['password_cracker'], "Password Cracker")
            
            elif choice == "5":
                run_tool(TOOLS['port_scanner'], "Port Scanner")
            
            elif choice == "6":
                run_tool(TOOLS['wifi_cracker'], "WiFi Cracker Demo")
            
            elif choice == "7":
                run_tool(TOOLS['phishing_server'], "Phishing Server")
            
            elif choice == "8":
                # Actions rapides
                while True:
                    clear_screen()
                    print_banner()
                    quick_actions_menu()
                    
                    action = input(f"\n    {C.GREEN}👉 Action: {C.END}").strip().upper()
                    
                    if action == "A":
                        quick_network_scan()
                    elif action == "B":
                        quick_wifi_passwords()
                    elif action == "C":
                        quick_phone_screenshot()
                    elif action == "D":
                        quick_generate_password()
                    elif action == "E":
                        quick_check_password()
                    elif action == "R":
                        break
                    else:
                        print(f"    {C.RED}Option invalide{C.END}")
                    
                    input(f"\n    {C.CYAN}⏎ Entrée pour continuer...{C.END}")
                continue  # Skip the pause at the end
            
            elif choice == "9":
                check_tools()
            
            elif choice == "10":
                system_info()
            
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
