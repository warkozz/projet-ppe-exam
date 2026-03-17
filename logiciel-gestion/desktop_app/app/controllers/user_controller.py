from app.models.user import User
from app.models.db import SessionLocal
from app.utils.hashing import hash_password
from sqlalchemy.exc import IntegrityError

class UserController:
    def __init__(self):
        pass

    def list_users(self):
        db = SessionLocal()
        try:
            return db.query(User).all()
        finally:
            db.close()

    def create_user(self, username, email, password, role='user', active=True):
        db = SessionLocal()
        try:
            if db.query(User).filter_by(username=username).first():
                raise ValueError('Nom d\'utilisateur déjà utilisé')
            if db.query(User).filter_by(email=email).first():
                raise ValueError('Email déjà utilisé')
            user = User(username=username, email=email, password_hash=hash_password(password), role=role, active=active)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError as e:
            db.rollback()
            if 'username' in str(e):
                raise ValueError('Nom d\'utilisateur déjà utilisé')
            elif 'email' in str(e):
                raise ValueError('Email déjà utilisé')
            else:
                raise ValueError('Erreur de contrainte de base de données')
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def update_user(self, user_id, **kwargs):
        db = SessionLocal()
        try:
            user = db.query(User).get(user_id)
            if not user:
                raise ValueError('Utilisateur introuvable')
            if 'username' in kwargs:
                existing = db.query(User).filter_by(username=kwargs['username']).first()
                if existing and existing.id != user_id:
                    raise ValueError('Nom d\'utilisateur déjà utilisé')
            if 'email' in kwargs:
                existing = db.query(User).filter_by(email=kwargs['email']).first()
                if existing and existing.id != user_id:
                    raise ValueError('Email déjà utilisé')
            for key, value in kwargs.items():
                if key == 'password' and value:
                    user.password_hash = hash_password(value)
                elif key == 'active':
                    user.active = bool(value)
                elif hasattr(user, key):
                    setattr(user, key, value)
            db.commit()
            return user
        except IntegrityError as e:
            db.rollback()
            if 'username' in str(e):
                raise ValueError('Nom d\'utilisateur déjà utilisé')
            elif 'email' in str(e):
                raise ValueError('Email déjà utilisé')
            else:
                raise ValueError('Erreur de contrainte de base de données')
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def delete_user(self, user_id):
        db = SessionLocal()
        try:
            user = db.query(User).get(user_id)
            if not user:
                raise ValueError('Utilisateur introuvable')
            db.delete(user)
            db.commit()
        except IntegrityError as e:
            db.rollback()
            raise ValueError('Impossible de supprimer cet utilisateur (contraintes de base de données)')
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
