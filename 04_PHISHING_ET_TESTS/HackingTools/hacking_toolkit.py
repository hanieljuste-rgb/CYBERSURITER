#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗                      ║
║   ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝                      ║
║   ███████║███████║██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗                     ║
║   ██╔══██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║                     ║
║   ██║  ██║██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝                     ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝                      ║
║                                                                              ║
║                    TOOLKIT ÉDUCATIF DE CYBERSÉCURITÉ                         ║
║                                                                              ║
║   ⚠️  AVERTISSEMENT: USAGE ÉDUCATIF ET LÉGAL UNIQUEMENT ⚠️                   ║
║                                                                              ║
║   L'utilisation de ces outils contre des systèmes sans autorisation          ║
║   explicite est illégale et peut entraîner des poursuites pénales.           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess

# Chemin vers Python
PYTHON_PATH = r"C:\Users\davis\AppData\Local\Programs\Python\Python314\python.exe"

# Répertoire des outils
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗                      ║
║   ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝                      ║
║   ███████║███████║██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗                     ║
║   ██╔══██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║                     ║
║   ██║  ██║██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝                     ║
║   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝                      ║
║                                                                              ║
║                    🎓 TOOLKIT ÉDUCATIF DE CYBERSÉCURITÉ 🎓                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

def print_menu():
    print("""
┌──────────────────────────────────────────────────────────────────────────────┐
│                           📋 MENU PRINCIPAL                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   🔍 RECONNAISSANCE                                                          │
│   ─────────────────                                                          │
│   [1] Scanner de Ports          - Découvrir les services ouverts             │
│                                                                              │
│   🔓 EXPLOITATION                                                            │
│   ────────────────                                                           │
│   [2] Brute Force               - Craquer les mots de passe                  │
│   [3] SQL Injection             - Exploiter les bases de données             │
│   [4] Phishing Server           - Simuler une attaque phishing               │
│                                                                              │
│   📡 RÉSEAU                                                                  │
│   ─────────                                                                  │
│   [5] WiFi Cracker              - Comprendre le cracking WiFi                │
│                                                                              │
│   💀 POST-EXPLOITATION                                                       │
│   ────────────────────                                                       │
│   [6] Keylogger                 - Enregistrer les frappes clavier            │
│   [7] Reverse Shell             - Accès à distance                           │
│                                                                              │
│   📱 MOBILE                                                                  │
│   ─────────                                                                  │
│   [8] Phone Controller (ADB)    - Contrôler un téléphone Android             │
│                                                                              │
│   ⚙️ UTILITAIRES                                                             │
│   ──────────────                                                             │
│   [9] Vérifier mes mots de passe (Have I Been Pwned)                         │
│                                                                              │
│   [0] Quitter                                                                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
    """)

def run_tool(script_name):
    """Exécuter un outil"""
    script_path = os.path.join(TOOLS_DIR, script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ Script non trouvé: {script_path}")
        input("\n[Appuyez sur Entrée pour continuer...]")
        return
    
    try:
        subprocess.run([PYTHON_PATH, script_path], check=False)
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    input("\n[Appuyez sur Entrée pour retourner au menu...]")

def check_passwords():
    """Vérifier si un mot de passe a été compromis"""
    import hashlib
    import urllib.request
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              🔐 VÉRIFICATION MOT DE PASSE (HIBP)                 ║
╚══════════════════════════════════════════════════════════════════╝

Cette vérification utilise l'API Have I Been Pwned.
Votre mot de passe n'est JAMAIS envoyé - seul un hash partiel est utilisé.
    """)
    
    password = input("Entrez un mot de passe à vérifier: ")
    
    if not password:
        print("❌ Mot de passe vide!")
        return
    
    # Calculer le hash SHA1
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]
    
    print(f"\n🔒 Hash SHA1: {sha1}")
    print(f"   Préfixe envoyé: {prefix}")
    print(f"   Suffixe gardé local: {suffix}")
    
    try:
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Python-Security-Check'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8')
        
        for line in data.splitlines():
            hash_suffix, count = line.split(':')
            if hash_suffix == suffix:
                print(f"\n🚨 ATTENTION: Ce mot de passe a été trouvé {int(count):,} fois dans des fuites!")
                print("   Vous devriez le changer IMMÉDIATEMENT!")
                return
        
        print("\n✅ Bonne nouvelle! Ce mot de passe n'a pas été trouvé dans les fuites connues.")
        
    except Exception as e:
        print(f"\n❌ Erreur de connexion: {e}")
    
    input("\n[Appuyez sur Entrée pour continuer...]")

def run_phone_controller():
    """Lancer le contrôleur de téléphone"""
    script_path = os.path.join(TOOLS_DIR, "..", "SecurityScripts", "phone_controller.py")
    
    if not os.path.exists(script_path):
        # Essayer le chemin alternatif
        script_path = r"C:\Users\davis\OneDrive\Bureau\HACKING\SecurityScripts\phone_controller.py"
    
    if os.path.exists(script_path):
        subprocess.run([PYTHON_PATH, script_path], check=False)
    else:
        print("❌ Script phone_controller.py non trouvé!")
    
    input("\n[Appuyez sur Entrée pour continuer...]")

def run_phishing_server():
    """Lancer le serveur de phishing"""
    script_path = os.path.join(TOOLS_DIR, "..", "PhishingDemo", "phishing_server.py")
    
    if not os.path.exists(script_path):
        script_path = r"C:\Users\davis\OneDrive\Bureau\HACKING\PhishingDemo\phishing_server.py"
    
    if os.path.exists(script_path):
        print("🌐 Démarrage du serveur de phishing...")
        print("   Ouvrez http://localhost:8080 dans votre navigateur")
        print("   Panel admin: http://localhost:8080/admin")
        print("   Appuyez sur Ctrl+C pour arrêter\n")
        subprocess.run([PYTHON_PATH, script_path], check=False)
    else:
        print("❌ Script phishing_server.py non trouvé!")
    
    input("\n[Appuyez sur Entrée pour continuer...]")

def main():
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        choice = input("🎯 Votre choix: ").strip()
        
        if choice == "1":
            run_tool("port_scanner.py")
        elif choice == "2":
            run_tool("brute_force_demo.py")
        elif choice == "3":
            run_tool("sql_injection_demo.py")
        elif choice == "4":
            run_phishing_server()
        elif choice == "5":
            run_tool("wifi_cracker_demo.py")
        elif choice == "6":
            run_tool("keylogger_demo.py")
        elif choice == "7":
            run_tool("reverse_shell_demo.py")
        elif choice == "8":
            run_phone_controller()
        elif choice == "9":
            clear_screen()
            check_passwords()
        elif choice == "0":
            print("\n👋 Au revoir! Reste éthique! 🛡️\n")
            break
        else:
            print("❌ Option invalide!")
            input("\n[Appuyez sur Entrée pour continuer...]")

if __name__ == "__main__":
    main()
