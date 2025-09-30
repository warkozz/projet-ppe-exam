from app.models.user import User
from app.models.db import SessionLocal
from app.utils.hashing import hash_password

class UserController:
    def __init__(self):
        self.db = SessionLocal()

    def list_users(self):
        return self.db.query(User).all()

    def create_user(self, username, email, password, role='user'):
        if self.db.query(User).filter_by(username=username).first():
            raise ValueError('Nom d\'utilisateur déjà utilisé')
        user = User(username=username, email=email, password_hash=hash_password(password), role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user_id, **kwargs):
        user = self.db.query(User).get(user_id)
        if not user:
            raise ValueError('Utilisateur introuvable')
        for key, value in kwargs.items():
            if key == 'password':
                user.password_hash = hash_password(value)
            elif key == 'role':
                user.role = value
            elif hasattr(user, key):
                setattr(user, key, value)
        self.db.commit()
        return user

    def delete_user(self, user_id):
        user = self.db.query(User).get(user_id)
        if not user:
            raise ValueError('Utilisateur introuvable')
        self.db.delete(user)
        self.db.commit()
