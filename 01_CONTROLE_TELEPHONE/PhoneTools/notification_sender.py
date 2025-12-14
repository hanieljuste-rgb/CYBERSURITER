#!/usr/bin/env python3
"""
📱 OUTIL D'ENVOI DE NOTIFICATIONS
Envoie des notifications à votre téléphone depuis le PC
"""

import subprocess
import os
from datetime import datetime

# Configuration
ADB_PATH = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
PHONE_IP = "100.88.242.60:5555"  # IP Tailscale du TECNO CK6

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_adb(command):
    """Exécuter une commande ADB"""
    full_cmd = f'"{ADB_PATH}" -s {PHONE_IP} {command}'
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Erreur: {e}"

def check_connection():
    """Vérifier la connexion au téléphone"""
    result = run_adb("shell echo connected")
    return "connected" in result

def send_notification(title, message):
    """Envoyer une notification au téléphone"""
    # Échapper les caractères spéciaux
    title = title.replace("'", "\\'").replace('"', '\\"')
    message = message.replace("'", "\\'").replace('"', '\\"')
    
    notif_id = f"notif_{datetime.now().strftime('%H%M%S')}"
    cmd = f"shell cmd notification post -t '{title}' '{message}' {notif_id}"
    result = run_adb(cmd)
    return "posting" in result.lower() or "notification" in result.lower()

def send_toast(message):
    """Envoyer un toast (message popup) au téléphone"""
    message = message.replace("'", "\\'").replace('"', '\\"')
    cmd = f'shell am broadcast -a android.intent.action.MAIN -e message "{message}"'
    run_adb(cmd)

def make_phone_vibrate():
    """Faire vibrer le téléphone"""
    # Utiliser un service audio pour vibrer
    run_adb('shell cmd vibrator vibrate 500')
    return True

def play_sound():
    """Jouer un son sur le téléphone"""
    run_adb('shell am start -a android.intent.action.VIEW -d "content://settings/system/notification_sound"')

def take_screenshot():
    """Prendre une capture d'écran"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    remote_path = f"/sdcard/screenshot_{timestamp}.png"
    local_path = f"C:\\Users\\davis\\OneDrive\\Bureau\\HACKING\\PhoneTools\\screenshots\\screenshot_{timestamp}.png"
    
    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    run_adb(f'shell screencap -p {remote_path}')
    run_adb(f'pull {remote_path} "{local_path}"')
    run_adb(f'shell rm {remote_path}')
    
    if os.path.exists(local_path):
        return local_path
    return None

def open_app(package_name):
    """Ouvrir une application sur le téléphone"""
    cmd = f'shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1'
    run_adb(cmd)

def send_sms_intent(numero, message):
    """Ouvrir l'app SMS avec un message pré-rempli"""
    message = message.replace(" ", "%20").replace("'", "\\'")
    cmd = f'shell am start -a android.intent.action.SENDTO -d "sms:{numero}" --es sms_body "{message}"'
    run_adb(cmd)

def call_number(numero):
    """Lancer un appel téléphonique"""
    cmd = f'shell am start -a android.intent.action.CALL -d "tel:{numero}"'
    run_adb(cmd)

def open_url(url):
    """Ouvrir une URL dans le navigateur"""
    cmd = f'shell am start -a android.intent.action.VIEW -d "{url}"'
    run_adb(cmd)

def set_alarm(hour, minute, message="Alarme"):
    """Définir une alarme"""
    cmd = f'shell am start -a android.intent.action.SET_ALARM --ei android.intent.extra.alarm.HOUR {hour} --ei android.intent.extra.alarm.MINUTES {minute} --es android.intent.extra.alarm.MESSAGE "{message}"'
    run_adb(cmd)

def get_battery_level():
    """Obtenir le niveau de batterie"""
    result = run_adb('shell dumpsys battery | grep level')
    try:
        level = result.split(':')[1].strip()
        return f"{level}%"
    except:
        return "Inconnu"

def main_menu():
    """Menu principal"""
    clear_screen()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║          📱 OUTIL DE CONTRÔLE TÉLÉPHONE                      ║
║              TECNO CK6 - Via Tailscale                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [1]  📢 Envoyer une notification                            ║
║  [2]  📳 Faire vibrer le téléphone                           ║
║  [3]  📸 Prendre une capture d'écran                         ║
║  [4]  💬 Préparer un SMS                                     ║
║  [5]  📞 Passer un appel                                     ║
║  [6]  🌐 Ouvrir une URL                                      ║
║  [7]  ⏰ Définir une alarme                                  ║
║  [8]  🔋 Voir le niveau de batterie                          ║
║  [9]  📱 Ouvrir une application                              ║
║  [10] 🔔 Envoyer plusieurs notifications                     ║
║                                                              ║
║  [0]  ❌ Quitter                                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

def main():
    """Fonction principale"""
    clear_screen()
    print("\n🔄 Vérification de la connexion au téléphone...")
    
    if not check_connection():
        print("❌ Téléphone non connecté!")
        print("   Vérifiez que Tailscale est actif sur le téléphone.")
        input("\nAppuyez sur Entrée pour réessayer...")
        return main()
    
    print("✅ Téléphone connecté!")
    battery = get_battery_level()
    print(f"🔋 Batterie: {battery}")
    
    while True:
        main_menu()
        
        try:
            choice = input("\n👉 Votre choix: ").strip()
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            break
        
        if choice == "0":
            print("\n👋 Au revoir!")
            break
            
        elif choice == "1":
            print("\n📢 ENVOYER UNE NOTIFICATION")
            print("-" * 40)
            title = input("Titre: ").strip() or "Message du PC"
            message = input("Message: ").strip() or "Notification test"
            
            if send_notification(title, message):
                print("✅ Notification envoyée!")
            else:
                print("❌ Erreur lors de l'envoi")
                
        elif choice == "2":
            print("\n📳 Vibration...")
            make_phone_vibrate()
            print("✅ Le téléphone a vibré!")
            
        elif choice == "3":
            print("\n📸 Capture d'écran en cours...")
            path = take_screenshot()
            if path:
                print(f"✅ Capture sauvegardée: {path}")
                os.startfile(os.path.dirname(path))
            else:
                print("❌ Erreur lors de la capture")
                
        elif choice == "4":
            print("\n💬 PRÉPARER UN SMS")
            print("-" * 40)
            numero = input("Numéro de téléphone: ").strip()
            message = input("Message: ").strip()
            if numero:
                send_sms_intent(numero, message)
                print("✅ App SMS ouverte sur le téléphone!")
                
        elif choice == "5":
            print("\n📞 PASSER UN APPEL")
            print("-" * 40)
            numero = input("Numéro à appeler: ").strip()
            if numero:
                call_number(numero)
                print(f"✅ Appel vers {numero} lancé!")
                
        elif choice == "6":
            print("\n🌐 OUVRIR UNE URL")
            print("-" * 40)
            url = input("URL (avec https://): ").strip()
            if not url.startswith("http"):
                url = "https://" + url
            open_url(url)
            print("✅ URL ouverte sur le téléphone!")
            
        elif choice == "7":
            print("\n⏰ DÉFINIR UNE ALARME")
            print("-" * 40)
            try:
                hour = int(input("Heure (0-23): ").strip())
                minute = int(input("Minutes (0-59): ").strip())
                msg = input("Message (optionnel): ").strip() or "Alarme"
                set_alarm(hour, minute, msg)
                print(f"✅ Alarme définie pour {hour:02d}:{minute:02d}!")
            except ValueError:
                print("❌ Heure invalide")
                
        elif choice == "8":
            battery = get_battery_level()
            print(f"\n🔋 Niveau de batterie: {battery}")
            
        elif choice == "9":
            print("\n📱 OUVRIR UNE APPLICATION")
            print("-" * 40)
            print("Applications populaires:")
            print("  1. WhatsApp      (com.whatsapp)")
            print("  2. Chrome        (com.android.chrome)")
            print("  3. YouTube       (com.google.android.youtube)")
            print("  4. Instagram     (com.instagram.android)")
            print("  5. TikTok        (com.zhiliaoapp.musically)")
            print("  6. Appareil photo (com.android.camera)")
            print("  7. Autre (entrer le package)")
            
            app_choice = input("\nChoix: ").strip()
            packages = {
                "1": "com.whatsapp",
                "2": "com.android.chrome", 
                "3": "com.google.android.youtube",
                "4": "com.instagram.android",
                "5": "com.zhiliaoapp.musically",
                "6": "com.android.camera"
            }
            
            if app_choice in packages:
                open_app(packages[app_choice])
                print("✅ Application ouverte!")
            elif app_choice == "7":
                pkg = input("Nom du package: ").strip()
                if pkg:
                    open_app(pkg)
                    print("✅ Application ouverte!")
                    
        elif choice == "10":
            print("\n🔔 ENVOYER PLUSIEURS NOTIFICATIONS")
            print("-" * 40)
            try:
                count = int(input("Nombre de notifications: ").strip())
                title = input("Titre: ").strip() or "Alerte"
                message = input("Message: ").strip() or "Notification"
                
                for i in range(count):
                    send_notification(f"{title} #{i+1}", message)
                    print(f"  ✅ Notification {i+1}/{count} envoyée")
                print(f"\n✅ {count} notifications envoyées!")
            except ValueError:
                print("❌ Nombre invalide")
        
        input("\n⏎ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
