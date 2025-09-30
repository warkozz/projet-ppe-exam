from app.models.db import SessionLocal
from app.models.terrain import Terrain
class TerrainController:
    def __init__(self):
        self.db = SessionLocal()
    def list_terrains(self):
        return self.db.query(Terrain).all()
    def create(self, name, location=None, active=True):
        t = Terrain(name=name, location=location, active=active)
        self.db.add(t); self.db.commit(); self.db.refresh(t); return t
    def update(self, terrain_id, **kwargs):
        t = self.db.query(Terrain).get(terrain_id)
        if not t: raise ValueError('Terrain not found')
        for k,v in kwargs.items(): setattr(t,k,v)
        self.db.commit(); return t
    def delete(self, terrain_id):
        t = self.db.query(Terrain).get(terrain_id)
        if not t: raise ValueError('Terrain not found')
        self.db.delete(t); self.db.commit(); return True
