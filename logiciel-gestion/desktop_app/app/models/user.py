from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(Enum('superadmin', 'admin', 'user', name='role_enum'), nullable=False, default='user')
    def __repr__(self): return f'<User(username={self.username})>'

# Relation User <-> Reservation (après import des deux classes)
from .reservation import Reservation
User.reservations = relationship('Reservation', back_populates='user')
