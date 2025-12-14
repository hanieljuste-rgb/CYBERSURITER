# PHONE MONITOR - Outil de monitoring ADB
# Usage legal sur VOTRE propre telephone uniquement

$ADB = "C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
$OutputDir = "C:\Users\davis\OneDrive\Bureau\HACKING\MonitorData"

if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

function Show-Menu {
    Clear-Host
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "   PHONE MONITOR - TECNO CK6" -ForegroundColor Cyan
    Write-Host "   Usage educatif sur votre propre appareil" -ForegroundColor Yellow
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  [1] Informations systeme"
    Write-Host "  [2] Liste des applications"
    Write-Host "  [3] Journal d appels"
    Write-Host "  [4] SMS (lecture)"
    Write-Host "  [5] Contacts"
    Write-Host "  [6] Capture d ecran"
    Write-Host "  [7] Explorer fichiers"
    Write-Host "  [8] Etat batterie"
    Write-Host "  [9] Connexions reseau"
    Write-Host "  [10] Derniere localisation"
    Write-Host "  [0] Quitter"
    Write-Host ""
}

function Get-SystemInfo {
    Write-Host "`nINFORMATIONS SYSTEME" -ForegroundColor Green
    Write-Host "Modele: " -NoNewline -ForegroundColor Yellow
    & $ADB shell getprop ro.product.model
    Write-Host "Android: " -NoNewline -ForegroundColor Yellow
    & $ADB shell getprop ro.build.version.release
    Write-Host "Securite: " -NoNewline -ForegroundColor Yellow
    & $ADB shell getprop ro.build.version.security_patch
    Write-Host "Fabricant: " -NoNewline -ForegroundColor Yellow
    & $ADB shell getprop ro.product.manufacturer
}

function Get-InstalledApps {
    Write-Host "`nAPPLICATIONS INSTALLEES" -ForegroundColor Green
    & $ADB shell pm list packages -3 | ForEach-Object { $_ -replace "package:", "" } | Sort-Object
}

function Get-CallLog {
    Write-Host "`nJOURNAL D APPELS" -ForegroundColor Green
    & $ADB shell "content query --uri content://call_log/calls --projection number:type:date:duration 2>/dev/null | head -20"
}

function Get-SMS {
    Write-Host "`nSMS" -ForegroundColor Green
    & $ADB shell "content query --uri content://sms/inbox --projection address:body:date 2>/dev/null | head -15"
}

function Get-Contacts {
    Write-Host "`nCONTACTS" -ForegroundColor Green
    & $ADB shell "content query --uri content://contacts/phones --projection display_name:number 2>/dev/null | head -20"
}

function Take-Screenshot {
    Write-Host "`nCAPTURE D ECRAN" -ForegroundColor Green
    $ts = Get-Date -Format "yyyyMMdd_HHmmss"
    $file = "screenshot_$ts.png"
    & $ADB shell screencap "/sdcard/$file"
    & $ADB pull "/sdcard/$file" "$OutputDir\$file"
    & $ADB shell rm "/sdcard/$file"
    Write-Host "Sauvegarde: $OutputDir\$file" -ForegroundColor Cyan
    Start-Process "$OutputDir\$file"
}

function Browse-Files {
    Write-Host "`nEXPLORATEUR FICHIERS" -ForegroundColor Green
    $path = Read-Host "Chemin (defaut /sdcard)"
    if ([string]::IsNullOrEmpty($path)) { $path = "/sdcard" }
    & $ADB shell "ls -la $path"
}

function Get-BatteryStatus {
    Write-Host "`nETAT BATTERIE" -ForegroundColor Green
    & $ADB shell dumpsys battery
}

function Get-NetworkInfo {
    Write-Host "`nCONNEXIONS RESEAU" -ForegroundColor Green
    & $ADB shell "ip addr show wlan0 2>/dev/null | grep inet"
}

function Get-Location {
    Write-Host "`nLOCALISATION" -ForegroundColor Green
    & $ADB shell "dumpsys location | grep -A 5 'last location' | head -10"
}

# Verifier connexion
$device = & $ADB devices | Select-String "device$"
if (!$device) {
    Write-Host "Aucun appareil connecte!" -ForegroundColor Red
    exit
}

Write-Host "Appareil detecte!" -ForegroundColor Green
Start-Sleep -Seconds 1

do {
    Show-Menu
    $choice = Read-Host "Option"
    
    switch ($choice) {
        "1" { Get-SystemInfo }
        "2" { Get-InstalledApps }
        "3" { Get-CallLog }
        "4" { Get-SMS }
        "5" { Get-Contacts }
        "6" { Take-Screenshot }
        "7" { Browse-Files }
        "8" { Get-BatteryStatus }
        "9" { Get-NetworkInfo }
        "10" { Get-Location }
        "0" { Write-Host "Au revoir!" -ForegroundColor Cyan }
        default { Write-Host "Option invalide" -ForegroundColor Red }
    }
    
    if ($choice -ne "0") {
        Write-Host "`nAppuyez sur Entree..." -ForegroundColor Gray
        Read-Host
    }
} while ($choice -ne "0")
