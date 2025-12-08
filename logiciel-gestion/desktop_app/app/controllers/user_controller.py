from app.models.user import User
from app.models.db import SessionLocal
from app.utils.hashing import hash_password
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.services.test_data import TestDataService

class UserController:
    def __init__(self):
        self.db = SessionLocal()

    def list_users(self):
        return self.db.query(User).all()

    def create_user(self, username, email, password, role='user', active=True):
        try:
            # Vérification des doublons avant insertion
            if self.db.query(User).filter_by(username=username).first():
                raise ValueError('Nom d\'utilisateur déjà utilisé')
            
            if self.db.query(User).filter_by(email=email).first():
                raise ValueError('Email déjà utilisé')
            
            user = User(username=username, email=email, password_hash=hash_password(password), role=role, active=active)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError as e:
            self.db.rollback()
            if 'username' in str(e):
                raise ValueError('Nom d\'utilisateur déjà utilisé')
            elif 'email' in str(e):
                raise ValueError('Email déjà utilisé')
            else:
                raise ValueError('Erreur de contrainte de base de données')
        except Exception as e:
            self.db.rollback()
            raise e

    def update_user(self, user_id, **kwargs):
        try:
            user = self.db.query(User).get(user_id)
            if not user:
                raise ValueError('Utilisateur introuvable')
            
            # Vérifier les contraintes avant modification
            if 'username' in kwargs:
                existing = self.db.query(User).filter_by(username=kwargs['username']).first()
                if existing and existing.id != user_id:
                    raise ValueError('Nom d\'utilisateur déjà utilisé')
                    
            if 'email' in kwargs:
                existing = self.db.query(User).filter_by(email=kwargs['email']).first()
                if existing and existing.id != user_id:
                    raise ValueError('Email déjà utilisé')
            
            for key, value in kwargs.items():
                if key == 'password' and value:
                    user.password_hash = hash_password(value)
                elif key == 'active':
                    user.active = bool(value)
                elif hasattr(user, key):
                    setattr(user, key, value)
            
            self.db.commit()
            return user
        except IntegrityError as e:
            self.db.rollback()
            if 'username' in str(e):
                raise ValueError('Nom d\'utilisateur déjà utilisé')
            elif 'email' in str(e):
                raise ValueError('Email déjà utilisé')
            else:
                raise ValueError('Erreur de contrainte de base de données')
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_user(self, user_id):
        try:
            user = self.db.query(User).get(user_id)
            if not user:
                raise ValueError('Utilisateur introuvable')
            self.db.delete(user)
            self.db.commit()
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError('Impossible de supprimer cet utilisateur (contraintes de base de données)')
        except Exception as e:
            self.db.rollback()
            raise e
