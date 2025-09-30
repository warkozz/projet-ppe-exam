from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from .db import Base
class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    terrain_id = Column(Integer, ForeignKey('terrains.id'), nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    status = Column(String(20), default='confirmed')
    notes = Column(String(250), nullable=True)
    user = relationship('User', back_populates='reservations')
    terrain = relationship('Terrain', back_populates='reservations')
    def __repr__(self): return f'<Reservation({self.id})>'
