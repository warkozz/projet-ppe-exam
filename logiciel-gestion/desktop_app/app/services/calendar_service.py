# calendar_service.py - Service pour la gestion du calendrier des réservations
from datetime import datetime, date, timedelta
from collections import defaultdict
from typing import Dict, List, Optional, Tuple
from sqlalchemy import and_, extract, func, or_, Date, Time
from app.models.db import SessionLocal
from app.models.reservation import Reservation
from app.models.user import User  
from app.models.terrain import Terrain

class CalendarService:
    """Service pour gérer les données du calendrier des réservations"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def get_monthly_reservations(self, year: int, month: int) -> Dict[int, List[dict]]:
        """
        Récupère toutes les réservations pour un mois donné
        Retourne: {jour: [liste des réservations]}
        """
        try:
            reservations = self.db.query(Reservation)\
                .join(User, Reservation.user_id == User.id)\
                .join(Terrain, Reservation.terrain_id == Terrain.id)\
                .filter(
                    and_(
                        extract('year', Reservation.start) == year,
                        extract('month', Reservation.start) == month,
                        Reservation.status == 'confirmed'
                    )
                )\
                .all()
            
            # Grouper par jour
            reservations_by_day = defaultdict(list)
            
            for reservation in reservations:
                day = reservation.start.day
                
                # Récupérer les détails utilisateur et terrain
                user = reservation.user
                terrain = reservation.terrain
                
                reservation_data = {
                    'id': reservation.id,
                    'user_id': reservation.user_id,
                    'terrain_id': reservation.terrain_id,
                    'start': reservation.start,
                    'end': reservation.end,
                    'user_name': user.username if user else f"User {reservation.user_id}",
                    'user_email': user.email if user and user.email else "",
                    'user_name': user.username if user else f"User {reservation.user_id}",
                    'user_email': user.email if user and user.email else "",
                    'terrain_name': terrain.name if terrain else f"Terrain {reservation.terrain_id}",
                    'terrain_location': terrain.location if terrain and terrain.location else "",
                    'notes': reservation.notes or "",
                    'status': reservation.status,
                    'time_slot': f"{reservation.start.strftime('%H:%M')} - {reservation.end.strftime('%H:%M')}",
                    'duration_hours': (reservation.end - reservation.start).seconds // 3600
                }
                
                reservations_by_day[day].append(reservation_data)
            
            return dict(reservations_by_day)
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des réservations mensuelles: {e}")
            return {}
    
    def get_monthly_reservations_filtered(self, year: int, month: int, 
                                        user_id: Optional[int] = None, 
                                        terrain_id: Optional[int] = None) -> Dict[int, List[dict]]:
        """
        Récupère les réservations d'un mois avec filtres appliqués
        Retourne: {jour: [liste des réservations]}
        """
        try:
            query = self.db.query(Reservation)\
                .join(User, Reservation.user_id == User.id)\
                .join(Terrain, Reservation.terrain_id == Terrain.id)
            
            # Filtres de base
            query = query.filter(
                and_(
                    extract('year', Reservation.start) == year,
                    extract('month', Reservation.start) == month,
                    Reservation.status == 'confirmed'
                )
            )
            
            # Filtres optionnels
            if user_id:
                query = query.filter(Reservation.user_id == user_id)
                
            if terrain_id:
                query = query.filter(Reservation.terrain_id == terrain_id)
            
            reservations = query.order_by(Reservation.start).all()
            
            # Regrouper par jour
            reservations_by_day = defaultdict(list)
            
            for reservation in reservations:
                day = reservation.start.day
                user = reservation.user
                terrain = reservation.terrain
                
                reservation_data = {
                    'id': reservation.id,
                    'start': reservation.start,
                    'end': reservation.end,
                    'user_name': user.username if user else f"User {reservation.user_id}",
                    'user_email': user.email if user and user.email else "",
                    'terrain_name': terrain.name if terrain else f"Terrain {reservation.terrain_id}",
                    'terrain_location': terrain.location if terrain and terrain.location else "",
                    'notes': reservation.notes or "",
                    'status': reservation.status,
                    'time_slot': f"{reservation.start.strftime('%H:%M')} - {reservation.end.strftime('%H:%M')}",
                    'duration_hours': (reservation.end - reservation.start).seconds // 3600
                }
                
                reservations_by_day[day].append(reservation_data)
            
            return dict(reservations_by_day)
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des réservations filtrées: {e}")
            return {}
    
    def get_yearly_overview(self, year: int) -> Dict[str, int]:
        """
        Récupère un aperçu annuel du nombre de réservations par mois
        """
        try:
            monthly_counts = self.db.query(
                extract('month', Reservation.start).label('month'),
                func.count(Reservation.id).label('count')
            )\
            .filter(
                and_(
                    extract('year', Reservation.start) == year,
                    Reservation.status == 'confirmed'
                )
            )\
            .group_by(extract('month', Reservation.start))\
            .all()
            
            # Créer un dictionnaire avec tous les mois (0 par défaut)
            months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin',
                     'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
            
            result = {}
            for i, month_name in enumerate(months, 1):
                result[month_name] = 0
            
            # Remplir avec les vraies données
            for month, count in monthly_counts:
                month_name = months[int(month) - 1]
                result[month_name] = count
                
            return result
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de l'aperçu annuel: {e}")
            return {}
    
    def get_day_reservations(self, target_date: date) -> List[dict]:
        """
        Récupère toutes les réservations pour une date précise
        """
        try:
            start_datetime = datetime.combine(target_date, datetime.min.time())
            end_datetime = datetime.combine(target_date, datetime.max.time())
            
            reservations = self.db.query(Reservation)\
                .join(User, Reservation.user_id == User.id)\
                .join(Terrain, Reservation.terrain_id == Terrain.id)\
                .filter(
                    and_(
                        Reservation.start >= start_datetime,
                        Reservation.start <= end_datetime,
                        Reservation.status == 'confirmed'
                    )
                )\
                .order_by(Reservation.start)\
                .all()
            
            result = []
            for reservation in reservations:
                user = reservation.user
                terrain = reservation.terrain
                
                result.append({
                    'id': reservation.id,
                    'user_id': reservation.user_id,
                    'terrain_id': reservation.terrain_id,
                    'start': reservation.start,
                    'end': reservation.end,
                    'user_name': user.username if user else f"User {reservation.user_id}",
                    'user_email': user.email if user and user.email else "",
                    'user_role': user.role if user else "user",
                    'terrain_name': terrain.name if terrain else f"Terrain {reservation.terrain_id}",
                    'terrain_location': terrain.location if terrain and terrain.location else "",
                    'terrain_active': terrain.active if terrain else True,
                    'notes': reservation.notes or "",
                    'status': reservation.status,
                    'time_slot': f"{reservation.start.strftime('%H:%M')} - {reservation.end.strftime('%H:%M')}",
                    'duration_hours': (reservation.end - reservation.start).seconds // 3600,
                    'created_at': reservation.created_at if hasattr(reservation, 'created_at') else None
                })
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des réservations du jour: {e}")
            return []
    
    def get_filtered_reservations(self, 
                                 start_date: date, 
                                 end_date: date,
                                 user_id: Optional[int] = None,
                                 terrain_id: Optional[int] = None,
                                 status: Optional[str] = 'active') -> List[dict]:
        """
        Récupère les réservations avec des filtres avancés
        """
        try:
            query = self.db.query(Reservation)\
                .join(User, Reservation.user_id == User.id)\
                .join(Terrain, Reservation.terrain_id == Terrain.id)
            
            # Filtres de base
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time())
            
            query = query.filter(
                and_(
                    Reservation.start >= start_datetime,
                    Reservation.start <= end_datetime
                )
            )
            
            # Filtres optionnels
            if status:
                query = query.filter(Reservation.status == status)
            
            if user_id:
                query = query.filter(Reservation.user_id == user_id)
                
            if terrain_id:
                query = query.filter(Reservation.terrain_id == terrain_id)
            
            reservations = query.order_by(Reservation.start).all()
            
            result = []
            for reservation in reservations:
                user = reservation.user
                terrain = reservation.terrain
                
                result.append({
                    'id': reservation.id,
                    'date': reservation.start.date(),
                    'start': reservation.start,
                    'end': reservation.end,
                    'user_name': user.username if user else f"User {reservation.user_id}",
                    'terrain_name': terrain.name if terrain else f"Terrain {reservation.terrain_id}",
                    'notes': reservation.notes or "",
                    'status': reservation.status,
                    'time_slot': f"{reservation.start.strftime('%H:%M')} - {reservation.end.strftime('%H:%M')}",
                })
            
            return result
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des réservations filtrées: {e}")
            return []
    
    def get_calendar_statistics(self, year: int) -> Dict[str, any]:
        """
        Calcule des statistiques pour le calendrier
        """
        try:
            # Total réservations année
            total_reservations = self.db.query(func.count(Reservation.id))\
                .filter(
                    and_(
                        extract('year', Reservation.start) == year,
                        Reservation.status == 'confirmed'
                    )
                )\
                .scalar()
            
            # Jours avec réservations
            days_with_reservations = self.db.query(
                func.count(func.distinct(func.date(Reservation.start)))
            )\
            .filter(
                and_(
                    extract('year', Reservation.start) == year,
                    Reservation.status == 'confirmed'
                )
            )\
            .scalar()
            
            # Terrain le plus réservé
            most_booked_terrain = self.db.query(
                Terrain.name,
                func.count(Reservation.id).label('count')
            )\
            .join(Reservation, Terrain.id == Reservation.terrain_id)\
            .filter(
                and_(
                    extract('year', Reservation.start) == year,
                    Reservation.status == 'confirmed'
                )
            )\
            .group_by(Terrain.name)\
            .order_by(func.count(Reservation.id).desc())\
            .first()
            
            return {
                'total_reservations': total_reservations or 0,
                'days_with_reservations': days_with_reservations or 0,
                'most_booked_terrain': {
                    'name': most_booked_terrain[0] if most_booked_terrain else 'Aucun',
                    'count': most_booked_terrain[1] if most_booked_terrain else 0
                },
                'year': year
            }
            
        except Exception as e:
            print(f"❌ Erreur lors du calcul des statistiques: {e}")
            return {
                'total_reservations': 0,
                'days_with_reservations': 0,
                'most_booked_terrain': {'name': 'Aucun', 'count': 0},
                'year': year
            }
    
    def get_available_years(self) -> List[int]:
        """
        Récupère toutes les années qui ont des réservations
        """
        try:
            years = self.db.query(
                func.distinct(extract('year', Reservation.start)).label('year')
            )\
            .filter(Reservation.status == 'confirmed')\
            .order_by(extract('year', Reservation.start))\
            .all()
            
            result = [int(year[0]) for year in years]
            
            # Toujours inclure l'année courante et suivante
            current_year = datetime.now().year
            if current_year not in result:
                result.append(current_year)
            if (current_year + 1) not in result:
                result.append(current_year + 1)
                
            return sorted(result)
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des années: {e}")
            return [datetime.now().year, datetime.now().year + 1]
    
    def get_upcoming_reservations(self, limit=10):
        """Obtenir les prochaines réservations confirmées"""
        try:
            today = datetime.now().date()
            current_time = datetime.now().time()
            
            # Récupérer les réservations futures (à partir d'aujourd'hui)
            upcoming = self.db.query(Reservation).join(User).join(Terrain).filter(
                and_(
                    Reservation.status == 'confirmed',
                    or_(
                        Reservation.start.cast(Date) > today,
                        and_(
                            Reservation.start.cast(Date) == today,
                            Reservation.start.cast(Time) >= current_time
                        )
                    )
                )
            ).order_by(
                Reservation.start.asc()
            ).limit(limit).all()
            
            result = []
            for reservation in upcoming:
                result.append({
                    'id': reservation.id,
                    'date': reservation.start.date(),
                    'time_slot': reservation.start.strftime('%H:%M'),
                    'terrain_name': reservation.terrain.name,
                    'user_name': reservation.user.username,
                    'status': reservation.status
                })
            
            return result
        except Exception as e:
            print(f"❌ Erreur réservations à venir: {e}")
            return []
    
    def get_past_reservations(self, limit=10):
        """Obtenir les réservations passées"""
        try:
            today = datetime.now().date()
            current_time = datetime.now().time()
            
            # Récupérer les réservations passées
            past = self.db.query(Reservation).join(User).join(Terrain).filter(
                and_(
                    Reservation.status == 'confirmed',
                    or_(
                        Reservation.start.cast(Date) < today,
                        and_(
                            Reservation.start.cast(Date) == today,
                            Reservation.start.cast(Time) < current_time
                        )
                    )
                )
            ).order_by(
                Reservation.start.desc()
            ).limit(limit).all()
            
            result = []
            for reservation in past:
                result.append({
                    'id': reservation.id,
                    'date': reservation.start.date(),
                    'time_slot': reservation.start.strftime('%H:%M'),
                    'terrain_name': reservation.terrain.name,
                    'user_name': reservation.user.username,
                    'status': reservation.status
                })
            
            return result
        except Exception as e:
            print(f"❌ Erreur réservations passées: {e}")
            return []
    
    def close(self):
        """Fermer la session de base de données"""
        self.db.close()
    
    def __del__(self):
        """Destructeur pour s'assurer que la session est fermée"""
        if hasattr(self, 'db'):
            self.db.close()