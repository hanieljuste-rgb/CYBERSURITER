#!/usr/bin/env python3
"""
📶 BLUETOOTH SECURITY SCANNER - Outil Éducatif
Scanner et analyseur de sécurité Bluetooth

⚠️ USAGE LÉGAL UNIQUEMENT - Scannez uniquement VOS appareils !
"""

import subprocess
import sys
import os
import re
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║           📶 BLUETOOTH SECURITY SCANNER 📶                    ║
╠═══════════════════════════════════════════════════════════════╣
║     Analyse de sécurité Bluetooth - Usage éducatif            ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.YELLOW}⚠️  AVERTISSEMENT : Scannez UNIQUEMENT vos propres appareils !{Colors.RESET}
{Colors.RED}    L'accès non autorisé à des appareils est ILLÉGAL.{Colors.RESET}
""")

def menu():
    print(f"""
{Colors.BOLD}═══════════════════════════════════════════════════════════════
                    OUTILS BLUETOOTH
═══════════════════════════════════════════════════════════════{Colors.RESET}

  {Colors.CYAN}[1]{Colors.RESET}  📡 Scanner les appareils Bluetooth à proximité
  {Colors.CYAN}[2]{Colors.RESET}  🔍 Voir les appareils appairés sur ce PC
  {Colors.CYAN}[3]{Colors.RESET}  📊 Informations sur votre adaptateur Bluetooth
  {Colors.CYAN}[4]{Colors.RESET}  🛡️  Vérifier la sécurité de votre config
  {Colors.CYAN}[5]{Colors.RESET}  📚 Apprendre les attaques Bluetooth
  {Colors.CYAN}[6]{Colors.RESET}  🔒 Guide de protection
  
  {Colors.RED}[0]{Colors.RESET}  ❌ Quitter

""")

def scan_bluetooth_devices():
    """Scanner les appareils Bluetooth à proximité (Windows)"""
    print(f"\n{Colors.CYAN}═══ SCAN DES APPAREILS BLUETOOTH ═══{Colors.RESET}\n")
    print(f"{Colors.YELLOW}[*] Recherche des appareils Bluetooth...{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Cela peut prendre quelques secondes...{Colors.RESET}\n")
    
    try:
        # Méthode 1: PowerShell Get-PnpDevice
        result = subprocess.run([
            'powershell', '-Command',
            '''
            Write-Host "`n=== APPAREILS BLUETOOTH DÉTECTÉS ===" -ForegroundColor Cyan
            
            # Appareils Bluetooth connectés ou connus
            $btDevices = Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue | 
                         Where-Object { $_.FriendlyName -notlike "*Radio*" -and $_.FriendlyName -notlike "*Adapter*" }
            
            if ($btDevices) {
                $btDevices | ForEach-Object {
                    $status = if ($_.Status -eq "OK") { "[CONNECTÉ]" } else { "[CONNU]" }
                    Write-Host "$status $($_.FriendlyName)" -ForegroundColor Green
                    Write-Host "   Device ID: $($_.InstanceId)" -ForegroundColor Gray
                }
            } else {
                Write-Host "Aucun appareil Bluetooth trouvé" -ForegroundColor Yellow
            }
            
            Write-Host "`n=== APPAREILS AUDIO BLUETOOTH ===" -ForegroundColor Cyan
            $audioDevices = Get-PnpDevice -Class AudioEndpoint -ErrorAction SilentlyContinue |
                           Where-Object { $_.FriendlyName -match "Bluetooth|BT|Wireless" }
            
            if ($audioDevices) {
                $audioDevices | ForEach-Object {
                    Write-Host "[AUDIO] $($_.FriendlyName)" -ForegroundColor Magenta
                }
            }
            '''
        ], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        print(result.stdout)
        if result.stderr:
            print(f"{Colors.YELLOW}Note: {result.stderr}{Colors.RESET}")
            
    except Exception as e:
        print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Assurez-vous que le Bluetooth est activé{Colors.RESET}")

def get_paired_devices():
    """Afficher les appareils appairés"""
    print(f"\n{Colors.CYAN}═══ APPAREILS BLUETOOTH APPAIRÉS ═══{Colors.RESET}\n")
    
    try:
        result = subprocess.run([
            'powershell', '-Command',
            '''
            $btFolderPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters\\Devices"
            
            if (Test-Path $btFolderPath) {
                $devices = Get-ChildItem -Path $btFolderPath -ErrorAction SilentlyContinue
                
                Write-Host "Appareils appairés trouvés: $($devices.Count)" -ForegroundColor Green
                Write-Host ""
                
                foreach ($device in $devices) {
                    $name = (Get-ItemProperty -Path $device.PSPath -Name "Name" -ErrorAction SilentlyContinue).Name
                    $mac = $device.PSChildName -replace '(.{2})(?!$)', '$1:'
                    
                    if ($name) {
                        $nameStr = [System.Text.Encoding]::UTF8.GetString($name)
                        Write-Host "[APPAIRÉ] $nameStr" -ForegroundColor Cyan
                        Write-Host "   MAC: $mac" -ForegroundColor Gray
                        Write-Host ""
                    }
                }
            } else {
                Write-Host "Aucun appareil appairé trouvé ou Bluetooth désactivé" -ForegroundColor Yellow
            }
            '''
        ], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        print(result.stdout)
        
    except Exception as e:
        print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")

def get_adapter_info():
    """Informations sur l'adaptateur Bluetooth"""
    print(f"\n{Colors.CYAN}═══ INFORMATIONS ADAPTATEUR BLUETOOTH ═══{Colors.RESET}\n")
    
    try:
        result = subprocess.run([
            'powershell', '-Command',
            '''
            $adapter = Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue | 
                       Where-Object { $_.FriendlyName -like "*Radio*" -or $_.FriendlyName -like "*Adapter*" }
            
            if ($adapter) {
                Write-Host "[ADAPTATEUR] $($adapter.FriendlyName)" -ForegroundColor Green
                Write-Host "   Status: $($adapter.Status)" -ForegroundColor $(if($adapter.Status -eq "OK"){"Green"}else{"Red"})
                Write-Host "   Device ID: $($adapter.InstanceId)" -ForegroundColor Gray
                
                # Vérifier si Bluetooth est activé
                $btService = Get-Service -Name bthserv -ErrorAction SilentlyContinue
                if ($btService) {
                    Write-Host "`n[SERVICE] Bluetooth Support Service" -ForegroundColor Cyan
                    Write-Host "   Status: $($btService.Status)" -ForegroundColor $(if($btService.Status -eq "Running"){"Green"}else{"Yellow"})
                }
            } else {
                Write-Host "Aucun adaptateur Bluetooth trouvé" -ForegroundColor Red
            }
            
            # Vérifier le mode découverte
            Write-Host "`n[SÉCURITÉ] Vérification du mode découverte..." -ForegroundColor Yellow
            $regPath = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Bluetooth"
            '''
        ], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        print(result.stdout)
        
    except Exception as e:
        print(f"{Colors.RED}[!] Erreur: {e}{Colors.RESET}")

def check_security():
    """Vérifier la configuration de sécurité Bluetooth"""
    print(f"\n{Colors.CYAN}═══ ANALYSE DE SÉCURITÉ BLUETOOTH ═══{Colors.RESET}\n")
    
    checks = []
    
    # Check 1: Service Bluetooth
    try:
        result = subprocess.run([
            'powershell', '-Command',
            '(Get-Service -Name bthserv -ErrorAction SilentlyContinue).Status'
        ], capture_output=True, text=True)
        
        if 'Running' in result.stdout:
            checks.append((f"{Colors.YELLOW}⚠️  Service Bluetooth actif", 
                          "Désactivez-le quand non utilisé"))
        else:
            checks.append((f"{Colors.GREEN}✅ Service Bluetooth inactif", "OK"))
    except:
        pass
    
    # Afficher les résultats
    print(f"{Colors.BOLD}Résultats de l'analyse :{Colors.RESET}\n")
    
    for check, detail in checks:
        print(f"  {check}{Colors.RESET}")
        print(f"     └─ {detail}\n")
    
    # Recommandations
    print(f"""
{Colors.BOLD}═══ RECOMMANDATIONS DE SÉCURITÉ ═══{Colors.RESET}

  {Colors.GREEN}✓{Colors.RESET} Désactivez le Bluetooth quand vous ne l'utilisez pas
  {Colors.GREEN}✓{Colors.RESET} Mettez votre appareil en mode "non découvrable"
  {Colors.GREEN}✓{Colors.RESET} N'acceptez jamais d'appairage de sources inconnues
  {Colors.GREEN}✓{Colors.RESET} Supprimez les anciens appareils appairés non utilisés
  {Colors.GREEN}✓{Colors.RESET} Gardez votre système à jour (patches de sécurité)
  {Colors.GREEN}✓{Colors.RESET} Évitez d'utiliser le Bluetooth dans les lieux publics
""")

def learn_attacks():
    """Apprendre les différentes attaques Bluetooth"""
    clear()
    print(f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║            📚 ATTAQUES BLUETOOTH - ÉDUCATION 📚               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.RED}⚠️ INFORMATION ÉDUCATIVE UNIQUEMENT - NE PAS REPRODUIRE !{Colors.RESET}

{Colors.BOLD}═══ 1. BLUEJACKING (Faible risque) ═══{Colors.RESET}
{Colors.CYAN}Description:{Colors.RESET} Envoi de messages non sollicités via Bluetooth
{Colors.YELLOW}Comment:{Colors.RESET} L'attaquant envoie une vCard ou message à des appareils découvrables
{Colors.GREEN}Protection:{Colors.RESET} Mode non-découvrable, refuser les connexions inconnues

{Colors.BOLD}═══ 2. BLUESNARFING (Risque élevé) ═══{Colors.RESET}
{Colors.CYAN}Description:{Colors.RESET} Vol de données (contacts, SMS, emails, photos)
{Colors.YELLOW}Comment:{Colors.RESET} Exploitation de failles OBEX pour accéder aux fichiers
{Colors.GREEN}Protection:{Colors.RESET} Mises à jour, désactiver Bluetooth, mode non-découvrable

{Colors.BOLD}═══ 3. BLUEBUGGING (Risque critique) ═══{Colors.RESET}
{Colors.CYAN}Description:{Colors.RESET} Prise de contrôle totale du téléphone
{Colors.YELLOW}Comment:{Colors.RESET} Accès aux commandes AT du modem via Bluetooth
{Colors.GREEN}Protection:{Colors.RESET} Firmware à jour, ne jamais appairer avec des inconnus

{Colors.BOLD}═══ 4. BLUBORNE (CVE-2017-0781) ═══{Colors.RESET}
{Colors.CYAN}Description:{Colors.RESET} Attaque sans appairage, propagation automatique
{Colors.YELLOW}Comment:{Colors.RESET} Exploitation de failles dans la pile Bluetooth
{Colors.GREEN}Protection:{Colors.RESET} MISES À JOUR CRITIQUES (corrigé depuis 2017)

{Colors.BOLD}═══ 5. KNOB ATTACK (2019) ═══{Colors.RESET}
{Colors.CYAN}Description:{Colors.RESET} Affaiblissement du chiffrement Bluetooth
{Colors.YELLOW}Comment:{Colors.RESET} Force une clé de chiffrement de 1 octet seulement
{Colors.GREEN}Protection:{Colors.RESET} Mises à jour firmware, éviter les lieux publics

{Colors.BOLD}═══ 6. BIAS ATTACK (2020) ═══{Colors.RESET}
{Colors.CYAN}Description:{Colors.RESET} Usurpation d'identité d'un appareil appairé
{Colors.YELLOW}Comment:{Colors.RESET} Contourne l'authentification Bluetooth Classic
{Colors.GREEN}Protection:{Colors.RESET} Supprimer les anciens appairages, mises à jour

{Colors.BOLD}═══ 7. BRAKTOOTH (2021) ═══{Colors.RESET}
{Colors.CYAN}Description:{Colors.RESET} Famille de 16 vulnérabilités Bluetooth
{Colors.YELLOW}Comment:{Colors.RESET} Crash, freeze ou exécution de code à distance
{Colors.GREEN}Protection:{Colors.RESET} Patches constructeurs, désactiver si non nécessaire

""")
    input(f"\n{Colors.CYAN}Appuyez sur Entrée pour continuer...{Colors.RESET}")

def protection_guide():
    """Guide de protection Bluetooth"""
    clear()
    print(f"""
{Colors.GREEN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║              🛡️ GUIDE DE PROTECTION BLUETOOTH 🛡️              ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.BOLD}═══ RÈGLES DE BASE ═══{Colors.RESET}

  {Colors.GREEN}[1]{Colors.RESET} DÉSACTIVEZ quand non utilisé
      └─ Le Bluetooth actif = surface d'attaque ouverte
      
  {Colors.GREEN}[2]{Colors.RESET} MODE NON-DÉCOUVRABLE par défaut
      └─ Rend votre appareil invisible aux scans
      
  {Colors.GREEN}[3]{Colors.RESET} REFUSEZ les appairages suspects
      └─ Ne jamais accepter une connexion inconnue
      
  {Colors.GREEN}[4]{Colors.RESET} NETTOYEZ vos appairages
      └─ Supprimez les anciens appareils non utilisés
      
  {Colors.GREEN}[5]{Colors.RESET} MISES À JOUR régulières
      └─ Les patches corrigent les vulnérabilités

{Colors.BOLD}═══ COMMENT DÉSACTIVER LE BLUETOOTH ═══{Colors.RESET}

{Colors.CYAN}Windows:{Colors.RESET}
  • Paramètres → Appareils → Bluetooth → Désactiver
  • Ou : Win+A → Cliquer sur l'icône Bluetooth

{Colors.CYAN}Android:{Colors.RESET}
  • Balayer vers le bas → Icône Bluetooth → Désactiver
  • Paramètres → Connexions → Bluetooth → Off

{Colors.CYAN}iPhone:{Colors.RESET}
  • Réglages → Bluetooth → Désactiver
  • Control Center pour désactivation temporaire

{Colors.BOLD}═══ VÉRIFIER LES APPAIRAGES (Android) ═══{Colors.RESET}

  1. Paramètres → Connexions → Bluetooth
  2. Voir "Appareils appairés"
  3. Supprimer ceux que vous ne reconnaissez pas

{Colors.BOLD}═══ SIGNES D'UNE ATTAQUE BLUETOOTH ═══{Colors.RESET}

  {Colors.RED}⚠️{Colors.RESET} Demandes d'appairage inattendues
  {Colors.RED}⚠️{Colors.RESET} Messages ou fichiers reçus sans raison
  {Colors.RED}⚠️{Colors.RESET} Batterie qui se vide rapidement
  {Colors.RED}⚠️{Colors.RESET} Données mobiles utilisées sans raison
  {Colors.RED}⚠️{Colors.RESET} Appareil lent ou qui chauffe anormalement

""")
    input(f"\n{Colors.CYAN}Appuyez sur Entrée pour continuer...{Colors.RESET}")

def main():
    while True:
        clear()
        banner()
        menu()
        
        choice = input(f"{Colors.CYAN}Votre choix : {Colors.RESET}").strip()
        
        if choice == '1':
            scan_bluetooth_devices()
            input(f"\n{Colors.CYAN}Appuyez sur Entrée pour continuer...{Colors.RESET}")
        elif choice == '2':
            get_paired_devices()
            input(f"\n{Colors.CYAN}Appuyez sur Entrée pour continuer...{Colors.RESET}")
        elif choice == '3':
            get_adapter_info()
            input(f"\n{Colors.CYAN}Appuyez sur Entrée pour continuer...{Colors.RESET}")
        elif choice == '4':
            check_security()
            input(f"\n{Colors.CYAN}Appuyez sur Entrée pour continuer...{Colors.RESET}")
        elif choice == '5':
            learn_attacks()
        elif choice == '6':
            protection_guide()
        elif choice == '0':
            print(f"\n{Colors.GREEN}[+] Au revoir !{Colors.RESET}\n")
            break
        else:
            print(f"{Colors.RED}[!] Choix invalide{Colors.RESET}")
            input(f"\n{Colors.CYAN}Appuyez sur Entrée...{Colors.RESET}")

if __name__ == "__main__":
    main()
