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

def check_install_permission():
    print("==================================================")
    print("   AUDIT DES INSTALLATEURS D'APPLICATIONS         ")
    print("==================================================")
    print("Recherche des applications ayant le droit :")
    print("'REQUEST_INSTALL_PACKAGES' (Installation d'apps inconnues)\n")

    # Liste les packages ayant la permission demandée (-g pour granted ne marche pas toujours sur toutes les versions ADB/Android, on filtre manuellement)
    # On liste d'abord tous les packages qui *déclarent* utiliser cette permission
    cmd = "shell cmd package list packages -d -g android.permission.REQUEST_INSTALL_PACKAGES"
    output = run_adb(cmd)
    
    if not output:
        # Fallback pour certaines versions Android
        cmd = "shell pm list packages -g android.permission.REQUEST_INSTALL_PACKAGES"
        output = run_adb(cmd)

    if not output:
        print("Aucune application trouvée avec cette permission via la méthode standard.")
        print("Essai d'une méthode alternative...")
        # Méthode plus lente mais plus précise : vérifier les apps courantes
        common_installers = ["com.android.chrome", "com.transsion.phoenix", "com.whatsapp", "com.android.vending"]
        for app in common_installers:
            res = run_adb(f"shell appops get {app} REQUEST_INSTALL_PACKAGES")
            if "allow" in res:
                print(f"⚠️  [DANGER] {app} : AUTORISÉ à installer des applications !")
            elif "deny" in res:
                print(f"✅ [SÉCURISÉ] {app} : Refusé")
            else:
                pass
    else:
        lines = output.splitlines()
        print(f"Trouvé {len(lines)} applications potentielles :")
        for line in lines:
            package = line.replace("package:", "").strip()
            # Vérification réelle avec appops pour voir si c'est activé par l'utilisateur
            status = run_adb(f"shell appops get {package} REQUEST_INSTALL_PACKAGES")
            
            if "allow" in status:
                print(f"🚨 [ACTIF] {package}")
                print("   -> Cette application peut installer n'importe quoi sans votre accord explicite.")
            else:
                print(f"🛡️ [INACTIF] {package} (Permission demandée mais désactivée)")

    print("\n==================================================")
    print("CONSEIL DE SÉCURITÉ :")
    print("Allez dans Paramètres > Applis > Accès spécial > Installation d'applis inconnues")
    print("et désactivez TOUT sauf si nécessaire.")

if __name__ == "__main__":
    check_install_permission()
