from app.models.db import SessionLocal
from app.models.terrain import Terrain
from app.services.test_data import TestDataService

class TerrainController:
    def __init__(self):
        pass
    def list_terrains(self):
        db = SessionLocal()
        try:
            return db.query(Terrain).all()
        finally:
            db.close()
            
    def get_terrain_by_id(self, terrain_id):
        """Récupère un terrain par son ID"""
        db = SessionLocal()
        try:
            return db.query(Terrain).get(terrain_id)
        finally:
            db.close()
    def create(self, name, location=None, active=True):
        db = SessionLocal()
        try:
            t = Terrain(name=name, location=location, active=active)
            db.add(t)
            db.commit()
            db.refresh(t)
            return t
        finally:
            db.close()

    def update(self, terrain_id, **kwargs):
        db = SessionLocal()
        try:
            t = db.query(Terrain).get(terrain_id)
            if not t:
                raise ValueError('Terrain not found')
            for k, v in kwargs.items():
                setattr(t, k, v)
            db.commit()
            return t
        finally:
            db.close()

    def delete(self, terrain_id):
        db = SessionLocal()
        try:
            t = db.query(Terrain).get(terrain_id)
            if not t:
                raise ValueError('Terrain not found')
            db.delete(t)
            db.commit()
            return True
        finally:
            db.close()
