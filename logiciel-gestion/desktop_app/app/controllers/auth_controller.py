from app.models.db import SessionLocal
from app.models.user import User
from app.utils.hashing import hash_password, verify_password

class AuthController:
    def __init__(self):
        self.current_user = None
        
    def login(self, username: str, password: str):
        """Authentifie un utilisateur"""
        try:
            db = SessionLocal()
            user = db.query(User).filter(User.username == username).first()
            
            if user and verify_password(password, user.password_hash):
                if user.active:
                    self.current_user = user
                    return user
                else:
                    raise Exception("Compte désactivé")
            else:
                raise Exception("Nom d'utilisateur ou mot de passe incorrect")
                
        except Exception as e:
            raise Exception(f"Erreur de connexion : {str(e)}")
        finally:
            if 'db' in locals():
                db.close()
                
    def register(self, username, email, password, role='user'):
        """Enregistre un nouvel utilisateur"""
        try:
            db = SessionLocal()
            if db.query(User).filter_by(username=username).first():
                raise ValueError('Nom d\'utilisateur déjà existant')
            user = User(username=username, email=email, password_hash=hash_password(password), role=role)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            print(f"Erreur lors de l'enregistrement: {str(e)}")
            raise e
        finally:
            if 'db' in locals():
                db.close()
