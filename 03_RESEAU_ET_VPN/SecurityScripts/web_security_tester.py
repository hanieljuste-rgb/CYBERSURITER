#!/usr/bin/env python3
"""
🌐 Web Security Tester - Tests de sécurité web basiques
Auteur: Formation Cybersécurité
Usage: python web_security_tester.py
⚠️ À utiliser UNIQUEMENT sur vos propres sites ou avec autorisation !
"""

import urllib.request
import urllib.parse
import ssl
import socket
import re

class WebSecurityTester:
    
    def __init__(self, target_url):
        self.target = target_url
        self.results = []
    
    def check_https(self):
        """Vérifie si le site utilise HTTPS"""
        if self.target.startswith('https://'):
            return {'test': 'HTTPS', 'status': '✅ PASS', 'details': 'Le site utilise HTTPS'}
        return {'test': 'HTTPS', 'status': '❌ FAIL', 'details': 'Le site n\'utilise pas HTTPS'}
    
    def check_headers(self):
        """Vérifie les headers de sécurité"""
        results = []
        
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(self.target, headers={'User-Agent': 'SecurityTest/1.0'})
            response = urllib.request.urlopen(req, timeout=10, context=ctx)
            headers = dict(response.headers)
            
            # Headers de sécurité importants
            security_headers = {
                'X-Frame-Options': 'Protection contre le clickjacking',
                'X-Content-Type-Options': 'Empêche le MIME sniffing',
                'X-XSS-Protection': 'Protection XSS (navigateurs anciens)',
                'Strict-Transport-Security': 'Force HTTPS (HSTS)',
                'Content-Security-Policy': 'Politique de sécurité du contenu',
                'Referrer-Policy': 'Contrôle les infos de referrer',
                'Permissions-Policy': 'Contrôle les permissions du navigateur'
            }
            
            for header, description in security_headers.items():
                if header in headers or header.lower() in [h.lower() for h in headers]:
                    results.append({
                        'test': f'Header: {header}',
                        'status': '✅ PRÉSENT',
                        'details': description
                    })
                else:
                    results.append({
                        'test': f'Header: {header}',
                        'status': '⚠️ ABSENT',
                        'details': f'Recommandé: {description}'
                    })
            
            # Vérifier Server header (peut révéler des infos)
            if 'Server' in headers:
                results.append({
                    'test': 'Header: Server',
                    'status': '⚠️ EXPOSÉ',
                    'details': f'Révèle: {headers["Server"]} (peut aider les attaquants)'
                })
            
        except Exception as e:
            results.append({
                'test': 'Headers',
                'status': '❌ ERREUR',
                'details': str(e)
            })
        
        return results
    
    def check_ssl_certificate(self):
        """Vérifie le certificat SSL"""
        if not self.target.startswith('https://'):
            return {'test': 'Certificat SSL', 'status': '❌ N/A', 'details': 'Pas de HTTPS'}
        
        try:
            hostname = urllib.parse.urlparse(self.target).netloc
            ctx = ssl.create_default_context()
            
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Extraire les infos
                    issuer = dict(x[0] for x in cert['issuer'])
                    subject = dict(x[0] for x in cert['subject'])
                    
                    return {
                        'test': 'Certificat SSL',
                        'status': '✅ VALIDE',
                        'details': f"Émetteur: {issuer.get('organizationName', 'N/A')}, "
                                   f"Expire: {cert['notAfter']}"
                    }
        
        except ssl.SSLCertVerificationError as e:
            return {'test': 'Certificat SSL', 'status': '❌ INVALIDE', 'details': str(e)}
        except Exception as e:
            return {'test': 'Certificat SSL', 'status': '❌ ERREUR', 'details': str(e)}
    
    def check_common_files(self):
        """Vérifie la présence de fichiers sensibles exposés"""
        results = []
        
        sensitive_paths = [
            ('robots.txt', 'Peut révéler des chemins cachés'),
            ('.git/config', '⚠️ Dépôt Git exposé - CRITIQUE'),
            ('.env', '⚠️ Variables d\'environnement exposées - CRITIQUE'),
            ('wp-config.php.bak', 'Backup WordPress exposé'),
            ('.htaccess', 'Configuration Apache exposée'),
            ('phpinfo.php', 'Informations PHP exposées'),
            ('server-status', 'Status Apache exposé'),
            ('admin/', 'Interface admin accessible'),
            ('backup/', 'Dossier backup accessible'),
            ('.DS_Store', 'Fichier macOS exposé')
        ]
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        base_url = self.target.rstrip('/')
        
        for path, description in sensitive_paths:
            try:
                url = f"{base_url}/{path}"
                req = urllib.request.Request(url, headers={'User-Agent': 'SecurityTest/1.0'})
                response = urllib.request.urlopen(req, timeout=5, context=ctx)
                
                if response.status == 200:
                    results.append({
                        'test': f'Fichier: {path}',
                        'status': '⚠️ ACCESSIBLE',
                        'details': description
                    })
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    results.append({
                        'test': f'Fichier: {path}',
                        'status': f'ℹ️ HTTP {e.code}',
                        'details': ''
                    })
            except:
                pass
        
        if not results:
            results.append({
                'test': 'Fichiers sensibles',
                'status': '✅ OK',
                'details': 'Aucun fichier sensible courant détecté'
            })
        
        return results
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        print(f"\n🔍 Analyse de sécurité de: {self.target}")
        print("=" * 60)
        
        all_results = []
        
        # Test HTTPS
        result = self.check_https()
        all_results.append(result)
        print(f"{result['status']} {result['test']}: {result['details']}")
        
        # Test SSL
        result = self.check_ssl_certificate()
        all_results.append(result)
        print(f"{result['status']} {result['test']}: {result['details']}")
        
        # Test Headers
        print("\n📋 Headers de sécurité:")
        for result in self.check_headers():
            all_results.append(result)
            print(f"  {result['status']} {result['test']}")
        
        # Test fichiers sensibles
        print("\n📁 Fichiers sensibles:")
        for result in self.check_common_files():
            all_results.append(result)
            print(f"  {result['status']} {result['test']}: {result['details']}")
        
        # Résumé
        passed = len([r for r in all_results if '✅' in r['status']])
        warnings = len([r for r in all_results if '⚠️' in r['status']])
        failed = len([r for r in all_results if '❌' in r['status']])
        
        print("\n" + "=" * 60)
        print(f"📊 RÉSUMÉ: ✅ {passed} OK | ⚠️ {warnings} Avertissements | ❌ {failed} Échecs")
        
        return all_results


def menu():
    """Menu interactif"""
    
    while True:
        print("\n" + "="*50)
        print("🌐 WEB SECURITY TESTER")
        print("="*50)
        print("⚠️ À utiliser UNIQUEMENT sur vos propres sites!")
        print("="*50)
        print("1. 🔍 Tester un site web")
        print("2. 📚 Voir les vulnérabilités courantes (éducatif)")
        print("0. ❌ Quitter")
        print("="*50)
        
        choice = input("Choix: ").strip()
        
        if choice == '1':
            url = input("\nURL à tester (ex: https://example.com): ").strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            tester = WebSecurityTester(url)
            tester.run_all_tests()
        
        elif choice == '2':
            print("\n📚 VULNÉRABILITÉS WEB COURANTES (OWASP Top 10)")
            print("=" * 60)
            vulns = [
                ("A01 - Broken Access Control", "Accès non autorisé à des ressources"),
                ("A02 - Cryptographic Failures", "Données sensibles mal protégées"),
                ("A03 - Injection (SQL, XSS...)", "Code malveillant injecté"),
                ("A04 - Insecure Design", "Failles de conception"),
                ("A05 - Security Misconfiguration", "Mauvaise configuration"),
                ("A06 - Vulnerable Components", "Dépendances vulnérables"),
                ("A07 - Auth Failures", "Authentification défaillante"),
                ("A08 - Data Integrity Failures", "Intégrité des données compromise"),
                ("A09 - Security Logging Failures", "Logs insuffisants"),
                ("A10 - SSRF", "Server-Side Request Forgery")
            ]
            for vuln, desc in vulns:
                print(f"  • {vuln}")
                print(f"    → {desc}\n")
        
        elif choice == '0':
            print("👋 Au revoir!")
            break
        
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    menu()
