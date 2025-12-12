#!/usr/bin/env python3
"""
Script de création des utilisateurs administrateurs par défaut
Football Manager 5v5 - Version 2.0
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.utils.hashing import hash_password
from app.models.db import SessionLocal, engine
from app.models.user import User
from app.models.terrain import Terrain
from app.models.reservation import Reservation
from app.models.db import Base
from datetime import datetime, timedelta

def create_database_tables():
    """Créer toutes les tables"""
    print("🔧 Création des tables de base de données...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès")

def create_default_users():
    """Créer les utilisateurs par défaut avec de vrais mots de passe hachés"""
    db = SessionLocal()
    
    try:
        # Vérifier si des utilisateurs existent déjà
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"ℹ️  {existing_users} utilisateur(s) déjà présent(s) dans la base")
            return
        
        print("👥 Création des utilisateurs par défaut...")
        
        # Superadmin
        admin = User(
            username='admin',
            email='admin@foot5.com',
            password_hash=hash_password('admin123'),
            role='superadmin',
            active=True
        )
        
        # Manager
        manager = User(
            username='manager',
            email='manager@foot5.com', 
            password_hash=hash_password('manager123'),
            role='admin',
            active=True
        )
        
        # User test
        user = User(
            username='user1',
            email='user1@foot5.com',
            password_hash=hash_password('user123'),
            role='user',
            active=True
        )
        
        # Utilisateurs supplémentaires pour tests
        test_users = []
        for i in range(2, 6):
            test_user = User(
                username=f'test{i}',
                email=f'test{i}@foot5.com',
                password_hash=hash_password('test123'),
                role='user',
                active=True
            )
            test_users.append(test_user)
        
        # Ajouter tous les utilisateurs
        users_to_add = [admin, manager, user] + test_users
        for u in users_to_add:
            db.add(u)
        
        db.commit()
        
        print("✅ Utilisateurs créés avec succès:")
        print("   👑 Superadmin - Username: admin, Password: admin123")
        print("   🔑 Manager - Username: manager, Password: manager123") 
        print("   👤 User - Username: user1, Password: user123")
        print(f"   👥 {len(test_users)} utilisateurs test supplémentaires")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des utilisateurs: {e}")
        db.rollback()
    finally:
        db.close()

def create_default_terrains():
    """Créer les terrains par défaut"""
    db = SessionLocal()
    
    try:
        # Vérifier si des terrains existent déjà
        existing_terrains = db.query(Terrain).count()
        if existing_terrains > 0:
            print(f"ℹ️  {existing_terrains} terrain(s) déjà présent(s) dans la base")
            return
            
        print("🏟️ Création des terrains par défaut...")
        
        terrains = [
            Terrain(name="Terrain A", location="Salle Centrale", active=True),
            Terrain(name="Terrain B", location="Salle Nord", active=True),
            Terrain(name="Terrain C", location="Salle Sud", active=True),
            Terrain(name="Terrain D", location="Salle Est", active=True),
            Terrain(name="Terrain E", location="Salle Ouest", active=True),
            Terrain(name="Terrain F", location="Salle Annexe", active=False)  # Terrain inactif pour test
        ]
        
        for terrain in terrains:
            db.add(terrain)
        
        db.commit()
        print(f"✅ {len(terrains)} terrains créés avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des terrains: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_reservations():
    """Créer quelques réservations d'exemple"""
    db = SessionLocal()
    
    try:
        # Vérifier si des réservations existent déjà
        existing_reservations = db.query(Reservation).count()
        if existing_reservations > 0:
            print(f"ℹ️  {existing_reservations} réservation(s) déjà présente(s) dans la base")
            return
            
        print("📅 Création de réservations d'exemple...")
        
        # Obtenir les IDs des utilisateurs et terrains
        users = db.query(User).all()
        terrains = db.query(Terrain).filter(Terrain.active == True).all()
        
        if not users or not terrains:
            print("⚠️ Impossible de créer les réservations: utilisateurs ou terrains manquants")
            return
        
        # Créer quelques réservations pour aujourd'hui et demain
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        
        sample_reservations = [
            Reservation(
                user_id=users[0].id,
                terrain_id=terrains[0].id,
                start=today.replace(hour=14, minute=0, second=0, microsecond=0),
                end=today.replace(hour=16, minute=0, second=0, microsecond=0),
                status='confirmed',
                notes='Match amical équipe A'
            ),
            Reservation(
                user_id=users[1].id if len(users) > 1 else users[0].id,
                terrain_id=terrains[1].id if len(terrains) > 1 else terrains[0].id,
                start=today.replace(hour=18, minute=0, second=0, microsecond=0),
                end=today.replace(hour=20, minute=0, second=0, microsecond=0),
                status='confirmed',
                notes='Entraînement équipe B'
            ),
            Reservation(
                user_id=users[2] if len(users) > 2 else users[0].id,
                terrain_id=terrains[0].id,
                start=tomorrow.replace(hour=10, minute=0, second=0, microsecond=0),
                end=tomorrow.replace(hour=12, minute=0, second=0, microsecond=0),
                status='pending',
                notes='Tournoi junior'
            )
        ]
        
        for reservation in sample_reservations:
            db.add(reservation)
        
        db.commit()
        print(f"✅ {len(sample_reservations)} réservations d'exemple créées")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des réservations: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Fonction principale de setup"""
    print("🏟️ Football Manager 5v5 - Setup Base de Données")
    print("=" * 50)
    
    try:
        # 1. Créer les tables
        create_database_tables()
        
        # 2. Créer les utilisateurs par défaut
        create_default_users()
        
        # 3. Créer les terrains par défaut
        create_default_terrains()
        
        # 4. Créer quelques réservations d'exemple
        create_sample_reservations()
        
        print("\n🎉 Setup terminé avec succès!")
        print("\n📋 Informations de connexion:")
        print("   👑 Superadmin: admin / admin123")
        print("   🔑 Manager: manager / manager123")
        print("   👤 Utilisateur: user1 / user123")
        print("\n⚠️  N'oubliez pas de changer ces mots de passe par défaut!")
        
    except Exception as e:
        print(f"❌ Erreur durant le setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()