#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║     ██╗    ██╗ █████╗ ██╗   ██╗███████╗                                          ║
║     ██║    ██║██╔══██╗██║   ██║██╔════╝                                          ║
║     ██║ █╗ ██║███████║██║   ██║█████╗                                            ║
║     ██║███╗██║██╔══██║╚██╗ ██╔╝██╔══╝                                            ║
║     ╚███╔███╔╝██║  ██║ ╚████╔╝ ███████╗                                          ║
║      ╚══╝╚══╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝                                          ║
║                                                                                  ║
║               💸 WAVE AUTO TRANSFERT AVANCÉ v2.0 💸                              ║
║                                                                                  ║
║  Automatisation complète des transferts Wave avec capture de confirmation        ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
"""

import subprocess
import os
import sys
import time
import json
import re
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

ADB_PATH = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
DEVICE = "100.88.242.60:5555"  # IP Tailscale
OUTPUT_DIR = Path(r"C:\Users\davis\OneDrive\Bureau\HACKING\02_EXTRACTION_DONNEES\WAVE_TRANSACTIONS")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Coordonnées écran TECNO CK6 (1080x2400)
# À ajuster selon ton téléphone
COORDS = {
    'send_money_btn': (540, 800),      # Bouton "Envoyer de l'argent"
    'phone_input': (540, 600),          # Champ numéro de téléphone
    'amount_input': (540, 800),         # Champ montant
    'continue_btn': (540, 1800),        # Bouton Continuer
    'confirm_btn': (540, 2000),         # Bouton Confirmer
    'pin_field': (540, 1400),           # Champ PIN
    'cancel_btn': (100, 100),           # Bouton annuler/retour
}

# Package Wave
WAVE_PACKAGE = "com.wave.personal"

# Couleurs
class C:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Historique des transactions
TRANSACTIONS_LOG = OUTPUT_DIR / "transactions_history.json"

# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS ADB
# ═══════════════════════════════════════════════════════════════════════════════

def run_adb(command, timeout=30):
    """Exécute une commande ADB"""
    full_cmd = f'"{ADB_PATH}" -s {DEVICE} {command}'
    try:
        result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout + result.stderr, result.returncode == 0
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]", False
    except Exception as e:
        return f"[ERREUR] {e}", False

def check_connection():
    """Vérifie la connexion au téléphone"""
    output, success = run_adb("shell getprop ro.product.model")
    return "TECNO" in output or "CK6" in output, output.strip()

def tap(x, y):
    """Tape sur l'écran à la position (x, y)"""
    run_adb(f"shell input tap {x} {y}")
    time.sleep(0.3)

def swipe(x1, y1, x2, y2, duration=300):
    """Glisse sur l'écran"""
    run_adb(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")
    time.sleep(0.3)

def input_text(text):
    """Entre du texte"""
    # Échapper les caractères spéciaux
    text = text.replace(' ', '%s').replace('&', '\\&').replace('<', '\\<').replace('>', '\\>').replace("'", "\\'")
    run_adb(f'shell input text "{text}"')
    time.sleep(0.2)

def press_key(keycode):
    """Appuie sur une touche"""
    run_adb(f"shell input keyevent {keycode}")
    time.sleep(0.2)

def screenshot(filename=None):
    """Prend une capture d'écran"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = OUTPUT_DIR / f"wave_screenshot_{timestamp}.png"
    
    run_adb(f"shell screencap -p /sdcard/screen.png")
    run_adb(f"pull /sdcard/screen.png {filename}")
    run_adb("shell rm /sdcard/screen.png")
    
    return filename

def get_screen_text():
    """Récupère le texte à l'écran via UI Automator"""
    run_adb("shell uiautomator dump /sdcard/ui.xml")
    output, _ = run_adb("shell cat /sdcard/ui.xml")
    run_adb("shell rm /sdcard/ui.xml")
    return output

def wait_for_text(text, timeout=30):
    """Attend qu'un texte apparaisse à l'écran"""
    start = time.time()
    while time.time() - start < timeout:
        screen = get_screen_text()
        if text.lower() in screen.lower():
            return True
        time.sleep(1)
    return False

def is_wave_running():
    """Vérifie si Wave est au premier plan"""
    output, _ = run_adb("shell dumpsys activity activities | grep mResumedActivity")
    return WAVE_PACKAGE in output

# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS WAVE
# ═══════════════════════════════════════════════════════════════════════════════

def open_wave():
    """Ouvre l'application Wave"""
    print(f"\n    {C.CYAN}📱 Ouverture de Wave...{C.END}")
    
    run_adb(f"shell monkey -p {WAVE_PACKAGE} -c android.intent.category.LAUNCHER 1")
    time.sleep(3)
    
    if is_wave_running():
        print(f"    {C.GREEN}✓ Wave ouvert{C.END}")
        return True
    else:
        print(f"    {C.RED}✗ Échec ouverture Wave{C.END}")
        return False

def go_to_send_money():
    """Navigue vers l'écran d'envoi d'argent"""
    print(f"    {C.CYAN}💸 Navigation vers Envoyer...{C.END}")
    
    # Tap sur "Envoyer" depuis l'écran d'accueil
    tap(*COORDS['send_money_btn'])
    time.sleep(2)
    
    # Vérifier si on est sur le bon écran
    screen = get_screen_text()
    if "numéro" in screen.lower() or "phone" in screen.lower() or "envoyer" in screen.lower():
        print(f"    {C.GREEN}✓ Écran d'envoi{C.END}")
        return True
    
    return False

def enter_phone_number(phone):
    """Entre le numéro de téléphone"""
    print(f"    {C.CYAN}📞 Saisie du numéro: {phone}{C.END}")
    
    # Tap sur le champ
    tap(*COORDS['phone_input'])
    time.sleep(0.5)
    
    # Effacer le champ existant
    run_adb("shell input keyevent KEYCODE_CTRL_LEFT+KEYCODE_A")
    time.sleep(0.2)
    
    # Entrer le numéro
    input_text(phone)
    time.sleep(0.5)
    
    print(f"    {C.GREEN}✓ Numéro saisi{C.END}")
    return True

def enter_amount(amount):
    """Entre le montant"""
    print(f"    {C.CYAN}💰 Saisie du montant: {amount} FCFA{C.END}")
    
    # Tap sur le champ montant
    tap(*COORDS['amount_input'])
    time.sleep(0.5)
    
    # Entrer le montant
    input_text(str(amount))
    time.sleep(0.5)
    
    print(f"    {C.GREEN}✓ Montant saisi{C.END}")
    return True

def click_continue():
    """Clique sur Continuer"""
    print(f"    {C.CYAN}➡️ Clic sur Continuer...{C.END}")
    
    tap(*COORDS['continue_btn'])
    time.sleep(2)
    
    return True

def enter_pin(pin):
    """Entre le code PIN"""
    print(f"    {C.CYAN}🔐 Saisie du PIN...{C.END}")
    
    # Tap sur le champ PIN
    tap(*COORDS['pin_field'])
    time.sleep(0.5)
    
    # Entrer le PIN
    input_text(pin)
    time.sleep(1)
    
    print(f"    {C.GREEN}✓ PIN saisi{C.END}")
    return True

def confirm_transfer():
    """Confirme le transfert"""
    print(f"    {C.CYAN}✅ Confirmation du transfert...{C.END}")
    
    tap(*COORDS['confirm_btn'])
    time.sleep(3)
    
    # Prendre une capture de confirmation
    screenshot_file = screenshot()
    print(f"    {C.GREEN}✓ Capture de confirmation: {screenshot_file}{C.END}")
    
    return screenshot_file

def capture_confirmation():
    """Capture l'écran de confirmation"""
    print(f"\n    {C.CYAN}📸 Capture de la confirmation...{C.END}")
    
    # Attendre que l'écran de confirmation apparaisse
    time.sleep(3)
    
    # Capture
    filename = screenshot()
    
    # Récupérer le texte pour extraire les détails
    screen_text = get_screen_text()
    
    # Extraire les infos de confirmation
    confirmation_info = {
        'timestamp': datetime.now().isoformat(),
        'screenshot': str(filename),
        'screen_text': screen_text[:500] if screen_text else "N/A"
    }
    
    # Chercher le code de transaction
    trans_match = re.search(r'([A-Z0-9]{8,12})', screen_text)
    if trans_match:
        confirmation_info['transaction_id'] = trans_match.group(1)
        print(f"    {C.GREEN}✓ ID Transaction: {trans_match.group(1)}{C.END}")
    
    return confirmation_info

# ═══════════════════════════════════════════════════════════════════════════════
# TRANSFERT COMPLET
# ═══════════════════════════════════════════════════════════════════════════════

def perform_transfer(phone, amount, pin=None, auto_confirm=False):
    """Effectue un transfert complet"""
    
    print(f"\n{C.CYAN}{'═' * 60}{C.END}")
    print(f"{C.BOLD}{C.CYAN}💸 TRANSFERT WAVE{C.END}")
    print(f"{C.CYAN}{'═' * 60}{C.END}")
    print(f"    {C.WHITE}Destinataire: {phone}{C.END}")
    print(f"    {C.WHITE}Montant: {amount} FCFA{C.END}")
    print(f"{C.CYAN}{'═' * 60}{C.END}\n")
    
    transaction = {
        'timestamp': datetime.now().isoformat(),
        'phone': phone,
        'amount': amount,
        'status': 'pending',
        'screenshots': []
    }
    
    try:
        # Étape 1: Ouvrir Wave
        if not open_wave():
            transaction['status'] = 'failed'
            transaction['error'] = 'Impossible d\'ouvrir Wave'
            return transaction
        
        # Capture écran accueil
        transaction['screenshots'].append(str(screenshot()))
        
        # Étape 2: Aller à Envoyer
        if not go_to_send_money():
            print(f"    {C.YELLOW}⚠️ Navigation manuelle peut être nécessaire{C.END}")
        
        time.sleep(1)
        
        # Étape 3: Entrer le numéro
        enter_phone_number(phone)
        
        # Étape 4: Entrer le montant
        enter_amount(amount)
        
        # Capture avant confirmation
        transaction['screenshots'].append(str(screenshot()))
        
        # Étape 5: Continuer
        click_continue()
        
        # Capture de vérification
        transaction['screenshots'].append(str(screenshot()))
        
        if not auto_confirm:
            print(f"\n    {C.YELLOW}⚠️ VÉRIFIEZ L'ÉCRAN DU TÉLÉPHONE{C.END}")
            print(f"    {C.WHITE}Le transfert est prêt à être confirmé{C.END}")
            
            confirm = input(f"\n    {C.GREEN}Confirmer le transfert? (oui/non): {C.END}").strip().lower()
            
            if confirm != "oui":
                print(f"    {C.YELLOW}Transfert annulé{C.END}")
                transaction['status'] = 'cancelled'
                return transaction
        
        # Étape 6: Entrer le PIN si fourni
        if pin:
            enter_pin(pin)
        else:
            print(f"\n    {C.YELLOW}📱 Entrez votre PIN sur le téléphone{C.END}")
            input(f"    {C.CYAN}Appuyez sur Entrée une fois le PIN saisi...{C.END}")
        
        # Étape 7: Confirmer
        confirm_file = confirm_transfer()
        transaction['screenshots'].append(str(confirm_file))
        
        # Étape 8: Capturer la confirmation
        confirmation = capture_confirmation()
        transaction['confirmation'] = confirmation
        transaction['status'] = 'completed'
        
        print(f"\n    {C.GREEN}{'═' * 50}{C.END}")
        print(f"    {C.GREEN}✓ TRANSFERT EFFECTUÉ AVEC SUCCÈS!{C.END}")
        print(f"    {C.GREEN}{'═' * 50}{C.END}")
        
    except Exception as e:
        print(f"\n    {C.RED}✗ Erreur: {e}{C.END}")
        transaction['status'] = 'error'
        transaction['error'] = str(e)
    
    # Sauvegarder dans l'historique
    save_transaction(transaction)
    
    return transaction

def quick_transfer(phone, amount):
    """Transfert rapide sans confirmation interactive"""
    print(f"\n    {C.YELLOW}⚡ Mode rapide - Ouverture de Wave avec pré-remplissage{C.END}")
    
    # Ouvrir Wave avec un intent pour envoyer
    # Note: Wave ne supporte pas directement les intents, donc on simule
    
    open_wave()
    time.sleep(2)
    go_to_send_money()
    enter_phone_number(phone)
    enter_amount(amount)
    
    print(f"\n    {C.GREEN}✓ Champs pré-remplis!{C.END}")
    print(f"    {C.WHITE}Vérifiez et confirmez sur le téléphone{C.END}")

# ═══════════════════════════════════════════════════════════════════════════════
# HISTORIQUE
# ═══════════════════════════════════════════════════════════════════════════════

def save_transaction(transaction):
    """Sauvegarde une transaction dans l'historique"""
    
    history = []
    
    if TRANSACTIONS_LOG.exists():
        try:
            with open(TRANSACTIONS_LOG, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []
    
    history.append(transaction)
    
    with open(TRANSACTIONS_LOG, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    
    print(f"    {C.GREEN}✓ Transaction sauvegardée{C.END}")

def view_history():
    """Affiche l'historique des transactions"""
    
    if not TRANSACTIONS_LOG.exists():
        print(f"    {C.YELLOW}Aucune transaction enregistrée{C.END}")
        return
    
    with open(TRANSACTIONS_LOG, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    print(f"\n{C.CYAN}{'═' * 70}{C.END}")
    print(f"{C.BOLD}{C.CYAN}📜 HISTORIQUE DES TRANSACTIONS ({len(history)}){C.END}")
    print(f"{C.CYAN}{'═' * 70}{C.END}\n")
    
    for i, trans in enumerate(history[-20:], 1):  # Dernières 20
        status_color = C.GREEN if trans['status'] == 'completed' else C.RED if trans['status'] == 'failed' else C.YELLOW
        
        print(f"    {C.WHITE}[{i}]{C.END} {trans['timestamp'][:19]}")
        print(f"        📞 {trans['phone']} | 💰 {trans['amount']} FCFA")
        print(f"        Status: {status_color}{trans['status'].upper()}{C.END}")
        
        if trans.get('confirmation', {}).get('transaction_id'):
            print(f"        ID: {trans['confirmation']['transaction_id']}")
        print()

def export_history():
    """Exporte l'historique en CSV"""
    
    if not TRANSACTIONS_LOG.exists():
        print(f"    {C.YELLOW}Aucune transaction à exporter{C.END}")
        return
    
    with open(TRANSACTIONS_LOG, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    csv_file = OUTPUT_DIR / f"wave_history_{datetime.now().strftime('%Y%m%d')}.csv"
    
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("Date,Heure,Destinataire,Montant,Status,Transaction_ID\n")
        
        for trans in history:
            date = trans['timestamp'][:10]
            time_str = trans['timestamp'][11:19]
            phone = trans['phone']
            amount = trans['amount']
            status = trans['status']
            trans_id = trans.get('confirmation', {}).get('transaction_id', 'N/A')
            
            f.write(f"{date},{time_str},{phone},{amount},{status},{trans_id}\n")
    
    print(f"    {C.GREEN}✓ Historique exporté: {csv_file}{C.END}")

# ═══════════════════════════════════════════════════════════════════════════════
# SOLDE ET INFOS
# ═══════════════════════════════════════════════════════════════════════════════

def get_wave_balance():
    """Tente de récupérer le solde Wave (nécessite que l'app soit ouverte)"""
    
    print(f"\n    {C.CYAN}💰 Récupération du solde...{C.END}")
    
    if not is_wave_running():
        open_wave()
        time.sleep(3)
    
    # Capture l'écran
    screenshot_file = screenshot()
    
    # Récupère le texte
    screen_text = get_screen_text()
    
    # Chercher un pattern de solde (ex: "12 500 FCFA" ou "Solde: 12500")
    balance_match = re.search(r'(\d{1,3}(?:[\s,]\d{3})*)\s*(?:FCFA|F\s*CFA|XOF)', screen_text, re.IGNORECASE)
    
    if balance_match:
        balance = balance_match.group(1).replace(' ', '').replace(',', '')
        print(f"    {C.GREEN}✓ Solde trouvé: {balance} FCFA{C.END}")
        return int(balance)
    else:
        print(f"    {C.YELLOW}⚠️ Solde non détecté automatiquement{C.END}")
        print(f"    {C.WHITE}Capture sauvegardée: {screenshot_file}{C.END}")
        return None

# ═══════════════════════════════════════════════════════════════════════════════
# MENU PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    print(f"""
{C.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                     💸 WAVE AUTO TRANSFERT v2.0 💸                           ║
╚══════════════════════════════════════════════════════════════════════════════╝{C.END}
    """)

def show_menu():
    print(f"""
    {C.CYAN}┌────────────────────────────────────────────────────────────────────┐
    │  {C.BOLD}💸 TRANSFERTS{C.END}{C.CYAN}                                                    │
    ├────────────────────────────────────────────────────────────────────┤
    │  [1] Effectuer un transfert (guidé)                                │
    │  [2] Transfert rapide (pré-remplissage)                            │
    │  [3] Transferts multiples (batch)                                  │
    ├────────────────────────────────────────────────────────────────────┤
    │  {C.BOLD}📊 INFORMATIONS{C.END}{C.CYAN}                                                  │
    ├────────────────────────────────────────────────────────────────────┤
    │  [4] Voir le solde                                                 │
    │  [5] Historique des transactions                                   │
    │  [6] Exporter historique (CSV)                                     │
    ├────────────────────────────────────────────────────────────────────┤
    │  {C.BOLD}🔧 UTILITAIRES{C.END}{C.CYAN}                                                   │
    ├────────────────────────────────────────────────────────────────────┤
    │  [7] Ouvrir Wave                                                   │
    │  [8] Capture d'écran                                               │
    │  [9] Calibrer les coordonnées                                      │
    ├────────────────────────────────────────────────────────────────────┤
    │  [0] Quitter                                                       │
    └────────────────────────────────────────────────────────────────────┘{C.END}
    """)

def calibrate_coords():
    """Aide à calibrer les coordonnées de l'écran"""
    
    print(f"\n    {C.CYAN}🔧 CALIBRATION DES COORDONNÉES{C.END}")
    print(f"    {C.WHITE}Ouvre Wave et positionne-le sur l'écran d'accueil{C.END}")
    input(f"    {C.CYAN}Appuie sur Entrée quand c'est prêt...{C.END}")
    
    print(f"\n    {C.YELLOW}Je vais taper à différents endroits.{C.END}")
    print(f"    {C.WHITE}Note où chaque tap atterrit sur ton téléphone.{C.END}\n")
    
    test_points = [
        ("Centre", 540, 1200),
        ("Haut", 540, 400),
        ("Bas", 540, 2000),
        ("Bouton Envoyer (supposé)", 540, 800),
    ]
    
    for name, x, y in test_points:
        print(f"    Test: {name} ({x}, {y})")
        tap(x, y)
        time.sleep(2)
        response = input(f"    Où a atterri le tap? (ou 'ok' si correct): ").strip()
        if response != 'ok':
            print(f"    {C.YELLOW}Note: {name} devrait être ajusté{C.END}")
    
    print(f"\n    {C.GREEN}Calibration terminée. Ajuste COORDS dans le script si nécessaire.{C.END}")

def batch_transfer():
    """Effectue plusieurs transferts à la suite"""
    
    print(f"\n    {C.CYAN}📋 TRANSFERTS MULTIPLES{C.END}")
    print(f"    {C.WHITE}Entre les transferts au format: numéro,montant{C.END}")
    print(f"    {C.WHITE}Un par ligne, ligne vide pour terminer{C.END}\n")
    
    transfers = []
    
    while True:
        line = input("    > ").strip()
        if not line:
            break
        
        parts = line.split(',')
        if len(parts) == 2:
            phone, amount = parts[0].strip(), parts[1].strip()
            transfers.append((phone, int(amount)))
            print(f"      {C.GREEN}✓ Ajouté: {phone} - {amount} FCFA{C.END}")
        else:
            print(f"      {C.RED}Format invalide{C.END}")
    
    if not transfers:
        print(f"    {C.YELLOW}Aucun transfert à effectuer{C.END}")
        return
    
    total = sum(t[1] for t in transfers)
    print(f"\n    {C.CYAN}Total: {len(transfers)} transferts pour {total:,} FCFA{C.END}")
    confirm = input(f"    Continuer? (oui/non): ").strip().lower()
    
    if confirm != "oui":
        return
    
    for phone, amount in transfers:
        print(f"\n{'═' * 50}")
        perform_transfer(phone, amount)
        time.sleep(2)

def main():
    print_banner()
    
    # Vérifier connexion
    connected, model = check_connection()
    if connected:
        print(f"    {C.GREEN}✓ Connecté à: {model}{C.END}")
    else:
        print(f"    {C.RED}✗ Téléphone non connecté{C.END}")
        print(f"    {C.WHITE}Exécute: adb connect {DEVICE}{C.END}")
    
    while True:
        show_menu()
        choice = input(f"\n    {C.GREEN}👉 Choix: {C.END}").strip()
        
        try:
            if choice == "1":
                phone = input("    Numéro destinataire: ").strip()
                amount = int(input("    Montant (FCFA): ").strip())
                perform_transfer(phone, amount)
            
            elif choice == "2":
                phone = input("    Numéro destinataire: ").strip()
                amount = int(input("    Montant (FCFA): ").strip())
                quick_transfer(phone, amount)
            
            elif choice == "3":
                batch_transfer()
            
            elif choice == "4":
                get_wave_balance()
            
            elif choice == "5":
                view_history()
            
            elif choice == "6":
                export_history()
            
            elif choice == "7":
                open_wave()
            
            elif choice == "8":
                file = screenshot()
                print(f"    {C.GREEN}✓ Capture: {file}{C.END}")
            
            elif choice == "9":
                calibrate_coords()
            
            elif choice == "0":
                print(f"\n    {C.YELLOW}👋 Au revoir!{C.END}\n")
                break
            
            else:
                print(f"    {C.RED}Option invalide{C.END}")
        
        except KeyboardInterrupt:
            print(f"\n    {C.YELLOW}Interrompu{C.END}")
        except Exception as e:
            print(f"    {C.RED}Erreur: {e}{C.END}")
        
        input(f"\n    {C.CYAN}⏎ Entrée pour continuer...{C.END}")

if __name__ == "__main__":
    main()
