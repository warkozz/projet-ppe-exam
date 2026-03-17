from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Text, Numeric
from sqlalchemy.orm import relationship
from .db import Base
class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    terrain_id = Column(Integer, ForeignKey('terrains.id'), nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    status = Column(String(20), default='pending')
    notes = Column(Text, nullable=True)
    total_cost = Column(Numeric(10, 2), nullable=True, default=0.00)
    user = relationship('User', back_populates='reservations')
    terrain = relationship('Terrain', back_populates='reservations')
    def __repr__(self): return f'<Reservation({self.id})>'
