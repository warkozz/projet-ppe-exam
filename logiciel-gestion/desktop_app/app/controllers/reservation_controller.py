from datetime import datetime
from app.models.db import SessionLocal
from app.models.reservation import Reservation
from app.services.cpp_bridge import check_conflict
class ReservationController:
    def __init__(self):
        self.db = SessionLocal()
    def create_reservation(self, user_id, terrain_id, start: datetime, end: datetime, notes=''):
        conflict = check_conflict(self.db, terrain_id, start, end)
        if conflict: raise ValueError('Conflict detected')
        r = Reservation(user_id=user_id, terrain_id=terrain_id, start=start, end=end, notes=notes)
        self.db.add(r); self.db.commit(); self.db.refresh(r); return r
    def get_reservations(self, date_from=None, date_to=None):
        q = self.db.query(Reservation)
        if date_from: q = q.filter(Reservation.start >= date_from)
        if date_to: q = q.filter(Reservation.end <= date_to)
        return q.all()
    def cancel_reservation(self, reservation_id):
        r = self.db.query(Reservation).get(reservation_id)
        if not r: raise ValueError('Reservation not found')
        r.status = 'cancelled'; self.db.commit(); return r
