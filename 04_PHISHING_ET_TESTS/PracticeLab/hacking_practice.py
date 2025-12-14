#!/usr/bin/env python3
"""
🎯 LABORATOIRE DE PRATIQUE CYBERSÉCURITÉ
=========================================
Un environnement interactif pour apprendre les techniques de hacking
de manière légale sur ton propre système.
"""

import subprocess
import os
import socket
import json
import sqlite3
import hashlib
from datetime import datetime
import sys

# Configuration
ADB_PATH = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
OUTPUT_DIR = r"C:\Users\davis\OneDrive\Bureau\HACKING\PracticeLab\extracted_data"

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

def banner():
    print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════╗
║  {Colors.RED}🎯 LABORATOIRE DE HACKING ÉDUCATIF 🎯{Colors.CYAN}                          ║
║══════════════════════════════════════════════════════════════════║
║  {Colors.GREEN}Pratique légale sur ton propre appareil{Colors.CYAN}                       ║
║  {Colors.YELLOW}Apprends les techniques utilisées par les pentesters{Colors.CYAN}          ║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
""")

def run_adb(command):
    """Exécute une commande ADB"""
    try:
        full_cmd = f'"{ADB_PATH}" {command}'
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Erreur: {e}"

def ensure_output_dir():
    """Crée le dossier de sortie"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============== MODULE 1: RECONNAISSANCE ==============

def module_reconnaissance():
    """Module de reconnaissance réseau"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  📡 MODULE 1: RECONNAISSANCE RÉSEAU")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("La reconnaissance est la PREMIÈRE phase de tout pentest.")
    print("On collecte des informations sur la cible AVANT d'attaquer.\n")
    
    print(f"{Colors.GREEN}[PRATIQUE]{Colors.RESET} Scannons ton réseau local...\n")
    
    # Obtenir l'IP locale
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"  {Colors.CYAN}🖥️  Hostname:{Colors.RESET} {hostname}")
    print(f"  {Colors.CYAN}🌐 IP locale:{Colors.RESET} {local_ip}")
    
    # Scanner les ports locaux
    print(f"\n  {Colors.YELLOW}Scan des ports localhost...{Colors.RESET}")
    common_ports = [21, 22, 80, 443, 3306, 3389, 5432, 8080, 8888]
    
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            services = {21:"FTP", 22:"SSH", 80:"HTTP", 443:"HTTPS", 3306:"MySQL", 3389:"RDP", 5432:"PostgreSQL", 8080:"HTTP-Alt", 8888:"HTTP-Alt"}
            print(f"    {Colors.GREEN}[OUVERT]{Colors.RESET} Port {port} ({services.get(port, 'Unknown')})")
        sock.close()
    
    # Info téléphone
    print(f"\n  {Colors.YELLOW}Reconnaissance téléphone...{Colors.RESET}")
    print(f"    📱 Modèle: {run_adb('shell getprop ro.product.model').strip()}")
    print(f"    🤖 Android: {run_adb('shell getprop ro.build.version.release').strip()}")
    print(f"    🏭 Marque: {run_adb('shell getprop ro.product.brand').strip()}")
    
    print(f"\n{Colors.GREEN}✅ Reconnaissance terminée!{Colors.RESET}")

# ============== MODULE 2: EXTRACTION DONNÉES ==============

def module_extraction():
    """Module d'extraction Android"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  📦 MODULE 2: EXTRACTION DE DONNÉES ANDROID")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("Avec ADB, on peut extraire beaucoup de données sensibles.")
    print("C'est pourquoi il faut désactiver le débogage USB en public!\n")
    
    ensure_output_dir()
    
    extractions = [
        ("SMS", "shell content query --uri content://sms --projection address,body,date --sort 'date DESC LIMIT 5'"),
        ("Contacts", "shell content query --uri content://contacts/phones --projection display_name,number"),
        ("Appels", "shell content query --uri content://call_log/calls --projection number,duration,type --sort 'date DESC LIMIT 5'"),
        ("Apps tierces", "shell pm list packages -3"),
        ("Downloads", "shell ls -la /sdcard/Download/ 2>/dev/null | head -8"),
    ]
    
    for name, cmd in extractions:
        print(f"\n  {Colors.YELLOW}📥 {name}...{Colors.RESET}")
        result = run_adb(cmd)
        
        lines = result.strip().split('\n')[:3]
        for line in lines:
            if line.strip():
                print(f"    {Colors.GREEN}→{Colors.RESET} {line[:65]}...")
        
        filepath = os.path.join(OUTPUT_DIR, f"{name}.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"    {Colors.CYAN}💾 Sauvé: {name}.txt{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}✅ Extraction terminée! Fichiers dans: {OUTPUT_DIR}{Colors.RESET}")

# ============== MODULE 3: SQL INJECTION ==============

def module_sql_injection():
    """Démonstration SQL Injection"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  🌐 MODULE 3: SQL INJECTION (DÉMONSTRATION)")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("L'injection SQL permet de manipuler les requêtes base de données.")
    print("C'est une des vulnérabilités les plus dangereuses!\n")
    
    # Base de données de test
    ensure_output_dir()
    db_path = os.path.join(OUTPUT_DIR, "demo.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)")
    cursor.executemany("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", [
        ("admin", "SuperSecret123!", "admin@company.com"),
        ("john", "password123", "john@example.com"),
        ("alice", "qwerty", "alice@example.com"),
    ])
    conn.commit()
    
    print(f"{Colors.GREEN}[PRATIQUE]{Colors.RESET} Simulation d'attaque\n")
    
    # Requête normale
    print(f"  {Colors.CYAN}1. Requête NORMALE:{Colors.RESET}")
    print(f"     Input: admin")
    print(f"     SQL: SELECT * FROM users WHERE username = 'admin'")
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    print(f"     Résultat: {cursor.fetchone()}\n")
    
    # Injection
    print(f"  {Colors.RED}2. Requête avec INJECTION:{Colors.RESET}")
    malicious = "' OR '1'='1' --"
    print(f"     Input: {malicious}")
    print(f"     SQL: SELECT * FROM users WHERE username = '' OR '1'='1' --'")
    
    # Simulation (on ne peut pas vraiment injecter avec sqlite3 paramétré)
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(f"\n     {Colors.RED}💀 TOUS LES UTILISATEURS EXPOSÉS:{Colors.RESET}")
    for row in results:
        print(f"        ID:{row[0]} | User:{row[1]} | Pass:{row[2]} | Email:{row[3]}")
    
    conn.close()
    
    print(f"\n{Colors.GREEN}[PROTECTION]{Colors.RESET}")
    print("  • Utiliser des requêtes paramétréees")
    print("  • Valider les entrées utilisateur")
    print("  • Principe du moindre privilège")

# ============== MODULE 4: PASSWORD CRACKING ==============

def module_password_cracking():
    """Cracking de mots de passe"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  🔐 MODULE 4: CRACKING DE MOTS DE PASSE")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("Les mots de passe sont stockés en hash. Les attaquants utilisent:")
    print("  • Attaque par dictionnaire")
    print("  • Brute force")
    print("  • Rainbow tables\n")
    
    # Hash à cracker
    target_hash = "5f4dcc3b5aa765d61d8327deb882cf99"  # "password" en MD5
    
    print(f"{Colors.GREEN}[PRATIQUE]{Colors.RESET} Attaque par dictionnaire\n")
    print(f"  {Colors.YELLOW}Hash MD5 cible:{Colors.RESET} {target_hash}\n")
    
    wordlist = ["admin", "123456", "password", "qwerty", "letmein", "welcome"]
    
    print(f"  {Colors.CYAN}Tentatives:{Colors.RESET}")
    for word in wordlist:
        word_hash = hashlib.md5(word.encode()).hexdigest()
        if word_hash == target_hash:
            print(f"    {word:15} → {word_hash} {Colors.GREEN}✅ TROUVÉ!{Colors.RESET}")
            print(f"\n  {Colors.GREEN}🎉 Mot de passe cracké: {word}{Colors.RESET}")
            break
        else:
            print(f"    {word:15} → {word_hash} {Colors.RED}❌{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}[PROTECTION]{Colors.RESET}")
    print("  • Mots de passe longs (12+ caractères)")
    print("  • Utiliser un gestionnaire de mots de passe")
    print("  • Activer le 2FA")

# ============== MODULE 5: SCREENSHOT & KEYLOGGER DEMO ==============

def module_spyware_demo():
    """Démonstration de techniques de surveillance"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  👁️ MODULE 5: SURVEILLANCE (DÉMONSTRATION)")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("Les attaquants peuvent surveiller leurs victimes via:")
    print("  • Captures d'écran")
    print("  • Keyloggers (enregistrement de frappes)")
    print("  • Enregistrement audio/caméra\n")
    
    print(f"{Colors.GREEN}[PRATIQUE]{Colors.RESET} Capture d'écran du téléphone\n")
    
    ensure_output_dir()
    screenshot_path = os.path.join(OUTPUT_DIR, "screenshot_demo.png")
    
    print(f"  {Colors.YELLOW}Capture en cours...{Colors.RESET}")
    run_adb("shell screencap -p /sdcard/screen.png")
    run_adb(f"pull /sdcard/screen.png \"{screenshot_path}\"")
    run_adb("shell rm /sdcard/screen.png")
    
    if os.path.exists(screenshot_path):
        print(f"  {Colors.GREEN}✅ Screenshot sauvé: {screenshot_path}{Colors.RESET}")
    else:
        print(f"  {Colors.RED}❌ Échec de la capture{Colors.RESET}")
    
    # Clipboard
    print(f"\n  {Colors.YELLOW}Lecture du presse-papier...{Colors.RESET}")
    clipboard = run_adb("shell service call clipboard 2 s16 com.android.shell")
    print(f"    {Colors.CYAN}Presse-papier:{Colors.RESET} (données brutes disponibles)")
    
    print(f"\n{Colors.GREEN}[PROTECTION]{Colors.RESET}")
    print("  • Ne pas installer d'apps de sources inconnues")
    print("  • Vérifier les permissions des applications")
    print("  • Utiliser un antivirus mobile")

# ============== MODULE 6: PERSISTENCE ==============

def module_persistence():
    """Démonstration de persistance"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  🎭 MODULE 6: PERSISTANCE & POST-EXPLOITATION")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("Après compromission, un attaquant cherche à:")
    print("  • Maintenir l'accès")
    print("  • Élever ses privilèges")
    print("  • Exfiltrer des données\n")
    
    print(f"{Colors.GREEN}[PRATIQUE]{Colors.RESET} Collecte d'informations\n")
    
    # Infos système Windows
    print(f"  {Colors.YELLOW}Système Windows:{Colors.RESET}")
    info = [
        ("Utilisateur", subprocess.run("whoami", shell=True, capture_output=True, text=True).stdout.strip()),
        ("Hostname", socket.gethostname()),
        ("Répertoire", os.getcwd()),
    ]
    for name, val in info:
        print(f"    {Colors.CYAN}{name}:{Colors.RESET} {val}")
    
    # Infos Android
    print(f"\n  {Colors.YELLOW}Téléphone Android:{Colors.RESET}")
    phone_info = [
        ("Batterie", run_adb("shell dumpsys battery | findstr level").strip()),
        ("WiFi actuel", run_adb("shell dumpsys wifi | findstr 'mWifiInfo'").strip()[:60]),
        ("Processus", run_adb("shell ps -A | wc -l").strip() + " processus"),
    ]
    for name, val in phone_info:
        if val:
            print(f"    {Colors.CYAN}{name}:{Colors.RESET} {val}")
    
    print(f"\n{Colors.GREEN}[PROTECTION]{Colors.RESET}")
    print("  • Surveiller les processus inhabituels")
    print("  • Vérifier les autorisations d'applications")
    print("  • Faire des audits de sécurité réguliers")

# ============== MENU PRINCIPAL ==============

def main_menu():
    """Menu principal"""
    os.system('color')  # Active les couleurs Windows
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        
        print(f"{Colors.YELLOW}Choisis un module:{Colors.RESET}\n")
        print(f"  {Colors.CYAN}[1]{Colors.RESET} 📡 Reconnaissance réseau")
        print(f"  {Colors.CYAN}[2]{Colors.RESET} 📦 Extraction données Android")
        print(f"  {Colors.CYAN}[3]{Colors.RESET} 🌐 SQL Injection (démo)")
        print(f"  {Colors.CYAN}[4]{Colors.RESET} 🔐 Password Cracking")
        print(f"  {Colors.CYAN}[5]{Colors.RESET} 👁️ Surveillance (screenshot)")
        print(f"  {Colors.CYAN}[6]{Colors.RESET} 🎭 Post-exploitation")
        print(f"  {Colors.CYAN}[7]{Colors.RESET} 🚀 TOUT EXÉCUTER")
        print(f"  {Colors.CYAN}[0]{Colors.RESET} ❌ Quitter\n")
        
        try:
            choice = input(f"{Colors.GREEN}Ton choix > {Colors.RESET}").strip()
        except:
            break
        
        if choice == "1":
            module_reconnaissance()
        elif choice == "2":
            module_extraction()
        elif choice == "3":
            module_sql_injection()
        elif choice == "4":
            module_password_cracking()
        elif choice == "5":
            module_spyware_demo()
        elif choice == "6":
            module_persistence()
        elif choice == "7":
            for mod in [module_reconnaissance, module_extraction, module_sql_injection, 
                       module_password_cracking, module_spyware_demo, module_persistence]:
                mod()
                input(f"\n{Colors.YELLOW}[Entrée pour continuer...]{Colors.RESET}")
        elif choice == "0":
            print(f"\n{Colors.GREEN}Merci d'avoir pratiqué! 🎓{Colors.RESET}\n")
            break
        
        if choice != "0":
            input(f"\n{Colors.YELLOW}[Entrée pour revenir au menu...]{Colors.RESET}")

if __name__ == "__main__":
    main_menu()
