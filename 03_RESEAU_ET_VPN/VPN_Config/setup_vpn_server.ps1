# ═══════════════════════════════════════════════════════════════════
#  🔐 SCRIPT DE CONFIGURATION VPN WIREGUARD - À exécuter en ADMIN
# ═══════════════════════════════════════════════════════════════════

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║  🔐 CONFIGURATION VPN WIREGUARD                                    ║
║  Ce script va configurer ton PC comme serveur VPN                  ║
╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# Vérifier les droits admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'Administrateur!" -ForegroundColor Red
    Write-Host "   Clic droit -> Exécuter en tant qu'administrateur" -ForegroundColor Yellow
    pause
    exit
}

Write-Host "✅ Droits administrateur confirmés" -ForegroundColor Green

# 1. Activer le routage IP
Write-Host "`n[1/5] Activation du routage IP..." -ForegroundColor Yellow
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "IPEnableRouter" -Value 1
Write-Host "    ✅ Routage IP activé" -ForegroundColor Green

# 2. Créer la règle firewall
Write-Host "`n[2/5] Configuration du firewall..." -ForegroundColor Yellow
$ruleName = "WireGuard VPN Port 51820"
$existingRule = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
if ($existingRule) {
    Write-Host "    ⚠️ Règle existante, suppression..." -ForegroundColor Yellow
    Remove-NetFirewallRule -DisplayName $ruleName
}
New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Protocol UDP -LocalPort 51820 -Action Allow | Out-Null
New-NetFirewallRule -DisplayName "$ruleName - Outbound" -Direction Outbound -Protocol UDP -LocalPort 51820 -Action Allow | Out-Null
Write-Host "    ✅ Règle firewall créée (UDP 51820)" -ForegroundColor Green

# 3. Vérifier WireGuard
Write-Host "`n[3/5] Vérification de WireGuard..." -ForegroundColor Yellow
$wgPath = "C:\Program Files\WireGuard\wireguard.exe"
if (Test-Path $wgPath) {
    Write-Host "    ✅ WireGuard installé" -ForegroundColor Green
} else {
    Write-Host "    ❌ WireGuard non trouvé!" -ForegroundColor Red
    Write-Host "    Installe-le: winget install WireGuard.WireGuard" -ForegroundColor Yellow
}

# 4. Afficher les informations
Write-Host "`n[4/5] Informations de configuration..." -ForegroundColor Yellow
$publicIP = (Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing -TimeoutSec 5).Content
$localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like "192.168.*" } | Select-Object -First 1).IPAddress

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║  📊 INFORMATIONS RÉSEAU                                            ║
╠═══════════════════════════════════════════════════════════════════╣
║  IP Publique:    $publicIP                              ║
║  IP Locale:      $localIP                                    ║
║  Port VPN:       51820 (UDP)                                      ║
║  Réseau VPN:     10.0.0.0/24                                      ║
╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# 5. Instructions pour la box
Write-Host "[5/5] IMPORTANT - Configuration de la Box Internet" -ForegroundColor Yellow
Write-Host @"

    ⚠️ Tu dois maintenant configurer le PORT FORWARDING sur ta box:
    
    1. Ouvre http://192.168.1.1 dans ton navigateur
    2. Connecte-toi à l'interface d'administration
    3. Trouve "Redirection de ports" / "Port Forwarding" / "NAT"
    4. Ajoute cette règle:
    
       ┌────────────────────────────────────────────┐
       │  Nom:           WireGuard VPN              │
       │  Port externe:  51820                      │
       │  Port interne:  51820                      │
       │  Protocole:     UDP                        │
       │  IP destination: $localIP                  │
       └────────────────────────────────────────────┘
    
    5. Sauvegarde et redémarre la box si nécessaire

"@ -ForegroundColor White

Write-Host @"
═══════════════════════════════════════════════════════════════════
  PROCHAINES ÉTAPES:
═══════════════════════════════════════════════════════════════════

  1. Configure le port forwarding sur ta box (voir ci-dessus)
  
  2. Ouvre WireGuard (cherche dans le menu démarrer)
  
  3. Importe le fichier de configuration serveur:
     C:\Users\davis\OneDrive\Bureau\HACKING\VPN_Config\wg_server.conf
  
  4. Active le tunnel
  
  5. Sur ton autre appareil (laptop/téléphone), importe:
     wg_client.conf
  
  6. Connecte-toi au VPN et teste:
     ping 192.168.1.2 (ton téléphone)
     adb connect 192.168.1.2:5555

═══════════════════════════════════════════════════════════════════

"@ -ForegroundColor Green

pause
