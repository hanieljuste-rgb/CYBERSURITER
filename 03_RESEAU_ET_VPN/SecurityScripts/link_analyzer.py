import re
import sys
from urllib.parse import urlparse

def analyze_link(url):
    print(f"\n🔍 ANALYSE DU LIEN : {url}")
    print("-" * 50)
    
    score = 0
    warnings = []
    
    # 1. Vérification du protocole
    if not url.startswith("https://"):
        score += 20
        warnings.append("⚠️  Pas de HTTPS (Communication non chiffrée)")
    
    # Parsing de l'URL
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path
    except:
        print("❌ URL invalide ou malformée.")
        return

    # 2. Détection d'IP brute
    # Regex pour IP v4
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain):
        score += 40
        warnings.append("🚨 Utilise une adresse IP au lieu d'un nom de domaine (Très suspect)")

    # 3. Longueur excessive
    if len(url) > 70:
        score += 10
        warnings.append("⚠️  URL très longue (Technique pour cacher la vraie destination)")

    # 4. Caractères d'obfuscation (@)
    if "@" in url:
        score += 50
        warnings.append("🚨 Contient '@' (Redirection masquée vers un autre site)")

    # 5. Sous-domaines multiples (ex: paypal.com.security.badsite.com)
    parts = domain.split('.')
    if len(parts) > 4:
        score += 20
        warnings.append("⚠️  Trop de sous-domaines (Peut tenter d'imiter un site légitime)")

    # 6. Mots-clés sensibles dans le domaine (Typosquatting ou Social Engineering)
    suspicious_keywords = ['login', 'signin', 'bank', 'account', 'update', 'free', 'bonus', 'security', 'paypal', 'google', 'facebook']
    # On regarde si ces mots sont dans l'URL mais PAS dans le domaine principal (simplifié)
    for word in suspicious_keywords:
        if word in url and word not in domain:
             # C'est normal d'avoir 'google' dans 'google.com', mais suspect dans 'google-security.com' ou 'site.com/google'
             pass 
        if word in domain and "com" not in word: # Détection basique
             # warnings.append(f"ℹ️  Mot-clé '{word}' détecté (Vérifiez bien l'orthographe)")
             pass

    # 7. Extensions de domaine suspectes (TLD)
    suspicious_tlds = ['.xyz', '.top', '.club', '.info', '.tk', '.cn', '.ru']
    for tld in suspicious_tlds:
        if domain.endswith(tld):
            score += 15
            warnings.append(f"⚠️  Extension de domaine inhabituelle ({tld})")

    # RÉSULTATS
    print(f"DOMAINE DÉTECTÉ : {domain}")
    
    if warnings:
        print("\nPROBLÈMES DÉTECTÉS :")
        for w in warnings:
            print(w)
    else:
        print("\n✅ Aucun indicateur évident de phishing détecté.")

    print("-" * 50)
    print(f"SCORE DE RISQUE : {score}/100")
    
    if score >= 50:
        print("🔴 DANGER : Ce lien est très probablement malveillant.")
    elif score >= 20:
        print("🟠 ATTENTION : Soyez prudent, vérifiez la source.")
    else:
        print("🟢 SÛR (Probablement) : Semble légitime.")

def main():
    print("==================================================")
    print("   DÉTECTEUR DE LIENS MALVEILLANTS (ÉDUCATIF)     ")
    print("==================================================")
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # Exemples par défaut pour la démo
        print("Usage: python link_analyzer.py <url>")
        print("\n--- DÉMONSTRATION AVEC DES EXEMPLES ---")
        
        # Exemple 1 : Bon lien
        analyze_link("https://www.google.com")
        
        # Exemple 2 : Phishing classique (IP)
        analyze_link("http://192.168.1.50/login.html")
        
        # Exemple 3 : Obfuscation avec @
        analyze_link("https://www.google.com@malicious-site.com/login")
        
        # Exemple 4 : Sous-domaines trompeurs
        analyze_link("http://paypal.com.security-check.account-update.xyz/login")

if __name__ == "__main__":
    main()
