import os
import time
import subprocess

ADB_PATH = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
DEVICE_ID = "101132534I100038"

# Paramètres à personnaliser
NUMERO_DESTINATAIRE = ""  # <-- À remplir
MONTANT = ""              # <-- À remplir

# 1. Ouvrir l'application Wave
def ouvrir_wave():
    print("Ouverture de l'application Wave...")
    subprocess.run([ADB_PATH, "-s", DEVICE_ID, "shell", "monkey", "-p", "com.wave.personal", "-c", "android.intent.category.LAUNCHER", "1"])
    time.sleep(3)

# 2. Saisie automatisée (remplir les champs via input tap/text)
def saisir_infos():
    print("Remplissage du numéro et du montant...")
    # Exemple de tap (à adapter selon la position des champs sur l'écran)
    # subprocess.run([ADB_PATH, "-s", DEVICE_ID, "shell", "input", "tap", "x", "y"])
    # subprocess.run([ADB_PATH, "-s", DEVICE_ID, "shell", "input", "text", NUMERO_DESTINATAIRE])
    # subprocess.run([ADB_PATH, "-s", DEVICE_ID, "shell", "input", "tap", "x2", "y2"])
    # subprocess.run([ADB_PATH, "-s", DEVICE_ID, "shell", "input", "text", MONTANT])
    print("(À compléter selon la position des champs sur l'app)")
    time.sleep(2)

# 3. Capture d'écran
def capture_ecran():
    print("Capture d'écran...")
    subprocess.run([ADB_PATH, "-s", DEVICE_ID, "shell", "screencap", "-p", "/sdcard/wave_transfert.png"])
    subprocess.run([ADB_PATH, "-s", DEVICE_ID, "pull", "/sdcard/wave_transfert.png", r"C:\Users\davis\OneDrive\Bureau\HACKING\02_EXTRACTION_DONNEES\TECNO_CK6\wave_transfert.png"])
    print("Screenshot sauvegardé !")

if __name__ == "__main__":
    ouvrir_wave()
    saisir_infos()
    capture_ecran()
    print("Étapes terminées. Valide manuellement le transfert sur ton téléphone.")
