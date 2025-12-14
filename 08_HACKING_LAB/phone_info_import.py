#!/usr/bin/env python3
"""
📱 MODULE D'IMPORT D'INFOS TÉLÉPHONE
Importe et exploite les infos de TON téléphone Android pour des tests légaux
"""

import json
import os
from pprint import pprint

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def import_phone_info(json_path):
    if not os.path.exists(json_path):
        print(f"{Colors.RED}Fichier non trouvé : {json_path}{Colors.RESET}")
        return None
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"{Colors.GREEN}Infos importées depuis {json_path}:{Colors.RESET}\n")
    pprint(data)
    return data

def test_wifi_security(data):
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== TEST SÉCURITÉ WIFI ==={Colors.RESET}")
    wifi = data.get('wifi', {})
    if not wifi:
        print(f"{Colors.YELLOW}Aucune info WiFi trouvée.{Colors.RESET}")
        return
    ssid = wifi.get('ssid', 'Inconnu')
    mac = wifi.get('mac', 'Inconnu')
    security = wifi.get('security', 'Inconnu')
    print(f"SSID : {ssid}\nMAC : {mac}\nSécurité : {security}")
    if security.lower() in ['wpa2', 'wpa3']:
        print(f"{Colors.GREEN}✓ Sécurité correcte{Colors.RESET}")
    else:
        print(f"{Colors.RED}⚠️ Sécurité faible !{Colors.RESET}")

def test_apps_vulnerabilities(data):
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== TEST APPS VULNÉRABLES ==={Colors.RESET}")
    apps = data.get('apps', [])
    if not apps:
        print(f"{Colors.YELLOW}Aucune app trouvée.{Colors.RESET}")
        return
    # Exemple : recherche d'apps connues vulnérables
    vuln_list = ['TikTok', 'UC Browser', 'Clean Master', 'ES File Explorer', 'CamScanner']
    for app in apps:
        if app['name'] in vuln_list:
            print(f"{Colors.RED}⚠️ {app['name']} est connue pour des failles !{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}✓ {app['name']} OK{Colors.RESET}")

def test_permissions(data):
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== TEST PERMISSIONS SENSIBLES ==={Colors.RESET}")
    perms = data.get('permissions', [])
    if not perms:
        print(f"{Colors.YELLOW}Aucune permission trouvée.{Colors.RESET}")
        return
    for perm in perms:
        if perm in ['android.permission.READ_SMS', 'android.permission.RECORD_AUDIO', 'android.permission.ACCESS_FINE_LOCATION']:
            print(f"{Colors.RED}⚠️ Permission sensible : {perm}{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}✓ {perm}{Colors.RESET}")

def main():
    print(f"{Colors.BOLD}=== IMPORT D'INFOS TÉLÉPHONE ==={Colors.RESET}")
    json_path = input("Chemin du fichier JSON exporté depuis ton téléphone : ").strip()
    data = import_phone_info(json_path)
    if not data:
        return
    test_wifi_security(data)
    test_apps_vulnerabilities(data)
    test_permissions(data)

if __name__ == "__main__":
    main()
