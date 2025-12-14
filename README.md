# 🔐 HACKING LAB - GUIDE D'UTILISATION

## 📁 STRUCTURE DES DOSSIERS

```
HACKING/
│
├── 01_CONTROLE_TELEPHONE/          ← Outils pour contrôler VOTRE téléphone
│   ├── OUTIL_COMPLET_TELEPHONE.py  ★ OUTIL PRINCIPAL (extraction, surveillance)
│   ├── AndroidLab/                 ← Scripts Android
│   ├── MonitorPhone/               ← Monitoring PowerShell
│   └── PhoneTools/                 ← Outils divers
│
├── 02_EXTRACTION_DONNEES/          ← Données extraites de vos appareils
│   ├── TECNO_CK6/                  ← Données de votre téléphone
│   ├── DONNEES_VOLEES/             ← Anciennes extractions
│   └── WhatsApp_Backup/            ← Backups WhatsApp
│
├── 03_RESEAU_ET_VPN/               ← Configuration réseau et VPN
│   ├── VPN_Config/                 ← Config WireGuard
│   ├── VPN_GUIDE.md                ← Guide VPN
│   └── SecurityScripts/            ← Scripts réseau
│
├── 04_PHISHING_ET_TESTS/           ← Apprentissage sécurité
│   ├── LABO_APPRENTISSAGE_SECURITE.py  ★ COURS DE CYBERSÉCURITÉ
│   ├── PhishingDemo/               ← Démos phishing
│   ├── SecurityLab/                ← Labo vulnérabilités
│   ├── HackingTools/               ← Outils divers
│   └── PracticeLab/                ← Exercices
│
├── 05_GUIDES_ET_DOCS/              ← Documentation
│   └── GUIDE_CYBERSECURITE_COMPLET.md
│
├── 06_BACKUPS_TELEPHONES/          ← Sauvegardes
│   ├── Backup_Before_Root/
│   └── Backup_Tecno_Camon20/
│
├── 07_MTKCLIENT_FIRMWARE/          ← Firmware MediaTek
│   └── Firmware_Tecno_CK6/
│
├── mtkclient/                      ← Outil MTK (ne pas toucher)
│
└── CORBEILLE_A_TRIER/              ← Fichiers à supprimer ou trier
```

---

## 🚀 OUTILS PRINCIPAUX

### 1️⃣ Contrôle du téléphone
```powershell
# Lancer l'outil de contrôle téléphone
cd "C:\Users\davis\OneDrive\Bureau\HACKING\01_CONTROLE_TELEPHONE"
python OUTIL_COMPLET_TELEPHONE.py
```

**Fonctionnalités:**
- 📱 Extraction SMS, contacts, appels
- 📸 Capture d'écran / Enregistrement
- 📍 Localisation GPS
- 📂 Téléchargement photos/WhatsApp
- 🔔 Envoi de notifications
- 💀 Extraction complète (simulation d'attaque)

---

### 2️⃣ Laboratoire de cybersécurité
```powershell
# Lancer le labo d'apprentissage
cd "C:\Users\davis\OneDrive\Bureau\HACKING\04_PHISHING_ET_TESTS"
python LABO_APPRENTISSAGE_SECURITE.py
```

**Ce que vous apprendrez:**
- 🔍 Reconnaissance (scan de ports, DNS)
- 🔐 Mots de passe (hashing, cracking)
- 🎣 Phishing (détecter les arnaques)
- 💉 Injection SQL
- 🌐 XSS (Cross-Site Scripting)

---

## 📱 CONNEXION AU TÉLÉPHONE

### Via Tailscale (à distance)
```powershell
# Vérifier la connexion
& "C:\Program Files\Tailscale\tailscale.exe" status

# Se connecter au téléphone
adb connect 100.88.242.60:5555
```

### Via WiFi local
```powershell
adb connect 192.168.1.2:5555
```

### Via USB
Branchez le téléphone et c'est tout!

---

## 🔧 COMMANDES UTILES

```powershell
# Chemin ADB
$ADB = "C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"

# Lister les appareils
& $ADB devices -l

# Capture d'écran
& $ADB shell screencap /sdcard/screen.png
& $ADB pull /sdcard/screen.png

# Voir l'écran en direct
scrcpy

# Envoyer une notification
& $ADB shell "cmd notification post -t 'Titre' 'Message' notif1"

# Shell interactif
& $ADB shell
```

---

## 🎯 PAR OÙ COMMENCER?

1. **Débutant**: Lancez `LABO_APPRENTISSAGE_SECURITE.py` et suivez les leçons
2. **Intermédiaire**: Utilisez `OUTIL_COMPLET_TELEPHONE.py` sur votre téléphone
3. **Avancé**: Explorez les scripts dans `HackingTools/` et `SecurityLab/`

---

## ⚠️ RAPPEL IMPORTANT

Ces outils sont **UNIQUEMENT** pour:
- ✅ Apprendre la cybersécurité
- ✅ Tester sur VOS propres appareils
- ✅ Comprendre comment vous protéger

**JAMAIS** pour:
- ❌ Accéder aux appareils d'autres personnes
- ❌ Voler des données
- ❌ Activités illégales

---

*Créé le 6 décembre 2025*
