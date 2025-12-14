#!/usr/bin/env python3
"""
📱 Phone Controller - Contrôle ADB de votre téléphone
Auteur: Formation Cybersécurité
Usage: python phone_controller.py
"""

import subprocess
import os
import sys
from datetime import datetime

class PhoneController:
    def __init__(self):
        self.adb = "adb"
    
    def run_adb(self, command):
        """Exécute une commande ADB"""
        try:
            result = subprocess.run(
                f"{self.adb} {command}",
                shell=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Erreur: {e}"
    
    def is_connected(self):
        """Vérifie si un téléphone est connecté"""
        result = self.run_adb("devices")
        lines = result.split('\n')
        return len(lines) > 1 and 'device' in result
    
    def get_battery_info(self):
        """Obtient les infos de la batterie"""
        result = self.run_adb("shell dumpsys battery")
        info = {}
        for line in result.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                info[key.strip()] = value.strip()
        return info
    
    def screenshot(self, filename=None):
        """Prend une capture d'écran"""
        if not filename:
            filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.run_adb(f"exec-out screencap -p > {filename}")
        return filename
    
    def screen_record(self, duration=10, filename=None):
        """Enregistre l'écran"""
        if not filename:
            filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        remote_path = f"/sdcard/{filename}"
        print(f"🎬 Enregistrement pendant {duration} secondes...")
        self.run_adb(f"shell screenrecord --time-limit {duration} {remote_path}")
        self.run_adb(f"pull {remote_path} {filename}")
        self.run_adb(f"shell rm {remote_path}")
        return filename
    
    def get_installed_apps(self):
        """Liste les applications installées"""
        result = self.run_adb("shell pm list packages --user 0")
        apps = [line.replace('package:', '') for line in result.split('\n') if line]
        return apps
    
    def get_device_info(self):
        """Obtient les informations du téléphone"""
        info = {
            'Modèle': self.run_adb("shell getprop ro.product.model"),
            'Marque': self.run_adb("shell getprop ro.product.brand"),
            'Android': self.run_adb("shell getprop ro.build.version.release"),
            'SDK': self.run_adb("shell getprop ro.build.version.sdk"),
            'Série': self.run_adb("shell getprop ro.serialno"),
            'Wi-Fi MAC': self.run_adb("shell cat /sys/class/net/wlan0/address"),
        }
        return info
    
    def send_text(self, text):
        """Envoie du texte au téléphone (comme si on tapait)"""
        # Remplacer les espaces par %s pour ADB
        text = text.replace(' ', '%s')
        self.run_adb(f"shell input text '{text}'")
    
    def tap(self, x, y):
        """Simule un tap à la position x, y"""
        self.run_adb(f"shell input tap {x} {y}")
    
    def swipe(self, x1, y1, x2, y2, duration=300):
        """Simule un swipe"""
        self.run_adb(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")
    
    def press_key(self, keycode):
        """Appuie sur une touche (KEYCODE_HOME=3, KEYCODE_BACK=4, etc.)"""
        self.run_adb(f"shell input keyevent {keycode}")
    
    def go_home(self):
        """Retourne à l'écran d'accueil"""
        self.press_key(3)
    
    def go_back(self):
        """Appuie sur retour"""
        self.press_key(4)
    
    def open_app(self, package_name):
        """Ouvre une application"""
        self.run_adb(f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
    
    def get_current_activity(self):
        """Obtient l'activité/app en cours"""
        result = self.run_adb("shell dumpsys activity activities | grep mResumedActivity")
        return result
    
    def get_wifi_info(self):
        """Obtient les infos Wi-Fi détaillées"""
        info = {}
        
        # Nom du réseau Wi-Fi connecté (SSID)
        ssid = self.run_adb("shell dumpsys wifi | grep 'mWifiInfo'")
        if ssid:
            info['Détails bruts'] = ssid
        
        # Adresse IP
        ip = self.run_adb("shell ip addr show wlan0 | grep 'inet '")
        if ip:
            info['Adresse IP'] = ip.strip()
        
        # État Wi-Fi
        wifi_state = self.run_adb("shell settings get global wifi_on")
        info['Wi-Fi activé'] = 'Oui' if wifi_state == '1' else 'Non'
        
        # Nom du réseau connecté
        ssid_name = self.run_adb("shell dumpsys wifi | grep 'SSID:'")
        if ssid_name:
            info['SSID'] = ssid_name.split('SSID:')[1].split(',')[0].strip() if 'SSID:' in ssid_name else 'N/A'
        
        # Force du signal
        rssi = self.run_adb("shell dumpsys wifi | grep 'RSSI:'")
        if rssi and 'RSSI:' in rssi:
            info['Force signal (RSSI)'] = rssi.split('RSSI:')[1].split(',')[0].strip()
        
        # Vitesse de connexion
        speed = self.run_adb("shell dumpsys wifi | grep 'Link speed:'")
        if speed and 'Link speed:' in speed:
            info['Vitesse'] = speed.split('Link speed:')[1].split(',')[0].strip()
        
        # Adresse MAC
        mac = self.run_adb("shell cat /sys/class/net/wlan0/address")
        if mac:
            info['Adresse MAC'] = mac
        
        # Passerelle par défaut
        gateway = self.run_adb("shell ip route | grep default")
        if gateway:
            info['Passerelle'] = gateway
        
        return info
    
    def get_location(self):
        """Obtient la localisation GPS"""
        info = {}
        
        # Vérifier si le GPS est activé
        gps_enabled = self.run_adb("shell settings get secure location_providers_allowed")
        info['GPS activé'] = gps_enabled if gps_enabled else 'Non disponible'
        
        # Mode de localisation
        location_mode = self.run_adb("shell settings get secure location_mode")
        modes = {'0': 'Désactivé', '1': 'Capteurs uniquement', '2': 'Économie batterie', '3': 'Haute précision'}
        info['Mode localisation'] = modes.get(location_mode, location_mode)
        
        # Dernière localisation connue (plusieurs méthodes)
        # Méthode 1: dumpsys location
        location1 = self.run_adb("shell dumpsys location")
        if 'Location[' in location1:
            # Extraire les coordonnées
            import re
            coords = re.findall(r'Location\[.*?(-?\d+\.\d+),(-?\d+\.\d+)', location1)
            if coords:
                lat, lon = coords[0]
                info['Latitude'] = lat
                info['Longitude'] = lon
                info['Google Maps'] = f"https://maps.google.com/?q={lat},{lon}"
        
        # Méthode 2: via content provider (peut nécessiter root)
        last_loc = self.run_adb("shell dumpsys location | grep -A5 'last location'")
        if last_loc and 'last location' in last_loc.lower():
            info['Dernière position'] = last_loc[:200]
        
        # Méthode 3: GPS status
        gps_status = self.run_adb("shell dumpsys location | grep -i 'gps'")
        if gps_status:
            info['Status GPS'] = gps_status[:150]
        
        return info


def menu():
    """Menu interactif"""
    phone = PhoneController()
    
    if not phone.is_connected():
        print("❌ Aucun téléphone connecté!")
        print("Connectez votre téléphone via USB ou Wi-Fi (adb connect IP:5555)")
        return
    
    while True:
        print("\n" + "="*50)
        print("📱 PHONE CONTROLLER - Menu Principal")
        print("="*50)
        print("1.  📊 Infos du téléphone")
        print("2.  🔋 État de la batterie")
        print("3.  📸 Capture d'écran")
        print("4.  🎬 Enregistrer l'écran")
        print("5.  📱 Liste des applications")
        print("6.  🚀 Ouvrir une application")
        print("7.  🏠 Aller à l'accueil")
        print("8.  ⬅️  Retour")
        print("9.  ⌨️  Envoyer du texte")
        print("10. 👆 Simuler un tap")
        print("11. 📶 Infos Wi-Fi")
        print("12. 📍 Localisation")
        print("0.  ❌ Quitter")
        print("="*50)
        
        choice = input("Choix: ").strip()
        
        if choice == '1':
            print("\n📊 Informations du téléphone:")
            for key, value in phone.get_device_info().items():
                print(f"  {key}: {value}")
        
        elif choice == '2':
            print("\n🔋 Batterie:")
            info = phone.get_battery_info()
            print(f"  Niveau: {info.get('level', 'N/A')}%")
            print(f"  Statut: {'En charge' if info.get('status') == '2' else 'Débranchée'}")
            print(f"  Température: {int(info.get('temperature', 0))/10}°C")
        
        elif choice == '3':
            filename = phone.screenshot()
            print(f"📸 Capture sauvegardée: {filename}")
        
        elif choice == '4':
            duration = input("Durée en secondes (défaut: 10): ").strip() or "10"
            filename = phone.screen_record(int(duration))
            print(f"🎬 Vidéo sauvegardée: {filename}")
        
        elif choice == '5':
            apps = phone.get_installed_apps()
            print(f"\n📱 {len(apps)} applications installées:")
            for i, app in enumerate(apps[:20], 1):
                print(f"  {i}. {app}")
            if len(apps) > 20:
                print(f"  ... et {len(apps)-20} autres")
        
        elif choice == '6':
            package = input("Nom du package (ex: com.whatsapp): ").strip()
            phone.open_app(package)
            print(f"🚀 Ouverture de {package}")
        
        elif choice == '7':
            phone.go_home()
            print("🏠 Retour à l'accueil")
        
        elif choice == '8':
            phone.go_back()
            print("⬅️ Retour")
        
        elif choice == '9':
            text = input("Texte à envoyer: ").strip()
            phone.send_text(text)
            print("⌨️ Texte envoyé!")
        
        elif choice == '10':
            coords = input("Coordonnées x,y (ex: 500,1000): ").strip()
            x, y = coords.split(',')
            phone.tap(int(x), int(y))
            print(f"👆 Tap à ({x}, {y})")
        
        elif choice == '11':
            print("\n📶 Informations Wi-Fi:")
            print("-" * 40)
            wifi_info = phone.get_wifi_info()
            if isinstance(wifi_info, dict):
                for key, value in wifi_info.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  {wifi_info}")
        
        elif choice == '12':
            print("\n📍 Localisation GPS:")
            print("-" * 40)
            loc_info = phone.get_location()
            if isinstance(loc_info, dict):
                for key, value in loc_info.items():
                    if value and len(str(value)) < 200:
                        print(f"  {key}: {value}")
                if 'Google Maps' in loc_info:
                    print(f"\n  🗺️ Ouvrir dans Maps: {loc_info['Google Maps']}")
            else:
                print(f"  {loc_info}")
        
        elif choice == '0':
            print("👋 Au revoir!")
            break
        
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    menu()
