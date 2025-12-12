#!/usr/bin/env python3
"""
Script de vérification de l'installation
Football Manager 5v5 - Version 2.0
"""
import sys
import os

def check_dependencies():
    """Vérifier que toutes les dépendances sont installées"""
    print("📦 Vérification des dépendances...")
    
    required_packages = [
        ('PySide6', 'Interface graphique'),
        ('qt_material', 'Thème Material Design'),
        ('sqlalchemy', 'ORM Base de données'),
        ('pymysql', 'Connecteur MySQL'),
        ('bcrypt', 'Hachage des mots de passe'),
        ('dotenv', 'Configuration environnement')
    ]
    
    missing_packages = []
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ❌ {package} - {description} - MANQUANT")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Packages manquants: {', '.join(missing_packages)}")
        print("Installez avec: pip install -r requirements.txt")
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def check_database():
    """Vérifier la connexion à la base de données"""
    print("\n🗄️ Vérification de la base de données...")
    
    try:
        sys.path.append(os.path.dirname(__file__))
        from app.models.db import check_db_connection, SessionLocal
        from app.models.user import User
        from app.models.terrain import Terrain
        from app.models.reservation import Reservation
        
        # Test de connexion
        if not check_db_connection():
            print("   ❌ Connexion à la base de données échouée")
            print("   💡 Vérifiez que MySQL est démarré et que la base 'foot5' existe")
            return False
        
        print("   ✅ Connexion à la base de données réussie")
        
        # Vérifier les tables
        db = SessionLocal()
        try:
            # Compter les enregistrements
            users_count = db.query(User).count()
            terrains_count = db.query(Terrain).count() 
            reservations_count = db.query(Reservation).count()
            
            print(f"   📊 {users_count} utilisateur(s)")
            print(f"   🏟️ {terrains_count} terrain(s)")
            print(f"   📅 {reservations_count} réservation(s)")
            
            if users_count == 0:
                print("   ⚠️  Aucun utilisateur - Exécutez setup_admin.py")
                return False
                
            # Vérifier l'admin
            admin = db.query(User).filter(User.username == 'admin').first()
            if admin:
                print(f"   👑 Admin trouvé: {admin.username} ({admin.role})")
            else:
                print("   ⚠️  Admin par défaut introuvable")
                
        finally:
            db.close()
            
        print("✅ Base de données configurée correctement")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur base de données: {e}")
        return False

def check_configuration():
    """Vérifier les fichiers de configuration"""
    print("\n⚙️ Vérification de la configuration...")
    
    # Vérifier le fichier .env
    env_path = ".env"
    if os.path.exists(env_path):
        print("   ✅ Fichier .env trouvé")
        
        # Lire la configuration
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            db_url = os.getenv('DATABASE_URL', '')
            if 'foot5' in db_url:
                print("   ✅ Configuration base de données correcte")
            else:
                print("   ⚠️  Configuration base de données à vérifier")
                
        except Exception as e:
            print(f"   ⚠️  Erreur lecture .env: {e}")
    else:
        print("   ⚠️  Fichier .env manquant (utilisation config par défaut)")
    
    # Vérifier les fichiers essentiels
    essential_files = [
        'hybrid_main.py',
        'app/models/db.py',
        'app/controllers/auth_controller.py',
        'app/views/hybrid/dashboard_view.py'
    ]
    
    for file_path in essential_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - MANQUANT")
            return False
    
    print("✅ Configuration validée")
    return True

def test_application_startup():
    """Tester le démarrage de l'application (sans interface)"""
    print("\n🚀 Test de démarrage de l'application...")
    
    try:
        sys.path.append(os.path.dirname(__file__))
        
        # Test d'import des composants principaux
        from app.controllers.auth_controller import AuthController
        from app.controllers.user_controller import UserController
        from app.controllers.terrain_controller import TerrainController
        from app.controllers.reservation_controller import ReservationController
        
        print("   ✅ Contrôleurs importés avec succès")
        
        # Test de connexion admin
        auth = AuthController()
        result = auth.login('admin', 'admin123')
        if result['success']:
            print(f"   ✅ Connexion admin réussie ({result['user']['role']})")
        else:
            print(f"   ❌ Connexion admin échouée: {result.get('message', 'Erreur inconnue')}")
            return False
        
        print("✅ Application prête à démarrer")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur démarrage: {e}")
        return False

def main():
    """Fonction principale de vérification"""
    print("🏟️ Football Manager 5v5 - Vérification Installation")
    print("=" * 55)
    
    checks = [
        ("Dépendances", check_dependencies),
        ("Base de données", check_database), 
        ("Configuration", check_configuration),
        ("Démarrage application", test_application_startup)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ Erreur lors de {check_name}: {e}")
            all_passed = False
    
    print("\n" + "=" * 55)
    if all_passed:
        print("🎉 INSTALLATION VALIDÉE - Tout fonctionne correctement!")
        print("\n📋 Connexions disponibles:")
        print("   👑 admin / admin123 (Superadmin)")
        print("   🔑 manager / manager123 (Manager)")  
        print("   👤 user1 / user123 (Utilisateur)")
        print("\n🚀 Lancez l'application avec: python hybrid_main.py")
    else:
        print("❌ PROBLÈMES DÉTECTÉS - Consultez les messages ci-dessus")
        print("\n💡 Actions recommandées:")
        print("   1. pip install -r requirements.txt")
        print("   2. Démarrez XAMPP MySQL")
        print("   3. python setup_admin.py")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)