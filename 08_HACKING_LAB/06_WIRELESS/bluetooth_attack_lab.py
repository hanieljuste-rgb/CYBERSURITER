#!/usr/bin/env python3
"""
📱 BLUETOOTH ATTACK LAB - Test de sécurité sur VOTRE téléphone
Environnement de test légal pour votre propre appareil

⚠️ UNIQUEMENT SUR VOS PROPRES APPAREILS !
"""

import subprocess
import socket
import os
import sys
import time
from datetime import datetime

class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
    B = '\033[94m'; M = '\033[95m'; C = '\033[96m'
    W = '\033[97m'; X = '\033[0m'; BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""
{C.R}{C.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║         📱 BLUETOOTH ATTACK LAB - TEST DE SÉCURITÉ 📱         ║
╠═══════════════════════════════════════════════════════════════╣
║    Testez la sécurité Bluetooth de VOTRE téléphone            ║
╚═══════════════════════════════════════════════════════════════╝
{C.X}
{C.R}⚠️  AVERTISSEMENT LÉGAL :{C.X}
{C.Y}   • Testez UNIQUEMENT sur vos propres appareils
   • Toute attaque sur un appareil tiers est ILLÉGALE
   • Ce lab est à but éducatif uniquement{C.X}
""")

def check_requirements():
    """Vérifie les outils nécessaires"""
    print(f"\n{C.C}[*] Vérification des prérequis...{C.X}\n")
    
    tools = {
        'Python': True,
        'PowerShell': True,
        'Bluetooth Adapter': False
    }
    
    # Vérifier l'adaptateur Bluetooth
    try:
        result = subprocess.run([
            'powershell', '-Command',
            'Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue | Where-Object {$_.Status -eq "OK"}'
        ], capture_output=True, text=True, timeout=10)
        
        if result.stdout.strip():
            tools['Bluetooth Adapter'] = True
    except:
        pass
    
    for tool, status in tools.items():
        icon = f"{C.G}✓{C.X}" if status else f"{C.R}✗{C.X}"
        print(f"  {icon} {tool}")
    
    return all(tools.values())

def menu():
    print(f"""
{C.BOLD}═══════════════════════════════════════════════════════════════
              TESTS DE SÉCURITÉ BLUETOOTH
═══════════════════════════════════════════════════════════════{C.X}

  {C.C}[1]{C.X}  🔍 Scanner et identifier votre téléphone
  {C.C}[2]{C.X}  📡 Test de découvrabilité (votre tel visible?)
  {C.C}[3]{C.X}  📨 Test Bluejacking (envoi de message)
  {C.C}[4]{C.X}  🔓 Test de connexion OBEX
  {C.C}[5]{C.X}  📊 Analyse des services Bluetooth (SDP)
  {C.C}[6]{C.X}  🛡️  Rapport de sécurité complet
  {C.C}[7]{C.X}  📚 Comment se protéger
  
  {C.R}[0]{C.X}  Quitter

""")

def scan_for_phone():
    """Scanner pour trouver votre téléphone"""
    print(f"\n{C.C}═══ RECHERCHE DE VOTRE TÉLÉPHONE ═══{C.X}\n")
    
    print(f"{C.Y}[!] Assurez-vous que :{C.X}")
    print(f"    1. Le Bluetooth est ACTIVÉ sur votre téléphone")
    print(f"    2. Votre téléphone est en mode DÉCOUVRABLE")
    print(f"    3. Vous êtes à moins de 10 mètres\n")
    
    input(f"{C.C}Appuyez sur Entrée quand c'est prêt...{C.X}")
    
    print(f"\n{C.Y}[*] Recherche en cours...{C.X}\n")
    
    try:
        # Utiliser PowerShell pour scanner
        result = subprocess.run([
            'powershell', '-Command',
            '''
            Add-Type -AssemblyName System.Runtime.WindowsRuntime
            
            Write-Host "=== APPAREILS BLUETOOTH DÉTECTÉS ===" -ForegroundColor Cyan
            Write-Host ""
            
            # Méthode 1: PnpDevice
            $devices = Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue | 
                       Where-Object { $_.FriendlyName -notmatch "Radio|Adapter|Controller|Intel|Realtek|Broadcom" -and $_.Status -eq "OK" }
            
            $count = 0
            foreach ($device in $devices) {
                $count++
                Write-Host "[$count] $($device.FriendlyName)" -ForegroundColor Green
                
                # Essayer d'obtenir l'adresse MAC
                $instanceId = $device.InstanceId
                if ($instanceId -match "([0-9A-F]{12})") {
                    $mac = $matches[1] -replace '(.{2})(?!$)', '$1:'
                    Write-Host "    MAC: $mac" -ForegroundColor Gray
                }
                Write-Host "    Status: $($device.Status)" -ForegroundColor Gray
                Write-Host ""
            }
            
            if ($count -eq 0) {
                Write-Host "Aucun appareil trouvé." -ForegroundColor Yellow
                Write-Host "Vérifiez que votre téléphone est en mode découvrable." -ForegroundColor Yellow
            }
            
            # Méthode 2: Registry pour appareils appairés
            Write-Host "`n=== APPAREILS APPAIRÉS (Historique) ===" -ForegroundColor Cyan
            Write-Host ""
            
            $btPath = "HKLM:\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Devices"
            if (Test-Path $btPath) {
                $paired = Get-ChildItem $btPath -ErrorAction SilentlyContinue
                foreach ($p in $paired) {
                    $name = (Get-ItemProperty $p.PSPath -Name "Name" -ErrorAction SilentlyContinue).Name
                    if ($name) {
                        $nameStr = [System.Text.Encoding]::UTF8.GetString($name).Trim([char]0)
                        $mac = $p.PSChildName -replace '(.{2})(?!$)', '$1:'
                        Write-Host "[APPAIRÉ] $nameStr" -ForegroundColor Magenta
                        Write-Host "    MAC: $mac" -ForegroundColor Gray
                        Write-Host ""
                    }
                }
            }
            '''
        ], capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=30)
        
        print(result.stdout)
        
        if result.stderr:
            print(f"{C.Y}Note: {result.stderr}{C.X}")
            
    except subprocess.TimeoutExpired:
        print(f"{C.R}[!] Timeout - Le scan prend trop de temps{C.X}")
    except Exception as e:
        print(f"{C.R}[!] Erreur: {e}{C.X}")
    
    # Demander l'adresse MAC du téléphone
    print(f"\n{C.Y}[?] Entrez l'adresse MAC de VOTRE téléphone{C.X}")
    print(f"    Format: XX:XX:XX:XX:XX:XX")
    print(f"    (Trouvable dans Paramètres > À propos > Adresse Bluetooth)")
    mac = input(f"\n{C.C}Adresse MAC : {C.X}").strip().upper()
    
    if mac:
        # Sauvegarder pour les autres tests
        with open(os.path.join(os.path.dirname(__file__), 'target_device.txt'), 'w') as f:
            f.write(mac)
        print(f"\n{C.G}[+] Cible enregistrée: {mac}{C.X}")
        return mac
    return None

def test_discoverability():
    """Tester si le téléphone est découvrable"""
    print(f"\n{C.C}═══ TEST DE DÉCOUVRABILITÉ ═══{C.X}\n")
    
    print(f"""
{C.BOLD}Ce test vérifie si votre téléphone est visible aux autres.{C.X}

{C.Y}Un téléphone découvrable peut être :{C.X}
  • Scanné par n'importe qui à proximité
  • Cible potentielle d'attaques Bluetooth
  • Identifié (marque, modèle parfois visible)

{C.G}Recommandation : Mode NON-découvrable par défaut{C.X}
""")
    
    print(f"{C.Y}[*] Vérification...{C.X}\n")
    
    # Scanner pour voir si le téléphone apparaît
    try:
        result = subprocess.run([
            'powershell', '-Command',
            '''
            $ErrorActionPreference = "SilentlyContinue"
            
            # Compter les appareils Bluetooth visibles (hors adaptateurs)
            $devices = Get-PnpDevice -Class Bluetooth | 
                       Where-Object { $_.FriendlyName -notmatch "Radio|Adapter|Controller|Intel" -and $_.Status -eq "OK" }
            
            $count = ($devices | Measure-Object).Count
            
            Write-Host "Appareils Bluetooth découvrables détectés: $count" -ForegroundColor Cyan
            
            foreach ($d in $devices) {
                Write-Host "  → $($d.FriendlyName)" -ForegroundColor Yellow
            }
            '''
        ], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        print(result.stdout)
        
    except Exception as e:
        print(f"{C.R}[!] Erreur: {e}{C.X}")
    
    print(f"""
{C.BOLD}═══ RÉSULTAT DU TEST ═══{C.X}

{C.R}Si votre téléphone apparaît dans la liste :{C.X}
  ⚠️ Il est DÉCOUVRABLE = Vulnérable aux scans
  
{C.G}Si votre téléphone N'apparaît PAS :{C.X}
  ✓ Il est en mode non-découvrable = Plus sécurisé

{C.Y}Pour désactiver le mode découvrable :{C.X}
  Android: Paramètres > Bluetooth > Désactiver "Visible"
  iPhone: Le mode découvrable se désactive automatiquement
""")

def test_bluejacking():
    """Démonstration de Bluejacking (envoi de vCard)"""
    print(f"\n{C.C}═══ TEST BLUEJACKING ═══{C.X}\n")
    
    print(f"""
{C.BOLD}Qu'est-ce que le Bluejacking ?{C.X}

Le Bluejacking consiste à envoyer des messages non sollicités
via Bluetooth (vCard, contact, fichier) à des appareils proches.

{C.Y}Risques :{C.X}
  • Spam / Messages indésirables
  • Phishing (faux messages)
  • Social engineering

{C.R}Note: Windows ne supporte pas nativement l'envoi OBEX.{C.X}
{C.Y}Pour tester, vous aurez besoin de :{C.X}
  • Un téléphone Android avec une app comme "Bluetooth File Transfer"
  • Ou Kali Linux avec les outils BlueZ
""")
    
    print(f"\n{C.BOLD}═══ SIMULATION BLUEJACKING ═══{C.X}\n")
    
    # Créer un fichier vCard de test
    vcard_content = """BEGIN:VCARD
VERSION:3.0
FN:⚠️ ALERTE SÉCURITÉ
N:SÉCURITÉ;ALERTE;;;
TEL:0000000000
NOTE:Ceci est un test de sécurité Bluejacking. Si vous recevez ce message, votre Bluetooth est vulnérable aux spams.
END:VCARD"""
    
    vcard_path = os.path.join(os.path.dirname(__file__), 'test_bluejack.vcf')
    with open(vcard_path, 'w') as f:
        f.write(vcard_content)
    
    print(f"{C.G}[+] Fichier vCard de test créé: {vcard_path}{C.X}")
    
    print(f"""
{C.Y}Pour tester manuellement :{C.X}

1. Ouvrez les paramètres Bluetooth de Windows
2. Trouvez votre téléphone appairé
3. Clic droit > "Envoyer un fichier"
4. Sélectionnez le fichier: test_bluejack.vcf

{C.G}Si le fichier arrive sur votre téléphone sans confirmation :{C.X}
   ⚠️ Votre téléphone accepte les fichiers automatiquement = RISQUE

{C.G}Si une confirmation est demandée :{C.X}
   ✓ Votre téléphone demande l'autorisation = Plus sécurisé
""")
    
    # Ouvrir le dossier Bluetooth Windows
    print(f"\n{C.C}[*] Ouverture des paramètres Bluetooth...{C.X}")
    try:
        subprocess.run(['explorer', 'ms-settings:bluetooth'], shell=True)
    except:
        pass

def analyze_services():
    """Analyser les services Bluetooth exposés"""
    print(f"\n{C.C}═══ ANALYSE DES SERVICES BLUETOOTH (SDP) ═══{C.X}\n")
    
    print(f"""
{C.BOLD}Qu'est-ce que SDP ?{C.X}

SDP (Service Discovery Protocol) permet de découvrir les services
Bluetooth exposés par un appareil :
  • Transfert de fichiers (OBEX)
  • Audio (A2DP, HFP)
  • Clavier/Souris (HID)
  • Réseau (PAN)
  • etc.

{C.Y}Risques des services exposés :{C.X}
  • OBEX Push : Réception de fichiers non sollicités
  • OBEX FTP : Accès aux fichiers du téléphone
  • Serial Port : Exécution de commandes AT
""")
    
    # Lister les services Bluetooth connus sur Windows
    try:
        result = subprocess.run([
            'powershell', '-Command',
            '''
            Write-Host "=== SERVICES BLUETOOTH INSTALLÉS ===" -ForegroundColor Cyan
            Write-Host ""
            
            # Services Bluetooth Windows
            $btServices = Get-Service | Where-Object { $_.DisplayName -match "Bluetooth" }
            
            foreach ($svc in $btServices) {
                $status = if ($svc.Status -eq "Running") { "[ACTIF]" } else { "[INACTIF]" }
                $color = if ($svc.Status -eq "Running") { "Green" } else { "Gray" }
                Write-Host "$status $($svc.DisplayName)" -ForegroundColor $color
            }
            
            Write-Host ""
            Write-Host "=== PROFILS BLUETOOTH DU SYSTÈME ===" -ForegroundColor Cyan
            Write-Host ""
            
            # Profils Bluetooth
            $profiles = @(
                "A2DP (Audio)",
                "HFP (Mains-libres)", 
                "AVRCP (Télécommande)",
                "HID (Clavier/Souris)",
                "OBEX (Transfert fichiers)",
                "PAN (Réseau)"
            )
            
            foreach ($p in $profiles) {
                Write-Host "  • $p" -ForegroundColor Yellow
            }
            '''
        ], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        print(result.stdout)
        
    except Exception as e:
        print(f"{C.R}[!] Erreur: {e}{C.X}")
    
    print(f"""
{C.BOLD}═══ RECOMMANDATIONS ═══{C.X}

{C.G}Services à surveiller sur votre téléphone :{C.X}

  {C.R}⚠️ OBEX Object Push{C.X}
     Permet de recevoir des fichiers sans autorisation
     → Désactiver ou configurer pour demander confirmation

  {C.R}⚠️ OBEX File Transfer{C.X}
     Permet l'accès à vos fichiers
     → Ne jamais laisser activé en public

  {C.Y}⚡ Serial Port Profile{C.X}
     Peut exposer des commandes AT
     → Généralement désactivé par défaut
""")

def generate_security_report():
    """Générer un rapport de sécurité complet"""
    print(f"\n{C.C}═══ RAPPORT DE SÉCURITÉ BLUETOOTH ═══{C.X}\n")
    
    report = []
    score = 0
    max_score = 5
    
    print(f"{C.Y}[*] Analyse en cours...{C.X}\n")
    
    # Test 1: Service Bluetooth actif?
    try:
        result = subprocess.run([
            'powershell', '-Command',
            '(Get-Service bthserv -ErrorAction SilentlyContinue).Status'
        ], capture_output=True, text=True)
        
        if 'Running' in result.stdout:
            report.append((f"{C.Y}⚠️  Service Bluetooth actif{C.X}", 
                          "Désactivez quand non utilisé", 0))
        else:
            report.append((f"{C.G}✅ Service Bluetooth inactif{C.X}", 
                          "Bonne pratique", 1))
            score += 1
    except:
        pass
    
    # Test 2: Appareils appairés
    try:
        result = subprocess.run([
            'powershell', '-Command',
            '(Get-ChildItem "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters\\Devices" -ErrorAction SilentlyContinue | Measure-Object).Count'
        ], capture_output=True, text=True)
        
        count = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
        
        if count > 5:
            report.append((f"{C.R}❌ {count} appareils appairés{C.X}", 
                          "Trop d'appareils - nettoyez les anciens", 0))
        elif count > 0:
            report.append((f"{C.Y}⚠️  {count} appareils appairés{C.X}", 
                          "Vérifiez que vous les reconnaissez tous", 0))
        else:
            report.append((f"{C.G}✅ Aucun appareil appairé{C.X}", 
                          "Pas de risque d'usurpation", 1))
            score += 1
    except:
        pass
    
    # Afficher le rapport
    print(f"{C.BOLD}═══ RÉSULTATS ═══{C.X}\n")
    
    for check, detail, pts in report:
        print(f"  {check}")
        print(f"     └─ {detail}\n")
    
    # Score final
    percentage = (score / max_score) * 100 if max_score > 0 else 0
    
    if percentage >= 80:
        color = C.G
        status = "BONNE"
    elif percentage >= 50:
        color = C.Y
        status = "MOYENNE"
    else:
        color = C.R
        status = "FAIBLE"
    
    print(f"""
{C.BOLD}═══ SCORE DE SÉCURITÉ ═══{C.X}

  Score: {color}{score}/{max_score} ({percentage:.0f}%){C.X}
  Évaluation: {color}{status}{C.X}
""")
    
    # Sauvegarder le rapport
    report_path = os.path.join(os.path.dirname(__file__), f'bt_security_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("RAPPORT DE SÉCURITÉ BLUETOOTH\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Score: {score}/{max_score} ({percentage:.0f}%)\n")
        f.write(f"Évaluation: {status}\n\n")
        f.write("Recommandations:\n")
        f.write("- Désactiver Bluetooth quand non utilisé\n")
        f.write("- Supprimer les anciens appareils appairés\n")
        f.write("- Mode non-découvrable par défaut\n")
        f.write("- Mises à jour régulières\n")
    
    print(f"{C.G}[+] Rapport sauvegardé: {report_path}{C.X}")

def protection_tips():
    """Conseils de protection"""
    clear()
    print(f"""
{C.G}{C.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║            🛡️ PROTECTION CONTRE LES ATTAQUES BT 🛡️            ║
╚═══════════════════════════════════════════════════════════════╝
{C.X}

{C.BOLD}═══ RÈGLES D'OR ═══{C.X}

  {C.G}1.{C.X} DÉSACTIVEZ le Bluetooth quand vous ne l'utilisez pas
  
  {C.G}2.{C.X} MODE NON-DÉCOUVRABLE par défaut
     Android: Paramètres > Bluetooth > Visible désactivé
     
  {C.G}3.{C.X} REFUSEZ les demandes de connexion inconnues
     Ne jamais accepter un appairage suspect
     
  {C.G}4.{C.X} NETTOYEZ régulièrement les appareils appairés
     Supprimez ceux que vous n'utilisez plus
     
  {C.G}5.{C.X} MISES À JOUR du système et firmware
     Les patches corrigent les vulnérabilités

{C.BOLD}═══ SUR ANDROID ═══{C.X}

  • Paramètres > Connexions > Bluetooth
  • Désactiver "Visible par autres appareils"
  • Supprimer les appareils non reconnus
  • Activer uniquement pour l'appairage

{C.BOLD}═══ SUR IPHONE ═══{C.X}

  • Réglages > Bluetooth > Désactiver
  • L'iPhone n'est découvrable que dans les réglages BT
  • AirDrop : "Contacts uniquement" ou "Désactivé"

{C.BOLD}═══ SIGNES D'ATTAQUE ═══{C.X}

  {C.R}⚠️{C.X} Demandes d'appairage inattendues
  {C.R}⚠️{C.X} Fichiers reçus sans raison
  {C.R}⚠️{C.X} Batterie qui se vide vite
  {C.R}⚠️{C.X} Téléphone lent ou qui chauffe
  {C.R}⚠️{C.X} Connexions Bluetooth inconnues

{C.BOLD}═══ EN CAS DE DOUTE ═══{C.X}

  1. Désactivez immédiatement le Bluetooth
  2. Supprimez tous les appareils appairés
  3. Redémarrez le téléphone
  4. Vérifiez les apps installées récemment
  5. Changez vos mots de passe importants
""")
    input(f"\n{C.C}Appuyez sur Entrée pour continuer...{C.X}")

def main():
    clear()
    banner()
    
    if not check_requirements():
        print(f"\n{C.R}[!] Certains prérequis manquent.{C.X}")
        print(f"{C.Y}[*] Le lab fonctionnera en mode limité.{C.X}")
    
    input(f"\n{C.C}Appuyez sur Entrée pour continuer...{C.X}")
    
    while True:
        clear()
        banner()
        menu()
        
        choice = input(f"{C.C}Votre choix : {C.X}").strip()
        
        if choice == '1':
            scan_for_phone()
            input(f"\n{C.C}Appuyez sur Entrée...{C.X}")
        elif choice == '2':
            test_discoverability()
            input(f"\n{C.C}Appuyez sur Entrée...{C.X}")
        elif choice == '3':
            test_bluejacking()
            input(f"\n{C.C}Appuyez sur Entrée...{C.X}")
        elif choice == '4':
            print(f"\n{C.Y}[*] Test OBEX nécessite des outils Linux (BlueZ){C.X}")
            print(f"{C.C}[*] Installez Kali Linux en VM pour ce test{C.X}")
            input(f"\n{C.C}Appuyez sur Entrée...{C.X}")
        elif choice == '5':
            analyze_services()
            input(f"\n{C.C}Appuyez sur Entrée...{C.X}")
        elif choice == '6':
            generate_security_report()
            input(f"\n{C.C}Appuyez sur Entrée...{C.X}")
        elif choice == '7':
            protection_tips()
        elif choice == '0':
            print(f"\n{C.G}[+] Au revoir !{C.X}\n")
            break
        else:
            print(f"{C.R}[!] Choix invalide{C.X}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.Y}[!] Interruption. Au revoir !{C.X}\n")
