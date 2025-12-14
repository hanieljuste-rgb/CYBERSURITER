import subprocess
import sys

def run_adb(command):
    # Chemin ADB complet
    adb_path = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
    full_cmd = f'"{adb_path}" {command}'
    try:
        # shell=True pour gérer les arguments complexes
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        return result.stdout.strip().splitlines()
    except Exception as e:
        print(f"Erreur ADB: {e}")
        return []

def get_third_party_apps():
    print("\n[*] Recherche des applications tierces (installées par l'utilisateur)...")
    # -3 : Tiers uniquement, -f : voir le chemin du fichier (souvent /data/app/...)
    lines = run_adb("shell pm list packages -f -3")
    apps = []
    for line in lines:
        # Format: package:/data/app/~~.../com.example.app-base.apk=com.example.app
        if "=" in line:
            parts = line.split("=")
            pkg_name = parts[-1].strip()
            path = parts[0].replace("package:", "").strip()
            apps.append((pkg_name, path))
    return apps

def check_device_admins():
    print("\n[*] Recherche des applications 'Administrateur de l'appareil'...")
    # Ces applis ont des droits élevés et sont dures à désinstaller
    lines = run_adb("shell dumpsys device_policy")
    admins = []
    capture = False
    for line in lines:
        if "admin=" in line or "ComponentInfo{" in line:
            if "com.android" not in line and "com.google" not in line: # Filtrer système
                admins.append(line.strip())
    return admins

def check_battery_whitelist():
    print("\n[*] Recherche des applications ignorant l'optimisation batterie...")
    # Les spywares se mettent ici pour ne pas être tués par Android
    lines = run_adb("shell dumpsys deviceidle whitelist")
    whitelisted = []
    for line in lines:
        if "," in line and "com." in line:
            # Format souvent: com.package.name,12345
            app = line.split(",")[0].strip()
            if "com.google" not in app and "com.android" not in app:
                whitelisted.append(app)
    return whitelisted

def main():
    print("==================================================")
    print("   DÉTECTEUR DE LOGICIELS ESPIONS (FORENSICS)     ")
    print("==================================================")

    # 1. Apps Tierces
    apps = get_third_party_apps()
    print(f"   -> {len(apps)} applications tierces trouvées.")
    
    print("\n--- LISTE DES APPLICATIONS SUSPECTES POTENTIELLES ---")
    print("(Vérifiez si vous ne reconnaissez pas un nom)")
    for name, path in apps:
        # Filtrer les applis très connues pour alléger la vue (optionnel)
        if "facebook" in name or "whatsapp" in name or "instagram" in name:
            continue
        print(f" [?] {name}")
        # print(f"     Chemin: {path}")

    # 2. Admins
    admins = check_device_admins()
    if admins:
        print("\n⚠️  ATTENTION: Applications Administrateur trouvées (hors système) :")
        for admin in admins:
            print(f"  - {admin}")
    else:
        print("\n✅ Aucune application administrateur suspecte détectée via dumpsys simple.")

    # 3. Batterie
    whitelist = check_battery_whitelist()
    if whitelist:
        print("\n⚠️  ATTENTION: Ces applis tournent en permanence (Batterie Whitelist) :")
        for app in whitelist:
            print(f"  - {app}")
    else:
        print("\n✅ Liste blanche batterie propre (ou vide).")

    print("\n==================================================")
    print("CONSEIL: Si vous voyez une application inconnue ci-dessus :")
    print("1. Cherchez son nom sur Google.")
    print("2. Désinstallez-la via : adb uninstall <nom_du_paquet>")

if __name__ == "__main__":
    main()
