import subprocess
import os
import sys

def run_adb_command(command):
    # Chemin vers ADB (adapté à votre environnement)
    adb_path = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
    full_command = [adb_path] + command.split()
    try:
        # Utilisation de utf-8 et ignore pour éviter les erreurs d'encodage
        result = subprocess.run(full_command, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def check_device_info():
    print("\n--- 1. INFORMATIONS DE L'APPAREIL ---")
    model = run_adb_command("shell getprop ro.product.model")
    version = run_adb_command("shell getprop ro.build.version.release")
    patch = run_adb_command("shell getprop ro.build.version.security_patch")
    print(f"Modèle: {model}")
    print(f"Version Android: {version}")
    print(f"Niveau de correctif de sécurité: {patch}")
    
    try:
        if version and int(version.split('.')[0]) < 12:
            print("⚠️  AVERTISSEMENT: Version Android ancienne. Risque de sécurité élevé.")
        else:
            print("✅ Version Android récente.")
    except:
        pass

def check_root_status():
    print("\n--- 2. VÉRIFICATION ROOT ---")
    su_check = run_adb_command("shell which su")
    if su_check and "not found" not in su_check:
        print("⚠️  DANGER: L'appareil semble être ROOTÉ (binaire 'su' trouvé).")
        print("   Les applications malveillantes peuvent prendre le contrôle total.")
    else:
        print("✅ L'appareil ne semble pas être rooté (standard).")

def check_dangerous_permissions():
    print("\n--- 3. ANALYSE DES PERMISSIONS DANGEREUSES ---")
    
    print("[*] Applications pouvant lire vos SMS (READ_SMS):")
    sms_apps = run_adb_command("shell cmd package list packages -g android.permission.READ_SMS")
    if sms_apps:
        count = len(sms_apps.splitlines())
        print(f"   -> {count} applications trouvées.")
        # Afficher les 5 premières
        for line in sms_apps.splitlines()[:5]:
            print(f"      - {line.replace('package:', '')}")
    else:
        print("   Aucune trouvée.")

    print("\n[*] Applications pouvant vous écouter (RECORD_AUDIO):")
    audio_apps = run_adb_command("shell cmd package list packages -g android.permission.RECORD_AUDIO")
    if audio_apps:
        count = len(audio_apps.splitlines())
        print(f"   -> {count} applications trouvées.")
    else:
        print("   Aucune trouvée.")

def check_developer_options():
    print("\n--- 4. CONFIGURATION DE SÉCURITÉ ---")
    adb_setting = run_adb_command("shell settings get global adb_enabled")
    install_non_market = run_adb_command("shell settings get secure install_non_market_apps")
    
    if adb_setting == "1":
        print("⚠️  CRITIQUE: Le débogage USB (ADB) est ACTIVÉ.")
        print("   C'est la faille que nous avons utilisée pour tous les tests précédents.")
        print("   Action recommandée: Désactiver dans les Options pour les développeurs.")
    else:
        print("✅ Débogage USB désactivé.")

    if install_non_market == "1":
        print("⚠️  ATTENTION: L'installation d'applications inconnues est autorisée.")
    else:
        print("✅ Installation d'applications inconnues restreinte.")

def main():
    print("==================================================")
    print("   AUDIT DE SÉCURITÉ MOBILE - RAPPORT ÉDUCATIF    ")
    print("==================================================")
    
    devices = run_adb_command("devices")
    if "device" not in devices and "unauthorized" not in devices: # Basic check
        # On continue quand même car adb devices retourne toujours quelque chose
        pass

    check_device_info()
    check_root_status()
    check_dangerous_permissions()
    check_developer_options()
    
    print("\n==================================================")
    print("FIN DE L'AUDIT")

if __name__ == "__main__":
    main()
