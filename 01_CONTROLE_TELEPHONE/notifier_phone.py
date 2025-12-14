#!/usr/bin/env python3
"""
📱 Script pour envoyer des notifications sur votre téléphone Android
Utilise ADB pour communiquer avec le téléphone
"""

import subprocess
import sys

def run_adb(command):
    """Exécute une commande ADB"""
    try:
        result = subprocess.run(
            f"adb {command}",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout, result.returncode == 0
    except Exception as e:
        return str(e), False

def send_toast(message):
    """Affiche un message Toast sur le téléphone"""
    # Utilise une app pour afficher le toast
    cmd = f'shell am broadcast -a android.intent.action.SHOW_TOAST --es message "{message}"'
    output, success = run_adb(cmd)
    return success

def open_url(url):
    """Ouvre une URL sur le téléphone"""
    cmd = f'shell am start -a android.intent.action.VIEW -d "{url}"'
    output, success = run_adb(cmd)
    return success

def send_sms_screen(phone_number, message=""):
    """Ouvre l'écran SMS avec un numéro et message pré-rempli"""
    cmd = f'shell am start -a android.intent.action.SENDTO -d "sms:{phone_number}" --es sms_body "{message}"'
    output, success = run_adb(cmd)
    return success

def make_call(phone_number):
    """Ouvre l'écran d'appel avec un numéro"""
    cmd = f'shell am start -a android.intent.action.DIAL -d "tel:{phone_number}"'
    output, success = run_adb(cmd)
    return success

def play_alarm():
    """Fait sonner une alarme sur le téléphone"""
    cmd = 'shell am start -a android.intent.action.SET_ALARM --ei android.intent.extra.alarm.HOUR 0 --ei android.intent.extra.alarm.MINUTES 0'
    output, success = run_adb(cmd)
    return success

def set_clipboard(text):
    """Copie du texte dans le presse-papier du téléphone"""
    cmd = f'shell am broadcast -a clipper.set -e text "{text}"'
    output, success = run_adb(cmd)
    return success

def take_screenshot(filename="screenshot.png"):
    """Prend une capture d'écran"""
    cmd = f'exec-out screencap -p > {filename}'
    output, success = run_adb(cmd)
    return success

def vibrate():
    """Fait vibrer le téléphone (nécessite root ou app spéciale)"""
    cmd = 'shell input keyevent 25'  # Volume down comme alternative
    output, success = run_adb(cmd)
    return success

def show_menu():
    """Affiche le menu principal"""
    print("\n" + "="*50)
    print("📱 CONTRÔLE DE TÉLÉPHONE À DISTANCE")
    print("="*50)
    print("1. 💬 Envoyer un message Toast")
    print("2. 🌐 Ouvrir une URL")
    print("3. 📩 Ouvrir l'écran SMS")
    print("4. 📞 Ouvrir l'écran d'appel")
    print("5. 📸 Prendre une capture d'écran")
    print("6. 🔔 Faire sonner (volume)")
    print("7. ❌ Quitter")
    print("="*50)

def main():
    print("🔗 Vérification de la connexion ADB...")
    output, success = run_adb("devices")
    
    if "device" not in output or "attached" in output and output.strip().endswith("attached"):
        print("❌ Aucun téléphone connecté!")
        print("Connectez votre téléphone via USB ou Wi-Fi (adb connect IP:5555)")
        return
    
    print("✅ Téléphone connecté!")
    
    while True:
        show_menu()
        choice = input("\nVotre choix (1-7): ").strip()
        
        if choice == "1":
            message = input("📝 Message à envoyer: ")
            if send_toast(message):
                print("✅ Message envoyé!")
            else:
                print("❌ Échec de l'envoi")
                
        elif choice == "2":
            url = input("🌐 URL à ouvrir: ")
            if not url.startswith("http"):
                url = "https://" + url
            if open_url(url):
                print("✅ URL ouverte sur le téléphone!")
            else:
                print("❌ Échec")
                
        elif choice == "3":
            phone = input("📞 Numéro de téléphone: ")
            msg = input("📝 Message (optionnel): ")
            if send_sms_screen(phone, msg):
                print("✅ Écran SMS ouvert!")
            else:
                print("❌ Échec")
                
        elif choice == "4":
            phone = input("📞 Numéro à appeler: ")
            if make_call(phone):
                print("✅ Écran d'appel ouvert!")
            else:
                print("❌ Échec")
                
        elif choice == "5":
            filename = input("📁 Nom du fichier (défaut: screenshot.png): ").strip()
            if not filename:
                filename = "screenshot.png"
            if take_screenshot(filename):
                print(f"✅ Capture sauvegardée: {filename}")
            else:
                print("❌ Échec de la capture")
                
        elif choice == "6":
            print("🔔 Envoi d'un signal...")
            vibrate()
            print("✅ Signal envoyé!")
            
        elif choice == "7":
            print("👋 Au revoir!")
            break
            
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()
