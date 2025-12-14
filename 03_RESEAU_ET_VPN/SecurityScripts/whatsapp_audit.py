import subprocess
import sys

def run_adb(command):
    adb_path = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
    full_cmd = f'"{adb_path}" {command}'
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def check_whatsapp_files():
    print("\n--- 1. ANALYSE DU STOCKAGE (Fichiers Accessibles) ---")
    # Check public media folder
    path = "/sdcard/Android/media/com.whatsapp/WhatsApp/Databases"
    print(f"[*] Vérification du dossier de sauvegarde: {path}")
    files = run_adb(f"shell ls -l {path}")
    
    if "No such file" in files:
        # Try old path
        path = "/sdcard/WhatsApp/Databases"
        files = run_adb(f"shell ls -l {path}")

    if "msgstore" in files:
        print("⚠️  Sauvegardes chiffrées trouvées (msgstore.db.cryptXX).")
        print("   Ces fichiers contiennent vos messages, mais ils sont CHIFFRÉS.")
        print("   Pour les lire, un attaquant aurait besoin de la clé de déchiffrement.")
    else:
        print("✅ Aucune sauvegarde accessible publiquement trouvée.")

    # Check for the key (should fail on non-root)
    print("\n[*] Tentative d'accès à la clé de chiffrement (/data/data/com.whatsapp/files/key)...")
    key_check = run_adb("shell ls -l /data/data/com.whatsapp/files/key")
    
    if "Permission denied" in key_check or "inaccessible" in key_check or "opendir failed" in key_check:
        print("✅ ACCÈS REFUSÉ. C'est une bonne nouvelle !")
        print("   Android protège cette clé. Sans root, personne ne peut déchiffrer vos messages.")
    else:
        print(f"🚨 RÉSULTAT INATTENDU: {key_check}")
        print("   Si vous voyez le fichier, votre téléphone est vulnérable.")

def check_whatsapp_permissions():
    print("\n--- 2. PERMISSIONS CRITIQUES ---")
    # On récupère les infos du package
    perms = run_adb("shell dumpsys package com.whatsapp")
    
    critical_perms = {
        "android.permission.RECORD_AUDIO": "Microphone (Écoute)",
        "android.permission.CAMERA": "Caméra (Espionnage visuel)",
        "android.permission.READ_CONTACTS": "Contacts (Vol de carnet d'adresses)",
        "android.permission.ACCESS_FINE_LOCATION": "Localisation GPS"
    }
    
    print("Permissions accordées (Analyse) :")
    found_any = False
    for line in perms.splitlines():
        line = line.strip()
        for perm, desc in critical_perms.items():
            # La sortie dumpsys varie selon les versions Android, on cherche le pattern large
            if perm in line and "granted=true" in line:
                print(f"   ⚠️  {desc} : ACCORDÉ")
                found_any = True
            # Parfois c'est juste listé sous "runtime permissions:"
            elif perm in line and "granted=true" not in line and "granted=false" not in line:
                 # C'est une déclaration, pas forcément un octroi, on ignore pour éviter les faux positifs
                 pass
    
    if not found_any:
        print("   (Impossible de déterminer les permissions exactes via ADB simple, ou aucune permission critique active)")

def main():
    print("==================================================")
    print("   AUDIT DE SÉCURITÉ WHATSAPP (DÉFENSIF)          ")
    print("==================================================")
    
    check_whatsapp_files()
    check_whatsapp_permissions()

    print("\n==================================================")
    print("CONCLUSION:")
    print("Si quelqu'un vole ces fichiers 'msgstore' sans la clé,")
    print("il ne pourra rien lire. C'est le chiffrement AES-256.")

if __name__ == "__main__":
    main()
