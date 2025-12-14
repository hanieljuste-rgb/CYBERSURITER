# ============================================
# PHONE MONITOR - Outil de monitoring ADB
# Pour VOTRE propre telephone uniquement
# ============================================

$ADB = "C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"

function Show-Menu {
    Clear-Host
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "   PHONE MONITOR - Votre TECNO CK6" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "[1]  Lire les SMS recus" -ForegroundColor Green
    Write-Host "[2]  Lire les SMS envoyes" -ForegroundColor Green
    Write-Host "[3]  Voir les contacts" -ForegroundColor Green
    Write-Host "[4]  Historique des appels" -ForegroundColor Green
    Write-Host "[5]  Capture d'ecran" -ForegroundColor Yellow
    Write-Host "[6]  Liste des applications" -ForegroundColor Yellow
    Write-Host "[7]  Informations systeme" -ForegroundColor Yellow
    Write-Host "[8]  Espace de stockage" -ForegroundColor Yellow
    Write-Host "[9]  Batterie" -ForegroundColor Yellow
    Write-Host "[10] Reseaux WiFi enregistres" -ForegroundColor Magenta
    Write-Host "[11] Localisation GPS (si active)" -ForegroundColor Magenta
    Write-Host "[12] Telecharger des fichiers" -ForegroundColor Magenta
    Write-Host "[13] Afficher l'ecran en direct (scrcpy)" -ForegroundColor Cyan
    Write-Host "[14] Enregistrer l'ecran" -ForegroundColor Cyan
    Write-Host "[15] Notifications recentes" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "[0]  Quitter" -ForegroundColor Red
    Write-Host ""
}

function Read-SMS-Inbox {
    Write-Host "`n=== SMS RECUS ===" -ForegroundColor Cyan
    & $ADB shell "content query --uri content://sms/inbox --projection address:body:date --sort 'date DESC' 2>/dev/null | head -20"
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function Read-SMS-Sent {
    Write-Host "`n=== SMS ENVOYES ===" -ForegroundColor Cyan
    & $ADB shell "content query --uri content://sms/sent --projection address:body:date --sort 'date DESC' 2>/dev/null | head -20"
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function Read-Contacts {
    Write-Host "`n=== CONTACTS ===" -ForegroundColor Cyan
    & $ADB shell "content query --uri content://contacts/phones --projection display_name:number 2>/dev/null | head -30"
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function Read-CallLog {
    Write-Host "`n=== HISTORIQUE DES APPELS ===" -ForegroundColor Cyan
    & $ADB shell "content query --uri content://call_log/calls --projection number:name:type:date:duration --sort 'date DESC' 2>/dev/null | head -20"
    Write-Host "`nType: 1=Entrant, 2=Sortant, 3=Manque"
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function Take-Screenshot {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $filename = "screenshot_$timestamp.png"
    Write-Host "`n=== CAPTURE D'ECRAN ===" -ForegroundColor Cyan
    & $ADB shell "screencap /sdcard/$filename"
    & $ADB pull "/sdcard/$filename" "C:\Users\davis\OneDrive\Bureau\HACKING\MonitorPhone\$filename"
    & $ADB shell "rm /sdcard/$filename"
    Write-Host "Capture sauvegardee: MonitorPhone\$filename" -ForegroundColor Green
    Start-Process "C:\Users\davis\OneDrive\Bureau\HACKING\MonitorPhone\$filename"
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function List-Apps {
    Write-Host "`n=== APPLICATIONS INSTALLEES ===" -ForegroundColor Cyan
    Write-Host "Applications tierces:" -ForegroundColor Yellow
    & $ADB shell "pm list packages -3" | ForEach-Object { $_ -replace "package:", "" }
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function System-Info {
    Write-Host "`n=== INFORMATIONS SYSTEME ===" -ForegroundColor Cyan
    Write-Host "Modele:" -ForegroundColor Yellow
    & $ADB shell "getprop ro.product.model"
    Write-Host "`nVersion Android:" -ForegroundColor Yellow
    & $ADB shell "getprop ro.build.version.release"
    Write-Host "`nNumero de serie:" -ForegroundColor Yellow
    & $ADB shell "getprop ro.serialno"
    Write-Host "`nIMEI (si disponible):" -ForegroundColor Yellow
    & $ADB shell "service call iphonesubinfo 1 2>/dev/null | grep -o '[0-9]' | tr -d '\n'"
    Write-Host ""
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function Storage-Info {
    Write-Host "`n=== ESPACE DE STOCKAGE ===" -ForegroundColor Cyan
    & $ADB shell "df -h /sdcard"
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function Battery-Info {
    Write-Host "`n=== BATTERIE ===" -ForegroundColor Cyan
    & $ADB shell "dumpsys battery"
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function WiFi-Networks {
    Write-Host "`n=== RESEAUX WIFI ENREGISTRES ===" -ForegroundColor Cyan
    & $ADB shell "cat /data/misc/wifi/WifiConfigStore.xml 2>/dev/null | grep -E 'SSID|PreSharedKey'" 
    Write-Host "(Necessite root pour les mots de passe)" -ForegroundColor Yellow
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function GPS-Location {
    Write-Host "`n=== LOCALISATION ===" -ForegroundColor Cyan
    & $ADB shell "dumpsys location | grep -E 'last location|latitude|longitude' | head -10"
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function Download-Files {
    Write-Host "`n=== TELECHARGER DES FICHIERS ===" -ForegroundColor Cyan
    Write-Host "Dossiers disponibles:"
    Write-Host "1. Photos (DCIM)"
    Write-Host "2. Downloads"
    Write-Host "3. WhatsApp Media"
    Write-Host "4. Documents"
    $choice = Read-Host "Choisissez (1-4)"
    
    $dest = "C:\Users\davis\OneDrive\Bureau\HACKING\MonitorPhone\Downloads"
    if (-not (Test-Path $dest)) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }
    
    switch ($choice) {
        "1" { & $ADB pull "/sdcard/DCIM" "$dest\DCIM" }
        "2" { & $ADB pull "/sdcard/Download" "$dest\Download" }
        "3" { & $ADB pull "/sdcard/WhatsApp/Media" "$dest\WhatsApp" }
        "4" { & $ADB pull "/sdcard/Documents" "$dest\Documents" }
    }
    Write-Host "Fichiers telecharges dans: $dest" -ForegroundColor Green
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function Live-Screen {
    Write-Host "`n=== AFFICHAGE EN DIRECT ===" -ForegroundColor Cyan
    $scrcpy = Get-ChildItem -Path "C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages" -Filter "scrcpy.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
    if ($scrcpy) {
        Start-Process $scrcpy
    } else {
        Write-Host "scrcpy non trouve. Installez avec: winget install Genymobile.scrcpy" -ForegroundColor Red
    }
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function Record-Screen {
    Write-Host "`n=== ENREGISTREMENT ECRAN ===" -ForegroundColor Cyan
    $duration = Read-Host "Duree en secondes (max 180)"
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $filename = "record_$timestamp.mp4"
    Write-Host "Enregistrement en cours... (Ctrl+C pour arreter)" -ForegroundColor Yellow
    & $ADB shell "screenrecord --time-limit $duration /sdcard/$filename"
    & $ADB pull "/sdcard/$filename" "C:\Users\davis\OneDrive\Bureau\HACKING\MonitorPhone\$filename"
    Write-Host "Video sauvegardee: MonitorPhone\$filename" -ForegroundColor Green
    Read-Host "`nAppuyez sur Entree pour continuer"
}

function Recent-Notifications {
    Write-Host "`n=== NOTIFICATIONS RECENTES ===" -ForegroundColor Cyan
    & $ADB shell "dumpsys notification --noredact | grep -E 'pkg=|title=|text=' | head -30"
    Read-Host "`nAppuyez sur Entree pour continuer"
}

# Menu principal
do {
    Show-Menu
    $selection = Read-Host "Choisissez une option"
    
    switch ($selection) {
        "1" { Read-SMS-Inbox }
        "2" { Read-SMS-Sent }
        "3" { Read-Contacts }
        "4" { Read-CallLog }
        "5" { Take-Screenshot }
        "6" { List-Apps }
        "7" { System-Info }
        "8" { Storage-Info }
        "9" { Battery-Info }
        "10" { WiFi-Networks }
        "11" { GPS-Location }
        "12" { Download-Files }
        "13" { Live-Screen }
        "14" { Record-Screen }
        "15" { Recent-Notifications }
        "0" { Write-Host "Au revoir!" -ForegroundColor Yellow }
        default { Write-Host "Option invalide" -ForegroundColor Red; Start-Sleep 1 }
    }
} while ($selection -ne "0")
