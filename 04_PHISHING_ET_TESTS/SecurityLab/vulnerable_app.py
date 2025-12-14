#!/usr/bin/env python3
"""
🔬 SECURITY LAB - Application Web Vulnérable Éducative
======================================================
⚠️  USAGE ÉDUCATIF UNIQUEMENT - Ne jamais déployer sur un vrai serveur !

Cette application contient des vulnérabilités INTENTIONNELLES pour apprendre :
- SQL Injection
- XSS (Cross-Site Scripting)  
- Command Injection
- Broken Authentication

Lancez avec : python vulnerable_app.py
Accédez à : http://localhost:8888
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import html
import sqlite3
import os
import subprocess

# Base de données en mémoire (vulnérable intentionnellement)
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        )
    ''')
    # Utilisateurs de test
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'admin123', 'admin')")
    cursor.execute("INSERT INTO users VALUES (2, 'user', 'password', 'user')")
    cursor.execute("INSERT INTO users VALUES (3, 'guest', 'guest', 'guest')")
    conn.commit()
    return conn

DB = init_db()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🔬 Security Lab - {title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: #eee; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #e94560; }}
        h2 {{ color: #0f3460; background: #e94560; padding: 10px; border-radius: 5px; }}
        .vuln-box {{ background: #16213e; padding: 20px; margin: 20px 0; border-radius: 10px; border-left: 4px solid #e94560; }}
        input, button {{ padding: 10px; margin: 5px; font-size: 16px; }}
        input {{ background: #0f3460; border: 1px solid #e94560; color: #fff; width: 300px; }}
        button {{ background: #e94560; color: white; border: none; cursor: pointer; }}
        button:hover {{ background: #ff6b6b; }}
        .result {{ background: #0f3460; padding: 15px; margin-top: 10px; border-radius: 5px; }}
        .warning {{ background: #ff6b6b; color: #000; padding: 10px; border-radius: 5px; }}
        a {{ color: #e94560; }}
        pre {{ background: #0a0a15; padding: 10px; overflow-x: auto; }}
        .nav {{ background: #0f3460; padding: 10px; margin-bottom: 20px; border-radius: 5px; }}
        .nav a {{ margin-right: 15px; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔬 Security Lab Éducatif</h1>
        <div class="nav">
            <a href="/">🏠 Accueil</a>
            <a href="/sql">💉 SQL Injection</a>
            <a href="/xss">🎭 XSS</a>
            <a href="/cmd">⚡ Command Injection</a>
            <a href="/auth">🔐 Auth Bypass</a>
        </div>
        {content}
    </div>
</body>
</html>
'''

class VulnerableHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)
        
        if path == '/':
            self.send_page('Accueil', self.home_page())
        elif path == '/sql':
            self.send_page('SQL Injection', self.sql_page(params))
        elif path == '/xss':
            self.send_page('XSS', self.xss_page(params))
        elif path == '/cmd':
            self.send_page('Command Injection', self.cmd_page(params))
        elif path == '/auth':
            self.send_page('Authentication', self.auth_page(params))
        else:
            self.send_error(404)
    
    def send_page(self, title, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        page = HTML_TEMPLATE.format(title=title, content=content)
        self.wfile.write(page.encode('utf-8'))
    
    def home_page(self):
        return '''
        <div class="warning">
            ⚠️ Cette application est INTENTIONNELLEMENT vulnérable !<br>
            Usage éducatif uniquement. Ne jamais exposer sur Internet.
        </div>
        
        <div class="vuln-box">
            <h2>🎯 Exercices disponibles</h2>
            <ul>
                <li><strong><a href="/sql">SQL Injection</a></strong> - Apprenez à exploiter et prévenir les injections SQL</li>
                <li><strong><a href="/xss">XSS (Cross-Site Scripting)</a></strong> - Comprenez les attaques XSS</li>
                <li><strong><a href="/cmd">Command Injection</a></strong> - Exécution de commandes système</li>
                <li><strong><a href="/auth">Auth Bypass</a></strong> - Contournement d'authentification</li>
            </ul>
        </div>
        
        <div class="vuln-box">
            <h2>📚 Comment utiliser ce lab</h2>
            <ol>
                <li>Choisissez un exercice ci-dessus</li>
                <li>Lisez l'explication de la vulnérabilité</li>
                <li>Essayez d'exploiter la faille</li>
                <li>Étudiez la solution et la correction</li>
            </ol>
        </div>
        '''
    
    def sql_page(self, params):
        result = ""
        user_input = params.get('username', [''])[0]
        
        if user_input:
            # ⚠️ VULNÉRABLE : Concaténation directe (NE JAMAIS FAIRE EN PROD)
            query = f"SELECT * FROM users WHERE username = '{user_input}'"
            try:
                cursor = DB.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                result = f'''
                <div class="result">
                    <strong>Requête exécutée :</strong><br>
                    <pre>{html.escape(query)}</pre>
                    <strong>Résultats :</strong><br>
                    <pre>{rows if rows else "Aucun résultat"}</pre>
                </div>
                '''
            except Exception as e:
                result = f'<div class="result">Erreur SQL : {html.escape(str(e))}</div>'
        
        return f'''
        <div class="vuln-box">
            <h2>💉 SQL Injection</h2>
            <p><strong>Vulnérabilité :</strong> La requête SQL utilise la concaténation de chaînes.</p>
            
            <form method="GET">
                <label>Rechercher un utilisateur :</label><br>
                <input type="text" name="username" placeholder="Entrez un nom d'utilisateur" value="{html.escape(user_input)}">
                <button type="submit">Rechercher</button>
            </form>
            {result}
        </div>
        
        <div class="vuln-box">
            <h2>🎯 Exercices à essayer</h2>
            <ol>
                <li><code>admin</code> - Recherche normale</li>
                <li><code>' OR '1'='1</code> - Affiche tous les utilisateurs</li>
                <li><code>' OR '1'='1' --</code> - Bypass avec commentaire</li>
                <li><code>' UNION SELECT 1,2,3,4 --</code> - Injection UNION</li>
            </ol>
        </div>
        
        <div class="vuln-box">
            <h2>🛡️ Comment corriger</h2>
            <pre>
# ❌ VULNÉRABLE
query = f"SELECT * FROM users WHERE username = '{{user_input}}'"

# ✅ SÉCURISÉ - Requêtes paramétrées
cursor.execute("SELECT * FROM users WHERE username = ?", (user_input,))
            </pre>
        </div>
        '''
    
    def xss_page(self, params):
        user_input = params.get('message', [''])[0]
        
        # ⚠️ VULNÉRABLE : Pas d'échappement HTML
        unsafe_output = user_input
        # ✅ SÉCURISÉ : Avec échappement
        safe_output = html.escape(user_input)
        
        return f'''
        <div class="vuln-box">
            <h2>🎭 XSS (Cross-Site Scripting)</h2>
            <p><strong>Vulnérabilité :</strong> L'entrée utilisateur est affichée sans échappement.</p>
            
            <form method="GET">
                <label>Laissez un message :</label><br>
                <input type="text" name="message" placeholder="Votre message" value="">
                <button type="submit">Envoyer</button>
            </form>
        </div>
        
        <div class="vuln-box">
            <h2>❌ Affichage vulnérable (sans échappement)</h2>
            <div class="result">{unsafe_output}</div>
        </div>
        
        <div class="vuln-box">
            <h2>✅ Affichage sécurisé (avec échappement)</h2>
            <div class="result">{safe_output}</div>
        </div>
        
        <div class="vuln-box">
            <h2>🎯 Exercices à essayer</h2>
            <ol>
                <li><code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code></li>
                <li><code>&lt;img src=x onerror="alert('XSS')"&gt;</code></li>
                <li><code>&lt;svg onload="alert('XSS')"&gt;</code></li>
            </ol>
        </div>
        
        <div class="vuln-box">
            <h2>🛡️ Comment corriger</h2>
            <pre>
import html

# ❌ VULNÉRABLE
output = user_input

# ✅ SÉCURISÉ
output = html.escape(user_input)
            </pre>
        </div>
        '''
    
    def cmd_page(self, params):
        result = ""
        user_input = params.get('host', [''])[0]
        
        # Liste blanche de commandes autorisées pour la sécurité du lab
        allowed_hosts = ['localhost', '127.0.0.1']
        
        if user_input:
            if any(user_input.startswith(h) for h in allowed_hosts):
                # Simulation d'un ping (sans vraiment exécuter pour la sécurité)
                result = f'''
                <div class="result">
                    <strong>Commande simulée :</strong><br>
                    <pre>ping {html.escape(user_input)}</pre>
                    <strong>Note :</strong> Exécution réelle désactivée pour sécurité.
                </div>
                '''
            else:
                result = f'''
                <div class="result">
                    <strong>Tentative détectée :</strong><br>
                    <pre>ping {html.escape(user_input)}</pre>
                    <p>⚠️ Dans une vraie app vulnérable, ceci pourrait exécuter des commandes !</p>
                </div>
                '''
        
        return f'''
        <div class="vuln-box">
            <h2>⚡ Command Injection</h2>
            <p><strong>Vulnérabilité :</strong> L'entrée utilisateur est passée directement au shell.</p>
            
            <form method="GET">
                <label>Ping un hôte :</label><br>
                <input type="text" name="host" placeholder="localhost" value="{html.escape(user_input)}">
                <button type="submit">Ping</button>
            </form>
            {result}
        </div>
        
        <div class="vuln-box">
            <h2>🎯 Payloads théoriques (non exécutés ici)</h2>
            <ol>
                <li><code>localhost; whoami</code> - Chaînage de commandes</li>
                <li><code>localhost | dir</code> - Pipe</li>
                <li><code>localhost && ipconfig</code> - Exécution conditionnelle</li>
            </ol>
        </div>
        
        <div class="vuln-box">
            <h2>🛡️ Comment corriger</h2>
            <pre>
# ❌ VULNÉRABLE
os.system(f"ping {{user_input}}")

# ✅ SÉCURISÉ - Utiliser subprocess avec liste d'arguments
import subprocess
import shlex

# Validation + échappement
if re.match(r'^[a-zA-Z0-9.-]+$', user_input):
    subprocess.run(['ping', '-c', '4', user_input], capture_output=True)
            </pre>
        </div>
        '''
    
    def auth_page(self, params):
        result = ""
        username = params.get('user', [''])[0]
        password = params.get('pass', [''])[0]
        
        if username or password:
            # ⚠️ VULNÉRABLE : SQL Injection dans l'authentification
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            try:
                cursor = DB.cursor()
                cursor.execute(query)
                user = cursor.fetchone()
                if user:
                    result = f'''
                    <div class="result" style="background: #2ecc71;">
                        ✅ Connexion réussie !<br>
                        Bienvenue {html.escape(str(user[1]))} (Role: {html.escape(str(user[3]))})
                    </div>
                    '''
                else:
                    result = '<div class="result">❌ Identifiants incorrects</div>'
            except Exception as e:
                result = f'<div class="result">Erreur : {html.escape(str(e))}</div>'
        
        return f'''
        <div class="vuln-box">
            <h2>🔐 Authentication Bypass</h2>
            <p><strong>Vulnérabilité :</strong> SQL Injection dans le formulaire de login.</p>
            
            <form method="GET">
                <input type="text" name="user" placeholder="Utilisateur" value="{html.escape(username)}"><br>
                <input type="password" name="pass" placeholder="Mot de passe"><br>
                <button type="submit">Se connecter</button>
            </form>
            {result}
        </div>
        
        <div class="vuln-box">
            <h2>🎯 Exercices</h2>
            <ol>
                <li>Connexion normale : <code>admin / admin123</code></li>
                <li>Bypass : <code>admin' --</code> (mot de passe vide)</li>
                <li>Bypass : <code>' OR '1'='1' --</code></li>
            </ol>
        </div>
        
        <div class="vuln-box">
            <h2>🛡️ Comment corriger</h2>
            <pre>
# ❌ VULNÉRABLE
query = f"SELECT * FROM users WHERE username = '{{username}}' AND password = '{{password}}'"

# ✅ SÉCURISÉ
# 1. Requêtes paramétrées
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password_hash))

# 2. Hachage des mots de passe
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            </pre>
        </div>
        '''
    
    def log_message(self, format, *args):
        print(f"[LAB] {args[0]}")


def main():
    port = 8888
    server = HTTPServer(('localhost', port), VulnerableHandler)
    print("=" * 60)
    print("🔬 SECURITY LAB - Environnement Éducatif")
    print("=" * 60)
    print(f"✅ Serveur démarré sur http://localhost:{port}")
    print("⚠️  Usage éducatif uniquement !")
    print("   Appuyez sur Ctrl+C pour arrêter")
    print("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Serveur arrêté.")
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        try:
            server.shutdown()
        except:
            pass

if __name__ == '__main__':
    main()
