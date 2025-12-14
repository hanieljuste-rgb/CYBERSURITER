#!/usr/bin/env python3
"""
🎯 LABORATOIRE DE PRATIQUE CYBERSÉCURITÉ
=========================================
Un environnement interactif pour apprendre les techniques de hacking
de manière légale sur ton propre système.

Auteur: Laboratoire Éducatif
"""

import subprocess
import os
import socket
import json
import sqlite3
import hashlib
import base64
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
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
    """Crée le dossier de sortie si nécessaire"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============== MODULE 1: RECONNAISSANCE ==============

def module_reconnaissance():
    """Module de reconnaissance réseau"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  📡 MODULE 1: RECONNAISSANCE RÉSEAU")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("La reconnaissance est la PREMIÈRE phase de tout test de pénétration.")
    print("On collecte des informations sur la cible AVANT d'attaquer.\n")
    
    print(f"{Colors.GREEN}[PRATIQUE]{Colors.RESET} Scannons ton réseau local...\n")
    
    # Obtenir l'IP locale
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"  {Colors.CYAN}🖥️  Ton hostname:{Colors.RESET} {hostname}")
    print(f"  {Colors.CYAN}🌐 Ton IP locale:{Colors.RESET} {local_ip}")
    
    # Scanner les ports locaux ouverts
    print(f"\n  {Colors.YELLOW}Scanning des ports ouverts sur localhost...{Colors.RESET}")
    common_ports = [21, 22, 23, 25, 53, 80, 443, 445, 3306, 3389, 5432, 8080, 8888]
    open_ports = []
    
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            open_ports.append(port)
            service = {
                21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
                53: "DNS", 80: "HTTP", 443: "HTTPS", 445: "SMB",
                3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
                8080: "HTTP-Alt", 8888: "HTTP-Alt"
            }.get(port, "Unknown")
            print(f"    {Colors.GREEN}[OUVERT]{Colors.RESET} Port {port} ({service})")
        sock.close()
    
    if not open_ports:
        print(f"    {Colors.YELLOW}Aucun port commun ouvert détecté{Colors.RESET}")
    
    # Info téléphone via ADB
    print(f"\n  {Colors.YELLOW}Reconnaissance du téléphone connecté...{Colors.RESET}")
    
    device_info = run_adb("shell getprop ro.product.model")
    android_ver = run_adb("shell getprop ro.build.version.release")
    imei = run_adb("shell service call iphonesubinfo 1")
    
    print(f"    📱 Modèle: {device_info.strip()}")
    print(f"    🤖 Android: {android_ver.strip()}")
    
    print(f"\n{Colors.GREEN}✅ Reconnaissance terminée!{Colors.RESET}")
    print(f"\n{Colors.CYAN}[LEÇON APPRISE]{Colors.RESET}")
    print("Un attaquant utiliserait ces infos pour:")
    print("  • Identifier les services vulnérables")
    print("  • Trouver des exploits spécifiques à la version Android")
    print("  • Planifier les prochaines étapes de l'attaque")

# ============== MODULE 2: EXTRACTION DE DONNÉES ==============

def module_extraction():
    """Module d'extraction de données Android"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  📦 MODULE 2: EXTRACTION DE DONNÉES ANDROID")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("Avec un accès ADB, on peut extraire beaucoup de données d'un téléphone.")
    print("C'est pourquoi il ne faut JAMAIS activer le débogage USB en public!\n")
    
    ensure_output_dir()
    
    extractions = [
        ("SMS (messages)", "shell content query --uri content://sms --projection address,body,date --sort 'date DESC' --limit 5"),
        ("Contacts", "shell content query --uri content://contacts/phones --projection display_name,number --limit 5"),
        ("Historique d'appels", "shell content query --uri content://call_log/calls --projection number,duration,type --limit 5"),
        ("Applications installées", "shell pm list packages -3"),
        ("Fichiers récents", "shell ls -la /sdcard/Download/ | head -10"),
    ]
    
    for name, cmd in extractions:
        print(f"\n  {Colors.YELLOW}📥 Extraction: {name}...{Colors.RESET}")
        result = run_adb(cmd)
        
        # Afficher un extrait
        lines = result.strip().split('\n')[:3]
        for line in lines:
            if line.strip():
                print(f"    {Colors.GREEN}→{Colors.RESET} {line[:70]}...")
        
        # Sauvegarder
        safe_name = name.replace(" ", "_").replace("(", "").replace(")", "")
        filepath = os.path.join(OUTPUT_DIR, f"{safe_name}.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"    {Colors.CYAN}💾 Sauvegardé: {filepath}{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}✅ Extraction terminée!{Colors.RESET}")
    print(f"\n{Colors.CYAN}[LEÇON APPRISE]{Colors.RESET}")
    print("Avec ADB activé, un attaquant peut:")
    print("  • Voler tous tes SMS (codes 2FA inclus!)")
    print("  • Copier tes contacts")
    print("  • Voir ton historique d'appels")
    print("  • Installer des applications malveillantes")

# ============== MODULE 3: VULNÉRABILITÉS WEB ==============

def module_web_vulnerabilities():
    """Module sur les vulnérabilités web"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  🌐 MODULE 3: VULNÉRABILITÉS WEB (DÉMONSTRATION)")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("Les applications web ont souvent des vulnérabilités:")
    print("  • SQL Injection - Manipuler les requêtes base de données")
    print("  • XSS - Injecter du JavaScript malveillant")
    print("  • CSRF - Forcer des actions non autorisées\n")
    
    # Créer une base de données de démonstration
    db_path = os.path.join(OUTPUT_DIR, "demo_vulnerable.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
    
    # Données de test
    test_users = [
        ("admin", "admin123", "admin@example.com"),
        ("user1", "password", "user1@example.com"),
        ("john", "secret", "john@example.com"),
    ]
    
    cursor.execute("DELETE FROM users")
    cursor.executemany("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", test_users)
    conn.commit()
    
    print(f"{Colors.GREEN}[PRATIQUE]{Colors.RESET} Démonstration SQL Injection\n")
    
    # Requête vulnérable
    print(f"  {Colors.YELLOW}Requête VULNÉRABLE:{Colors.RESET}")
    print(f"  SELECT * FROM users WHERE username = '$input'")
    
    # Exploitation
    malicious_input = "' OR '1'='1"
    print(f"\n  {Colors.RED}Entrée malveillante:{Colors.RESET} {malicious_input}")
    print(f"  {Colors.RED}Requête résultante:{Colors.RESET}")
    print(f"  SELECT * FROM users WHERE username = '' OR '1'='1'")
    
    # Exécution (simulation)
    cursor.execute("SELECT * FROM users WHERE username = '' OR '1'='1'")
    results = cursor.fetchall()
    
    print(f"\n  {Colors.GREEN}Résultat de l'injection:{Colors.RESET}")
    for row in results:
        print(f"    → ID:{row[0]} | User:{row[1]} | Pass:{row[2]} | Email:{row[3]}")
    
    conn.close()
    
    print(f"\n  {Colors.CYAN}💡 L'attaquant a récupéré TOUS les utilisateurs!{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}✅ Démonstration terminée!{Colors.RESET}")
    print(f"\n{Colors.CYAN}[PROTECTION]{Colors.RESET}")
    print("Pour se protéger:")
    print("  • Utiliser des requêtes préparées (paramètres)")
    print("  • Valider et échapper les entrées utilisateur")
    print("  • Utiliser un ORM (Object-Relational Mapping)")

# ============== MODULE 4: CRACKING DE MOTS DE PASSE ==============

def module_password_cracking():
    """Module sur le cracking de mots de passe"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  🔐 MODULE 4: CRACKING DE MOTS DE PASSE")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("Les mots de passe sont souvent stockés sous forme de hash.")
    print("Les attaquants utilisent plusieurs techniques:\n")
    print("  • Dictionnaire - Tester des mots de passe courants")
    print("  • Brute Force - Tester toutes les combinaisons")
    print("  • Rainbow Tables - Tables pré-calculées\n")
    
    # Créer un hash à cracker
    passwords_to_crack = {
        "5f4dcc3b5aa765d61d8327deb882cf99": "password",
        "e10adc3949ba59abbe56e057f20f883e": "123456",
        "d8578edf8458ce06fbc5bb76a58c5ca4": "qwerty",
        "827ccb0eea8a706c4c34a16891f84e7b": "12345",
    }
    
    # Mini wordlist
    wordlist = ["admin", "password", "123456", "qwerty", "12345", "letmein", "welcome", "monkey"]
    
    print(f"{Colors.GREEN}[PRATIQUE]{Colors.RESET} Cracking par dictionnaire\n")
    
    target_hash = "5f4dcc3b5aa765d61d8327deb882cf99"
    print(f"  {Colors.YELLOW}Hash MD5 à cracker:{Colors.RESET} {target_hash}\n")
    
    print(f"  {Colors.CYAN}Tentatives:{Colors.RESET}")
    found = False
    for word in wordlist:
        word_hash = hashlib.md5(word.encode()).hexdigest()
        status = "✅ TROUVÉ!" if word_hash == target_hash else "❌"
        color = Colors.GREEN if word_hash == target_hash else Colors.RED
        print(f"    {word:15} → {word_hash} {color}{status}{Colors.RESET}")
        
        if word_hash == target_hash:
            found = True
            print(f"\n  {Colors.GREEN}🎉 Mot de passe trouvé: {word}{Colors.RESET}")
            break
    
    print(f"\n{Colors.GREEN}✅ Démonstration terminée!{Colors.RESET}")
    print(f"\n{Colors.CYAN}[LEÇON APPRISE]{Colors.RESET}")
    print("Pour des mots de passe sécurisés:")
    print("  • Minimum 12 caractères")
    print("  • Mélanger majuscules, minuscules, chiffres, symboles")
    print("  • Utiliser un gestionnaire de mots de passe")
    print("  • Activer l'authentification à 2 facteurs (2FA)")

# ============== MODULE 5: CAPTURE RÉSEAU ==============

def module_network_capture():
    """Module sur la capture réseau"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  📡 MODULE 5: ANALYSE RÉSEAU")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("Sur un réseau non sécurisé, un attaquant peut:")
    print("  • Capturer le trafic (Man-in-the-Middle)")
    print("  • Voir les données non chiffrées")
    print("  • Voler des sessions et cookies\n")
    
    print(f"{Colors.GREEN}[PRATIQUE]{Colors.RESET} Analyse des connexions actives\n")
    
    # Netstat
    result = subprocess.run("netstat -an | findstr ESTABLISHED", shell=True, capture_output=True, text=True)
    connections = result.stdout.strip().split('\n')[:10]
    
    print(f"  {Colors.YELLOW}Connexions établies:{Colors.RESET}")
    for conn in connections:
        if conn.strip():
            print(f"    {Colors.GREEN}→{Colors.RESET} {conn.strip()}")
    
    # WiFi du téléphone
    print(f"\n  {Colors.YELLOW}WiFi sauvegardés sur le téléphone:{Colors.RESET}")
    wifi_result = run_adb("shell cat /data/misc/wifi/WifiConfigStore.xml 2>/dev/null || echo 'Accès refusé (root requis)'")
    
    if "refusé" in wifi_result or "denied" in wifi_result.lower():
        print(f"    {Colors.RED}⚠️ Accès root requis pour voir les mots de passe WiFi{Colors.RESET}")
    else:
        print(f"    {Colors.GREEN}Fichier de configuration WiFi accessible{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}✅ Analyse terminée!{Colors.RESET}")
    print(f"\n{Colors.CYAN}[PROTECTION]{Colors.RESET}")
    print("Pour te protéger:")
    print("  • Toujours utiliser HTTPS")
    print("  • Éviter les WiFi publics non sécurisés")
    print("  • Utiliser un VPN")

# ============== MODULE 6: POST-EXPLOITATION ==============

def module_post_exploitation():
    """Module de post-exploitation"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"  🎭 MODULE 6: POST-EXPLOITATION")
    print(f"{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("Après avoir compromis un système, un attaquant cherche à:")
    print("  • Maintenir l'accès (persistance)")
    print("  • Escalader les privilèges")
    print("  • Se déplacer latéralement dans le réseau")
    print("  • Exfiltrer des données\n")
    
    print(f"{Colors.GREEN}[PRATIQUE]{Colors.RESET} Collecte d'informations système\n")
    
    # Infos Windows
    print(f"  {Colors.YELLOW}Informations système Windows:{Colors.RESET}")
    
    info_commands = [
        ("Utilisateur actuel", "whoami"),
        ("Hostname", "hostname"),
        ("Architecture", "wmic os get osarchitecture"),
    ]
    
    for name, cmd in info_commands:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        value = result.stdout.strip().split('\n')[-1].strip()
        print(f"    {Colors.CYAN}{name}:{Colors.RESET} {value}")
    
    # Infos téléphone avancées
    print(f"\n  {Colors.YELLOW}Informations téléphone:{Colors.RESET}")
    
    phone_commands = [
        ("Batterie", "shell dumpsys battery | findstr level"),
        ("Stockage", "shell df -h /sdcard | tail -1"),
        ("Processus actifs", "shell ps | wc -l"),
    ]
    
    for name, cmd in phone_commands:
        result = run_adb(cmd)
        print(f"    {Colors.CYAN}{name}:{Colors.RESET} {result.strip()[:50]}")
    
    print(f"\n{Colors.GREEN}✅ Post-exploitation terminée!{Colors.RESET}")
    print(f"\n{Colors.CYAN}[LEÇON APPRISE]{Colors.RESET}")
    print("Ces informations permettraient à un attaquant de:")
    print("  • Adapter son malware à l'environnement")
    print("  • Trouver des vecteurs de persistance")
    print("  • Identifier d'autres cibles sur le réseau")

# ============== MENU PRINCIPAL ==============

def main_menu():
    """Menu principal"""
    while True:
        banner()
        print(f"{Colors.YELLOW}Choisis un module à pratiquer:{Colors.RESET}\n")
        print(f"  {Colors.CYAN}[1]{Colors.RESET} 📡 Reconnaissance réseau")
        print(f"  {Colors.CYAN}[2]{Colors.RESET} 📦 Extraction de données Android")
        print(f"  {Colors.CYAN}[3]{Colors.RESET} 🌐 Vulnérabilités Web (SQL Injection)")
        print(f"  {Colors.CYAN}[4]{Colors.RESET} 🔐 Cracking de mots de passe")
        print(f"  {Colors.CYAN}[5]{Colors.RESET} 📡 Analyse réseau")
        print(f"  {Colors.CYAN}[6]{Colors.RESET} 🎭 Post-exploitation")
        print(f"  {Colors.CYAN}[7]{Colors.RESET} 🚀 EXÉCUTER TOUS LES MODULES")
        print(f"  {Colors.CYAN}[0]{Colors.RESET} ❌ Quitter\n")
        
        try:
            choice = input(f"{Colors.GREEN}Ton choix > {Colors.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nAu revoir!")
            break
        
        if choice == "1":
            module_reconnaissance()
        elif choice == "2":
            module_extraction()
        elif choice == "3":
            module_web_vulnerabilities()
        elif choice == "4":
            module_password_cracking()
        elif choice == "5":
            module_network_capture()
        elif choice == "6":
            module_post_exploitation()
        elif choice == "7":
            print(f"\n{Colors.MAGENTA}🚀 Exécution de tous les modules...{Colors.RESET}")
            module_reconnaissance()
            input(f"\n{Colors.YELLOW}Appuie sur Entrée pour continuer...{Colors.RESET}")
            module_extraction()
            input(f"\n{Colors.YELLOW}Appuie sur Entrée pour continuer...{Colors.RESET}")
            module_web_vulnerabilities()
            input(f"\n{Colors.YELLOW}Appuie sur Entrée pour continuer...{Colors.RESET}")
            module_password_cracking()
            input(f"\n{Colors.YELLOW}Appuie sur Entrée pour continuer...{Colors.RESET}")
            module_network_capture()
            input(f"\n{Colors.YELLOW}Appuie sur Entrée pour continuer...{Colors.RESET}")
            module_post_exploitation()
        elif choice == "0":
            print(f"\n{Colors.GREEN}Merci d'avoir pratiqué! Continue à apprendre! 🎓{Colors.RESET}\n")
            break
        else:
            print(f"{Colors.RED}Option invalide!{Colors.RESET}")
        
        input(f"\n{Colors.YELLOW}Appuie sur Entrée pour revenir au menu...{Colors.RESET}")

if __name__ == "__main__":
    # Activer les couleurs sur Windows
    os.system('color')
    main_menu()
