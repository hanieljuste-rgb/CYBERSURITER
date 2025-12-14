#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║     ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗          ║
║     ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗         ║
║     ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║         ║
║     ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║         ║
║     ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝         ║
║     ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝          ║
║                                                                                  ║
║                    🔓 PASSWORD CRACKER AVANCÉ v2.0 🔓                            ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import hashlib
import itertools
import string
import time
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

OUTPUT_DIR = Path(r"C:\Users\davis\OneDrive\Bureau\HACKING\02_EXTRACTION_DONNEES\PASSWORDS")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

WORDLIST_DIR = Path(r"C:\Users\davis\OneDrive\Bureau\HACKING\Tools\wordlists")
WORDLIST_DIR.mkdir(parents=True, exist_ok=True)

# Couleurs
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

# Mots de passe communs (top 100)
COMMON_PASSWORDS = [
    "123456", "password", "123456789", "12345678", "12345", "1234567", "1234567890",
    "qwerty", "abc123", "111111", "123123", "admin", "letmein", "welcome", "monkey",
    "password1", "1234", "sunshine", "master", "hello", "freedom", "whatever",
    "qazwsx", "trustno1", "000000", "football", "baseball", "iloveyou", "dragon",
    "password123", "batman", "login", "passw0rd", "123qwe", "mustang", "access",
    "shadow", "michael", "superman", "696969", "654321", "joshua", "1q2w3e4r",
    "jennifer", "hunter", "buster", "soccer", "harley", "ranger", "thomas",
    "tigger", "robert", "soccer", "charlie", "cheese", "martin", "george",
    "computer", "corvette", "mercedes", "maverick", "phoenix", "ferrari", "thunder",
    "cowboy", "boomer", "austin", "brandon", "steven", "rafael", "matthew",
    "killer", "summer", "winter", "falcon", "taylor", "ashley", "nicole",
    "pepper", "joshua", "andrew", "daniel", "mother", "father", "nothing",
    "michelle", "viking", "pookie", "sparky", "helpme", "ginger", "yellow",
    "azerty", "00000000", "11111111", "12341234", "abcd1234", "admin123", "root",
    "toor", "guest", "test", "oracle", "mysql", "postgres", "linux", "windows"
]

# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS DE HACHAGE
# ═══════════════════════════════════════════════════════════════════════════════

def identify_hash(hash_str):
    """Identifie le type de hash"""
    hash_len = len(hash_str)
    
    patterns = {
        32: ["MD5", "NTLM"],
        40: ["SHA1"],
        56: ["SHA224"],
        64: ["SHA256", "SHA3-256"],
        96: ["SHA384"],
        128: ["SHA512", "SHA3-512"],
    }
    
    if hash_len in patterns:
        return patterns[hash_len]
    
    # Patterns spéciaux
    if hash_str.startswith("$2a$") or hash_str.startswith("$2b$"):
        return ["bcrypt"]
    if hash_str.startswith("$1$"):
        return ["MD5-crypt"]
    if hash_str.startswith("$5$"):
        return ["SHA256-crypt"]
    if hash_str.startswith("$6$"):
        return ["SHA512-crypt"]
    if hash_str.startswith("$apr1$"):
        return ["APR1-MD5"]
    if hash_str.startswith("$argon2"):
        return ["Argon2"]
    
    return ["Inconnu"]

def hash_password(password, algorithm):
    """Hash un mot de passe avec l'algorithme spécifié"""
    pwd = password.encode('utf-8')
    
    if algorithm == "MD5":
        return hashlib.md5(pwd).hexdigest()
    elif algorithm == "SHA1":
        return hashlib.sha1(pwd).hexdigest()
    elif algorithm == "SHA224":
        return hashlib.sha224(pwd).hexdigest()
    elif algorithm == "SHA256":
        return hashlib.sha256(pwd).hexdigest()
    elif algorithm == "SHA384":
        return hashlib.sha384(pwd).hexdigest()
    elif algorithm == "SHA512":
        return hashlib.sha512(pwd).hexdigest()
    elif algorithm == "NTLM":
        return hashlib.new('md4', password.encode('utf-16le')).hexdigest()
    else:
        return hashlib.md5(pwd).hexdigest()

def verify_hash(password, target_hash, algorithm):
    """Vérifie si un mot de passe correspond au hash"""
    computed = hash_password(password, algorithm)
    return computed.lower() == target_hash.lower()

# ═══════════════════════════════════════════════════════════════════════════════
# ATTAQUES
# ═══════════════════════════════════════════════════════════════════════════════

def dictionary_attack(target_hash, algorithm, wordlist=None, show_progress=True):
    """Attaque par dictionnaire"""
    
    if wordlist is None:
        passwords = COMMON_PASSWORDS
        source = "Mots de passe communs"
    elif isinstance(wordlist, list):
        passwords = wordlist
        source = "Liste personnalisée"
    else:
        # Charger depuis fichier
        try:
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            source = str(wordlist)
        except:
            print(f"    {C.RED}Erreur: Impossible de charger {wordlist}{C.END}")
            return None
    
    total = len(passwords)
    print(f"\n    {C.CYAN}📖 Attaque dictionnaire ({source}){C.END}")
    print(f"    {C.WHITE}Hash: {target_hash[:40]}...{C.END}")
    print(f"    {C.WHITE}Algo: {algorithm} | Mots: {total:,}{C.END}\n")
    
    start_time = time.time()
    found = None
    
    for i, pwd in enumerate(passwords):
        if show_progress and i % 1000 == 0:
            pct = int(i / total * 100)
            speed = i / (time.time() - start_time + 0.001)
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            print(f"\r    [{bar}] {pct}% | {speed:.0f} pwd/s | Test: {pwd[:20]:<20}", end="", flush=True)
        
        if verify_hash(pwd, target_hash, algorithm):
            found = pwd
            break
    
    elapsed = time.time() - start_time
    
    if found:
        print(f"\r    {C.GREEN}{'█' * 20} 100%{C.END}                                        ")
        print(f"\n    {C.GREEN}✓ MOT DE PASSE TROUVÉ!{C.END}")
        print(f"    {C.BOLD}{C.GREEN}→ {found}{C.END}")
        print(f"    {C.WHITE}Temps: {elapsed:.2f}s{C.END}")
    else:
        print(f"\r    {C.RED}{'█' * 20} 100%{C.END}                                        ")
        print(f"\n    {C.RED}✗ Mot de passe non trouvé dans le dictionnaire{C.END}")
    
    return found

def brute_force_attack(target_hash, algorithm, charset=None, min_len=1, max_len=6, show_progress=True):
    """Attaque par force brute"""
    
    if charset is None:
        charset = string.ascii_lowercase + string.digits
    
    print(f"\n    {C.CYAN}🔨 Attaque force brute{C.END}")
    print(f"    {C.WHITE}Hash: {target_hash[:40]}...{C.END}")
    print(f"    {C.WHITE}Algo: {algorithm} | Charset: {len(charset)} chars | Longueur: {min_len}-{max_len}{C.END}")
    
    # Calculer le nombre de combinaisons
    total_combos = sum(len(charset) ** i for i in range(min_len, max_len + 1))
    print(f"    {C.YELLOW}⚠️ Combinaisons possibles: {total_combos:,}{C.END}\n")
    
    if total_combos > 100000000:
        print(f"    {C.RED}⚠️ ATTENTION: Cela peut prendre des heures/jours!{C.END}")
        confirm = input(f"    Continuer? (oui/non): ").strip().lower()
        if confirm != "oui":
            return None
    
    start_time = time.time()
    found = None
    tested = 0
    
    for length in range(min_len, max_len + 1):
        if found:
            break
        
        print(f"    {C.CYAN}Longueur {length}...{C.END}")
        
        for combo in itertools.product(charset, repeat=length):
            pwd = ''.join(combo)
            tested += 1
            
            if show_progress and tested % 10000 == 0:
                elapsed = time.time() - start_time
                speed = tested / (elapsed + 0.001)
                pct = tested / total_combos * 100
                bar = "█" * int(pct // 5) + "░" * (20 - int(pct // 5))
                print(f"\r    [{bar}] {pct:.1f}% | {speed:.0f} pwd/s | Test: {pwd:<10}", end="", flush=True)
            
            if verify_hash(pwd, target_hash, algorithm):
                found = pwd
                break
    
    elapsed = time.time() - start_time
    
    if found:
        print(f"\r    {C.GREEN}{'█' * 20} TROUVÉ!{C.END}                                ")
        print(f"\n    {C.GREEN}✓ MOT DE PASSE TROUVÉ!{C.END}")
        print(f"    {C.BOLD}{C.GREEN}→ {found}{C.END}")
        print(f"    {C.WHITE}Testé: {tested:,} combinaisons en {elapsed:.2f}s{C.END}")
    else:
        print(f"\r    {C.RED}✗ Non trouvé après {tested:,} essais ({elapsed:.2f}s){C.END}")
    
    return found

def rule_based_attack(target_hash, algorithm, base_words):
    """Attaque avec règles de mutation"""
    
    print(f"\n    {C.CYAN}🎯 Attaque avec règles de mutation{C.END}")
    print(f"    {C.WHITE}Mots de base: {len(base_words)}{C.END}\n")
    
    mutations = []
    
    for word in base_words:
        # Original
        mutations.append(word)
        
        # Majuscule
        mutations.append(word.upper())
        mutations.append(word.capitalize())
        
        # Leet speak
        leet = word.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '$')
        mutations.append(leet)
        
        # Avec chiffres
        for i in range(100):
            mutations.append(f"{word}{i}")
            mutations.append(f"{i}{word}")
        
        # Caractères spéciaux
        for char in ['!', '@', '#', '$', '*', '123', '!@#']:
            mutations.append(f"{word}{char}")
            mutations.append(f"{char}{word}")
        
        # Double
        mutations.append(word * 2)
        
        # Inversé
        mutations.append(word[::-1])
        
        # Avec années
        for year in range(1980, 2026):
            mutations.append(f"{word}{year}")
    
    print(f"    {C.WHITE}Mutations générées: {len(mutations):,}{C.END}\n")
    
    return dictionary_attack(target_hash, algorithm, mutations)

def hybrid_attack(target_hash, algorithm, wordlist=None):
    """Attaque hybride: dictionnaire + mutations + brute force court"""
    
    print(f"\n{C.CYAN}{'═' * 60}{C.END}")
    print(f"{C.BOLD}{C.CYAN}🔥 ATTAQUE HYBRIDE{C.END}")
    print(f"{C.CYAN}{'═' * 60}{C.END}")
    
    # Phase 1: Dictionnaire rapide
    print(f"\n    {C.YELLOW}Phase 1: Dictionnaire commun...{C.END}")
    result = dictionary_attack(target_hash, algorithm, show_progress=False)
    if result:
        return result
    
    # Phase 2: Mutations
    print(f"\n    {C.YELLOW}Phase 2: Mutations courantes...{C.END}")
    result = rule_based_attack(target_hash, algorithm, COMMON_PASSWORDS[:50])
    if result:
        return result
    
    # Phase 3: Brute force court (1-4 chars)
    print(f"\n    {C.YELLOW}Phase 3: Force brute (1-4 caractères)...{C.END}")
    result = brute_force_attack(target_hash, algorithm, max_len=4, show_progress=False)
    if result:
        return result
    
    print(f"\n    {C.RED}✗ Mot de passe résistant à l'attaque hybride{C.END}")
    return None

# ═══════════════════════════════════════════════════════════════════════════════
# GÉNÉRATEUR DE WORDLIST
# ═══════════════════════════════════════════════════════════════════════════════

def generate_wordlist(base_info, filename=None):
    """Génère une wordlist personnalisée basée sur des informations"""
    
    print(f"\n    {C.CYAN}📝 Génération de wordlist personnalisée...{C.END}\n")
    
    words = set()
    
    # Infos de base
    name = base_info.get('name', '').lower()
    surname = base_info.get('surname', '').lower()
    birthdate = base_info.get('birthdate', '')  # format: DDMMYYYY
    pet = base_info.get('pet', '').lower()
    city = base_info.get('city', '').lower()
    phone = base_info.get('phone', '')
    
    base_words = [name, surname, pet, city]
    base_words = [w for w in base_words if w]
    
    for word in base_words:
        # Original et variantes
        words.add(word)
        words.add(word.capitalize())
        words.add(word.upper())
        
        # Avec date de naissance
        if birthdate:
            words.add(f"{word}{birthdate}")
            words.add(f"{word}{birthdate[:4]}")  # DDMM
            words.add(f"{word}{birthdate[4:]}")  # YYYY
            words.add(f"{birthdate}{word}")
        
        # Combinaisons
        for other in base_words:
            if other != word:
                words.add(f"{word}{other}")
                words.add(f"{word}_{other}")
                words.add(f"{word}.{other}")
        
        # Leet speak
        leet = word.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '$')
        words.add(leet)
        
        # Avec chiffres
        for i in range(1000):
            words.add(f"{word}{i}")
        
        # Avec caractères spéciaux
        for char in ['!', '@', '#', '$', '*', '123', '!@#', '2024', '2025']:
            words.add(f"{word}{char}")
    
    # Téléphone
    if phone:
        words.add(phone)
        words.add(phone[-4:])
        words.add(phone[-6:])
    
    # Années communes
    for year in range(1980, 2026):
        for word in base_words:
            words.add(f"{word}{year}")
    
    wordlist = sorted(list(words))
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = WORDLIST_DIR / f"custom_wordlist_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(wordlist))
    
    print(f"    {C.GREEN}✓ Wordlist générée: {len(wordlist):,} mots{C.END}")
    print(f"    {C.GREEN}✓ Fichier: {filename}{C.END}")
    
    return filename, wordlist

def download_wordlist(name="rockyou"):
    """Télécharge une wordlist connue"""
    
    wordlists = {
        "rockyou": "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt",
        "common": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt",
    }
    
    if name not in wordlists:
        print(f"    {C.RED}Wordlist '{name}' non disponible{C.END}")
        return None
    
    print(f"    {C.CYAN}📥 Téléchargement de {name}...{C.END}")
    
    try:
        import urllib.request
        url = wordlists[name]
        filename = WORDLIST_DIR / f"{name}.txt"
        urllib.request.urlretrieve(url, filename)
        print(f"    {C.GREEN}✓ Téléchargé: {filename}{C.END}")
        return filename
    except Exception as e:
        print(f"    {C.RED}Erreur: {e}{C.END}")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def hash_text(text, algorithm="MD5"):
    """Hash un texte"""
    result = hash_password(text, algorithm)
    print(f"\n    {C.WHITE}Texte: {text}{C.END}")
    print(f"    {C.GREEN}{algorithm}: {result}{C.END}")
    return result

def analyze_password_strength(password):
    """Analyse la force d'un mot de passe"""
    
    print(f"\n    {C.CYAN}🔐 Analyse du mot de passe: {password}{C.END}\n")
    
    score = 0
    feedback = []
    
    # Longueur
    length = len(password)
    if length < 6:
        feedback.append(f"{C.RED}✗ Trop court (<6 caractères){C.END}")
    elif length < 8:
        feedback.append(f"{C.YELLOW}⚠ Court (6-7 caractères){C.END}")
        score += 1
    elif length < 12:
        feedback.append(f"{C.GREEN}✓ Bonne longueur (8-11 caractères){C.END}")
        score += 2
    else:
        feedback.append(f"{C.GREEN}✓ Excellente longueur (12+ caractères){C.END}")
        score += 3
    
    # Minuscules
    if any(c.islower() for c in password):
        feedback.append(f"{C.GREEN}✓ Contient des minuscules{C.END}")
        score += 1
    else:
        feedback.append(f"{C.RED}✗ Pas de minuscules{C.END}")
    
    # Majuscules
    if any(c.isupper() for c in password):
        feedback.append(f"{C.GREEN}✓ Contient des majuscules{C.END}")
        score += 1
    else:
        feedback.append(f"{C.YELLOW}⚠ Pas de majuscules{C.END}")
    
    # Chiffres
    if any(c.isdigit() for c in password):
        feedback.append(f"{C.GREEN}✓ Contient des chiffres{C.END}")
        score += 1
    else:
        feedback.append(f"{C.YELLOW}⚠ Pas de chiffres{C.END}")
    
    # Caractères spéciaux
    if any(c in string.punctuation for c in password):
        feedback.append(f"{C.GREEN}✓ Contient des caractères spéciaux{C.END}")
        score += 2
    else:
        feedback.append(f"{C.YELLOW}⚠ Pas de caractères spéciaux{C.END}")
    
    # Patterns communs
    if password.lower() in COMMON_PASSWORDS:
        feedback.append(f"{C.RED}✗ MOT DE PASSE COMMUN - TRÈS DANGEREUX!{C.END}")
        score = 0
    
    # Séquences
    sequences = ['123', '234', '345', 'abc', 'bcd', 'qwerty', 'azerty']
    if any(seq in password.lower() for seq in sequences):
        feedback.append(f"{C.YELLOW}⚠ Contient des séquences prévisibles{C.END}")
        score -= 1
    
    # Score final
    if score <= 2:
        strength = f"{C.RED}FAIBLE{C.END}"
        crack_time = "Quelques secondes"
    elif score <= 4:
        strength = f"{C.YELLOW}MOYEN{C.END}"
        crack_time = "Quelques heures"
    elif score <= 6:
        strength = f"{C.GREEN}FORT{C.END}"
        crack_time = "Quelques jours"
    else:
        strength = f"{C.GREEN}TRÈS FORT{C.END}"
        crack_time = "Années/Impossible"
    
    print(f"    Force: {strength}")
    print(f"    Temps de crack estimé: {crack_time}\n")
    
    for fb in feedback:
        print(f"    {fb}")
    
    return score

def generate_secure_password(length=16):
    """Génère un mot de passe sécurisé"""
    import secrets
    
    # Assurer au moins un de chaque type
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*()_+-=")
    ]
    
    # Remplir le reste
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    password.extend(secrets.choice(all_chars) for _ in range(length - 4))
    
    # Mélanger
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

# ═══════════════════════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                     🔓 PASSWORD CRACKER v2.0 🔓                              ║
╚══════════════════════════════════════════════════════════════════════════════╝{C.END}
    """)

def show_menu():
    print(f"""
    {C.CYAN}┌────────────────────────────────────────────────────────────────────┐
    │  {C.BOLD}🔓 CRACKER DE HASH{C.END}{C.CYAN}                                              │
    ├────────────────────────────────────────────────────────────────────┤
    │  [1] Identifier un hash                                            │
    │  [2] Attaque dictionnaire                                          │
    │  [3] Attaque force brute                                           │
    │  [4] Attaque avec règles (mutations)                               │
    │  [5] Attaque hybride (auto)                                        │
    ├────────────────────────────────────────────────────────────────────┤
    │  {C.BOLD}📝 WORDLISTS{C.END}{C.CYAN}                                                     │
    ├────────────────────────────────────────────────────────────────────┤
    │  [6] Générer wordlist personnalisée                                │
    │  [7] Télécharger wordlist (rockyou)                                │
    ├────────────────────────────────────────────────────────────────────┤
    │  {C.BOLD}🔧 UTILITAIRES{C.END}{C.CYAN}                                                   │
    ├────────────────────────────────────────────────────────────────────┤
    │  [8] Hasher un texte                                               │
    │  [9] Analyser force d'un mot de passe                              │
    │  [10] Générer mot de passe sécurisé                                │
    ├────────────────────────────────────────────────────────────────────┤
    │  [0] Quitter                                                       │
    └────────────────────────────────────────────────────────────────────┘{C.END}
    """)

def main():
    print_banner()
    
    while True:
        show_menu()
        choice = input(f"\n    {C.GREEN}👉 Choix: {C.END}").strip()
        
        try:
            if choice == "1":
                hash_str = input("    Hash à identifier: ").strip()
                types = identify_hash(hash_str)
                print(f"\n    {C.CYAN}Type(s) probable(s): {', '.join(types)}{C.END}")
            
            elif choice == "2":
                hash_str = input("    Hash à cracker: ").strip()
                algo = input("    Algorithme (MD5/SHA1/SHA256/NTLM) [MD5]: ").strip().upper() or "MD5"
                wordlist_path = input("    Wordlist (vide = communs): ").strip()
                
                if wordlist_path:
                    dictionary_attack(hash_str, algo, wordlist_path)
                else:
                    dictionary_attack(hash_str, algo)
            
            elif choice == "3":
                hash_str = input("    Hash à cracker: ").strip()
                algo = input("    Algorithme [MD5]: ").strip().upper() or "MD5"
                max_len = int(input("    Longueur max [4]: ").strip() or "4")
                
                brute_force_attack(hash_str, algo, max_len=max_len)
            
            elif choice == "4":
                hash_str = input("    Hash à cracker: ").strip()
                algo = input("    Algorithme [MD5]: ").strip().upper() or "MD5"
                words = input("    Mots de base (séparés par virgule): ").strip().split(',')
                
                rule_based_attack(hash_str, algo, [w.strip() for w in words])
            
            elif choice == "5":
                hash_str = input("    Hash à cracker: ").strip()
                algo = input("    Algorithme [MD5]: ").strip().upper() or "MD5"
                
                hybrid_attack(hash_str, algo)
            
            elif choice == "6":
                print("\n    📝 Informations pour générer la wordlist:")
                info = {
                    'name': input("    Prénom: ").strip(),
                    'surname': input("    Nom: ").strip(),
                    'birthdate': input("    Date de naissance (DDMMYYYY): ").strip(),
                    'pet': input("    Nom animal de compagnie: ").strip(),
                    'city': input("    Ville: ").strip(),
                    'phone': input("    Téléphone: ").strip(),
                }
                generate_wordlist(info)
            
            elif choice == "7":
                download_wordlist("rockyou")
            
            elif choice == "8":
                text = input("    Texte à hasher: ").strip()
                algo = input("    Algorithme [MD5]: ").strip().upper() or "MD5"
                hash_text(text, algo)
            
            elif choice == "9":
                password = input("    Mot de passe à analyser: ").strip()
                analyze_password_strength(password)
            
            elif choice == "10":
                length = int(input("    Longueur [16]: ").strip() or "16")
                pwd = generate_secure_password(length)
                print(f"\n    {C.GREEN}🔐 Mot de passe généré:{C.END}")
                print(f"    {C.BOLD}{C.CYAN}{pwd}{C.END}")
                analyze_password_strength(pwd)
            
            elif choice == "0":
                print(f"\n    {C.YELLOW}👋 Au revoir!{C.END}\n")
                break
            
            else:
                print(f"    {C.RED}Option invalide{C.END}")
        
        except KeyboardInterrupt:
            print(f"\n    {C.YELLOW}Interrompu{C.END}")
        except Exception as e:
            print(f"    {C.RED}Erreur: {e}{C.END}")
        
        input(f"\n    {C.CYAN}⏎ Entrée pour continuer...{C.END}")

if __name__ == "__main__":
    main()
