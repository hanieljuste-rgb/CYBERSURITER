# ══════════════════════════════════════════════════════════════════════════
#  📱 INFORMATIONS DE CONNEXION À DISTANCE - TECNO CK6
# ══════════════════════════════════════════════════════════════════════════

## 🔌 CONNEXION ACTUELLE

| Information | Valeur |
|-------------|--------|
| **Modèle** | TECNO CK6 |
| **Numéro de série** | 101132534I100038 |
| **IP WiFi** | 192.168.1.2 |
| **Port ADB** | 5555 |
| **WiFi SSID** | Fiberbox-2.4G-CE06 / Fiberbox-5G-CE06 |
| **MAC WiFi** | 9c:63:5b:bf:ce:08 |

---

## 🌐 POUR CONNEXION À DISTANCE (MÊME RÉSEAU WIFI)

### Étape 1: Prérequis sur le téléphone
1. ✅ Débogage USB activé
2. ✅ ADB en mode TCP/IP activé (fait!)
3. ✅ Même réseau WiFi que le PC

### Étape 2: Commande de connexion
```powershell
# Se connecter au téléphone via WiFi
adb connect 192.168.1.2:5555

# Vérifier la connexion
adb devices
```

### Étape 3: Utilisation
```powershell
# Toutes les commandes ADB fonctionnent maintenant sans câble!
adb -s 192.168.1.2:5555 shell
adb -s 192.168.1.2:5555 pull /sdcard/DCIM/
adb -s 192.168.1.2:5555 shell screencap -p /sdcard/screen.png
```

---

## ⚠️ LIMITATIONS DE LA CONNEXION WiFi/ADB

| Ce qui fonctionne | Ce qui NE fonctionne PAS |
|-------------------|--------------------------|
| ✅ Exécuter des commandes shell | ❌ Connexion depuis Internet |
| ✅ Transférer des fichiers | ❌ Connexion hors du réseau local |
| ✅ Installer des APK | ❌ Après redémarrage du téléphone |
| ✅ Prendre des screenshots | ❌ Si le WiFi change |
| ✅ Lire SMS/Contacts/etc | ❌ Sans débogage USB activé |

---

## 🌍 CONNEXION DEPUIS INTERNET (HORS RÉSEAU LOCAL)

Pour contrôler le téléphone depuis n'importe où dans le monde, tu as besoin de:

### Option 1: Port Forwarding (routeur)
1. Accéder à ta box (192.168.1.1)
2. Rediriger le port externe → 192.168.1.2:5555
3. Utiliser ton IP publique

### Option 2: VPN (recommandé)
1. Installer un serveur VPN chez toi (WireGuard, OpenVPN)
2. Te connecter au VPN depuis n'importe où
3. Utiliser l'IP locale 192.168.1.2:5555

### Option 3: Tunnel SSH/Ngrok
```bash
# Avec ngrok (nécessite installation sur un PC local allumé)
ngrok tcp 192.168.1.2:5555
```

### Option 4: Applications RAT/Spyware (ILLÉGAL sur appareils d'autrui)
- AhMyth, AndroRAT, etc.
- ⚠️ À utiliser UNIQUEMENT sur TON propre appareil

---

## 📋 INFORMATIONS IMPORTANTES À NOTER

```
╔═══════════════════════════════════════════════════════════╗
║  GARDE CES INFORMATIONS POUR CONNEXION FUTURE:            ║
╠═══════════════════════════════════════════════════════════╣
║  IP Téléphone:     192.168.1.2                            ║
║  Port ADB:         5555                                   ║
║  Commande:         adb connect 192.168.1.2:5555           ║
║  WiFi requis:      Fiberbox-2.4G-CE06                     ║
║  Série:            101132534I100038                       ║
╚═══════════════════════════════════════════════════════════╝
```

---

## ⚠️ SI LA CONNEXION EST PERDUE

```powershell
# 1. Reconnecter le câble USB
# 2. Réactiver le mode TCP/IP
adb tcpip 5555

# 3. Déconnecter le câble
# 4. Se reconnecter en WiFi
adb connect 192.168.1.2:5555
```

---

## 🔐 SÉCURITÉ

- Le débogage USB est un **risque de sécurité**
- Désactive-le quand tu ne l'utilises pas
- Ne te connecte pas à des WiFi publics avec ADB actif
- Révoque les autorisations ADB régulièrement
