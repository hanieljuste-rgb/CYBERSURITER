# 🔐 GUIDE VPN PERSONNEL - Accès distant à ton téléphone
# ═══════════════════════════════════════════════════════

## 📊 TES INFORMATIONS RÉSEAU

| Élément | Valeur |
|---------|--------|
| IP Publique | 160.155.240.231 |
| IP PC (serveur VPN) | 192.168.1.13 |
| IP Téléphone | 192.168.1.2 |
| Passerelle (Box) | 192.168.1.1 |
| Port WireGuard | 51820 (UDP) |

---

## 🏗️ ARCHITECTURE

```
    INTERNET                          TON RÉSEAU LOCAL
┌──────────────┐                    ┌─────────────────────────┐
│              │     Port 51820     │                         │
│  Toi dehors  │◄──────────────────►│  PC (Serveur WireGuard) │
│  (Client)    │        VPN         │  192.168.1.13           │
│              │                    │          │              │
└──────────────┘                    │          ▼ ADB          │
                                    │  ┌─────────────────┐    │
                                    │  │ Téléphone       │    │
                                    │  │ 192.168.1.2     │    │
                                    │  └─────────────────┘    │
                                    └─────────────────────────┘
```

---

## 📋 ÉTAPES DE CONFIGURATION

### ÉTAPE 1: Installer WireGuard sur Windows

1. Télécharge WireGuard: https://www.wireguard.com/install/
2. Ou via winget:
```powershell
winget install WireGuard.WireGuard
```

### ÉTAPE 2: Générer les clés

Après installation, ouvre PowerShell en admin:
```powershell
cd "C:\Program Files\WireGuard"
.\wg.exe genkey > server_private.key
Get-Content server_private.key | .\wg.exe pubkey > server_public.key
.\wg.exe genkey > client_private.key
Get-Content client_private.key | .\wg.exe pubkey > client_public.key
```

### ÉTAPE 3: Configuration Serveur (sur ton PC)

Crée le fichier `wg0.conf`:
```ini
[Interface]
PrivateKey = <CONTENU_DE_server_private.key>
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = netsh interface ipv4 set interface "wg0" forwarding=enabled
PostDown = netsh interface ipv4 set interface "wg0" forwarding=disabled

[Peer]
# Client (toi quand tu es dehors)
PublicKey = <CONTENU_DE_client_public.key>
AllowedIPs = 10.0.0.2/32
```

### ÉTAPE 4: Configuration Client (sur ton laptop/téléphone externe)

```ini
[Interface]
PrivateKey = <CONTENU_DE_client_private.key>
Address = 10.0.0.2/24
DNS = 8.8.8.8

[Peer]
# Serveur (ton PC maison)
PublicKey = <CONTENU_DE_server_public.key>
AllowedIPs = 192.168.1.0/24, 10.0.0.0/24
Endpoint = 160.155.240.231:51820
PersistentKeepalive = 25
```

### ÉTAPE 5: Ouvrir le port sur ta Box

1. Accède à ta box: http://192.168.1.1
2. Trouve "Redirection de ports" ou "Port forwarding"
3. Ajoute:
   - Port externe: 51820
   - Port interne: 51820
   - Protocole: UDP
   - IP destination: 192.168.1.13

### ÉTAPE 6: Activer IP Forwarding Windows

PowerShell (Admin):
```powershell
# Activer le routage IP
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" -Name "IPEnableRouter" -Value 1

# Redémarrer le service
Restart-Service RemoteAccess
```

### ÉTAPE 7: Règle Firewall

```powershell
New-NetFirewallRule -DisplayName "WireGuard VPN" -Direction Inbound -Protocol UDP -LocalPort 51820 -Action Allow
```

---

## 📱 UTILISATION DEPUIS L'EXTÉRIEUR

Une fois connecté au VPN:

```powershell
# Tu seras sur le réseau 10.0.0.x mais tu pourras accéder à 192.168.1.x

# Connecter au téléphone
adb connect 192.168.1.2:5555

# Vérifier
adb devices

# Utiliser normalement
adb shell
```

---

## ⚠️ IMPORTANT - IP DYNAMIQUE

Si ton IP publique (160.155.240.231) change:

### Solution 1: DynDNS gratuit
1. Crée un compte sur https://www.noip.com/
2. Crée un hostname: monvpn.ddns.net
3. Installe leur client sur ton PC
4. Utilise ce hostname au lieu de l'IP

### Solution 2: Vérifier l'IP
```powershell
# Script pour vérifier ton IP actuelle
(Invoke-WebRequest "https://api.ipify.org").Content
```

---

## 🚀 ALTERNATIVE PLUS SIMPLE: TAILSCALE

Tailscale est un VPN mesh qui gère tout automatiquement!

### Installation:
```powershell
winget install tailscale.tailscale
```

### Configuration:
1. Installe Tailscale sur ton PC
2. Installe Tailscale sur ton téléphone (Play Store)
3. Connecte les deux au même compte
4. Ils se voient automatiquement!

### Avantages:
- ✅ Pas de port forwarding
- ✅ Pas de configuration complexe
- ✅ Fonctionne partout (même derrière NAT)
- ✅ Gratuit pour usage personnel

---

## 📊 COMPARAISON DES SOLUTIONS

| Solution | Difficulté | Avantages | Inconvénients |
|----------|------------|-----------|---------------|
| WireGuard | ⭐⭐⭐ | Contrôle total, Rapide | Configuration manuelle |
| Tailscale | ⭐ | Super simple | Dépend d'un service tiers |
| OpenVPN | ⭐⭐⭐⭐ | Très configurable | Plus lent, complexe |
| ZeroTier | ⭐⭐ | Réseau virtuel | Performance moyenne |

---

## 🔧 DÉPANNAGE

### Le VPN ne se connecte pas
```powershell
# Vérifier que WireGuard tourne
Get-Service WireGuardTunnel*

# Tester le port
Test-NetConnection -ComputerName 160.155.240.231 -Port 51820 -InformationLevel Detailed
```

### Impossible d'accéder au réseau local
- Vérifie que IP Forwarding est activé
- Vérifie les règles firewall
- Vérifie que AllowedIPs inclut 192.168.1.0/24

---

## 📁 FICHIERS GÉNÉRÉS

Les configurations seront dans:
`C:\Users\davis\OneDrive\Bureau\HACKING\VPN_Config\`
