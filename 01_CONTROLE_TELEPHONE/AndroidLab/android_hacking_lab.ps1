# ============================================================================
#        ANDROID HACKING LAB - Outil Educatif Complet
#        Pour pratiquer sur VOTRE propre telephone
# ============================================================================

$ADB = "C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
$OutputDir = "C:\Users\davis\OneDrive\Bureau\HACKING\AndroidLab\Extracted"

# Creer le dossier de sortie
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

function Show-Banner {
    Clear-Host
    Write-Host @"
===============================================================================
     _              _           _     _   _            _    _             
    / \   _ __   __| |_ __ ___ (_) __| | | | __ _  ___| | _(_)_ __   __ _ 
   / _ \ | '_ \ / _` | '__/ _ \| |/ _` | | |/ _` |/ __| |/ / | '_ \ / _` |
  / ___ \| | | | (_| | | | (_) | | (_| | | | (_| | (__|   <| | | | | (_| |
 /_/   \_\_| |_|\__,_|_|  \___/|_|\__,_| |_|\__,_|\___|_|\_\_|_| |_|\__, |
                                                                    |___/ 
                    LABORATOIRE EDUCATIF - TECNO CK6
===============================================================================
"@ -ForegroundColor Cyan
}

function Show-Menu {
    Write-Host ""
    Write-Host "=== MENU PRINCIPAL ===" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "[EXTRACTION DE DONNEES]" -ForegroundColor Green
    Write-Host "  1.  SMS (Inbox + Sent)"
    Write-Host "  2.  Contacts"
    Write-Host "  3.  Historique d'appels"
    Write-Host "  4.  WhatsApp (bases de donnees)"
    Write-Host "  5.  Photos et Videos"
    Write-Host ""
    Write-Host "[SURVEILLANCE]" -ForegroundColor Magenta
    Write-Host "  6.  Screenshot en direct"
    Write-Host "  7.  Enregistrement ecran"
    Write-Host "  8.  Affichage live (scrcpy)"
    Write-Host "  9.  Notifications en temps reel"
    Write-Host "  10. Localisation GPS"
    Write-Host ""
    Write-Host "[INFORMATIONS SYSTEME]" -ForegroundColor Cyan
    Write-Host "  11. Infos appareil (IMEI, modele, etc)"
    Write-Host "  12. Applications installees"
    Write-Host "  13. Permissions des apps"
    Write-Host "  14. Processus en cours"
    Write-Host "  15. Reseaux WiFi enregistres"
    Write-Host ""
    Write-Host "[CONTROLE]" -ForegroundColor Red
    Write-Host "  16. Installer une APK"
    Write-Host "  17. Desinstaller une app"
    Write-Host "  18. Accorder des permissions"
    Write-Host "  19. Envoyer des touches/texte"
    Write-Host "  20. Shell interactif"
    Write-Host ""
    Write-Host "[EXTRACTION COMPLETE]" -ForegroundColor Yellow
    Write-Host "  99. TOUT EXTRAIRE (backup complet)"
    Write-Host ""
    Write-Host "  0.  Quitter"
    Write-Host ""
}

# ============================================================================
# FONCTIONS D'EXTRACTION
# ============================================================================

function Get-SMS {
    Write-Host "`n=== EXTRACTION SMS ===" -ForegroundColor Cyan
    
    Write-Host "`n[+] SMS Recus:" -ForegroundColor Green
    $inbox = & $ADB shell "content query --uri content://sms/inbox --projection address:body:date --sort 'date DESC' 2>/dev/null"
    $inbox | ForEach-Object { Write-Host $_ }
    
    Write-Host "`n[+] SMS Envoyes:" -ForegroundColor Green
    $sent = & $ADB shell "content query --uri content://sms/sent --projection address:body:date --sort 'date DESC' 2>/dev/null"
    $sent | ForEach-Object { Write-Host $_ }
    
    # Sauvegarder
    $inbox | Out-File "$OutputDir\sms_inbox.txt" -Encoding UTF8
    $sent | Out-File "$OutputDir\sms_sent.txt" -Encoding UTF8
    Write-Host "`n[+] Sauvegarde: $OutputDir\sms_*.txt" -ForegroundColor Yellow
    
    Read-Host "`nAppuyez sur Entree"
}

function Get-Contacts {
    Write-Host "`n=== EXTRACTION CONTACTS ===" -ForegroundColor Cyan
    
    $contacts = & $ADB shell "content query --uri content://contacts/phones --projection display_name:number 2>/dev/null"
    $contacts | ForEach-Object { Write-Host $_ }
    
    $contacts | Out-File "$OutputDir\contacts.txt" -Encoding UTF8
    Write-Host "`n[+] Sauvegarde: $OutputDir\contacts.txt" -ForegroundColor Yellow
    Write-Host "[+] Total: $(($contacts | Measure-Object).Count) contacts" -ForegroundColor Green
    
    Read-Host "`nAppuyez sur Entree"
}

function Get-CallLog {
    Write-Host "`n=== HISTORIQUE D'APPELS ===" -ForegroundColor Cyan
    Write-Host "Type: 1=Entrant, 2=Sortant, 3=Manque`n" -ForegroundColor Yellow
    
    $calls = & $ADB shell "content query --uri content://call_log/calls --projection number:name:type:date:duration --sort 'date DESC' 2>/dev/null"
    $calls | Select-Object -First 30 | ForEach-Object { Write-Host $_ }
    
    $calls | Out-File "$OutputDir\call_log.txt" -Encoding UTF8
    Write-Host "`n[+] Sauvegarde: $OutputDir\call_log.txt" -ForegroundColor Yellow
    
    Read-Host "`nAppuyez sur Entree"
}

function Get-WhatsApp {
    Write-Host "`n=== EXTRACTION WHATSAPP ===" -ForegroundColor Cyan
    
    # Creer dossier WhatsApp
    $waDir = "$OutputDir\WhatsApp"
    if (-not (Test-Path $waDir)) { New-Item -ItemType Directory -Path $waDir -Force | Out-Null }
    
    Write-Host "[+] Extraction des medias WhatsApp..." -ForegroundColor Yellow
    & $ADB pull "/sdcard/WhatsApp" $waDir 2>$null
    
    Write-Host "[+] Recherche de bases de donnees..." -ForegroundColor Yellow
    & $ADB pull "/sdcard/WhatsApp/Databases" "$waDir\Databases" 2>$null
    
    # Lister ce qui a ete extrait
    $files = Get-ChildItem -Path $waDir -Recurse -File | Measure-Object
    Write-Host "`n[+] $($files.Count) fichiers extraits dans: $waDir" -ForegroundColor Green
    
    Read-Host "`nAppuyez sur Entree"
}

function Get-Media {
    Write-Host "`n=== EXTRACTION PHOTOS/VIDEOS ===" -ForegroundColor Cyan
    
    $mediaDir = "$OutputDir\Media"
    if (-not (Test-Path $mediaDir)) { New-Item -ItemType Directory -Path $mediaDir -Force | Out-Null }
    
    Write-Host "[1] DCIM (Camera)" -ForegroundColor Yellow
    Write-Host "[2] Pictures" -ForegroundColor Yellow
    Write-Host "[3] Download" -ForegroundColor Yellow
    Write-Host "[4] TOUT" -ForegroundColor Yellow
    
    $choice = Read-Host "Choisir"
    
    switch ($choice) {
        "1" { 
            Write-Host "`n[+] Extraction DCIM..." -ForegroundColor Cyan
            & $ADB pull "/sdcard/DCIM" "$mediaDir\DCIM"
        }
        "2" { 
            Write-Host "`n[+] Extraction Pictures..." -ForegroundColor Cyan
            & $ADB pull "/sdcard/Pictures" "$mediaDir\Pictures"
        }
        "3" { 
            Write-Host "`n[+] Extraction Download..." -ForegroundColor Cyan
            & $ADB pull "/sdcard/Download" "$mediaDir\Download"
        }
        "4" {
            Write-Host "`n[+] Extraction complete..." -ForegroundColor Cyan
            & $ADB pull "/sdcard/DCIM" "$mediaDir\DCIM"
            & $ADB pull "/sdcard/Pictures" "$mediaDir\Pictures"
            & $ADB pull "/sdcard/Download" "$mediaDir\Download"
            & $ADB pull "/sdcard/Movies" "$mediaDir\Movies"
        }
    }
    
    $files = Get-ChildItem -Path $mediaDir -Recurse -File -ErrorAction SilentlyContinue | Measure-Object
    Write-Host "`n[+] $($files.Count) fichiers extraits" -ForegroundColor Green
    
    Read-Host "`nAppuyez sur Entree"
}

# ============================================================================
# FONCTIONS DE SURVEILLANCE
# ============================================================================

function Take-Screenshot {
    Write-Host "`n=== CAPTURE D'ECRAN ===" -ForegroundColor Cyan
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $filename = "screenshot_$timestamp.png"
    
    Write-Host "[+] Capture en cours..." -ForegroundColor Yellow
    & $ADB shell "screencap /sdcard/$filename"
    & $ADB pull "/sdcard/$filename" "$OutputDir\$filename"
    & $ADB shell "rm /sdcard/$filename"
    
    Write-Host "[+] Sauvegarde: $OutputDir\$filename" -ForegroundColor Green
    
    # Ouvrir l'image
    Start-Process "$OutputDir\$filename"
    
    Read-Host "`nAppuyez sur Entree"
}

function Record-Screen {
    Write-Host "`n=== ENREGISTREMENT ECRAN ===" -ForegroundColor Cyan
    
    $duration = Read-Host "Duree en secondes (max 180)"
    if ([int]$duration -gt 180) { $duration = 180 }
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $filename = "record_$timestamp.mp4"
    
    Write-Host "[+] Enregistrement pendant $duration secondes..." -ForegroundColor Yellow
    Write-Host "    (L'ecran du telephone s'enregistre)" -ForegroundColor Gray
    
    & $ADB shell "screenrecord --time-limit $duration /sdcard/$filename"
    & $ADB pull "/sdcard/$filename" "$OutputDir\$filename"
    & $ADB shell "rm /sdcard/$filename"
    
    Write-Host "[+] Sauvegarde: $OutputDir\$filename" -ForegroundColor Green
    
    Read-Host "`nAppuyez sur Entree"
}

function Start-LiveScreen {
    Write-Host "`n=== AFFICHAGE EN DIRECT ===" -ForegroundColor Cyan
    
    $scrcpy = Get-ChildItem -Path "C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages" -Filter "scrcpy.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
    
    if ($scrcpy) {
        Write-Host "[+] Lancement de scrcpy..." -ForegroundColor Green
        Start-Process $scrcpy
    } else {
        Write-Host "[-] scrcpy non trouve. Installation..." -ForegroundColor Red
        winget install Genymobile.scrcpy
    }
    
    Read-Host "`nAppuyez sur Entree"
}

function Get-Notifications {
    Write-Host "`n=== NOTIFICATIONS EN TEMPS REEL ===" -ForegroundColor Cyan
    Write-Host "(Ctrl+C pour arreter)`n" -ForegroundColor Yellow
    
    # Afficher les notifications actuelles
    & $ADB shell "dumpsys notification --noredact" | Select-String -Pattern "pkg=|android.title=|android.text=" | Select-Object -First 50
    
    Read-Host "`nAppuyez sur Entree"
}

function Get-Location {
    Write-Host "`n=== LOCALISATION GPS ===" -ForegroundColor Cyan
    
    Write-Host "[+] Derniere position connue:" -ForegroundColor Yellow
    & $ADB shell "dumpsys location" | Select-String -Pattern "last location|mLastLocation|latitude|longitude" | Select-Object -First 10
    
    Write-Host "`n[+] Providers actifs:" -ForegroundColor Yellow
    & $ADB shell "settings get secure location_providers_allowed"
    
    Read-Host "`nAppuyez sur Entree"
}

# ============================================================================
# FONCTIONS INFORMATIONS SYSTEME
# ============================================================================

function Get-DeviceInfo {
    Write-Host "`n=== INFORMATIONS APPAREIL ===" -ForegroundColor Cyan
    
    Write-Host "`n[MATERIEL]" -ForegroundColor Yellow
    Write-Host "Modele:      " -NoNewline; & $ADB shell "getprop ro.product.model"
    Write-Host "Marque:      " -NoNewline; & $ADB shell "getprop ro.product.brand"
    Write-Host "Fabricant:   " -NoNewline; & $ADB shell "getprop ro.product.manufacturer"
    Write-Host "Device:      " -NoNewline; & $ADB shell "getprop ro.product.device"
    
    Write-Host "`n[SYSTEME]" -ForegroundColor Yellow
    Write-Host "Android:     " -NoNewline; & $ADB shell "getprop ro.build.version.release"
    Write-Host "SDK:         " -NoNewline; & $ADB shell "getprop ro.build.version.sdk"
    Write-Host "Build:       " -NoNewline; & $ADB shell "getprop ro.build.display.id"
    Write-Host "Securite:    " -NoNewline; & $ADB shell "getprop ro.build.version.security_patch"
    
    Write-Host "`n[IDENTIFIANTS]" -ForegroundColor Yellow
    Write-Host "Serial:      " -NoNewline; & $ADB shell "getprop ro.serialno"
    Write-Host "Android ID:  " -NoNewline; & $ADB shell "settings get secure android_id"
    
    Write-Host "`n[RESEAU]" -ForegroundColor Yellow
    Write-Host "WiFi MAC:    " -NoNewline; & $ADB shell "cat /sys/class/net/wlan0/address 2>/dev/null"
    Write-Host "IP:          " -NoNewline; & $ADB shell "ip addr show wlan0 2>/dev/null" | Select-String -Pattern "inet " | ForEach-Object { $_.ToString().Trim() }
    
    Write-Host "`n[BATTERIE]" -ForegroundColor Yellow
    & $ADB shell "dumpsys battery" | Select-String -Pattern "level|status|health|temperature"
    
    Read-Host "`nAppuyez sur Entree"
}

function Get-InstalledApps {
    Write-Host "`n=== APPLICATIONS INSTALLEES ===" -ForegroundColor Cyan
    
    Write-Host "`n[+] Applications tierces:" -ForegroundColor Yellow
    $apps = & $ADB shell "pm list packages -3" | ForEach-Object { $_ -replace "package:", "" }
    $apps | ForEach-Object { Write-Host "  - $_" }
    
    $apps | Out-File "$OutputDir\installed_apps.txt" -Encoding UTF8
    Write-Host "`n[+] Total: $(($apps | Measure-Object).Count) applications" -ForegroundColor Green
    Write-Host "[+] Sauvegarde: $OutputDir\installed_apps.txt" -ForegroundColor Yellow
    
    Read-Host "`nAppuyez sur Entree"
}

function Get-AppPermissions {
    Write-Host "`n=== PERMISSIONS DES APPLICATIONS ===" -ForegroundColor Cyan
    
    $app = Read-Host "Nom du package (ex: com.whatsapp)"
    
    if ($app) {
        Write-Host "`n[+] Permissions de $app :" -ForegroundColor Yellow
        & $ADB shell "dumpsys package $app" | Select-String -Pattern "permission|granted"
    }
    
    Read-Host "`nAppuyez sur Entree"
}

function Get-Processes {
    Write-Host "`n=== PROCESSUS EN COURS ===" -ForegroundColor Cyan
    
    & $ADB shell "ps -A" | Select-Object -First 30
    
    Read-Host "`nAppuyez sur Entree"
}

function Get-WiFiNetworks {
    Write-Host "`n=== RESEAUX WIFI ENREGISTRES ===" -ForegroundColor Cyan
    
    Write-Host "[+] Tentative d'extraction (necessite root pour mots de passe)..." -ForegroundColor Yellow
    
    # Sans root - juste les SSIDs
    & $ADB shell "cmd wifi list-networks 2>/dev/null"
    
    # Avec root (si disponible)
    & $ADB shell "su -c 'cat /data/misc/wifi/WifiConfigStore.xml' 2>/dev/null" | Select-String -Pattern "SSID|PreSharedKey"
    
    Read-Host "`nAppuyez sur Entree"
}

# ============================================================================
# FONCTIONS DE CONTROLE
# ============================================================================

function Install-APK {
    Write-Host "`n=== INSTALLER UNE APK ===" -ForegroundColor Cyan
    
    $apkPath = Read-Host "Chemin de l'APK"
    
    if (Test-Path $apkPath) {
        Write-Host "[+] Installation en cours..." -ForegroundColor Yellow
        & $ADB install -r $apkPath
        Write-Host "[+] Installation terminee!" -ForegroundColor Green
    } else {
        Write-Host "[-] Fichier non trouve!" -ForegroundColor Red
    }
    
    Read-Host "`nAppuyez sur Entree"
}

function Uninstall-App {
    Write-Host "`n=== DESINSTALLER UNE APP ===" -ForegroundColor Cyan
    
    # Lister les apps
    Write-Host "[+] Applications tierces:" -ForegroundColor Yellow
    & $ADB shell "pm list packages -3" | ForEach-Object { Write-Host ($_ -replace "package:", "  - ") }
    
    $package = Read-Host "`nPackage a desinstaller"
    
    if ($package) {
        & $ADB shell "pm uninstall $package"
        Write-Host "[+] Desinstallation terminee!" -ForegroundColor Green
    }
    
    Read-Host "`nAppuyez sur Entree"
}

function Grant-Permission {
    Write-Host "`n=== ACCORDER DES PERMISSIONS ===" -ForegroundColor Cyan
    
    $package = Read-Host "Package (ex: com.whatsapp)"
    
    Write-Host "`nPermissions disponibles:" -ForegroundColor Yellow
    Write-Host "  1. READ_SMS"
    Write-Host "  2. READ_CONTACTS"
    Write-Host "  3. ACCESS_FINE_LOCATION"
    Write-Host "  4. CAMERA"
    Write-Host "  5. RECORD_AUDIO"
    Write-Host "  6. READ_CALL_LOG"
    Write-Host "  7. Personnalisee"
    
    $choice = Read-Host "Choix"
    
    $perm = switch ($choice) {
        "1" { "android.permission.READ_SMS" }
        "2" { "android.permission.READ_CONTACTS" }
        "3" { "android.permission.ACCESS_FINE_LOCATION" }
        "4" { "android.permission.CAMERA" }
        "5" { "android.permission.RECORD_AUDIO" }
        "6" { "android.permission.READ_CALL_LOG" }
        "7" { Read-Host "Permission complete" }
    }
    
    if ($perm) {
        & $ADB shell "pm grant $package $perm"
        Write-Host "[+] Permission accordee!" -ForegroundColor Green
    }
    
    Read-Host "`nAppuyez sur Entree"
}

function Send-Input {
    Write-Host "`n=== ENVOYER DES TOUCHES/TEXTE ===" -ForegroundColor Cyan
    
    Write-Host "[1] Envoyer du texte"
    Write-Host "[2] Appuyer sur une touche"
    Write-Host "[3] Tap sur l'ecran (x,y)"
    Write-Host "[4] Swipe"
    
    $choice = Read-Host "Choix"
    
    switch ($choice) {
        "1" {
            $text = Read-Host "Texte a envoyer"
            $escaped = $text -replace " ", "%s"
            & $ADB shell "input text '$escaped'"
        }
        "2" {
            Write-Host "Codes: 3=Home, 4=Back, 26=Power, 24/25=Volume" -ForegroundColor Yellow
            $key = Read-Host "Code touche"
            & $ADB shell "input keyevent $key"
        }
        "3" {
            $x = Read-Host "Position X"
            $y = Read-Host "Position Y"
            & $ADB shell "input tap $x $y"
        }
        "4" {
            Write-Host "Swipe de (x1,y1) vers (x2,y2)" -ForegroundColor Yellow
            $coords = Read-Host "x1 y1 x2 y2"
            & $ADB shell "input swipe $coords"
        }
    }
    
    Write-Host "[+] Commande envoyee!" -ForegroundColor Green
    Read-Host "`nAppuyez sur Entree"
}

function Start-Shell {
    Write-Host "`n=== SHELL INTERACTIF ===" -ForegroundColor Cyan
    Write-Host "Tapez 'exit' pour quitter`n" -ForegroundColor Yellow
    
    & $ADB shell
    
    Read-Host "`nAppuyez sur Entree"
}

# ============================================================================
# EXTRACTION COMPLETE
# ============================================================================

function Extract-Everything {
    Write-Host "`n=== EXTRACTION COMPLETE ===" -ForegroundColor Red
    Write-Host "Cette operation va extraire TOUTES les donnees accessibles.`n" -ForegroundColor Yellow
    
    $confirm = Read-Host "Confirmer? (oui/non)"
    
    if ($confirm -eq "oui") {
        Write-Host "`n[1/8] SMS..." -ForegroundColor Cyan
        $inbox = & $ADB shell "content query --uri content://sms/inbox 2>/dev/null"
        $sent = & $ADB shell "content query --uri content://sms/sent 2>/dev/null"
        $inbox | Out-File "$OutputDir\sms_inbox.txt" -Encoding UTF8
        $sent | Out-File "$OutputDir\sms_sent.txt" -Encoding UTF8
        
        Write-Host "[2/8] Contacts..." -ForegroundColor Cyan
        $contacts = & $ADB shell "content query --uri content://contacts/phones 2>/dev/null"
        $contacts | Out-File "$OutputDir\contacts.txt" -Encoding UTF8
        
        Write-Host "[3/8] Appels..." -ForegroundColor Cyan
        $calls = & $ADB shell "content query --uri content://call_log/calls 2>/dev/null"
        $calls | Out-File "$OutputDir\call_log.txt" -Encoding UTF8
        
        Write-Host "[4/8] Infos systeme..." -ForegroundColor Cyan
        & $ADB shell "getprop" | Out-File "$OutputDir\system_props.txt" -Encoding UTF8
        
        Write-Host "[5/8] Applications..." -ForegroundColor Cyan
        & $ADB shell "pm list packages -3" | Out-File "$OutputDir\apps.txt" -Encoding UTF8
        
        Write-Host "[6/8] WhatsApp..." -ForegroundColor Cyan
        & $ADB pull "/sdcard/WhatsApp" "$OutputDir\WhatsApp" 2>$null
        
        Write-Host "[7/8] Photos DCIM..." -ForegroundColor Cyan
        & $ADB pull "/sdcard/DCIM" "$OutputDir\DCIM" 2>$null
        
        Write-Host "[8/8] Downloads..." -ForegroundColor Cyan
        & $ADB pull "/sdcard/Download" "$OutputDir\Download" 2>$null
        
        Write-Host "`n========================================" -ForegroundColor Green
        Write-Host "EXTRACTION COMPLETE!" -ForegroundColor Green
        Write-Host "Dossier: $OutputDir" -ForegroundColor Yellow
        Write-Host "========================================" -ForegroundColor Green
        
        # Ouvrir le dossier
        Start-Process $OutputDir
    }
    
    Read-Host "`nAppuyez sur Entree"
}

# ============================================================================
# BOUCLE PRINCIPALE
# ============================================================================

do {
    Show-Banner
    Show-Menu
    $selection = Read-Host "Votre choix"
    
    switch ($selection) {
        "1"  { Get-SMS }
        "2"  { Get-Contacts }
        "3"  { Get-CallLog }
        "4"  { Get-WhatsApp }
        "5"  { Get-Media }
        "6"  { Take-Screenshot }
        "7"  { Record-Screen }
        "8"  { Start-LiveScreen }
        "9"  { Get-Notifications }
        "10" { Get-Location }
        "11" { Get-DeviceInfo }
        "12" { Get-InstalledApps }
        "13" { Get-AppPermissions }
        "14" { Get-Processes }
        "15" { Get-WiFiNetworks }
        "16" { Install-APK }
        "17" { Uninstall-App }
        "18" { Grant-Permission }
        "19" { Send-Input }
        "20" { Start-Shell }
        "99" { Extract-Everything }
        "0"  { Write-Host "`nAu revoir!" -ForegroundColor Yellow }
        default { Write-Host "Option invalide" -ForegroundColor Red; Start-Sleep 1 }
    }
} while ($selection -ne "0")
