#!/usr/bin/env python3
"""
🏁 CTF Practice - Exercices Capture The Flag
Challenges d'entraînement pour apprendre le hacking
"""

import os
import sys
import hashlib
import base64
import binascii
import random
import string

class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
    B = '\033[94m'; M = '\033[95m'; C = '\033[96m'
    W = '\033[97m'; X = '\033[0m'; BOLD = '\033[1m'

# Flags secrets (en réalité ils seraient cachés)
FLAGS = {
    1: "FLAG{b4s3_64_d3c0d3d}",
    2: "FLAG{h3x_1s_e4sy}",
    3: "FLAG{r0t13_cl4ss1c}",
    4: "FLAG{md5_cr4ck3d}",
    5: "FLAG{sql_1nj3ct10n_m4st3r}",
    6: "FLAG{x0r_cyph3r_k1ng}",
    7: "FLAG{b1n4ry_r34d3r}",
    8: "FLAG{st3g4n0_h1dd3n}",
}

def banner():
    print(f"""
{C.C}{C.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║              🏁 CTF PRACTICE - CHALLENGES                     ║
╠═══════════════════════════════════════════════════════════════╣
║  Exercices pour apprendre le hacking de manière ludique       ║
╚═══════════════════════════════════════════════════════════════╝
{C.X}
{C.Y}Trouvez les flags cachés dans chaque challenge !{C.X}
{C.C}Format: FLAG{{...}}{C.X}
""")

def menu():
    print(f"""
{C.BOLD}═══════════════════════════════════════════════════════════════
                      CHALLENGES CTF
═══════════════════════════════════════════════════════════════{C.X}

  {C.G}[ CRYPTO ]{C.X}
  {C.C}[1]{C.X}  🔤 Base64 Decode - Niveau Facile
  {C.C}[2]{C.X}  🔢 Hexadecimal - Niveau Facile
  {C.C}[3]{C.X}  🔄 ROT13 - Niveau Facile
  {C.C}[4]{C.X}  #️⃣ Hash Cracking - Niveau Moyen
  {C.C}[5]{C.X}  ⊕ XOR Cipher - Niveau Moyen
  {C.C}[6]{C.X}  💻 Binary - Niveau Moyen
  
  {C.G}[ WEB ]{C.X}
  {C.C}[7]{C.X}  💉 SQL Injection Quiz
  {C.C}[8]{C.X}  🕸️ XSS Challenge
  
  {C.G}[ MISC ]{C.X}
  {C.C}[9]{C.X}  📂 Steganography Basics
  {C.C}[10]{C.X} 🔎 OSINT Challenge
  
  {C.Y}[S]{C.X}  📊 Voir mon score
  {C.R}[0]{C.X}  Retour au menu principal
""")

# Stockage des flags trouvés
found_flags = set()

def check_flag(challenge_num, user_input):
    """Vérifie si le flag est correct"""
    correct_flag = FLAGS.get(challenge_num, "")
    if user_input.strip().upper() == correct_flag.upper() or user_input.strip() == correct_flag:
        found_flags.add(challenge_num)
        print(f"\n{C.G}🎉 CORRECT ! Vous avez trouvé le flag !{C.X}")
        print(f"{C.G}Flag: {correct_flag}{C.X}")
        return True
    else:
        print(f"\n{C.R}❌ Incorrect. Essayez encore !{C.X}")
        return False

def challenge_base64():
    """Challenge Base64"""
    print(f"\n{C.C}═══ CHALLENGE 1: BASE64 DECODE ═══{C.X}")
    print(f"{C.Y}Niveau: Facile{C.X}\n")
    
    # Flag encodé en base64
    encoded = base64.b64encode(FLAGS[1].encode()).decode()
    
    print(f"Décodez ce message Base64 pour trouver le flag:\n")
    print(f"{C.M}{encoded}{C.X}\n")
    
    print(f"{C.Y}Indice: Utilisez un décodeur Base64 ou Python:{C.X}")
    print(f"{C.C}import base64; print(base64.b64decode('...').decode()){C.X}\n")
    
    answer = input(f"{C.G}Votre réponse (FLAG{{...}}) : {C.X}")
    check_flag(1, answer)

def challenge_hex():
    """Challenge Hexadecimal"""
    print(f"\n{C.C}═══ CHALLENGE 2: HEXADECIMAL ═══{C.X}")
    print(f"{C.Y}Niveau: Facile{C.X}\n")
    
    # Flag en hex
    hex_encoded = binascii.hexlify(FLAGS[2].encode()).decode()
    
    print(f"Convertissez cet hexadécimal en texte:\n")
    print(f"{C.M}{hex_encoded}{C.X}\n")
    
    print(f"{C.Y}Indice: bytes.fromhex('...').decode(){C.X}\n")
    
    answer = input(f"{C.G}Votre réponse : {C.X}")
    check_flag(2, answer)

def challenge_rot13():
    """Challenge ROT13"""
    print(f"\n{C.C}═══ CHALLENGE 3: ROT13 ═══{C.X}")
    print(f"{C.Y}Niveau: Facile{C.X}\n")
    
    # ROT13 du flag
    def rot13(text):
        result = ""
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + 13) % 26 + base)
            else:
                result += char
        return result
    
    encoded = rot13(FLAGS[3])
    
    print(f"Déchiffrez ce message ROT13:\n")
    print(f"{C.M}{encoded}{C.X}\n")
    
    print(f"{C.Y}Indice: ROT13 est son propre inverse (appliquez ROT13 deux fois = texte original){C.X}\n")
    
    answer = input(f"{C.G}Votre réponse : {C.X}")
    check_flag(3, answer)

def challenge_hash():
    """Challenge Hash Cracking"""
    print(f"\n{C.C}═══ CHALLENGE 4: HASH CRACKING ═══{C.X}")
    print(f"{C.Y}Niveau: Moyen{C.X}\n")
    
    # Hash MD5 du flag
    hash_md5 = hashlib.md5(FLAGS[4].encode()).hexdigest()
    
    print(f"Trouvez le texte original de ce hash MD5:\n")
    print(f"{C.M}{hash_md5}{C.X}\n")
    
    print(f"{C.Y}Indice: Le flag est au format FLAG{{...}}{C.X}")
    print(f"{C.Y}Indice 2: Essayez crackstation.net ou hashcat{C.X}\n")
    
    # Donner plus d'indices
    print(f"{C.C}Le mot dans le flag ressemble à 'md5_cr4ck3d'{C.X}\n")
    
    answer = input(f"{C.G}Votre réponse : {C.X}")
    check_flag(4, answer)

def challenge_xor():
    """Challenge XOR"""
    print(f"\n{C.C}═══ CHALLENGE 5: XOR CIPHER ═══{C.X}")
    print(f"{C.Y}Niveau: Moyen{C.X}\n")
    
    key = 42  # Clé XOR simple
    flag = FLAGS[6]
    
    # XOR chaque caractère
    xored = [ord(c) ^ key for c in flag]
    
    print(f"Déchiffrez ce message XOR (clé = {key}):\n")
    print(f"{C.M}{xored}{C.X}\n")
    
    print(f"{C.Y}Indice: Pour chaque nombre, faites XOR avec la clé{C.X}")
    print(f"{C.C}chr(nombre ^ {key}) pour chaque nombre{C.X}\n")
    
    answer = input(f"{C.G}Votre réponse : {C.X}")
    check_flag(6, answer)

def challenge_binary():
    """Challenge Binary"""
    print(f"\n{C.C}═══ CHALLENGE 6: BINARY ═══{C.X}")
    print(f"{C.Y}Niveau: Moyen{C.X}\n")
    
    # Flag en binaire
    binary = ' '.join(format(ord(c), '08b') for c in FLAGS[7])
    
    print(f"Convertissez ce binaire en texte:\n")
    print(f"{C.M}{binary}{C.X}\n")
    
    print(f"{C.Y}Indice: Chaque groupe de 8 bits = 1 caractère ASCII{C.X}\n")
    
    answer = input(f"{C.G}Votre réponse : {C.X}")
    check_flag(7, answer)

def challenge_sql():
    """Quiz SQL Injection"""
    print(f"\n{C.C}═══ CHALLENGE 7: SQL INJECTION QUIZ ═══{C.X}")
    print(f"{C.Y}Niveau: Moyen{C.X}\n")
    
    print(f"""
Vous avez trouvé un formulaire de login vulnérable.
La requête SQL est:
{C.M}SELECT * FROM users WHERE username='$user' AND password='$pass'{C.X}

Question: Quel payload permet de bypasser l'authentification?

  {C.C}[A]{C.X} admin' --
  {C.C}[B]{C.X} admin'; DROP TABLE users;--
  {C.C}[C]{C.X} ' OR '1'='1
  {C.C}[D]{C.X} Toutes les réponses ci-dessus

""")
    
    answer = input(f"{C.G}Votre réponse (A/B/C/D) : {C.X}").upper()
    
    if answer == 'D':
        print(f"\n{C.G}🎉 CORRECT !{C.X}")
        print(f"Toutes ces injections peuvent fonctionner dans différents contextes.")
        print(f"\n{C.G}Flag: {FLAGS[5]}{C.X}")
        found_flags.add(5)
    else:
        print(f"\n{C.Y}Pas tout à fait. La bonne réponse est D.{C.X}")
        print(f"Toutes ces techniques sont des SQL injections valides !")

def challenge_stego():
    """Bases de la stéganographie"""
    print(f"\n{C.C}═══ CHALLENGE 9: STEGANOGRAPHY ═══{C.X}")
    print(f"{C.Y}Niveau: Moyen{C.X}\n")
    
    print(f"""
La stéganographie consiste à cacher des informations dans d'autres fichiers.

{C.BOLD}Techniques courantes:{C.X}
• Cacher du texte dans les métadonnées d'images (EXIF)
• Cacher des données dans les bits de poids faible (LSB)
• Cacher des fichiers dans d'autres fichiers (file carving)

{C.BOLD}Outils à connaître:{C.X}
• {C.G}steghide{C.X} - Cache/extrait des données dans images
• {C.G}exiftool{C.X} - Lit les métadonnées
• {C.G}binwalk{C.X} - Analyse les fichiers embedded
• {C.G}strings{C.X} - Extrait les strings d'un fichier
• {C.G}zsteg{C.X} - Analyse stégo pour PNG

{C.BOLD}Challenge:{C.X}
Le flag est caché dans ce texte. Regardez les premières lettres de chaque mot:

{C.M}Flag Lasts As Great, Staying Tough, Etching Good And Nice, Overcoming Hidden, Invisible, Doubting, Dangerous, Endings, Now.{C.X}
""")
    
    answer = input(f"\n{C.G}Quel est le flag caché ? : {C.X}")
    if "FLAG" in answer.upper() and "HIDDEN" in answer.upper():
        print(f"\n{C.G}🎉 Vous avez compris le principe !{C.X}")
        print(f"{C.G}Flag: {FLAGS[8]}{C.X}")
        found_flags.add(8)
    else:
        print(f"\n{C.Y}Indice: Lisez la première lettre de chaque mot...{C.X}")

def show_score():
    """Affiche le score actuel"""
    print(f"\n{C.C}═══ VOTRE SCORE ═══{C.X}\n")
    
    total = len(FLAGS)
    found = len(found_flags)
    
    print(f"{C.G}Flags trouvés: {found}/{total}{C.X}\n")
    
    for num in range(1, total + 1):
        if num in found_flags:
            print(f"  {C.G}[✓] Challenge {num}: {FLAGS[num]}{C.X}")
        else:
            print(f"  {C.R}[✗] Challenge {num}: ???{C.X}")
    
    percentage = (found / total) * 100
    print(f"\n{C.Y}Progression: {percentage:.0f}%{C.X}")
    
    if found == total:
        print(f"\n{C.G}🏆 FÉLICITATIONS ! Vous avez trouvé tous les flags !{C.X}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()
    
    while True:
        menu()
        choice = input(f"\n{C.C}Choisissez un challenge : {C.X}").strip().upper()
        
        if choice == '0':
            break
        elif choice == '1':
            challenge_base64()
        elif choice == '2':
            challenge_hex()
        elif choice == '3':
            challenge_rot13()
        elif choice == '4':
            challenge_hash()
        elif choice == '5':
            challenge_xor()
        elif choice == '6':
            challenge_binary()
        elif choice == '7':
            challenge_sql()
        elif choice == '8':
            print(f"\n{C.Y}[!] XSS Challenge - Utilisez DVWA ou PortSwigger Academy{C.X}")
        elif choice == '9':
            challenge_stego()
        elif choice == '10':
            print(f"\n{C.Y}[!] OSINT - Utilisez TryHackMe 'OSINT' room{C.X}")
        elif choice == 'S':
            show_score()
        else:
            print(f"\n{C.R}[!] Option invalide{C.X}")
        
        input(f"\n{C.Y}Appuyez sur Entrée pour continuer...{C.X}")

if __name__ == "__main__":
    main()
