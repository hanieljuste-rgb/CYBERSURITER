#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              LABORATOIRE D'APPRENTISSAGE CYBERSÉCURITÉ                       ║
║                                                                              ║
║  Apprenez comment les attaques fonctionnent pour mieux vous protéger         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import socket
import hashlib
import base64
import urllib.parse
import subprocess
import os
import json
import time
import threading
from datetime import datetime

# ============================================================================
# LEÇON 1: RECONNAISSANCE - Comment les hackers trouvent des informations
# ============================================================================

class Reconnaissance:
    """
    🔍 PHASE 1 D'UNE ATTAQUE: LA RECONNAISSANCE
    
    Avant d'attaquer, un hacker collecte des informations sur sa cible.
    C'est la phase la plus importante - elle peut prendre des semaines.
    """
    
    @staticmethod
    def expliquer():
        print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                   LEÇON 1: RECONNAISSANCE                        ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    🎯 OBJECTIF DES HACKERS:
    Collecter un maximum d'informations AVANT d'attaquer.
    
    📚 TYPES DE RECONNAISSANCE:
    
    1. PASSIVE (sans toucher la cible):
       - Recherche Google sur l'entreprise/personne
       - LinkedIn, Facebook, Instagram
       - Whois sur les domaines
       - Shodan pour les appareils connectés
    
    2. ACTIVE (interaction avec la cible):
       - Scan de ports
       - Scan de vulnérabilités
       - Enumération de services
    
    🛡️ COMMENT SE PROTÉGER:
    - Limiter les informations publiques
    - Paramètres de confidentialité sur les réseaux sociaux
    - Ne pas exposer de services inutiles sur Internet
        """)
    
    @staticmethod
    def scan_ports(ip, ports_communs=True):
        """
        Scan de ports - Trouve les services ouverts
        
        🔴 COMMENT ÇA MARCHE:
        Tente de se connecter à chaque port.
        Si la connexion réussit = port ouvert = service actif
        """
        print(f"\n🔍 Scan des ports sur {ip}")
        print("="*50)
        
        if ports_communs:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 
                    3306, 3389, 5432, 5900, 8080, 8443]
        else:
            ports = range(1, 1025)
        
        ouverts = []
        services = {
            21: "FTP (transfert fichiers)",
            22: "SSH (accès distant sécurisé)",
            23: "Telnet (accès distant non sécurisé ⚠️)",
            25: "SMTP (email)",
            53: "DNS",
            80: "HTTP (site web)",
            110: "POP3 (email)",
            143: "IMAP (email)",
            443: "HTTPS (site web sécurisé)",
            445: "SMB (partage Windows)",
            3306: "MySQL (base de données)",
            3389: "RDP (bureau distant Windows)",
            5432: "PostgreSQL (base de données)",
            5900: "VNC (bureau distant)",
            8080: "HTTP Proxy",
            8443: "HTTPS alternatif"
        }
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    service = services.get(port, "Inconnu")
                    ouverts.append((port, service))
                    print(f"  ✅ Port {port}: OUVERT - {service}")
                sock.close()
            except:
                pass
        
        if not ouverts:
            print("  Aucun port ouvert trouvé (ou hôte injoignable)")
        
        print(f"\n📊 {len(ouverts)} ports ouverts trouvés")
        return ouverts
    
    @staticmethod
    def dns_lookup(domaine):
        """Résolution DNS"""
        print(f"\n🌐 Lookup DNS pour: {domaine}")
        print("="*50)
        
        try:
            ip = socket.gethostbyname(domaine)
            print(f"  IP: {ip}")
            
            # Reverse lookup
            try:
                hostname = socket.gethostbyaddr(ip)
                print(f"  Hostname: {hostname[0]}")
            except:
                pass
            
            return ip
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
            return None

# ============================================================================
# LEÇON 2: MOTS DE PASSE - Comment ils sont stockés et crackés
# ============================================================================

class MotsDePasse:
    """
    🔐 LEÇON 2: SÉCURITÉ DES MOTS DE PASSE
    
    Comment les mots de passe sont stockés et comment les hackers les crackent.
    """
    
    @staticmethod
    def expliquer():
        print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                LEÇON 2: MOTS DE PASSE                            ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    📚 COMMENT LES MOTS DE PASSE SONT STOCKÉS:
    
    ❌ MAUVAIS: En clair (texte brut)
       Base de données: password = "motdepasse123"
       → Si la base est volée, tous les mots de passe sont lisibles!
    
    ⚠️ MOYEN: Hash simple (MD5, SHA1)
       Base de données: password = "482c811da5d5b4bc6d497ffa98491e38"
       → Vulnérable aux tables arc-en-ciel et brute force
    
    ✅ BON: Hash + Salt (bcrypt, Argon2)
       Base de données: password = "$2b$12$LQv3c1yqBWVHxkd0..."
       → Chaque mot de passe a un sel unique
       → Très lent à cracker
    
    🔴 TECHNIQUES D'ATTAQUE:
    
    1. DICTIONNAIRE: Essayer des mots courants
       password, 123456, qwerty, admin, motdepasse...
    
    2. BRUTE FORCE: Essayer toutes les combinaisons
       a, b, c... aa, ab, ac... (très long!)
    
    3. TABLES ARC-EN-CIEL: Hashes pré-calculés
       Bases de données de millions de hashes
    
    4. CREDENTIAL STUFFING: Réutiliser des fuites
       "Cette personne utilise le même mot de passe partout"
    
    🛡️ COMMENT SE PROTÉGER:
    - Mots de passe longs (12+ caractères)
    - Uniques pour chaque site
    - Gestionnaire de mots de passe (Bitwarden, 1Password)
    - 2FA activé partout
        """)
    
    @staticmethod
    def hasher(mot_de_passe, algorithme="sha256"):
        """Montre comment les mots de passe sont hashés"""
        print(f"\n🔐 Hachage de: '{mot_de_passe}'")
        print("="*50)
        
        # Différents algorithmes
        hashes = {
            "MD5": hashlib.md5(mot_de_passe.encode()).hexdigest(),
            "SHA1": hashlib.sha1(mot_de_passe.encode()).hexdigest(),
            "SHA256": hashlib.sha256(mot_de_passe.encode()).hexdigest(),
            "SHA512": hashlib.sha512(mot_de_passe.encode()).hexdigest()[:64] + "..."
        }
        
        for algo, hash_value in hashes.items():
            print(f"  {algo}: {hash_value}")
        
        print("""
    ⚠️ PROBLÈME: Le même mot de passe donne TOUJOURS le même hash!
    C'est pourquoi on utilise un "sel" (salt) aléatoire.
        """)
        
        # Avec salt
        import secrets
        salt = secrets.token_hex(16)
        salted = hashlib.sha256((salt + mot_de_passe).encode()).hexdigest()
        print(f"  SHA256 + Salt: {salt}:{salted}")
        print("  → Maintenant chaque hash est unique!")
        
        return hashes
    
    @staticmethod
    def demo_dictionnaire():
        """Démontre une attaque par dictionnaire"""
        print("\n🔴 DÉMONSTRATION: Attaque par dictionnaire")
        print("="*50)
        
        # Hash cible (simulé)
        mot_secret = "password123"
        hash_cible = hashlib.sha256(mot_secret.encode()).hexdigest()
        
        print(f"  Hash cible: {hash_cible[:32]}...")
        print("  Tentative de crack...\n")
        
        # Dictionnaire commun
        dictionnaire = [
            "password", "123456", "password123", "admin", "letmein",
            "welcome", "monkey", "dragon", "master", "qwerty",
            "login", "abc123", "starwars", "123123", "password1"
        ]
        
        for i, mot in enumerate(dictionnaire, 1):
            hash_test = hashlib.sha256(mot.encode()).hexdigest()
            print(f"  [{i:2}] Essai: {mot:15} → ", end="")
            
            if hash_test == hash_cible:
                print(f"✅ TROUVÉ!")
                print(f"\n  💀 Mot de passe cracké: {mot}")
                return mot
            else:
                print("❌")
            
            time.sleep(0.1)  # Ralentir pour la démo
        
        print("\n  Mot de passe non trouvé dans le dictionnaire")
        return None
    
    @staticmethod
    def evaluer_force(mot_de_passe):
        """Évalue la force d'un mot de passe"""
        print(f"\n📊 Évaluation de: '{mot_de_passe}'")
        print("="*50)
        
        score = 0
        feedback = []
        
        # Longueur
        if len(mot_de_passe) >= 8:
            score += 1
            feedback.append("✅ 8+ caractères")
        else:
            feedback.append("❌ Moins de 8 caractères")
        
        if len(mot_de_passe) >= 12:
            score += 1
            feedback.append("✅ 12+ caractères")
        
        if len(mot_de_passe) >= 16:
            score += 1
            feedback.append("✅ 16+ caractères (excellent!)")
        
        # Complexité
        if any(c.isupper() for c in mot_de_passe):
            score += 1
            feedback.append("✅ Contient des majuscules")
        else:
            feedback.append("❌ Pas de majuscules")
        
        if any(c.islower() for c in mot_de_passe):
            score += 1
            feedback.append("✅ Contient des minuscules")
        
        if any(c.isdigit() for c in mot_de_passe):
            score += 1
            feedback.append("✅ Contient des chiffres")
        else:
            feedback.append("❌ Pas de chiffres")
        
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in mot_de_passe):
            score += 1
            feedback.append("✅ Contient des symboles")
        else:
            feedback.append("❌ Pas de symboles")
        
        # Patterns communs
        patterns_faibles = ["123", "abc", "qwerty", "password", "azerty"]
        if any(p in mot_de_passe.lower() for p in patterns_faibles):
            score -= 2
            feedback.append("⚠️ Contient un pattern commun!")
        
        for f in feedback:
            print(f"  {f}")
        
        # Score final
        if score <= 2:
            niveau = "🔴 TRÈS FAIBLE"
        elif score <= 4:
            niveau = "🟠 FAIBLE"
        elif score <= 5:
            niveau = "🟡 MOYEN"
        elif score <= 6:
            niveau = "🟢 FORT"
        else:
            niveau = "💪 TRÈS FORT"
        
        print(f"\n  Score: {score}/7")
        print(f"  Niveau: {niveau}")
        
        return score

# ============================================================================
# LEÇON 3: PHISHING - Comment les gens se font piéger
# ============================================================================

class Phishing:
    """
    🎣 LEÇON 3: PHISHING
    
    Comment les hackers trompent les gens pour voler leurs informations.
    """
    
    @staticmethod
    def expliquer():
        print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                     LEÇON 3: PHISHING                            ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    🎣 QU'EST-CE QUE LE PHISHING?
    
    Technique pour tromper quelqu'un en se faisant passer pour
    une entité de confiance (banque, réseau social, entreprise...).
    
    📧 TYPES DE PHISHING:
    
    1. EMAIL PHISHING (le plus courant)
       "Votre compte sera suspendu, cliquez ici!"
       → Lien vers un faux site qui vole vos identifiants
    
    2. SPEAR PHISHING (ciblé)
       Email personnalisé avec vos infos (nom, entreprise...)
       → Plus crédible car personnalisé
    
    3. SMISHING (SMS)
       "Colis en attente, cliquez sur ce lien"
       → Faux site de La Poste, Chronopost...
    
    4. VISHING (téléphone)
       "Bonjour, c'est Microsoft, votre ordinateur a un virus"
       → Arnaque au support technique
    
    5. CLONE PHISHING
       Copie exacte d'un email légitime avec un lien modifié
    
    🔴 SIGNES D'UN PHISHING:
    
    ✓ Urgence artificielle ("Votre compte sera fermé dans 24h!")
    ✓ Fautes d'orthographe
    ✓ Adresse email suspecte (support@amaz0n-security.com)
    ✓ Lien qui ne correspond pas au site officiel
    ✓ Demande d'informations sensibles
    ✓ Pièces jointes suspectes (.exe, .js, .scr)
    
    🛡️ COMMENT SE PROTÉGER:
    
    1. VÉRIFIEZ L'EXPÉDITEUR (l'adresse email complète)
    2. SURVOLEZ les liens AVANT de cliquer
    3. ALLEZ directement sur le site (pas via le lien)
    4. ACTIVEZ la double authentification (2FA)
    5. NE JAMAIS donner son mot de passe par email/téléphone
        """)
    
    @staticmethod
    def analyser_url(url):
        """Analyse une URL pour détecter un phishing potentiel"""
        print(f"\n🔍 Analyse de l'URL: {url}")
        print("="*60)
        
        risques = []
        
        # Parser l'URL
        parsed = urllib.parse.urlparse(url)
        
        print(f"  Protocole: {parsed.scheme}")
        print(f"  Domaine: {parsed.netloc}")
        print(f"  Chemin: {parsed.path}")
        
        # Vérifications
        if parsed.scheme != "https":
            risques.append("⚠️ Pas de HTTPS - connexion non sécurisée")
        
        # Domaines suspects
        domaine = parsed.netloc.lower()
        
        # Typosquatting
        marques = ["google", "facebook", "amazon", "apple", "microsoft", 
                   "paypal", "netflix", "instagram", "twitter", "linkedin"]
        
        for marque in marques:
            if marque in domaine and f"{marque}.com" not in domaine:
                risques.append(f"⚠️ Possible typosquatting de {marque}")
        
        # Caractères suspects
        if any(c in domaine for c in ["0", "1", "l", "-"]):
            if any(m in domaine for m in marques):
                risques.append("⚠️ Caractères suspects (0 au lieu de o, 1 au lieu de l...)")
        
        # Sous-domaines suspects
        if domaine.count(".") > 2:
            risques.append("⚠️ Nombreux sous-domaines (technique de phishing)")
        
        # IP au lieu de domaine
        import re
        if re.match(r"\d+\.\d+\.\d+\.\d+", domaine):
            risques.append("🔴 Adresse IP au lieu d'un domaine - TRÈS SUSPECT!")
        
        # Mots suspects dans l'URL
        mots_suspects = ["login", "signin", "verify", "secure", "account", 
                        "update", "confirm", "banking", "password"]
        chemin = (parsed.path + parsed.query).lower()
        for mot in mots_suspects:
            if mot in chemin:
                risques.append(f"⚠️ Mot suspect dans l'URL: '{mot}'")
                break
        
        # Afficher les risques
        if risques:
            print("\n🚨 RISQUES DÉTECTÉS:")
            for r in risques:
                print(f"  {r}")
            print(f"\n  Score de risque: {len(risques)}/5")
            if len(risques) >= 2:
                print("  ⛔ PROBABLEMENT UN PHISHING!")
        else:
            print("\n✅ Aucun risque évident détecté")
            print("  (Restez vigilant, ce n'est pas une garantie)")
        
        return risques
    
    @staticmethod
    def demo_homograph():
        """Démontre les attaques homographes (caractères similaires)"""
        print("\n🔤 DÉMONSTRATION: Attaque Homographe")
        print("="*50)
        print("""
    Ces URLs semblent identiques mais ne le sont pas:
    
    1. apple.com      (légitime)
    2. аpple.com      (le 'a' est en cyrillique!)
    3. app1e.com      (le 'l' est un '1')
    4. appIe.com      (le 'l' est un 'I' majuscule)
    
    C'est pourquoi il faut TOUJOURS:
    - Taper l'adresse manuellement
    - Utiliser les favoris
    - Ne pas cliquer sur les liens dans les emails
        """)

# ============================================================================
# LEÇON 4: INJECTION SQL - Comprendre les failles web
# ============================================================================

class InjectionSQL:
    """
    💉 LEÇON 4: INJECTION SQL
    
    Une des failles les plus courantes et dangereuses.
    """
    
    @staticmethod
    def expliquer():
        print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                  LEÇON 4: INJECTION SQL                          ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    💉 QU'EST-CE QUE L'INJECTION SQL?
    
    Technique qui permet d'exécuter des commandes SQL malveillantes
    via les champs de saisie d'un site web.
    
    📖 EXEMPLE SIMPLE:
    
    Code vulnérable:
    ┌────────────────────────────────────────────────────────────┐
    │ query = "SELECT * FROM users WHERE user='" + username + "'"│
    └────────────────────────────────────────────────────────────┘
    
    Si l'utilisateur entre: admin' OR '1'='1
    
    La requête devient:
    ┌────────────────────────────────────────────────────────────┐
    │ SELECT * FROM users WHERE user='admin' OR '1'='1'          │
    └────────────────────────────────────────────────────────────┘
    
    → '1'='1' est TOUJOURS vrai
    → La requête retourne TOUS les utilisateurs!
    
    🔴 CE QU'UN ATTAQUANT PEUT FAIRE:
    
    1. Contourner l'authentification (se connecter sans mot de passe)
    2. Lire toute la base de données
    3. Modifier des données
    4. Supprimer des tables
    5. Exécuter des commandes système (dans certains cas)
    
    📝 PAYLOADS COURANTS:
    
    • ' OR '1'='1            → Bypass login
    • ' OR '1'='1' --        → Bypass avec commentaire
    • ' UNION SELECT * --    → Extraire des données
    • '; DROP TABLE users;-- → Supprimer une table
    
    🛡️ COMMENT SE PROTÉGER (pour les développeurs):
    
    1. Requêtes préparées (prepared statements)
    2. ORM (Object-Relational Mapping)
    3. Validation des entrées
    4. Principe du moindre privilège pour la DB
        """)
    
    @staticmethod
    def demo_vulnerable():
        """Démonstration d'un système vulnérable"""
        print("\n💉 DÉMONSTRATION: Système de login vulnérable")
        print("="*50)
        
        # Simulation d'une base de données
        users_db = {
            "admin": "supersecret",
            "user1": "password123",
            "john": "qwerty"
        }
        
        def login_vulnerable(username, password):
            """Fonction vulnérable (NE JAMAIS FAIRE ÇA!)"""
            # Simulation de la requête SQL
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            print(f"  Requête SQL: {query}")
            
            # Détection basique d'injection
            if "' OR " in username.upper() or "' OR " in password.upper():
                print("  → Injection détectée! Accès accordé (vulnérable)")
                return True
            
            return users_db.get(username) == password
        
        print("\n1. Login normal:")
        print("   Username: admin")
        print("   Password: supersecret")
        result = login_vulnerable("admin", "supersecret")
        print(f"   Résultat: {'✅ Accès accordé' if result else '❌ Accès refusé'}")
        
        print("\n2. Login avec mauvais mot de passe:")
        print("   Username: admin")
        print("   Password: wrongpassword")
        result = login_vulnerable("admin", "wrongpassword")
        print(f"   Résultat: {'✅ Accès accordé' if result else '❌ Accès refusé'}")
        
        print("\n3. 💀 INJECTION SQL:")
        print("   Username: admin' OR '1'='1")
        print("   Password: nimportequoi")
        result = login_vulnerable("admin' OR '1'='1", "nimportequoi")
        print(f"   Résultat: {'✅ Accès accordé' if result else '❌ Accès refusé'}")
        print("   → L'attaquant a contourné l'authentification!")

# ============================================================================
# LEÇON 5: XSS - Cross-Site Scripting
# ============================================================================

class XSS:
    """
    🌐 LEÇON 5: XSS (Cross-Site Scripting)
    """
    
    @staticmethod
    def expliquer():
        print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                    LEÇON 5: XSS                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    🌐 QU'EST-CE QUE LE XSS?
    
    Injection de code JavaScript malveillant dans une page web
    qui sera exécuté par les navigateurs des victimes.
    
    📖 TYPES DE XSS:
    
    1. REFLECTED XSS (réfléchi)
       Le script est dans l'URL et exécuté immédiatement
       Exemple: site.com/search?q=<script>alert('XSS')</script>
    
    2. STORED XSS (stocké)
       Le script est sauvegardé en base de données
       Exemple: commentaire malveillant sur un forum
    
    3. DOM-BASED XSS
       Manipulation du DOM côté client
    
    🔴 CE QU'UN ATTAQUANT PEUT FAIRE:
    
    • Voler les cookies de session (vol de compte)
    • Keylogger (enregistrer les frappes)
    • Rediriger vers un site de phishing
    • Modifier le contenu de la page
    • Télécharger des malwares
    
    📝 PAYLOADS COURANTS:
    
    • <script>alert('XSS')</script>
    • <img src=x onerror=alert('XSS')>
    • <svg onload=alert('XSS')>
    • <body onload=alert('XSS')>
    
    🛡️ COMMENT SE PROTÉGER:
    
    1. Échapper les caractères spéciaux (< > " ')
    2. Content Security Policy (CSP)
    3. HTTPOnly pour les cookies
    4. Validation côté serveur
        """)
    
    @staticmethod
    def demo_payloads():
        """Affiche des exemples de payloads XSS"""
        print("\n🌐 EXEMPLES DE PAYLOADS XSS")
        print("="*50)
        
        payloads = [
            ("<script>alert('XSS')</script>", "Basique"),
            ("<img src=x onerror=alert('XSS')>", "Via image"),
            ("<svg/onload=alert('XSS')>", "Via SVG"),
            ("<body onload=alert('XSS')>", "Via body"),
            ("javascript:alert('XSS')", "Via lien"),
            ("<iframe src='javascript:alert(1)'>", "Via iframe"),
            ("<input onfocus=alert('XSS') autofocus>", "Via input"),
        ]
        
        for payload, description in payloads:
            print(f"\n  {description}:")
            print(f"  {payload}")

# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def afficher_menu():
    print("\n" + "="*70)
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║         LABORATOIRE D'APPRENTISSAGE CYBERSÉCURITÉ               ║
    ║                                                                  ║
    ║   "Comprendre les attaques pour mieux se protéger"              ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    ┌─────────────────────────────────────────────────────────────────┐
    │  📚 LEÇONS THÉORIQUES                                           │
    ├─────────────────────────────────────────────────────────────────┤
    │  [1]  Reconnaissance (comment les hackers collectent des infos) │
    │  [2]  Mots de passe (comment ils sont crackés)                  │
    │  [3]  Phishing (comment les gens se font piéger)                │
    │  [4]  Injection SQL (failles des sites web)                     │
    │  [5]  XSS - Cross-Site Scripting                                │
    ├─────────────────────────────────────────────────────────────────┤
    │  🔧 OUTILS PRATIQUES                                            │
    ├─────────────────────────────────────────────────────────────────┤
    │  [10] Scanner de ports                                          │
    │  [11] Lookup DNS                                                │
    │  [12] Hasher un mot de passe                                    │
    │  [13] Évaluer la force d'un mot de passe                        │
    │  [14] Analyser une URL (détecter phishing)                      │
    │  [15] Démo attaque dictionnaire                                 │
    │  [16] Démo injection SQL                                        │
    ├─────────────────────────────────────────────────────────────────┤
    │  [0]  Quitter                                                   │
    └─────────────────────────────────────────────────────────────────┘
    """)

def main():
    while True:
        afficher_menu()
        choix = input("\n👉 Votre choix: ").strip()
        
        try:
            if choix == "0":
                print("\n👋 Bonne continuation dans votre apprentissage!")
                break
            
            # Leçons théoriques
            elif choix == "1":
                Reconnaissance.expliquer()
            elif choix == "2":
                MotsDePasse.expliquer()
            elif choix == "3":
                Phishing.expliquer()
            elif choix == "4":
                InjectionSQL.expliquer()
            elif choix == "5":
                XSS.expliquer()
            
            # Outils pratiques
            elif choix == "10":
                ip = input("IP ou domaine à scanner: ").strip()
                Reconnaissance.scan_ports(ip)
            elif choix == "11":
                domaine = input("Domaine à résoudre: ").strip()
                Reconnaissance.dns_lookup(domaine)
            elif choix == "12":
                mdp = input("Mot de passe à hasher: ").strip()
                MotsDePasse.hasher(mdp)
            elif choix == "13":
                mdp = input("Mot de passe à évaluer: ").strip()
                MotsDePasse.evaluer_force(mdp)
            elif choix == "14":
                url = input("URL à analyser: ").strip()
                Phishing.analyser_url(url)
            elif choix == "15":
                MotsDePasse.demo_dictionnaire()
            elif choix == "16":
                InjectionSQL.demo_vulnerable()
            
            else:
                print("❌ Option invalide")
        
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        input("\n⏎ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
