import os, ctypes
from app.models.reservation import Reservation
libname = 'libreservation_engine.so' if os.name!='nt' else 'reservation_engine.dll'
libpath = os.path.join(os.path.dirname(__file__), '..', 'cpp', 'build', libname)
try:
    _lib = ctypes.cdll.LoadLibrary(libpath)
    _lib.check_conflict.argtypes = [ctypes.c_int, ctypes.c_long, ctypes.c_long]
    _lib.check_conflict.restype = ctypes.c_int
    def check_conflict(db_session, terrain_id, start, end):
        st = int(start.timestamp()); en = int(end.timestamp()); return bool(_lib.check_conflict(int(terrain_id), st, en))
except Exception:
    # fallback python check
    def check_conflict(db_session, terrain_id, start, end, exclude_reservation_id=None):
        q = db_session.query(Reservation).filter(Reservation.terrain_id==terrain_id, Reservation.status!='cancelled')
        if exclude_reservation_id:
            q = q.filter(Reservation.id != exclude_reservation_id)
        for r in q.all():
            if not (end <= r.start or start >= r.end):
                return True
        return False
