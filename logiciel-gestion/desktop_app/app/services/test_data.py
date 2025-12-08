# test_data.py - Service de données de test pour le développement
from datetime import datetime, timedelta

class TestDataService:
    """Service pour générer des données de test"""
    
    @staticmethod
    def get_test_users():
        """Génère des utilisateurs de test"""
        class TestUser:
            def __init__(self, id, username, email, role="user", active=True, first_name="", last_name="", phone=""):
                self.id = id
                self.username = username
                self.email = email
                self.role = role
                self.active = active
                self.first_name = first_name
                self.last_name = last_name
                self.phone = phone
                self.created_at = datetime.now()
                self.last_login = None
                
        return [
            TestUser(1, "admin", "admin@test.com", "superadmin", True, "Admin", "Test", "0123456789"),
            TestUser(2, "user1", "user1@test.com", "user", True, "Jean", "Dupont", "0123456790"),
            TestUser(3, "manager", "manager@test.com", "admin", True, "Marie", "Martin", "0123456791"),
            TestUser(4, "user2", "user2@test.com", "user", True, "Pierre", "Durand", "0123456792"),
        ]
    
    @staticmethod
    def get_test_terrains():
        """Génère des terrains de test"""
        class TestTerrain:
            def __init__(self, id, name, active=True, description="", location="", capacity=10, price_per_hour=50.0, equipment=""):
                self.id = id
                self.name = name
                self.active = active
                self.description = description
                self.location = location
                self.capacity = capacity
                self.price_per_hour = price_per_hour
                self.equipment = equipment
                
        return [
            TestTerrain(1, "Terrain Central A", True, "Terrain principal avec gazon synthétique de qualité", "Complexe Sportif Nord", 10, 60.0, "Éclairage, Vestiaires, Parking"),
            TestTerrain(2, "Terrain Sud B", True, "Terrain secondaire avec bon revêtement", "Complexe Sportif Sud", 10, 45.0, "Éclairage, Parking"),
            TestTerrain(3, "Terrain Est C", True, "Terrain récent avec équipements modernes", "Complexe Sportif Est", 10, 50.0, "Éclairage, Vestiaires, Parking, Sonorisation"),
            TestTerrain(4, "Terrain Ouest D", False, "En maintenance - Rénovation des vestiaires", "Complexe Sportif Ouest", 10, 40.0, "Éclairage"),
        ]
    
    @staticmethod
    def get_test_reservations():
        """Génère des réservations de test"""
        class TestReservation:
            def __init__(self, id, user_id, terrain_id, start, end, notes="", status="active"):
                self.id = id
                self.user_id = user_id
                self.terrain_id = terrain_id
                self.start = start
                self.end = end
                self.notes = notes
                self.status = status
                # Relations simulées
                self.user = TestDataService.get_user_by_id(user_id)
                self.terrain = TestDataService.get_terrain_by_id(terrain_id)
                
        now = datetime.now()
        return [
            TestReservation(1, 2, 1, now + timedelta(hours=2), now + timedelta(hours=4), "Match amical équipe locale"),
            TestReservation(2, 3, 2, now + timedelta(days=1, hours=1), now + timedelta(days=1, hours=3), "Entraînement hebdomadaire"),
            TestReservation(3, 2, 1, now - timedelta(days=1, hours=2), now - timedelta(days=1), "Match terminé hier"),
            TestReservation(4, 4, 3, now + timedelta(days=2), now + timedelta(days=2, hours=2), "Tournoi amateur"),
            TestReservation(5, 2, 1, now + timedelta(days=7, hours=3), now + timedelta(days=7, hours=5), "Match de championnat"),
        ]
    
    @staticmethod
    def get_user_by_id(user_id):
        """Récupère un utilisateur par ID"""
        users = TestDataService.get_test_users()
        for user in users:
            if user.id == user_id:
                return user
        # Utilisateur par défaut
        class DefaultUser:
            def __init__(self):
                self.id = user_id
                self.username = f"user{user_id}"
        return DefaultUser()
    
    @staticmethod
    def get_terrain_by_id(terrain_id):
        """Récupère un terrain par ID"""
        terrains = TestDataService.get_test_terrains()
        for terrain in terrains:
            if terrain.id == terrain_id:
                return terrain
        # Terrain par défaut
        class DefaultTerrain:
            def __init__(self):
                self.id = terrain_id
                self.name = f"Terrain {terrain_id}"
        return DefaultTerrain()
    
    @staticmethod
    def get_dashboard_stats():
        """Génère des statistiques pour le dashboard"""
        return {
            'total_terrains': len([t for t in TestDataService.get_test_terrains() if t.active]),
            'total_reservations_today': 2,
            'total_users': len(TestDataService.get_test_users()),
            'revenue_today': 180.0,
            'occupancy_rate': 75.5
        }