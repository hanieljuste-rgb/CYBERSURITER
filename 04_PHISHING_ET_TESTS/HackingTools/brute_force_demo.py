#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║              BRUTE FORCE - DÉMONSTRATION                         ║
║                                                                  ║
║  ⚠️  USAGE ÉDUCATIF - NE PAS UTILISER SUR DES COMPTES RÉELS ⚠️   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import hashlib
import time
import itertools
import string
from datetime import datetime

def hash_password(password, algorithm='sha256'):
    """Hasher un mot de passe"""
    return hashlib.new(algorithm, password.encode()).hexdigest()

def dictionary_attack(target_hash, wordlist, algorithm='sha256'):
    """Attaque par dictionnaire"""
    print("\n📚 ATTAQUE PAR DICTIONNAIRE")
    print("-" * 50)
    
    attempts = 0
    start_time = time.time()
    
    for word in wordlist:
        attempts += 1
        word = word.strip()
        test_hash = hash_password(word, algorithm)
        
        if attempts % 1000 == 0:
            print(f"\r   Tentatives: {attempts:,} | Dernier test: {word[:20]:<20}", end="", flush=True)
        
        if test_hash == target_hash:
            elapsed = time.time() - start_time
            print(f"\n\n   ✅ MOT DE PASSE TROUVÉ: {word}")
            print(f"   ⏱️  Temps: {elapsed:.2f} secondes")
            print(f"   🔢 Tentatives: {attempts:,}")
            return word
    
    elapsed = time.time() - start_time
    print(f"\n\n   ❌ Non trouvé après {attempts:,} tentatives ({elapsed:.2f}s)")
    return None

def brute_force_attack(target_hash, charset, max_length=6, algorithm='sha256'):
    """Attaque par force brute"""
    print(f"\n🔨 ATTAQUE PAR FORCE BRUTE (max {max_length} caractères)")
    print(f"   Charset: {charset[:30]}{'...' if len(charset) > 30 else ''}")
    print("-" * 50)
    
    attempts = 0
    start_time = time.time()
    
    for length in range(1, max_length + 1):
        print(f"\n   📏 Test longueur {length}...")
        combinations = len(charset) ** length
        print(f"      Combinaisons possibles: {combinations:,}")
        
        for combo in itertools.product(charset, repeat=length):
            attempts += 1
            password = ''.join(combo)
            test_hash = hash_password(password, algorithm)
            
            if attempts % 10000 == 0:
                elapsed = time.time() - start_time
                speed = attempts / elapsed if elapsed > 0 else 0
                print(f"\r      Test: {password:<10} | {attempts:,} essais | {speed:.0f}/sec", end="", flush=True)
            
            if test_hash == target_hash:
                elapsed = time.time() - start_time
                print(f"\n\n   ✅ MOT DE PASSE TROUVÉ: {password}")
                print(f"   ⏱️  Temps: {elapsed:.2f} secondes")
                print(f"   🔢 Tentatives: {attempts:,}")
                return password
    
    elapsed = time.time() - start_time
    print(f"\n\n   ❌ Non trouvé après {attempts:,} tentatives ({elapsed:.2f}s)")
    return None

def simulate_online_attack():
    """Simuler une attaque en ligne (avec délai)"""
    print("\n🌐 SIMULATION ATTAQUE EN LIGNE (avec rate limiting)")
    print("-" * 50)
    
    # Mots de passe communs
    common_passwords = [
        "123456", "password", "123456789", "12345678", "12345",
        "1234567", "qwerty", "abc123", "password1", "1234567890",
        "admin", "letmein", "welcome", "monkey", "dragon",
        "master", "login", "princess", "solo", "passw0rd"
    ]
    
    target_password = "dragon"
    print(f"   🎯 Mot de passe cible (secret): {target_password}")
    print(f"   ⏱️  Délai entre essais: 0.5s (simule rate limiting)")
    print()
    
    for i, pwd in enumerate(common_passwords, 1):
        print(f"   [{i:02d}] Test: {pwd:<15}", end="")
        time.sleep(0.3)  # Simuler délai réseau
        
        if pwd == target_password:
            print("✅ SUCCÈS!")
            print(f"\n   🎉 Accès obtenu avec: {pwd}")
            return pwd
        else:
            print("❌")
    
    print("\n   Échec de l'attaque")
    return None

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              🔓 BRUTE FORCE - DÉMONSTRATION                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Le brute force teste toutes les combinaisons possibles          ║
║  pour trouver un mot de passe.                                   ║
║                                                                  ║
║  🎯 TYPES D'ATTAQUES:                                            ║
║     1. Dictionnaire - Utilise une liste de mots communs          ║
║     2. Force brute - Teste toutes les combinaisons               ║
║     3. Hybride - Combine les deux méthodes                       ║
║                                                                  ║
║  🛡️ PROTECTIONS:                                                 ║
║     - Rate limiting (délai entre essais)                         ║
║     - CAPTCHA après X échecs                                     ║
║     - Blocage de compte temporaire                               ║
║     - 2FA (même avec le mot de passe, bloqué)                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Menu
    print("📋 CHOISISSEZ UNE DÉMO:\n")
    print("   1. Attaque par dictionnaire (hash)")
    print("   2. Attaque force brute (hash)")  
    print("   3. Simulation attaque en ligne")
    print("   4. Comparer temps de crack selon complexité")
    print("   0. Quitter")
    
    choice = input("\n🎯 Votre choix: ").strip()
    
    if choice == "1":
        # Attaque dictionnaire
        password_to_crack = input("\nEntrez un mot de passe simple à craquer (ex: dragon): ").strip()
        if not password_to_crack:
            password_to_crack = "dragon"
        
        target_hash = hash_password(password_to_crack)
        print(f"\n🔐 Hash SHA256: {target_hash}")
        
        # Wordlist simple
        wordlist = [
            "password", "123456", "admin", "letmein", "welcome",
            "monkey", "dragon", "master", "qwerty", "login",
            "password1", "abc123", "111111", "mustang", "access",
            "shadow", "michael", "superman", "batman", "trustno1"
        ]
        
        dictionary_attack(target_hash, wordlist)
        
    elif choice == "2":
        # Force brute
        password_to_crack = input("\nEntrez un mot de passe COURT à craquer (max 4 chars, ex: abc): ").strip()
        if not password_to_crack:
            password_to_crack = "abc"
        
        if len(password_to_crack) > 4:
            print("⚠️ Trop long! Limité à 4 caractères pour la démo.")
            password_to_crack = password_to_crack[:4]
        
        target_hash = hash_password(password_to_crack)
        print(f"\n🔐 Hash SHA256: {target_hash}")
        
        # Déterminer le charset
        if password_to_crack.isdigit():
            charset = string.digits
        elif password_to_crack.isalpha():
            charset = string.ascii_lowercase
        else:
            charset = string.ascii_lowercase + string.digits
        
        brute_force_attack(target_hash, charset, max_length=len(password_to_crack))
        
    elif choice == "3":
        simulate_online_attack()
        
    elif choice == "4":
        print("\n⏱️ TEMPS ESTIMÉ POUR CRAQUER DIFFÉRENTS MOTS DE PASSE")
        print("-" * 60)
        print(f"{'Type':<30} {'Combinaisons':<15} {'Temps (10M/s)'}")
        print("-" * 60)
        
        tests = [
            ("4 chiffres (PIN)", 10**4),
            ("6 chiffres", 10**6),
            ("8 lettres minuscules", 26**8),
            ("8 alphanumérique", 62**8),
            ("8 + symboles", 95**8),
            ("12 alphanumérique", 62**12),
            ("16 alphanumérique", 62**16),
        ]
        
        for name, combos in tests:
            seconds = combos / 10_000_000  # 10 million/sec
            if seconds < 1:
                time_str = "< 1 seconde"
            elif seconds < 60:
                time_str = f"{seconds:.1f} secondes"
            elif seconds < 3600:
                time_str = f"{seconds/60:.1f} minutes"
            elif seconds < 86400:
                time_str = f"{seconds/3600:.1f} heures"
            elif seconds < 31536000:
                time_str = f"{seconds/86400:.1f} jours"
            elif seconds < 31536000 * 1000:
                time_str = f"{seconds/31536000:.0f} années"
            else:
                time_str = f"{seconds/31536000:.2e} années"
            
            print(f"{name:<30} {combos:<15,} {time_str}")
        
        print("-" * 60)
        print("\n💡 CONCLUSION: Un mot de passe de 12+ caractères avec")
        print("   lettres, chiffres et symboles est quasi-incassable!")
    
    print("\n" + "=" * 60)
    print("🎓 LEÇONS APPRISES:")
    print("=" * 60)
    print("""
   1. Les mots de passe courts sont craqués instantanément
   2. Les mots du dictionnaire sont vulnérables
   3. La complexité augmente le temps exponentiellement
   4. Utilisez un gestionnaire de mots de passe!
   5. Activez toujours la 2FA!
    """)

if __name__ == "__main__":
    main()
