from app.models.db import SessionLocal
from app.models.user import User
from app.utils.hashing import hash_password, verify_password
class AuthController:
    def __init__(self):
        self.db = SessionLocal()
    def register(self, username, email, password, is_admin=False):
        if self.db.query(User).filter_by(username=username).first():
            raise ValueError('Username already exists')
        user = User(username=username, email=email, password_hash=hash_password(password), is_admin=is_admin)
        self.db.add(user); self.db.commit(); self.db.refresh(user); return user
    def login(self, username, password):
        user = self.db.query(User).filter_by(username=username).first()
        if not user: return None
        if verify_password(password, user.password_hash): return user
        return None
