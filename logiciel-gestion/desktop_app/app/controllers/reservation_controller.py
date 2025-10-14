from datetime import datetime
from app.models.db import SessionLocal
from app.models.reservation import Reservation
from app.services.cpp_bridge import check_conflict
class ReservationController:
    def modify_reservation(self, reservation_id, user_id, terrain_id, start, end, notes=''):
        from app.services.cpp_bridge import check_conflict
        db = SessionLocal()
        try:
            r = db.query(Reservation).get(reservation_id)
            if not r:
                raise ValueError('Réservation introuvable')
            # Vérifie les conflits (hors la réservation courante)
            try:
                conflict = check_conflict(db, terrain_id, start, end, exclude_reservation_id=reservation_id)
            except TypeError:
                # Si la version C++ est utilisée, ignore l'exclusion (ne gère pas le cas)
                conflict = check_conflict(db, terrain_id, start, end)
            if conflict:
                raise ValueError('Conflit avec une autre réservation')
            r.user_id = user_id
            r.terrain_id = terrain_id
            r.start = start
            r.end = end
            r.notes = notes
            db.commit()
        finally:
            db.close()
    def __init__(self):
        pass

    def create_reservation(self, user_id, terrain_id, start: datetime, end: datetime, notes=''):
        db = SessionLocal()
        try:
            conflict = check_conflict(db, terrain_id, start, end)
            if conflict:
                raise ValueError('Ce terrain est déjà réservé sur ce créneau.')
            r = Reservation(user_id=user_id, terrain_id=terrain_id, start=start, end=end, notes=notes)
            db.add(r)
            db.commit()
            db.refresh(r)
            return r
        finally:
            db.close()

    def get_reservations(self, date_from=None, date_to=None):
        from sqlalchemy.orm import joinedload
        db = SessionLocal()
        try:
            q = db.query(Reservation).options(joinedload(Reservation.user), joinedload(Reservation.terrain))
            if date_from:
                q = q.filter(Reservation.start >= date_from)
            if date_to:
                q = q.filter(Reservation.end <= date_to)
            return q.all()
        finally:
            db.close()

    def cancel_reservation(self, reservation_id):
        db = SessionLocal()
        try:
            r = db.query(Reservation).get(reservation_id)
            if not r:
                raise ValueError('Réservation introuvable')
            r.status = 'cancelled'
            db.commit()
            return r
        finally:
            db.close()
