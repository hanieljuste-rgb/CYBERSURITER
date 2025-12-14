#!/usr/bin/env python3
"""
🔐 Module Cryptographie & Password Cracking
Apprentissage légal du cracking de mots de passe
"""

import os
import sys
import hashlib
import base64
import itertools
import string
import time
from pathlib import Path

class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
    B = '\033[94m'; M = '\033[95m'; C = '\033[96m'
    W = '\033[97m'; X = '\033[0m'; BOLD = '\033[1m'

def banner():
    print(f"""
{C.C}{C.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║           🔐 MODULE CRYPTOGRAPHIE & CRACKING                  ║
╠═══════════════════════════════════════════════════════════════╣
║  Apprentissage du hashing et cracking de mots de passe        ║
╚═══════════════════════════════════════════════════════════════╝
{C.X}
{C.Y}⚠️ Utilisez uniquement sur VOS propres hashs ou en CTF !{C.X}
""")

def menu():
    print(f"""
{C.BOLD}═══════════════════════════════════════════════════════════════
                   OUTILS CRYPTOGRAPHIQUES
═══════════════════════════════════════════════════════════════{C.X}

  {C.C}[1]{C.X}  Hash Generator - Créer des hashs
  {C.C}[2]{C.X}  Hash Identifier - Identifier un type de hash
  {C.C}[3]{C.X}  Dictionary Attack - Attaque par dictionnaire
  {C.C}[4]{C.X}  Brute Force Demo - Démonstration brute force
  {C.C}[5]{C.X}  Base64 Encode/Decode
  {C.C}[6]{C.X}  ROT13/Caesar Cipher
  {C.C}[7]{C.X}  Hash Lookup (online)
  {C.C}[8]{C.X}  Password Strength Checker
  {C.C}[9]{C.X}  Wordlist Generator
  {C.C}[10]{C.X} Guide des outils (Hashcat, John)
  
  {C.R}[0]{C.X}  Retour au menu principal
""")

def hash_generator():
    """Génère différents types de hashs"""
    print(f"\n{C.C}═══ HASH GENERATOR ═══{C.X}\n")
    text = input(f"{C.Y}Texte à hasher : {C.X}").strip()
    
    if not text:
        print(f"{C.R}[!] Texte vide{C.X}")
        return
    
    print(f"\n{C.G}Résultats pour '{text}':{C.X}\n")
    
    hashes = {
        'MD5': hashlib.md5(text.encode()).hexdigest(),
        'SHA1': hashlib.sha1(text.encode()).hexdigest(),
        'SHA256': hashlib.sha256(text.encode()).hexdigest(),
        'SHA512': hashlib.sha512(text.encode()).hexdigest(),
        'SHA3-256': hashlib.sha3_256(text.encode()).hexdigest(),
    }
    
    for name, value in hashes.items():
        print(f"  {C.C}{name:10}{C.X}: {value}")

def hash_identifier():
    """Identifie le type de hash"""
    print(f"\n{C.C}═══ HASH IDENTIFIER ═══{C.X}\n")
    hash_value = input(f"{C.Y}Entrez le hash : {C.X}").strip()
    
    length = len(hash_value)
    
    print(f"\n{C.G}Analyse du hash ({length} caractères):{C.X}\n")
    
    hash_types = []
    
    if length == 32:
        hash_types.extend(['MD5', 'MD4', 'NTLM', 'LM'])
    elif length == 40:
        hash_types.extend(['SHA1', 'MySQL5', 'RIPEMD-160'])
    elif length == 64:
        hash_types.extend(['SHA256', 'SHA3-256', 'Keccak-256'])
    elif length == 128:
        hash_types.extend(['SHA512', 'SHA3-512', 'Whirlpool'])
    elif length == 56:
        hash_types.append('SHA224')
    elif length == 96:
        hash_types.append('SHA384')
    elif hash_value.startswith('$1$'):
        hash_types.append('MD5crypt (Linux)')
    elif hash_value.startswith('$2a$') or hash_value.startswith('$2b$'):
        hash_types.append('bcrypt')
    elif hash_value.startswith('$5$'):
        hash_types.append('SHA256crypt (Linux)')
    elif hash_value.startswith('$6$'):
        hash_types.append('SHA512crypt (Linux)')
    elif hash_value.startswith('$argon2'):
        hash_types.append('Argon2')
    
    if hash_types:
        print(f"  {C.G}Types possibles:{C.X}")
        for ht in hash_types:
            print(f"    • {ht}")
    else:
        print(f"  {C.Y}Type non reconnu automatiquement{C.X}")

def dictionary_attack():
    """Attaque par dictionnaire simple"""
    print(f"\n{C.C}═══ DICTIONARY ATTACK ═══{C.X}\n")
    print(f"{C.Y}⚠️ Utilisez uniquement sur vos propres hashs !{C.X}\n")
    
    target_hash = input(f"{C.Y}Hash cible (MD5) : {C.X}").strip().lower()
    
    # Mini wordlist intégrée
    common_passwords = [
        'password', '123456', '12345678', 'qwerty', 'abc123',
        'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
        'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
        'bailey', 'passw0rd', 'shadow', '123123', '654321',
        'superman', 'qazwsx', 'michael', 'football', 'password1',
        'password123', 'admin', 'admin123', 'root', 'toor',
        'test', 'guest', 'master', 'changeme', 'hello'
    ]
    
    print(f"\n{C.G}[+] Lancement de l'attaque avec {len(common_passwords)} mots...{C.X}\n")
    
    found = False
    for password in common_passwords:
        test_hash = hashlib.md5(password.encode()).hexdigest()
        if test_hash == target_hash:
            print(f"\n{C.G}[✓] MOT DE PASSE TROUVÉ : {password}{C.X}")
            found = True
            break
    
    if not found:
        print(f"\n{C.Y}[!] Mot de passe non trouvé dans la wordlist{C.X}")
        print(f"{C.C}[i] Essayez avec une wordlist plus complète (rockyou.txt){C.X}")

def brute_force_demo():
    """Démonstration de brute force"""
    print(f"\n{C.C}═══ BRUTE FORCE DEMO ═══{C.X}\n")
    print(f"{C.Y}Cette démo montre comment fonctionne le brute force{C.X}")
    print(f"{C.Y}Entrez un mot de passe SIMPLE (max 4 caractères) pour la démo{C.X}\n")
    
    target = input(f"{C.Y}Mot de passe cible (ex: abc) : {C.X}").strip()
    
    if len(target) > 4:
        print(f"{C.R}[!] Trop long pour la démo (max 4 caractères){C.X}")
        return
    
    target_hash = hashlib.md5(target.encode()).hexdigest()
    charset = string.ascii_lowercase
    
    print(f"\n{C.G}[+] Brute force sur hash MD5 : {target_hash}{C.X}")
    print(f"{C.C}[*] Charset : a-z ({len(charset)} caractères){C.X}")
    
    start_time = time.time()
    attempts = 0
    
    for length in range(1, len(target) + 1):
        for combo in itertools.product(charset, repeat=length):
            attempts += 1
            guess = ''.join(combo)
            
            if attempts % 10000 == 0:
                print(f"\r{C.Y}[*] Tentatives : {attempts}...{C.X}", end='')
            
            if hashlib.md5(guess.encode()).hexdigest() == target_hash:
                elapsed = time.time() - start_time
                print(f"\n\n{C.G}[✓] TROUVÉ : {guess}{C.X}")
                print(f"{C.C}[i] Tentatives : {attempts}{C.X}")
                print(f"{C.C}[i] Temps : {elapsed:.2f} secondes{C.X}")
                return
    
    print(f"\n{C.R}[!] Non trouvé{C.X}")

def base64_tool():
    """Encode/Decode Base64"""
    print(f"\n{C.C}═══ BASE64 TOOL ═══{C.X}\n")
    
    print(f"  {C.C}[1]{C.X} Encoder")
    print(f"  {C.C}[2]{C.X} Décoder")
    
    choice = input(f"\n{C.Y}Choix : {C.X}").strip()
    text = input(f"{C.Y}Texte : {C.X}").strip()
    
    if choice == '1':
        result = base64.b64encode(text.encode()).decode()
        print(f"\n{C.G}Encodé : {result}{C.X}")
    elif choice == '2':
        try:
            result = base64.b64decode(text).decode()
            print(f"\n{C.G}Décodé : {result}{C.X}")
        except:
            print(f"\n{C.R}[!] Erreur de décodage{C.X}")

def rot_cipher():
    """ROT13 et Caesar cipher"""
    print(f"\n{C.C}═══ ROT/CAESAR CIPHER ═══{C.X}\n")
    
    text = input(f"{C.Y}Texte : {C.X}").strip()
    shift = input(f"{C.Y}Décalage (défaut 13) : {C.X}").strip()
    shift = int(shift) if shift else 13
    
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    
    print(f"\n{C.G}Résultat (ROT{shift}) : {result}{C.X}")

def password_strength():
    """Vérifie la force d'un mot de passe"""
    print(f"\n{C.C}═══ PASSWORD STRENGTH CHECKER ═══{C.X}\n")
    password = input(f"{C.Y}Mot de passe à tester : {C.X}").strip()
    
    score = 0
    feedback = []
    
    # Longueur
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Moins de 8 caractères")
    
    if len(password) >= 12:
        score += 1
    
    if len(password) >= 16:
        score += 1
    
    # Complexité
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("❌ Pas de minuscules")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("❌ Pas de majuscules")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("❌ Pas de chiffres")
    
    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("❌ Pas de caractères spéciaux")
    
    # Patterns faibles
    weak_patterns = ['123', 'abc', 'qwerty', 'password', 'admin']
    if any(p in password.lower() for p in weak_patterns):
        score -= 2
        feedback.append("❌ Contient un pattern faible")
    
    # Affichage
    print(f"\n{C.G}Score : {score}/7{C.X}\n")
    
    if score <= 2:
        print(f"{C.R}Force : TRÈS FAIBLE 🔴{C.X}")
    elif score <= 4:
        print(f"{C.Y}Force : FAIBLE 🟡{C.X}")
    elif score <= 5:
        print(f"{C.C}Force : MOYEN 🔵{C.X}")
    else:
        print(f"{C.G}Force : FORT 🟢{C.X}")
    
    if feedback:
        print(f"\n{C.Y}Améliorations suggérées:{C.X}")
        for f in feedback:
            print(f"  {f}")

def tools_guide():
    """Guide Hashcat et John the Ripper"""
    guide = f"""
{C.C}{C.BOLD}═══ GUIDE DES OUTILS DE CRACKING ═══{C.X}

{C.BOLD}═══ HASHCAT ═══{C.X}
{C.Y}L'outil de cracking le plus rapide (GPU){C.X}

{C.G}Modes d'attaque :{C.X}
  -a 0 : Dictionnaire
  -a 1 : Combinaison
  -a 3 : Brute force (mask)
  -a 6 : Dictionnaire + mask
  -a 7 : Mask + dictionnaire

{C.G}Types de hash courants (-m) :{C.X}
  0    : MD5
  100  : SHA1
  1400 : SHA256
  1800 : SHA512crypt (Linux)
  1000 : NTLM (Windows)
  3200 : bcrypt

{C.G}Exemples :{C.X}
  {C.M}hashcat -m 0 -a 0 hash.txt rockyou.txt{C.X}
  {C.M}hashcat -m 0 -a 3 hash.txt ?a?a?a?a?a?a{C.X}
  {C.M}hashcat -m 1000 -a 0 ntlm.txt wordlist.txt{C.X}

{C.BOLD}═══ JOHN THE RIPPER ═══{C.X}
{C.Y}Outil polyvalent, bon pour le cracking CPU{C.X}

{C.G}Commandes de base :{C.X}
  {C.M}john hash.txt{C.X}                    # Auto-detect
  {C.M}john --wordlist=rockyou.txt hash.txt{C.X}
  {C.M}john --format=raw-md5 hash.txt{C.X}
  {C.M}john --show hash.txt{C.X}             # Voir les résultats

{C.BOLD}═══ WORDLISTS POPULAIRES ═══{C.X}
  • rockyou.txt (~14 millions)
  • SecLists (collection)
  • CrackStation (~1.5 milliard)

{C.G}Téléchargement rockyou.txt :{C.X}
  {C.M}wget https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt{C.X}
"""
    print(guide)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    
    while True:
        menu()
        choice = input(f"\n{C.C}Choisissez une option : {C.X}").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            hash_generator()
        elif choice == '2':
            hash_identifier()
        elif choice == '3':
            dictionary_attack()
        elif choice == '4':
            brute_force_demo()
        elif choice == '5':
            base64_tool()
        elif choice == '6':
            rot_cipher()
        elif choice == '7':
            print(f"\n{C.Y}[i] Utilisez https://crackstation.net ou https://hashes.com{C.X}")
        elif choice == '8':
            password_strength()
        elif choice == '9':
            print(f"\n{C.Y}[i] Utilisez crunch ou cupp pour générer des wordlists{C.X}")
        elif choice == '10':
            tools_guide()
        else:
            print(f"\n{C.R}[!] Option invalide{C.X}")
        
        input(f"\n{C.Y}Appuyez sur Entrée pour continuer...{C.X}")

if __name__ == "__main__":
    main()
