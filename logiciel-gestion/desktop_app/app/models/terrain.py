from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .db import Base
class Terrain(Base):
    __tablename__ = 'terrains'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=True)
    active = Column(Boolean, default=True)
    reservations = relationship('Reservation', back_populates='terrain')
    def __repr__(self): return f'<Terrain(name={self.name})>'
