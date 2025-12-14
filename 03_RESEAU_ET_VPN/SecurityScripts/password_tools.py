#!/usr/bin/env python3
"""
🔐 Password Tools - Outils pour mots de passe
Auteur: Formation Cybersécurité
Usage: python password_tools.py
⚠️ À utiliser uniquement pour tester VOS propres systèmes !
"""

import hashlib
import secrets
import string
import os

class PasswordTools:
    
    @staticmethod
    def generate_password(length=16, use_upper=True, use_lower=True, 
                          use_digits=True, use_special=True):
        """Génère un mot de passe sécurisé"""
        chars = ""
        if use_lower:
            chars += string.ascii_lowercase
        if use_upper:
            chars += string.ascii_uppercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += string.punctuation
        
        if not chars:
            chars = string.ascii_letters + string.digits
        
        password = ''.join(secrets.choice(chars) for _ in range(length))
        return password
    
    @staticmethod
    def check_password_strength(password):
        """Analyse la force d'un mot de passe"""
        score = 0
        feedback = []
        
        # Longueur
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("❌ Trop court (min 8 caractères)")
        
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        # Complexité
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("❌ Ajoutez des minuscules")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("❌ Ajoutez des majuscules")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("❌ Ajoutez des chiffres")
        
        if any(c in string.punctuation for c in password):
            score += 1
        else:
            feedback.append("❌ Ajoutez des caractères spéciaux")
        
        # Patterns faibles
        weak_patterns = ['123', 'abc', 'qwerty', 'password', 'azerty']
        if any(p in password.lower() for p in weak_patterns):
            score -= 2
            feedback.append("❌ Contient un pattern faible")
        
        # Résultat
        if score >= 7:
            strength = "🟢 EXCELLENT"
        elif score >= 5:
            strength = "🟡 BON"
        elif score >= 3:
            strength = "🟠 MOYEN"
        else:
            strength = "🔴 FAIBLE"
        
        return {
            'score': max(0, score),
            'max_score': 7,
            'strength': strength,
            'feedback': feedback
        }
    
    @staticmethod
    def hash_password(password, algorithm='sha256'):
        """Hash un mot de passe"""
        algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512
        }
        
        if algorithm not in algorithms:
            raise ValueError(f"Algorithme inconnu: {algorithm}")
        
        return algorithms[algorithm](password.encode()).hexdigest()
    
    @staticmethod
    def hash_all(password):
        """Hash un mot de passe avec tous les algorithmes"""
        return {
            'MD5': hashlib.md5(password.encode()).hexdigest(),
            'SHA1': hashlib.sha1(password.encode()).hexdigest(),
            'SHA256': hashlib.sha256(password.encode()).hexdigest(),
            'SHA512': hashlib.sha512(password.encode()).hexdigest()
        }
    
    @staticmethod
    def crack_hash_wordlist(hash_to_crack, wordlist, algorithm='sha256'):
        """
        Tente de cracker un hash avec une wordlist
        ⚠️ ÉDUCATIF UNIQUEMENT - pour comprendre pourquoi les mots de passe faibles sont dangereux
        """
        algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512
        }
        
        hash_func = algorithms.get(algorithm)
        if not hash_func:
            return None
        
        hash_to_crack = hash_to_crack.lower()
        
        try:
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    word = line.strip()
                    if hash_func(word.encode()).hexdigest().lower() == hash_to_crack:
                        return word
        except FileNotFoundError:
            print(f"❌ Fichier wordlist non trouvé: {wordlist}")
        
        return None
    
    @staticmethod
    def create_sample_wordlist():
        """Crée une wordlist d'exemple pour les tests"""
        common_passwords = [
            "123456", "password", "123456789", "12345678", "12345",
            "1234567", "1234567890", "qwerty", "abc123", "111111",
            "123123", "admin", "letmein", "welcome", "monkey",
            "dragon", "master", "qwertyuiop", "login", "password1",
            "azerty", "soleil", "bonjour", "motdepasse", "france"
        ]
        
        with open("sample_wordlist.txt", "w") as f:
            for pwd in common_passwords:
                f.write(pwd + "\n")
        
        return "sample_wordlist.txt"


def menu():
    """Menu interactif"""
    tools = PasswordTools()
    
    while True:
        print("\n" + "="*50)
        print("🔐 PASSWORD TOOLS - Menu Principal")
        print("="*50)
        print("1. 🎲 Générer un mot de passe sécurisé")
        print("2. 💪 Vérifier la force d'un mot de passe")
        print("3. #️⃣  Hasher un mot de passe")
        print("4. 🔓 Cracker un hash (éducatif)")
        print("5. 📝 Créer une wordlist d'exemple")
        print("0. ❌ Quitter")
        print("="*50)
        
        choice = input("Choix: ").strip()
        
        if choice == '1':
            print("\n🎲 Génération de mot de passe")
            length = input("Longueur (défaut: 16): ").strip() or "16"
            password = tools.generate_password(int(length))
            print(f"\n✅ Mot de passe généré: {password}")
            
            # Vérifier sa force
            result = tools.check_password_strength(password)
            print(f"   Force: {result['strength']}")
        
        elif choice == '2':
            password = input("\nEntrez le mot de passe à analyser: ")
            result = tools.check_password_strength(password)
            
            print(f"\n📊 Analyse du mot de passe:")
            print(f"   Score: {result['score']}/{result['max_score']}")
            print(f"   Force: {result['strength']}")
            if result['feedback']:
                print("   Conseils:")
                for tip in result['feedback']:
                    print(f"     {tip}")
        
        elif choice == '3':
            password = input("\nMot de passe à hasher: ")
            hashes = tools.hash_all(password)
            
            print("\n#️⃣ Hashes générés:")
            for algo, hash_value in hashes.items():
                print(f"   {algo}: {hash_value}")
        
        elif choice == '4':
            print("\n⚠️ ÉDUCATIF: Ceci démontre pourquoi les mots de passe faibles sont dangereux")
            hash_input = input("Hash à cracker: ").strip()
            algo = input("Algorithme (md5/sha1/sha256/sha512): ").strip() or "sha256"
            wordlist = input("Wordlist (ou Entrée pour créer un exemple): ").strip()
            
            if not wordlist:
                wordlist = tools.create_sample_wordlist()
                print(f"   📝 Wordlist créée: {wordlist}")
            
            print("\n🔍 Recherche en cours...")
            result = tools.crack_hash_wordlist(hash_input, wordlist, algo)
            
            if result:
                print(f"   ✅ TROUVÉ: {result}")
                print("   ⚠️ Ce mot de passe est dans une wordlist commune - CHANGEZ-LE!")
            else:
                print("   ❌ Non trouvé dans la wordlist")
                print("   ✅ Bon signe! (mais ne garantit pas la sécurité)")
        
        elif choice == '5':
            filename = tools.create_sample_wordlist()
            print(f"\n📝 Wordlist créée: {filename}")
            print("   Contient les 25 mots de passe les plus courants")
        
        elif choice == '0':
            print("👋 Au revoir!")
            break
        
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    menu()
