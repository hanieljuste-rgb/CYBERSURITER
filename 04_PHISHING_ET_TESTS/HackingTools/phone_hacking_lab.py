#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           📱 PHONE HACKING LAB - TESTS SUR TON TÉLÉPHONE                     ║
║                                                                              ║
║           Tecno Camon 20 (CK6) - Android 14                                  ║
║                                                                              ║
║  ⚠️  TESTS ÉDUCATIFS SUR TON PROPRE APPAREIL UNIQUEMENT ⚠️                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import subprocess
import os
import time
import json
from datetime import datetime

# Configuration ADB
ADB_PATH = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
BACKUP_DIR = r"C:\Users\davis\OneDrive\Bureau\HACKING\PhoneHackingLab"

def run_adb(command):
    """Exécuter une commande ADB"""
    try:
        result = subprocess.run(
            f'"{ADB_PATH}" {command}',
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Erreur: {e}"

def check_connection():
    """Vérifier la connexion au téléphone"""
    print("\n🔍 Vérification de la connexion...")
    devices = run_adb("devices -l")
    print(devices)
    
    if "device" in devices and "offline" not in devices:
        print("✅ Téléphone connecté!")
        return True
    else:
        print("❌ Téléphone non connecté!")
        print("\n📋 Pour connecter:")
        print("   1. Branche le câble USB")
        print("   2. Accepte la demande sur le téléphone")
        print("   OU")
        print("   1. Active le débogage sans fil")
        print("   2. Note le code et le port")
        return False

def test_1_data_extraction():
    """Test 1: Extraction de données (comme un hacker)"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  TEST 1: EXTRACTION DE DONNÉES                                   ║
║                                                                  ║
║  Ce que fait un hacker quand il a accès physique à ton tel:      ║
║  - Extraire les contacts                                         ║
║  - Copier les photos/vidéos                                      ║
║  - Récupérer les messages                                        ║
║  - Voler les données d'applications                              ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("📊 Informations extraites de ton téléphone:\n")
    
    # Info système
    print("1️⃣ INFORMATIONS SYSTÈME:")
    print("-" * 40)
    model = run_adb("shell getprop ro.product.model")
    android = run_adb("shell getprop ro.build.version.release")
    imei = run_adb("shell service call iphonesubinfo 1 2>/dev/null")
    serial = run_adb("shell getprop ro.serialno")
    
    print(f"   Modèle: {model}")
    print(f"   Android: {android}")
    print(f"   Numéro série: {serial}")
    
    # Comptes
    print("\n2️⃣ COMPTES GOOGLE CONNECTÉS:")
    print("-" * 40)
    accounts = run_adb("shell pm list users")
    print(f"   {accounts}")
    
    # Apps installées
    print("\n3️⃣ APPLICATIONS SENSIBLES DÉTECTÉES:")
    print("-" * 40)
    sensitive_apps = {
        "com.whatsapp": "WhatsApp",
        "com.facebook.katana": "Facebook",
        "com.instagram.android": "Instagram",
        "com.google.android.gm": "Gmail",
        "com.paypal.android.p2pmobile": "PayPal",
        "com.zhiliaoapp.musically": "TikTok",
        "com.twitter.android": "Twitter/X",
        "com.snapchat.android": "Snapchat",
        "com.tinder": "Tinder",
        "com.binance.dev": "Binance",
        "org.telegram.messenger": "Telegram",
    }
    
    packages = run_adb("shell pm list packages")
    found = []
    for pkg, name in sensitive_apps.items():
        if pkg in packages:
            found.append(name)
            print(f"   ✓ {name}")
    
    # WiFi
    print("\n4️⃣ RÉSEAUX WIFI ENREGISTRÉS:")
    print("-" * 40)
    wifi = run_adb('shell cmd wifi list-networks 2>/dev/null || echo "Accès refusé sans root"')
    print(f"   {wifi[:200]}...")
    
    # Emplacement
    print("\n5️⃣ DERNIÈRE POSITION GPS:")
    print("-" * 40)
    location = run_adb('shell dumpsys location | grep "last location" | head -1')
    if location:
        print(f"   {location[:100]}")
    else:
        print("   Position non disponible")
    
    print("\n" + "=" * 60)
    print("🚨 UN HACKER AVEC ACCÈS À TON TÉLÉPHONE PEUT:")
    print("=" * 60)
    print("""
   • Voir tous tes messages WhatsApp/Telegram
   • Accéder à tes photos et vidéos intimes
   • Lire tes emails
   • Voler tes mots de passe enregistrés
   • Suivre ta position GPS
   • Accéder à tes comptes bancaires
   • Usurper ton identité
    """)

def test_2_remote_control():
    """Test 2: Contrôle à distance"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  TEST 2: CONTRÔLE À DISTANCE                                     ║
║                                                                  ║
║  Simulation de ce qu'un hacker peut faire à distance:            ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("🎮 Actions de contrôle à distance:\n")
    
    actions = [
        ("📸 Prendre une capture d'écran", "exec-out screencap -p > screenshot_hack.png"),
        ("📍 Obtenir la position GPS", 'shell dumpsys location | grep -i "last known" | head -3'),
        ("📱 Lister les SMS récents", 'shell content query --uri content://sms/inbox --projection address,body,date --sort "date DESC" 2>/dev/null | head -5'),
        ("📞 Historique d'appels", 'shell content query --uri content://call_log/calls --projection number,name,date,type --sort "date DESC" 2>/dev/null | head -5'),
        ("🔔 Afficher une notification", 'shell am broadcast -a android.intent.action.SHOW_TOAST --es android.intent.extra.TEXT "📱 Ton tel est hacké!" 2>/dev/null'),
        ("📊 Utilisation de la batterie", "shell dumpsys battery"),
    ]
    
    for desc, cmd in actions:
        print(f"\n{desc}:")
        print("-" * 50)
        result = run_adb(cmd)
        print(result[:300] if result else "   Pas d'accès")
        input("\n[Appuyez sur Entrée pour l'action suivante...]")

def test_3_spyware_simulation():
    """Test 3: Simulation de spyware"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  TEST 3: SIMULATION SPYWARE                                      ║
║                                                                  ║
║  Comment un spyware espionne ton téléphone 24/7                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("🕵️ Le spyware collecte ces données en continu:\n")
    
    # Créer un rapport d'espionnage
    spy_report = {
        "timestamp": datetime.now().isoformat(),
        "device_info": {},
        "location": {},
        "activity": {},
        "communications": {}
    }
    
    print("1️⃣ Collecte des infos système...")
    spy_report["device_info"]["model"] = run_adb("shell getprop ro.product.model")
    spy_report["device_info"]["android"] = run_adb("shell getprop ro.build.version.release")
    spy_report["device_info"]["battery"] = run_adb("shell cat /sys/class/power_supply/battery/capacity 2>/dev/null")
    
    print("2️⃣ Récupération de la position...")
    spy_report["location"]["wifi_network"] = run_adb("shell dumpsys wifi | grep 'mWifiInfo' | head -1")
    
    print("3️⃣ Surveillance des activités...")
    spy_report["activity"]["current_app"] = run_adb("shell dumpsys activity activities | grep mResumedActivity | head -1")
    spy_report["activity"]["screen_state"] = run_adb("shell dumpsys power | grep 'Display Power'")
    
    print("4️⃣ Interception des communications...")
    spy_report["communications"]["recent_calls"] = run_adb('shell content query --uri content://call_log/calls --projection number --sort "date DESC" 2>/dev/null | head -3')
    
    print("\n" + "=" * 60)
    print("📄 RAPPORT D'ESPIONNAGE GÉNÉRÉ:")
    print("=" * 60)
    print(json.dumps(spy_report, indent=2, ensure_ascii=False, default=str)[:1000])
    
    print("\n" + "=" * 60)
    print("🚨 UN VRAI SPYWARE FAIT TOUT CELA EN ARRIÈRE-PLAN:")
    print("=" * 60)
    print("""
   • Enregistre tous tes appels
   • Lit tous tes SMS/WhatsApp
   • Prend des photos à ton insu
   • Active le micro pour écouter
   • Suit ta position en temps réel
   • Envoie tout à un serveur distant
   • Se cache pour être indétectable
    """)

def test_4_phishing_to_phone():
    """Test 4: Envoyer un lien de phishing au téléphone"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  TEST 4: PHISHING VIA TÉLÉPHONE                                  ║
║                                                                  ║
║  Envoyer un lien de phishing vers ton téléphone                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    phishing_url = "http://192.168.1.13:8080/"
    
    print(f"🎣 Tentative d'ouvrir le lien de phishing sur ton téléphone...")
    print(f"   URL: {phishing_url}\n")
    
    # Ouvrir l'URL sur le téléphone
    result = run_adb(f'shell am start -a android.intent.action.VIEW -d "{phishing_url}"')
    
    if "Error" not in result:
        print("✅ Lien ouvert sur le téléphone!")
        print("\n🎯 Scénario d'attaque:")
        print("""
   1. Le hacker t'envoie un SMS: "Votre compte TikTok sera supprimé!
      Vérifiez ici: http://tikt0k-secure.com"
      
   2. Tu cliques sur le lien
   
   3. Une fausse page TikTok s'affiche
   
   4. Tu entres tes identifiants
   
   5. Le hacker reçoit tes identifiants en temps réel!
        """)
    else:
        print("❌ Impossible d'ouvrir le lien (serveur non démarré)")
        print("   Lance d'abord le serveur de phishing (option 4 du menu principal)")

def test_5_payload_injection():
    """Test 5: Injection de fichier malveillant"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  TEST 5: INJECTION DE FICHIER MALVEILLANT                        ║
║                                                                  ║
║  Simulation de dépôt d'un fichier malveillant sur ton téléphone  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Créer un faux fichier malveillant (inoffensif)
    fake_malware = """
# SIMULATION - FICHIER MALVEILLANT (INOFFENSIF)
# 
# Si c'était un vrai malware, il pourrait:
# - Installer une porte dérobée
# - Voler tes données
# - Enregistrer tes frappes
# - Activer ta caméra/micro
#
# Ce fichier est une démonstration éducative.
# Créé le: """ + datetime.now().isoformat()
    
    # Créer le fichier local
    malware_path = os.path.join(BACKUP_DIR, "demo_malware.txt")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    with open(malware_path, "w") as f:
        f.write(fake_malware)
    
    print("📤 Dépôt du fichier sur le téléphone...")
    result = run_adb(f'push "{malware_path}" /sdcard/Download/important_update.txt')
    print(result)
    
    # Vérifier
    check = run_adb("shell ls -la /sdcard/Download/important_update.txt")
    
    if "important_update.txt" in check:
        print("\n✅ Fichier 'malveillant' déposé avec succès!")
        print(f"   Emplacement: /sdcard/Download/important_update.txt")
        print("\n🎯 Scénarios réels:")
        print("""
   • APK modifié (TikTok Gold, WhatsApp Plus, etc.)
   • PDF avec exploit
   • Image contenant un virus (polyglot)
   • Script qui s'exécute automatiquement
        """)
        
        # Nettoyer
        input("\n[Appuyez sur Entrée pour supprimer le fichier de test...]")
        run_adb("shell rm /sdcard/Download/important_update.txt")
        print("🗑️ Fichier de test supprimé.")

def test_6_camera_access():
    """Test 6: Accès à la caméra"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  TEST 6: ACCÈS À LA CAMÉRA                                       ║
║                                                                  ║
║  Prendre une photo secrètement (comme un spyware)                ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("📷 Tentative de capture photo secrète...\n")
    
    # Prendre un screenshot (plus fiable que la caméra)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    screenshot_path = os.path.join(BACKUP_DIR, f"spy_capture_{int(time.time())}.png")
    
    print("1️⃣ Capture de l'écran actuel...")
    result = run_adb(f'exec-out screencap -p > "{screenshot_path}"')
    
    if os.path.exists(screenshot_path) and os.path.getsize(screenshot_path) > 0:
        print(f"✅ Screenshot capturé secrètement!")
        print(f"   Sauvegardé: {screenshot_path}")
        print(f"   Taille: {os.path.getsize(screenshot_path):,} bytes")
    else:
        print("❌ Capture échouée")
    
    print("\n🎯 Ce que fait un vrai spyware:")
    print("""
   • Active la caméra frontale sans allumer l'indicateur
   • Prend des photos périodiquement
   • Enregistre des vidéos
   • Active le micro pour enregistrer les conversations
   • Envoie tout à un serveur distant
   
   ⚠️ Certains spywares avancés peuvent:
   • Désactiver le son de l'obturateur
   • Masquer l'icône de la caméra
   • Capturer même écran éteint
    """)

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           📱 PHONE HACKING LAB - TESTS SUR TON TÉLÉPHONE                     ║
║                                                                              ║
║           Apprends comment les hackers attaquent les smartphones             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    if not check_connection():
        print("\n⚠️ Connecte ton téléphone d'abord!")
        return
    
    while True:
        print("""
┌──────────────────────────────────────────────────────────────────┐
│                      📋 TESTS DISPONIBLES                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   [1] Extraction de données    - Voler tes infos personnelles    │
│   [2] Contrôle à distance      - Commander ton téléphone         │
│   [3] Simulation spyware       - Espionnage continu              │
│   [4] Phishing via téléphone   - Ouvrir un lien piégé            │
│   [5] Injection de malware     - Déposer un fichier malveillant  │
│   [6] Accès caméra/écran       - Capture secrète                 │
│                                                                  │
│   [0] Quitter                                                    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
        """)
        
        choice = input("🎯 Choisis un test: ").strip()
        
        if choice == "1":
            test_1_data_extraction()
        elif choice == "2":
            test_2_remote_control()
        elif choice == "3":
            test_3_spyware_simulation()
        elif choice == "4":
            test_4_phishing_to_phone()
        elif choice == "5":
            test_5_payload_injection()
        elif choice == "6":
            test_6_camera_access()
        elif choice == "0":
            print("\n👋 Fin des tests! Maintenant tu sais comment te protéger!")
            break
        else:
            print("❌ Option invalide!")
        
        input("\n[Appuyez sur Entrée pour continuer...]")

if __name__ == "__main__":
    main()
