# calendar_view.py - Vue calendrier moderne et fonctionnelle
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QPushButton, QCalendarWidget, QFrame, QScrollArea, QSplitter,
    QComboBox, QDateEdit, QTextEdit, QListWidget, QListWidgetItem,
    QDialog, QDialogButtonBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QMessageBox, QTimeEdit,
    QFormLayout, QGroupBox, QProgressBar, QTabWidget, QCheckBox,
    QSpinBox, QSlider, QToolButton, QMenu, QSystemTrayIcon
)
from PySide6.QtCore import Qt, QDate, QTime, QTimer, Signal, QThread, QMutex, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QPalette, QColor, QTextCharFormat, QPainter, QPixmap, QIcon, QMovie, QAction
from datetime import datetime, date, timedelta
import calendar
from typing import List, Dict, Optional, Any
from app.services.calendar_service import CalendarService
from app.controllers.user_controller import UserController
from app.controllers.terrain_controller import TerrainController
from app.controllers.reservation_controller import ReservationController
from app.styles.theme import FootballTheme

class HoverButton(QPushButton):
    """Bouton avec effet de survol"""
    
    def __init__(self, text: str, icon: str = "", parent=None):
        super().__init__(f"{icon} {text}" if icon else text, parent)
        self.setStyleSheet(f"""
            QPushButton {{
                background: {FootballTheme.PRIMARY};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {FootballTheme.PRIMARY_DARK};
                transform: scale(1.02);
            }}
        """)

class EnhancedButton(QPushButton):
    """Bouton moderne avec animations et effets visuels"""
    
    def __init__(self, text: str, icon: str = "", button_type: str = "primary", parent=None):
        super().__init__(f"{icon} {text}" if icon else text, parent)
        self.button_type = button_type
        self.is_loading = False
        self._setup_styles()
        self._setup_animation()
        
        # Ajouter une tooltip si le texte est long
        if len(text) > 15:
            self.setToolTip(text)
    
    def _setup_styles(self):
        """Configuration des styles selon le type"""
        styles = {
            "primary": {
                "base": f"""QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {FootballTheme.PRIMARY}, stop:1 {FootballTheme.PRIMARY_DARK});
                    color: white; border: none; border-radius: 8px;
                    padding: 10px 15px; font-weight: 600; font-size: 14px;
                    margin: 2px; min-height: 20px;
                }}""",
                "hover": f"""QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {FootballTheme.PRIMARY_LIGHT}, stop:1 {FootballTheme.PRIMARY});
                    color: white; border: none; border-radius: 8px;
                    padding: 10px 15px; font-weight: 600; font-size: 14px;
                    margin: 2px; min-height: 20px; transform: scale(1.02);
                }}"""
            },
            "secondary": {
                "base": f"""QPushButton {{
                    background: white; color: {FootballTheme.PRIMARY};
                    border: 2px solid {FootballTheme.PRIMARY}; border-radius: 8px;
                    padding: 10px 15px; font-weight: 600; font-size: 14px;
                    margin: 2px; min-height: 20px;
                }}""",
                "hover": f"""QPushButton {{
                    background: {FootballTheme.PRIMARY_LIGHT}; color: white;
                    border: 2px solid {FootballTheme.PRIMARY}; border-radius: 8px;
                    padding: 10px 15px; font-weight: 600; font-size: 14px;
                    margin: 2px; min-height: 20px;
                }}"""
            },
            "danger": {
                "base": """QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #F44336, stop:1 #D32F2F);
                    color: white; border: none; border-radius: 8px;
                    padding: 10px 15px; font-weight: 600; font-size: 14px;
                    margin: 2px; min-height: 20px;
                }""",
                "hover": """QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #EF5350, stop:1 #F44336);
                    color: white; border: none; border-radius: 8px;
                    padding: 10px 15px; font-weight: 600; font-size: 14px;
                    margin: 2px; min-height: 20px;
                }"""
            }
        }
        
        self.base_style = styles.get(self.button_type, styles["primary"])["base"]
        self.hover_style = styles.get(self.button_type, styles["primary"])["hover"]
        self.setStyleSheet(self.base_style)
    
    def _setup_animation(self):
        """Configuration des animations"""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def enterEvent(self, event):
        if not self.is_loading:
            self.setStyleSheet(self.hover_style)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        if not self.is_loading:
            self.setStyleSheet(self.base_style)
        super().leaveEvent(event)
    
    def set_loading(self, loading: bool):
        """Activer/désactiver l'état de chargement"""
        self.is_loading = loading
        if loading:
            self.setText("⏳ Chargement...")
            self.setEnabled(False)
        else:
            # Restaurer le texte original (à implémenter selon les besoins)
            self.setEnabled(True)

# === CLASSE RESERVATIONDETAILSDIALOG SUPPRIMÉE ===
# Cette classe affichait la page "Reservations du ..." indésirée
# Remplacée par des appels directs à UnifiedReservationDialog

class FootballCalendarWidget(QCalendarWidget):
    """Widget calendrier personnalisé avec thème football"""
    
    dateClicked = Signal(QDate)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calendar_service = CalendarService()
        self.reservations_data = {}
        self._setup_style()
        
        # Connexions
        self.clicked.connect(self._on_date_clicked)
        self.currentPageChanged.connect(self._on_page_changed)
        
        # Charger les données du mois courant
        current_date = QDate.currentDate()

        
        # Forcer l'affichage du mois courant
        self.setCurrentPage(current_date.year(), current_date.month())
        self._load_month_data(current_date.year(), current_date.month())
    
    def _setup_style(self):
        """Configuration du style du calendrier"""
        # Style basique sans interférence avec les couleurs personnalisées
        self.setStyleSheet(f"""
            QCalendarWidget {{
                border: 2px solid {FootballTheme.PRIMARY};
                border-radius: 12px;
                font-size: 14px;
            }}
            QCalendarWidget QSpinBox {{
                background: {FootballTheme.PRIMARY};
                color: white;
                border: none;
                padding: 5px;
                font-weight: bold;
            }}
            QCalendarWidget QToolButton {{
                background: {FootballTheme.PRIMARY};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
                margin: 2px;
            }}
        """)
    
    def _load_month_data(self, year: int, month: int):
        """Charger les données de réservation pour un mois"""
        # Forcer l'expiration du cache de la session DB pour avoir les données les plus fraîches
        try:
            if hasattr(self.calendar_service, 'db') and self.calendar_service.db:
                self.calendar_service.db.expire_all()
                self.calendar_service.db.commit()
        except Exception:
            pass
        
        self.reservations_data = self.calendar_service.get_monthly_reservations(year, month)
        self._update_calendar_display()
    
    def _update_calendar_display(self):
        """Mettre à jour l'affichage du calendrier avec un point rouge pour les jours avec réservations"""
        # Forcer un rechargement complet de l'affichage
        self.updateCells()  # Met à jour toutes les cellules
        self.update()       # Met à jour le widget
        self.repaint()      # Redessine immédiatement
    
    def force_red_dots_update(self):
        """Forcer une mise à jour instantanée des points rouges (méthode utilitaire)"""
        current_year = self.yearShown()
        current_month = self.monthShown()
        
        # Forcer l'expiration du cache et recharger les données
        try:
            if hasattr(self.calendar_service, 'db') and self.calendar_service.db:
                self.calendar_service.db.expire_all()
                self.calendar_service.db.commit()
        except Exception:
            pass
        
        # Recharger les données et redessiner
        self.reservations_data = self.calendar_service.get_monthly_reservations(current_year, current_month)
        
        # Triple force du redessin pour garantir la mise à jour des points rouges
        QApplication.processEvents()
        self.updateCells()
        self.repaint()
    
    def paintCell(self, painter, rect, date):
        """Personnaliser l'affichage des cellules du calendrier"""
        # Dessiner la cellule normale d'abord
        super().paintCell(painter, rect, date)
        
        # Vérifier si cette date a des réservations (avec protection contre les données manquantes)
        has_reservations = False
        if hasattr(self, 'reservations_data') and self.reservations_data is not None:
            has_reservations = (date.year() == self.yearShown() and 
                              date.month() == self.monthShown() and 
                              date.day() in self.reservations_data and
                              len(self.reservations_data[date.day()]) > 0)
        
        # Points rouges pour les jours avec réservations (sans logs)
        
        if has_reservations:
            # Dessiner un petit point rouge dans le coin supérieur droit
            painter.save()
            painter.setBrush(QColor('red'))
            painter.setPen(QColor('red'))
            
            # Position du point (coin supérieur droit de la cellule)
            point_size = 6
            point_x = rect.right() - point_size - 2
            point_y = rect.top() + 2
            
            painter.drawEllipse(point_x, point_y, point_size, point_size)
            painter.restore()
            
            # Point rouge dessiné
    

    
    def _on_date_clicked(self, date: QDate):
        """Gérer le clic sur une date"""
        # Simplement émettre le signal sans ouvrir automatiquement le dialog
        self.dateClicked.emit(date)
        day = date.day()
        if day in self.reservations_data and len(self.reservations_data[day]) > 0:
            pass
    
    def _on_page_changed(self, year: int, month: int):
        """Gérer le changement de mois/année"""
        self._load_month_data(year, month)
    
    def get_date_reservations(self, date: QDate) -> list:
        """Récupérer les réservations pour une date spécifique"""
        python_date = date.toPython()
        return self.calendar_service.get_day_reservations(python_date)
    


class HybridCalendarView(QWidget):
    """Vue principale du calendrier des réservations"""
    
    def __init__(self, parent=None, notifications_service=None):
        super().__init__(parent)
        self.calendar_service = CalendarService()
        self.user_controller = UserController()
        self.terrain_controller = TerrainController()
        self.reservation_controller = ReservationController()  # AJOUTÉ
        self.notifications_service = notifications_service
        self.selected_date = QDate.currentDate()  # AJOUTÉ - Date sélectionnée
        
        # Se connecter aux notifications si le service est disponible
        if self.notifications_service:
            self.notifications_service.reservation_data_changed.connect(self._on_data_changed)
            print("🔔 Calendrier connecté aux notifications globales")
        
        self.setWindowTitle('📅 Calendrier des Réservations - Football Manager 5v5')
        self.setMinimumSize(1200, 800)
        
        # Style global
        self.setStyleSheet(f"""
            QWidget {{
                background: #f8f9fa;
                color: #1b5e20;
                font-family: 'Segoe UI', sans-serif;
            }}
            QLabel {{
                color: #1b5e20;
                font-weight: bold;
                padding: 4px;
                background: transparent;
            }}
            QComboBox, QDateEdit {{
                background: white;
                border: 2px solid #c8e6c9;
                border-radius: 4px;
                padding: 6px;
                color: #1b5e20;
                min-height: 20px;
            }}
            QFrame {{
                background: white;
                border: 1px solid {FootballTheme.TEXT_HINT};
                border-radius: 8px;
            }}
        """)
        
        self._build_ui()
        self._connect_events()
        self._load_initial_data()
    
    def _build_ui(self):
        """Construction de l'interface"""
        layout = QVBoxLayout(self)
        
        # En-tête avec titre
        header = self._create_header()
        layout.addWidget(header)
        
        # Barre de contrôles (filtres, navigation)
        controls = self._create_controls()
        layout.addWidget(controls)
        
        # Contenu principal avec splitter
        main_content = self._create_main_content()
        layout.addWidget(main_content)
        
        # Barre de statut/statistiques
        status_bar = self._create_status_bar()
        layout.addWidget(status_bar)
    
    def _create_header(self):
        """Créer l'en-tête"""
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_layout = QHBoxLayout(header_frame)
        
        # Titre principal
        title = QLabel('📅 Calendrier des Réservations')
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {FootballTheme.PRIMARY_DARK};
                background: {FootballTheme.SURFACE};
                padding: 15px;
                border-radius: 8px;
                border: 2px solid {FootballTheme.PRIMARY};
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Bouton retour
        self.btn_back = HoverButton('Retour', '🔙')
        self.btn_back.setFixedWidth(120)
        header_layout.addWidget(self.btn_back)
        
        return header_frame
    
    def _create_controls(self):
        """Créer la barre de contrôles"""
        controls_frame = QFrame()
        controls_frame.setFixedHeight(60)
        controls_layout = QHBoxLayout(controls_frame)
        
        controls_layout.addStretch()
        
        # Bouton actualiser
        self.btn_refresh = HoverButton('🔄 Actualiser', '')
        self.btn_refresh.setFixedWidth(120)
        controls_layout.addWidget(self.btn_refresh)
        
        # Bouton aujourd'hui
        self.btn_today = HoverButton('📍 Aujourd\'hui', '')
        self.btn_today.setFixedWidth(120)
        controls_layout.addWidget(self.btn_today)
        
        return controls_frame
    
    def _create_main_content(self):
        """Créer le contenu principal avec calendrier"""
        splitter = QSplitter(Qt.Horizontal)
        
        # Partie gauche: Calendrier
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Widget calendrier personnalisé
        self.calendar = FootballCalendarWidget()
        self.calendar.setMinimumSize(600, 500)
        # Connexion gérée dans _connect_events()
        left_layout.addWidget(self.calendar)
        
        splitter.addWidget(left_widget)
        
        # Partie droite: Statistiques et légendes
        right_widget = self._create_sidebar()
        splitter.addWidget(right_widget)
        
        # Ratio 70/30
        splitter.setSizes([700, 300])
        
        return splitter
    
    def _create_sidebar(self):
        """Créer la barre latérale avec statistiques"""
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        
        # Statistiques annuelles
        stats_frame = QFrame()
        stats_layout = QVBoxLayout(stats_frame)
        
        stats_title = QLabel('📊 Statistiques')
        stats_title.setStyleSheet(f"""
            font-size: 16px; 
            font-weight: bold; 
            color: {FootballTheme.PRIMARY_DARK};
            padding: 10px;
            background: {FootballTheme.SURFACE};
            border-radius: 6px;
        """)
        stats_layout.addWidget(stats_title)
        
        self.stats_content = QLabel('Chargement...')
        self.stats_content.setStyleSheet("padding: 10px;")
        self.stats_content.setWordWrap(True)
        stats_layout.addWidget(self.stats_content)
        
        sidebar_layout.addWidget(stats_frame)
        
        # Section Réservations à venir
        upcoming_frame = QFrame()
        upcoming_layout = QVBoxLayout(upcoming_frame)
        
        upcoming_title = QLabel('📅 Réservations à venir')
        upcoming_title.setStyleSheet(f"""
            font-size: 16px; 
            font-weight: bold; 
            color: {FootballTheme.PRIMARY_DARK};
            padding: 10px;
            background: {FootballTheme.SURFACE};
            border-radius: 6px;
        """)
        upcoming_layout.addWidget(upcoming_title)
        
        upcoming_list = QListWidget()
        upcoming_list.setMaximumHeight(150)
        upcoming_list.setStyleSheet(f"""
            QListWidget {{
                background: white;
                border: 1px solid {FootballTheme.PRIMARY_LIGHT};
                border-radius: 6px;
                padding: 5px;
                font-size: 13px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #eee;
                color: {FootballTheme.TEXT_PRIMARY};
            }}
            QListWidget::item:hover {{
                background: {FootballTheme.PRIMARY_LIGHT};
            }}
        """)
        upcoming_layout.addWidget(upcoming_list)
        self.upcoming_list = upcoming_list  # Sauvegarder la référence
        
        # Connexion pour le clic
        self.upcoming_list.itemClicked.connect(self._on_upcoming_item_clicked)
        
        sidebar_layout.addWidget(upcoming_frame)
        
        # Section Réservations passées
        past_frame = QFrame()
        past_layout = QVBoxLayout(past_frame)
        
        past_title = QLabel('📋 Réservations passées')
        past_title.setStyleSheet(f"""
            font-size: 16px; 
            font-weight: bold; 
            color: {FootballTheme.PRIMARY_DARK};
            padding: 10px;
            background: {FootballTheme.SURFACE};
            border-radius: 6px;
        """)
        past_layout.addWidget(past_title)
        
        past_list = QListWidget()
        past_list.setMaximumHeight(150)
        past_list.setStyleSheet(f"""
            QListWidget {{
                background: white;
                border: 1px solid {FootballTheme.PRIMARY_LIGHT};
                border-radius: 6px;
                padding: 5px;
                font-size: 13px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #eee;
                color: {FootballTheme.TEXT_SECONDARY};
            }}
            QListWidget::item:hover {{
                background: {FootballTheme.SURFACE};
            }}
        """)
        past_layout.addWidget(past_list)
        self.past_list = past_list  # Sauvegarder la référence
        
        # Connexion pour le clic
        self.past_list.itemClicked.connect(self._on_past_item_clicked)
        
        sidebar_layout.addWidget(past_frame)
        
        sidebar_layout.addStretch()
        
        return sidebar
    
    def _create_status_bar(self):
        """Créer la barre de statut"""
        status_frame = QFrame()
        status_frame.setFixedHeight(40)
        status_layout = QHBoxLayout(status_frame)
        
        self.status_label = QLabel('📅 Calendrier chargé')
        self.status_label.setStyleSheet(f"color: {FootballTheme.PRIMARY_DARK}; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        # Horloge temps réel
        self.time_label = QLabel()
        self.update_time()
        
        # Timer pour mettre à jour l'heure avec protection d'erreur
        try:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_time)
            self.timer.start(1000)  # Chaque seconde
        except Exception as e:
            print(f"⚠️ Erreur lors de la création du timer: {e}")
            self.timer = None
        
        # Timer de vérification des changements (fallback pour les notifications manquées)
        try:
            self.check_timer = QTimer(self)
            self.check_timer.timeout.connect(self._check_for_changes)
            self.check_timer.start(3000)  # Toutes les 3 secondes
            self.last_reservation_count = 0
            print("🔍 Timer de vérification des changements activé (toutes les 3s)")
        except Exception as e:
            print(f"⚠️ Erreur lors de la création du timer de vérification: {e}")
            self.check_timer = None
        
        status_layout.addWidget(self.time_label)
        
        return status_frame
    
    def _check_for_changes(self):
        """Vérifier périodiquement s'il y a eu des changements"""
        try:
            # Forcer le rechargement des données fraîches
            try:
                if hasattr(self.calendar_service, 'db') and self.calendar_service.db:
                    self.calendar_service.db.commit()
                    self.calendar_service.db.expire_all()
            except Exception:
                pass
            
            # Récupérer les réservations pour calcul de signature
            all_reservations = []
            upcoming = self.calendar_service.get_upcoming_reservations(50)
            past = self.calendar_service.get_past_reservations(50)
            all_reservations.extend(upcoming)
            all_reservations.extend(past)
            
            # Calculer signature pour détecter les changements
            signature_parts = []
            for res in all_reservations:
                res_sig = f"{res.get('id', 0)}_{str(res.get('notes', ''))}_{str(res.get('time_slot', ''))}_{str(res.get('status', ''))}_{str(res.get('terrain_name', ''))}_{str(res.get('user_name', ''))}"
                signature_parts.append(hash(res_sig))
            
            total_hash = hash(str(sorted(signature_parts)))
            current_signature = f"{len(all_reservations)}_{total_hash}"
            
            # Vérifier les changements
            if not hasattr(self, 'last_signature'):
                self.last_signature = current_signature
            elif current_signature != self.last_signature:

                self.last_signature = current_signature
                self._force_instant_calendar_update()
                
        except Exception as e:
            # Fallback silencieux
            if not hasattr(self, '_fallback_counter'):
                self._fallback_counter = 0
            self._fallback_counter += 1
            if self._fallback_counter >= 10:  # Toutes les 30 secondes
                self._force_instant_calendar_update()
                self._fallback_counter = 0
    
    def cleanup(self):
        """Nettoyer les ressources lors de la fermeture"""
        try:
            if hasattr(self, 'timer') and self.timer is not None:
                self.timer.stop()
                self.timer = None
            if hasattr(self, 'check_timer') and self.check_timer is not None:
                self.check_timer.stop()
                self.check_timer = None
        except Exception:
            pass
    
    def closeEvent(self, event):
        """Gérer la fermeture de la fenêtre"""
        self.cleanup()
        super().closeEvent(event)
    
    def _connect_events(self):
        """Connecter les événements"""
        self.calendar.dateClicked.connect(self._on_date_selected)
        self.btn_refresh.clicked.connect(self._refresh_data)
        self.btn_today.clicked.connect(self._go_to_today)
    
    def _load_initial_data(self):
        """Charger les données initiales"""
        try:
            # Charger statistiques
            self._update_statistics()
            
            # Charger les listes de réservations
            self._update_reservation_lists()
            
            print("✅ Calendrier initialisé avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation du calendrier: {e}")
            self.stats_content.setText("❌ Erreur de chargement")
    
    def _on_date_selected(self, date: QDate):
        """Gérer la sélection d'une date"""
        try:
            self.selected_date = date  # Mettre à jour la date sélectionnée
            reservations = self.calendar.get_date_reservations(date)
            
            # Ouvrir directement le dialog de gestion unifié
            self._show_reservation_management_dialog(date, reservations)
            
            # Mettre à jour le statut
            count = len(reservations)
            date_str = date.toString('dd/MM/yyyy')
            self.status_label.setText(f"📅 {date_str} - {count} réservation(s)")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sélection de date: {e}")
            self.status_label.setText("❌ Erreur lors du chargement")
    

    
    def _refresh_data(self):
        """Actualiser les données - MISE À JOUR COMPLÈTE DE TOUTE L'INTERFACE"""
        print("🔄 Actualisation du calendrier...")
        
        self._force_instant_calendar_update()
        self._update_statistics()
        self._update_reservation_lists()
        self._refresh_all_interface_elements()
        
        self.status_label.setText("✅ Calendrier actualisé")
        print("✅ Actualisation terminée")
    
    def _refresh_all_interface_elements(self):
        """Mettre à jour TOUS les éléments dynamiques de l'interface"""
        try:
            self.update_time()
            if hasattr(self, 'title_label'):
                current_time = datetime.now().strftime('%H:%M')
                self.title_label.setText(f'📅 Calendrier des Réservations - {current_time}')
            self.update()
            self.repaint()
        except Exception as e:
            print(f"❌ Erreur mise à jour interface: {e}")
    
    def _on_data_changed(self):
        """Callback appelé quand les données de réservation changent dans d'autres vues"""
        self._force_instant_calendar_update()
        
        # Forcer une deuxième mise à jour pour s'assurer que tout est synchronisé
        from PySide6.QtCore import QTimer
        QTimer.singleShot(200, self._final_sync_update)  # Augmenté à 200ms
        
        # Forcer une troisième mise à jour pour la sécurité
        QTimer.singleShot(500, lambda: self._refresh_data())
    
    def _force_instant_calendar_update(self):
        """Forcer la mise à jour du calendrier"""
        try:
            # 1. Garantir une date valide
            target_date = getattr(self, "selected_date", QDate.currentDate())
            
            # 2. Recharger le mois actuellement affiché
            current_year = self.calendar.yearShown()
            current_month = self.calendar.monthShown()
            
            # 3. Forcer le rechargement des données fraîches depuis la DB
            # Forcer le rechargement des données fraîches
            try:
                if hasattr(self.calendar_service, 'db') and self.calendar_service.db:
                    self.calendar_service.db.commit()
                    self.calendar_service.db.expire_all()
            except Exception:
                pass
            
            # Recharger les données du mois avec expiration du cache
            self.calendar._load_month_data(current_year, current_month)
            
            # Recharger aussi le mois de selected_date si différent
            if target_date.year() != current_year or target_date.month() != current_month:
                self.calendar._load_month_data(target_date.year(), target_date.month())
            
            # Redessin robuste du calendrier pour les points rouges
            QApplication.processEvents()  # Traiter les événements en attente
            self.calendar.updateCells()   # Recalculer toutes les cellules
            self.calendar.update()        # Marquer pour redessin
            self.calendar.repaint()       # Forcer le redessin immédiat
            
            # Refresh différé léger pour la sécurité
            QTimer.singleShot(200, lambda: self._gentle_refresh())
            
        except Exception as e:
            print(f"❌ Erreur mise à jour calendrier: {e}")
            
            # 5. Refresh différé léger pour la sécurité
            QTimer.singleShot(200, lambda: self._gentle_refresh())
        
        # 6. Vérifier que les données sont bien présentes après rechargement
        if hasattr(self.calendar, 'reservations_data'):
            days_with_reservations = [day for day, reservations in self.calendar.reservations_data.items() if len(reservations) > 0]
    
    def _final_paint_update(self):
        """Forcer une dernière mise à jour des points rouges"""
        try:
            self.calendar.updateCells()
            self.calendar.repaint()
        except Exception:
            pass
    
    def _gentle_refresh(self):
        """Refresh doux sans clignotement"""
        try:
            self.calendar.updateCells()
        except Exception:
            pass
        
        # Rafraîchir les listes
        self._update_reservation_lists()
        
        # Rafraîchir la vue complète
        self.update()
        self.repaint()
    
    def _final_sync_update(self):
        """Mise à jour finale pour s'assurer de la synchronisation"""
        self.calendar.updateCells()
        self._update_statistics()
    
    def _go_to_today(self):
        """Aller à aujourd'hui"""
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)
        
        self.status_label.setText("📍 Aujourd'hui sélectionné")
    
    def _update_statistics(self):
        """Mettre à jour les statistiques"""
        try:
            year = datetime.now().year
            stats = self.calendar_service.get_calendar_statistics(year)
            
            stats_text = f"""
📊 <b>Statistiques {year}</b><br><br>
🎯 <b>{stats['total_reservations']}</b> réservations totales<br><br>
📅 <b>{stats['days_with_reservations']}</b> jours avec réservations<br><br>
🏆 Terrain le plus populaire:<br>
🏟️ <b>{stats['most_booked_terrain']['name']}</b><br>
📈 <b>{stats['most_booked_terrain']['count']}</b> réservations
            """
            
            self.stats_content.setText(stats_text)
            
        except Exception as e:
            print(f"❌ Erreur mise à jour statistiques: {e}")
            self.stats_content.setText("❌ Erreur de chargement")
    
    def update_time(self):
        """Mettre à jour l'affichage de l'heure avec gestion d'erreur robuste"""
        try:
            if hasattr(self, 'time_label') and self.time_label is not None:
                current_time = datetime.now().strftime("%H:%M:%S")
                current_date = datetime.now().strftime("%A %d %B %Y")
                self.time_label.setText(f"🕐 {current_time} | 📅 {current_date}")
                self.time_label.setStyleSheet(f"color: {FootballTheme.PRIMARY_DARK}; font-weight: bold;")
        except Exception as e:
            # Silencieusement ignorer les erreurs de mise à jour de l'heure
            # pour éviter de crasher l'application
            pass
    
    def _update_reservation_lists(self):
        """Mettre à jour les listes de réservations passées et à venir"""
        try:
            # Charger les réservations à venir
            upcoming = self.calendar_service.get_upcoming_reservations(10)
            self.upcoming_list.clear()
            
            if not upcoming:
                item = QListWidgetItem("Aucune réservation à venir")
                item.setData(Qt.UserRole + 1, 'empty')
                self.upcoming_list.addItem(item)
            else:
                for reservation in upcoming:
                    date_str = reservation['date'].strftime('%d/%m/%Y')
                    text = f"{date_str} - {reservation['time_slot']}\n{reservation['terrain_name']} ({reservation['user_name']})"
                    item = QListWidgetItem(text)
                    # Stocker la date dans l'item pour la navigation
                    item.setData(Qt.UserRole, reservation['date'])
                    self.upcoming_list.addItem(item)
            
            # Charger les réservations passées
            past = self.calendar_service.get_past_reservations(10)
            self.past_list.clear()
            
            if not past:
                item = QListWidgetItem("Aucune réservation passée")
                item.setData(Qt.UserRole + 1, 'empty')
                self.past_list.addItem(item)
            else:
                for reservation in past:
                    date_str = reservation['date'].strftime('%d/%m/%Y')
                    text = f"{date_str} - {reservation['time_slot']}\n{reservation['terrain_name']} ({reservation['user_name']})"
                    item = QListWidgetItem(text)
                    # Stocker la date dans l'item pour la navigation
                    item.setData(Qt.UserRole, reservation['date'])
                    self.past_list.addItem(item)
                    
        except Exception as e:
            print(f"❌ Erreur mise à jour listes réservations: {e}")
    
    def _on_upcoming_item_clicked(self, item):
        """Gérer le clic sur un élément de la liste des réservations à venir"""
        date = item.data(Qt.UserRole)
        if date:
            self._navigate_to_date(date)
    
    def _on_past_item_clicked(self, item):
        """Gérer le clic sur un élément de la liste des réservations passées"""
        date = item.data(Qt.UserRole)
        if date:
            self._navigate_to_date(date)
    
    def _navigate_to_date(self, date):
        """Naviguer vers une date spécifique dans le calendrier"""
        try:
            # Convertir la date en QDate si nécessaire
            if hasattr(date, 'year'):  # Si c'est un objet date Python
                qdate = QDate(date.year, date.month, date.day)
            else:
                qdate = date
            
            # Changer la page du calendrier vers le mois de la date
            self.calendar.setCurrentPage(qdate.year(), qdate.month())
            
            # Sélectionner la date
            self.calendar.setSelectedDate(qdate)
            

            
        except Exception as e:
            print(f"❌ Erreur navigation vers date: {e}")
    
    # Méthode _on_calendar_date_clicked supprimée - redondante avec _on_date_selected
    
    def _show_reservation_management_dialog(self, date, reservations):
        """Afficher la fenêtre unifiée de gestion des réservations pour une date"""
        dialog = UnifiedReservationDialog(date, reservations, self.calendar_service, calendar_view=self, parent=self)
        result = dialog.exec()
        # Toujours recharger les données au retour du dialog, même si annulé

        self.calendar._load_month_data(date.year(), date.month())
        self._update_reservation_lists()
        
    def _save_notes_only(self, reservation, new_notes, dialog):
        """Sauvegarder seulement les notes d'une réservation"""
        try:
            # Convertir les dates de manière robuste
            from datetime import datetime
            
            # Conversion robuste de start
            if isinstance(reservation['start'], datetime):
                start_dt = reservation['start']
            elif isinstance(reservation['start'], str):
                start_dt = datetime.fromisoformat(reservation['start'])
            else:
                start_dt = datetime.combine(reservation['start'], datetime.min.time())
            
            # Conversion robuste de end    
            if isinstance(reservation['end'], datetime):
                end_dt = reservation['end']
            elif isinstance(reservation['end'], str):
                end_dt = datetime.fromisoformat(reservation['end'])
            else:
                end_dt = datetime.combine(reservation['end'], datetime.min.time())
            
            # Modifier seulement les notes (garder le même user_id et terrain_id)
            result = self.reservation_controller.modify_reservation(
                reservation['id'],
                reservation['user_id'],
                reservation['terrain_id'],
                start_dt,
                end_dt,
                new_notes
            )
            
            if result:
                QMessageBox.information(self, "Succès", "Notes sauvegardées!")
                dialog.accept()
                
                # MISE À JOUR INSTANTANÉE DIRECTE  
                # 1. Utiliser la vraie date de la réservation et mettre à jour selected_date
                start_datetime = reservation['start']  # C'est un datetime object
                reservation_date = QDate(start_datetime.year, start_datetime.month, start_datetime.day)
                
                # Garantir que selected_date correspond à la date de la réservation modifiée
                self.selected_date = reservation_date
                
                # 2. Forcer la mise à jour immédiate des points rouges
                self.calendar.force_red_dots_update()
                
                # Recharger aussi le mois complet si nécessaire
                if reservation_date.year() != self.calendar.yearShown() or reservation_date.month() != self.calendar.monthShown():
                    self.calendar._load_month_data(reservation_date.year(), reservation_date.month())
                
                # 3. Recharger TOUTES les listes de réservations
                self._update_reservation_lists()  # Listes principales (venir/passées)
                
                # 4. Si on est dans une modal, recharger aussi sa table
                if dialog and hasattr(dialog, '_load_reservations'):
                    dialog._load_reservations()  # Table de gauche dans la modal
                elif dialog and hasattr(dialog, 'reservation_list'):
                    # Recharger manuellement la liste dans la modal
                    current_date = dialog.date
                    python_date = current_date.toPython()
                    updated_reservations = self.calendar_service.get_day_reservations(python_date)
                    
                    dialog.reservation_list.clear()
                    for res in updated_reservations:
                        status_emoji = {'confirmed': '✅', 'pending': '⏳', 'cancelled': '❌'}.get(res['status'], '❓')
                        text = f"{status_emoji} {res['time_slot']} - {res['terrain_name']}\n" \
                               f"👤 {res['user_name']} ({res['user_email']})\n" \
                               f"📋 Status: {res['status']}"
                        if res.get('notes'):
                            text += f"\n💭 {res['notes']}"
                        
                        item = QListWidgetItem(text)
                        item.setData(Qt.UserRole, res)
                        dialog.reservation_list.addItem(item)
                
                # 4. Forcer une mise à jour de la vue complète
                self.update()
                self.repaint()
                
                # 5. Notification globale pour synchroniser les autres vues
                try:
                    from hybrid_main import app
                    if hasattr(app, 'notifications_service') and app.notifications_service:
                        app.notifications_service.notify_reservation_change()
                except:
                    pass
            else:
                QMessageBox.warning(self, "Erreur", "La sauvegarde des notes a échoué")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde: {str(e)}")


class UnifiedReservationDialog(QDialog):
    """Dialog unifié pour gérer les réservations avec actions intégrées"""
    
    def __init__(self, date, reservations, calendar_service, calendar_view=None, parent=None):
        super().__init__(parent)
        self.date = date
        self.reservations = reservations
        self.calendar_service = calendar_service
        self.calendar_view = calendar_view  # Référence directe à la vue calendrier
        self.reservation_controller = ReservationController()
        
        self.setWindowTitle(f"Gestion des réservations - {date.toString('dd/MM/yyyy')}")
        self.setMinimumSize(900, 600)
        self.setModal(True)
        
        self._setup_ui()
        self._load_reservations()
        # Rafraîchir automatiquement la vue calendrier quand la modale se ferme (quelle que soit la raison)
        if self.calendar_view:
            try:
                self.finished.disconnect()
            except Exception:
                pass
            self.finished.connect(lambda *_: self.calendar_view._refresh_data())
    
    def _setup_ui(self):
        """Configurer l'interface utilisateur unifiée"""
        main_layout = QHBoxLayout(self)
        
        # Partie gauche: Liste des réservations
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # En-tête avec navigation et date
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        # Flèche précédente
        self.prev_day_btn = QPushButton("◀️")
        self.prev_day_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {FootballTheme.PRIMARY};
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 12px;
                border: none;
                border-radius: 6px;
                margin: 5px;
                min-width: 40px;
            }}
            QPushButton:hover {{
                background-color: {FootballTheme.PRIMARY_DARK};
                transform: scale(1.1);
            }}
        """)
        self.prev_day_btn.clicked.connect(self._go_to_previous_day)
        self.prev_day_btn.setToolTip("Jour précédent")
        header_layout.addWidget(self.prev_day_btn)
        
        # Label de la date (maintenant au centre)
        self.date_label = QLabel(f"📅 Réservations du {self.date.toString('dddd dd MMMM yyyy')}")
        self.date_label.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {FootballTheme.PRIMARY_DARK};
                padding: 10px;
                background: {FootballTheme.SURFACE};
                border-radius: 6px;
                border: 1px solid {FootballTheme.PRIMARY};
            }}
        """)
        header_layout.addWidget(self.date_label)
        
        # Flèche suivante
        self.next_day_btn = QPushButton("▶️")
        self.next_day_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {FootballTheme.PRIMARY};
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 8px 12px;
                border: none;
                border-radius: 6px;
                margin: 5px;
                min-width: 40px;
            }}
            QPushButton:hover {{
                background-color: {FootballTheme.PRIMARY_DARK};
                transform: scale(1.1);
            }}
        """)
        self.next_day_btn.clicked.connect(self._go_to_next_day)
        self.next_day_btn.setToolTip("Jour suivant")
        header_layout.addWidget(self.next_day_btn)
        
        # Bouton d'ajout de réservation
        self.add_reservation_btn = QPushButton("➕ Ajouter réservation")
        self.add_reservation_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {FootballTheme.SUCCESS};
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 15px;
                border: none;
                border-radius: 6px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: #2E7D32;
                transform: scale(1.02);
            }}
        """)
        self.add_reservation_btn.clicked.connect(self._add_new_reservation)
        header_layout.addWidget(self.add_reservation_btn)
        
        left_layout.addWidget(header_widget)
        
        # Liste des réservations
        self.reservation_list = QListWidget()
        self.reservation_list.setStyleSheet(f"""
            QListWidget {{
                background: white;
                border: 1px solid {FootballTheme.PRIMARY_LIGHT};
                border-radius: 6px;
                padding: 5px;
                font-size: 13px;
                min-width: 400px;
            }}
            QListWidget::item {{
                padding: 10px;
                margin: 2px;
                border: 1px solid #ddd;
                border-radius: 6px;
                background: #f9f9f9;
                color: #1b5e20;
            }}
            QListWidget::item:hover {{
                background: {FootballTheme.PRIMARY_LIGHT};
                border-color: {FootballTheme.PRIMARY};
            }}
            QListWidget::item:selected {{
                background-color: {FootballTheme.PRIMARY};
                border: 2px solid {FootballTheme.PRIMARY_DARK};
                font-weight: bold;
            }}
        """)
        self.reservation_list.currentItemChanged.connect(self._on_reservation_selected)
        # 🔧 FIX: Ajouter aussi la connexion sur le clic pour forcer les couleurs
        self.reservation_list.itemClicked.connect(self._on_item_clicked)
        left_layout.addWidget(self.reservation_list)
        
        main_layout.addWidget(left_widget)
        
        # Partie droite: Actions pour la réservation sélectionnée
        self.details_widget = QWidget()  # Stocker comme attribut de classe
        right_layout = QVBoxLayout(self.details_widget)
        
        # Zone d'informations de la réservation sélectionnée
        self.info_label = QLabel("Sélectionnez une réservation pour voir les actions")
        self.info_label.setStyleSheet(f"""
            QLabel {{
                background: {FootballTheme.SURFACE};
                padding: 15px;
                border-radius: 8px;
                border: 1px solid {FootballTheme.PRIMARY_LIGHT};
                font-size: 14px;
                min-height: 120px;
            }}
        """)
        self.info_label.setAlignment(Qt.AlignTop)
        right_layout.addWidget(self.info_label)
        
        # Boutons d'action (plus gros et lisibles)
        self.action_buttons = QWidget()
        action_layout = QVBoxLayout(self.action_buttons)
        
        # Style commun pour tous les boutons d'action
        button_style = """
            QPushButton {{
                font-size: 16px;
                font-weight: bold;
                padding: 20px;
                border: none;
                border-radius: 10px;
                margin: 5px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                transform: scale(1.02);
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """
        
        self.modify_btn = QPushButton("📝 Ajouter une note")
        self.modify_btn.setStyleSheet(button_style + f"""
            QPushButton {{
                background-color: #42A5F5;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #1E88E5;
            }}
        """)
        self.modify_btn.clicked.connect(self._modify_selected_reservation)
        self.modify_btn.setEnabled(False)
        
        self.move_btn = QPushButton("📅 Déplacer date/heure")
        self.move_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #FF9800;
                color: white;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        self.move_btn.clicked.connect(self._move_selected_reservation)
        self.move_btn.setEnabled(False)
        
        self.delete_btn = QPushButton("🗑️ Supprimer la réservation")
        self.delete_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #F44336;
                color: white;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        self.delete_btn.clicked.connect(self._delete_selected_reservation)
        self.delete_btn.setEnabled(False)
        
        action_layout.addWidget(self.modify_btn)
        action_layout.addWidget(self.move_btn)
        action_layout.addWidget(self.delete_btn)
        action_layout.addStretch()
        
        right_layout.addWidget(self.action_buttons)
        
        main_layout.addWidget(self.details_widget)
        
        # Boutons globaux
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        # Bouton actualiser
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {FootballTheme.PRIMARY};
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: {FootballTheme.PRIMARY_DARK};
            }}
        """)
        refresh_btn.clicked.connect(self._refresh_modal_data)
        buttons_layout.addWidget(refresh_btn)
        
        # Bouton fermer  
        close_btn = QPushButton("❌ Fermer")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #9E9E9E;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                margin: 10px;
            }}
            QPushButton:hover {{
                background-color: #757575;
            }}
        """)
        close_btn.clicked.connect(self._close_dialog_properly)
        buttons_layout.addWidget(close_btn)
        
        # Ajouter le layout de boutons au layout principal
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        final_layout = QVBoxLayout(self)
        final_layout.addWidget(main_widget)
        final_layout.addLayout(buttons_layout)
        
        # Stocker la réservation actuellement sélectionnée
        self.selected_reservation = None
    
    def _refresh_modal_data(self):
        """Actualiser les données de la modal"""
        print("🔄 Actualisation des données de la modal...")
        
        # 🔧 FIX: Sauvegarder l'état avant rechargement
        had_selection = self.selected_reservation is not None
        
        # Recharger la table de gauche (avec préservation de sélection intégrée)
        self._load_reservations()
        
        # 🔧 FIX: S'assurer que les boutons sont dans le bon état
        if not had_selection and self.reservation_list.count() > 0:
            # Si on n'avait pas de sélection mais qu'il y a des réservations,
            # _load_reservations() devrait avoir sélectionné automatiquement la première
            current_item = self.reservation_list.currentItem()
            if current_item and current_item.data(Qt.UserRole):
                self.selected_reservation = current_item.data(Qt.UserRole)
                self._enable_action_buttons(True)
                print("🔧 Boutons d'action réactivés après actualisation")
        
        # Actualiser la vue calendrier principale aussi
        if self.calendar_view:
            self.calendar_view._refresh_data()
        
        print("✅ Modal actualisée avec succès")
    
    def _close_dialog_properly(self):
        """Fermer le dialog sans déclencher d'autres événements"""

        self.reject()
        # Assurer le rafraîchissement universel à la fermeture
        if self.calendar_view and hasattr(self.calendar_view, '_refresh_data'):
            self.calendar_view._refresh_data()
    
    def _reload_all_data(self):
        """Recharger toutes les données : liste actuelle, calendrier, et sidebar"""
        print("🔄 Rechargement complet des données...")
        
        # 1. Recharger la liste des réservations du dialog actuel
        self._load_reservations()
        
        # 2. Recharger le calendrier principal avec mise à jour forcée MULTIPLE
        if hasattr(self.parent(), 'calendar'):
            parent_calendar = self.parent().calendar
            current_year = self.date.year()
            current_month = self.date.month()
            
            # Forcer le rechargement des données
            parent_calendar._load_month_data(current_year, current_month)
            
            # Forcer la mise à jour visuelle PLUSIEURS FOIS
            parent_calendar.updateCells()
            parent_calendar.update()
            parent_calendar.repaint()
            
            # Utiliser le bouton actualiser du parent
            if hasattr(self.parent(), '_refresh_data'):
                self.parent()._refresh_data()
            
            # Recharger aussi les statistiques si la méthode existe
            if hasattr(self.parent(), '_update_statistics'):
                self.parent()._update_statistics()
                
            print("🔄 Mise à jour visuelle forcée du calendrier (multiple)")
        
        # 3. Recharger les listes de réservations dans la sidebar
        if hasattr(self.parent(), '_update_reservation_lists'):
            self.parent()._update_reservation_lists()
        
        # 4. Réinitialiser la sélection
        self.selected_reservation = None
        self._enable_action_buttons(False)
        self.info_label.setText("Sélectionnez une réservation pour voir les actions")
        
        print("✅ Rechargement terminé avec mise à jour visuelle")
    
    def _load_reservations(self):
        """Charger les réservations dans la liste"""
        try:
            python_date = self.date.toPython()
            reservations = self.calendar_service.get_day_reservations(python_date)
            
            # 🔧 FIX: Sauvegarder l'ID de la réservation sélectionnée avant le clear()
            selected_reservation_id = None
            if self.selected_reservation:
                selected_reservation_id = self.selected_reservation.get('id')
            
            self.reservation_list.clear()
            
            # Si aucune réservation, afficher un message d'invitation
            if not reservations:
                item = QListWidgetItem("📝 Il n'y a pas de réservations pour cette date.\n\n➕ Cliquez sur 'Ajouter réservation' pour en créer une !")
                item.setFlags(Qt.NoItemFlags)  # Non sélectionnable
                # 🔧 FIX: Utiliser setData pour le CSS au lieu de setForeground
                item.setData(Qt.UserRole + 1, 'empty')
                font = item.font()
                font.setItalic(True)
                item.setFont(font)
                self.reservation_list.addItem(item)
                
                # Mettre à jour le message info
                self.info_label.setText("""
                <h3>📅 Aucune réservation</h3>
                <p>Cette date n'a pas encore de réservations.</p>
                <p><b>💡 Astuce:</b> Utilisez le bouton "➕ Ajouter réservation" pour créer une nouvelle réservation.</p>
                """)
                
                # Désactiver les boutons d'action et réinitialiser la sélection
                self.selected_reservation = None
                self._enable_action_buttons(False)
                return
            
            # 🔧 FIX: Variable pour retrouver l'item à sélectionner
            item_to_select = None
            
            for reservation in reservations:
                # Créer le texte de l'item
                status_emoji = {
                    'confirmed': '✅',
                    'pending': '⏳',
                    'cancelled': '❌'
                }.get(reservation['status'], '❓')
                
                text = f"{status_emoji} {reservation['time_slot']} - {reservation['terrain_name']}\n" \
                       f"👤 {reservation['user_name']} ({reservation['user_email']})\n" \
                       f"📝 Status: {reservation['status']}"
                
                if reservation.get('notes'):
                    text += f"\n💭 {reservation['notes']}"
                
                item = QListWidgetItem(text)
                # Stocker les données de réservation dans l'item
                item.setData(Qt.UserRole, reservation)
                
                # 🔧 FIX: Vérifier si c'est l'item qui était sélectionné
                if selected_reservation_id and reservation.get('id') == selected_reservation_id:
                    item_to_select = item
                
                # 🔧 FIX: Ne pas utiliser setForeground() qui override le CSS
                # La couleur sera gérée par le CSS selon le statut
                # Stocker le statut comme propriété pour le CSS
                if reservation['status'] == 'confirmed':
                    item.setData(Qt.UserRole + 1, 'confirmed')
                elif reservation['status'] == 'pending':
                    item.setData(Qt.UserRole + 1, 'pending')
                else:
                    item.setData(Qt.UserRole + 1, 'cancelled')
                
                self.reservation_list.addItem(item)
            
            # 🔧 FIX: Restaurer la sélection si elle existait
            if item_to_select:
                self.reservation_list.setCurrentItem(item_to_select)
                print(f"🔄 Sélection restaurée pour réservation ID: {selected_reservation_id}")
            elif reservations:  # S'il y a des réservations mais pas de sélection précédente
                # Sélectionner automatiquement le premier item pour activer les boutons
                first_item = self.reservation_list.item(0)
                if first_item and first_item.data(Qt.UserRole):  # Vérifier que c'est une vraie réservation
                    self.reservation_list.setCurrentItem(first_item)
                    print("🔄 Première réservation sélectionnée automatiquement")
            else:
                # Pas de réservations, désactiver les boutons
                self.selected_reservation = None
                self._enable_action_buttons(False)
        
        except Exception as e:
            print(f"❌ Erreur chargement réservations dialog: {e}")
    
    def _on_reservation_selected(self, current, previous):
        """Gérer la sélection d'une réservation"""
        if current:
            reservation = current.data(Qt.UserRole)
            if reservation:
                self.selected_reservation = reservation
                self._update_reservation_info(reservation)
                self._enable_action_buttons(True)
            else:
                self.selected_reservation = None
                self._enable_action_buttons(False)
        else:
            self.selected_reservation = None
            self._enable_action_buttons(False)
    
    def _on_item_clicked(self, item):
        """Gérer le clic direct sur un item"""
        pass
    
    def _update_reservation_info(self, reservation):
        """Mettre à jour les informations de la réservation sélectionnée"""
        print(f"🔄 Mise à jour des infos pour réservation ID: {reservation.get('id', 'N/A')}")
        
        info_text = f"""
        <h3>📅 Réservation #{reservation['id']}</h3>
        <p><b>🕐 Heure:</b> {reservation['time_slot']}</p>
        <p><b>🏟️ Terrain:</b> {reservation['terrain_name']}</p>
        <p><b>👤 Utilisateur:</b> {reservation['user_name']}</p>
        <p><b>📧 Email:</b> {reservation['user_email']}</p>
        <p><b>📝 Statut:</b> {reservation['status']}</p>
        """
        if reservation.get('notes'):
            info_text += f"<p><b>📋 Notes:</b> {reservation['notes']}</p>"
        
        if hasattr(self, 'info_label'):
            self.info_label.setText(info_text)
            print("✅ Info_label mis à jour avec succès")
        else:
            print("❌ ERREUR: info_label n'existe pas!")
    
    def _enable_action_buttons(self, enabled):
        """Activer/désactiver les boutons d'action"""
        self.modify_btn.setEnabled(enabled)
        self.move_btn.setEnabled(enabled)
        self.delete_btn.setEnabled(enabled)
    
    def _modify_selected_reservation(self):
        """Ajouter une note à la réservation sélectionnée"""
        if not self.selected_reservation:
            return

        
        # Appeler directement la méthode de ce dialog
        self._modify_reservation_dialog(self.selected_reservation)
    
    def _move_selected_reservation(self):
        """Déplacer la réservation sélectionnée"""
        if not self.selected_reservation:
            return

        self._move_reservation_dialog(self.selected_reservation)
    
    def _delete_selected_reservation(self):
        """Supprimer la réservation sélectionnée"""
        if not self.selected_reservation:
            return

        self._delete_reservation(self.selected_reservation)
    
    def _modify_reservation(self, reservation):
        """Modifier une réservation (ouvre le dialog de déplacement)"""
        print(f"🔧 Modification réservation: {reservation}")
        # Utiliser le dialog de déplacement existant qui a déjà la mise à jour instantanée
        self._move_reservation_dialog(reservation)
    
    def _confirm_reservation(self, reservation):
        """Confirmer une réservation"""
        try:
            success = self.reservation_controller.confirm_reservation(reservation['id'])
            if success:
                QMessageBox.information(self, "Succès", "Réservation confirmée avec succès!")
                
                # MISE À JOUR INSTANTANÉE COMPLÈTE

                
                # 1. Mettre à jour selected_date avec la date de la réservation
                if isinstance(reservation['start'], str):
                    from datetime import datetime
                    start_datetime = datetime.fromisoformat(reservation['start'])
                else:
                    start_datetime = reservation['start']
                
                reservation_date = QDate(start_datetime.year, start_datetime.month, start_datetime.day)
                self.calendar_view.selected_date = reservation_date
                
                # 2. Actualiser le calendrier instantanément
                self.calendar_view._refresh_data()
                
                # 3. Notification globale
                try:
                    from hybrid_main import app
                    if hasattr(app, 'notifications_service') and app.notifications_service:
                        app.notifications_service.notify_reservation_change()
                except:
                    pass
                
                self._load_reservations()  # Recharger la table
                self.accept()  # Fermer et signaler des changements
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de confirmer la réservation.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la confirmation: {e}")
    
    def _clear_reservation_details(self):
        """Vider les détails de la réservation sélectionnée"""
        if hasattr(self, 'details_widget'):
            layout = self.details_widget.layout()
            if layout:
                # Nettoyer tous les widgets existants
                for i in reversed(range(layout.count())):
                    w = layout.itemAt(i).widget()
                    if w:
                        w.setParent(None)
                # Ajouter un message d'état
                no_selection_label = QLabel("📋 Aucune réservation sélectionnée")
                no_selection_label.setStyleSheet("color: #666; font-style: italic; padding: 20px;")
                layout.addWidget(no_selection_label)
        self.selected_reservation = None

        
    def _modify_reservation_dialog(self, reservation):
        """Dialog pour ajouter des notes à une réservation"""
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter une note à la réservation")
        dialog.setModal(True)
        dialog.setFixedSize(500, 300)
        
        layout = QFormLayout(dialog)
        
        # Affichage des infos de la réservation (non modifiables)
        info_label = QLabel(f"🏆 Réservation #{reservation['id']} - {reservation['user_name']} ({reservation['terrain_name']})")
        info_label.setStyleSheet("font-weight: bold; color: #2E7D32; padding: 10px;")
        layout.addRow(info_label)
        
        # Zone de notes
        notes_edit = QTextEdit()
        existing_notes = reservation.get('notes', '')

        notes_edit.setPlainText(existing_notes)
        notes_edit.setMaximumHeight(150)
        notes_edit.setPlaceholderText("Ajoutez vos notes ici...")
        
        layout.addRow("📝 Notes:", notes_edit)
        
        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        
        # Référence vers la vue calendrier pour appeler la méthode de sauvegarde
        calendar_view = self.calendar_view
        button_box.accepted.connect(lambda: calendar_view._save_notes_only(
            reservation, notes_edit.toPlainText(), dialog
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.exec()
    
    def _move_reservation_dialog(self, reservation):
        """Dialog pour déplacer une réservation"""
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Déplacer la réservation")
        dialog.setModal(True)
        dialog.setFixedSize(500, 400)
        
        layout = QFormLayout(dialog)
        
        # Sélection nouvelle date
        date_edit = QDateEdit()
        date_edit.setDate(self.date)
        date_edit.setCalendarPopup(True)
        
        # Sélection nouvelle heure
        start_time = QTimeEdit()
        start_time.setTime(reservation['start'].time())
        
        end_time = QTimeEdit()  
        end_time.setTime(reservation['end'].time())
        
        # Sélection terrain
        from app.controllers.terrain_controller import TerrainController
        terrain_controller = TerrainController()
        # Récupérer les vrais terrains de la base de données
        from app.models.db import SessionLocal
        from app.models.terrain import Terrain
        
        db = SessionLocal()
        try:
            terrains = db.query(Terrain).filter(Terrain.active == True).all()
            print(f"🏟️ {len(terrains)} terrains chargés pour déplacement")
        except Exception as e:
            print(f"❌ Erreur chargement terrains: {e}")
            # Fallback vers terrains de test
            terrains = [
                type('Terrain', (), {'id': 1, 'name': 'Terrain A', 'location': 'Salle Centrale'}),
                type('Terrain', (), {'id': 2, 'name': 'Terrain B', 'location': 'Salle Est'})
            ]
        finally:
            db.close()
        
        terrain_combo = QComboBox()
        for terrain in terrains:
            terrain_combo.addItem(f"{terrain.name} - {terrain.location}", terrain.id)
            if terrain.name == reservation['terrain_name']:
                terrain_combo.setCurrentIndex(terrain_combo.count() - 1)
        
        layout.addRow("📅 Nouvelle date:", date_edit)
        layout.addRow("🕐 Heure début:", start_time)
        layout.addRow("🕕 Heure fin:", end_time)
        layout.addRow("🏟️ Terrain:", terrain_combo)
        
        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self._save_reservation_move(
            reservation, date_edit.date(), start_time.time(), end_time.time(), 
            terrain_combo.currentData(), dialog
        ))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.exec()
    
    def _delete_reservation(self, reservation):
        """Supprimer une réservation"""
        reply = QMessageBox.question(
            self, "Confirmer la suppression", 
            f"Êtes-vous sûr de vouloir supprimer cette réservation ?\n\n"
            f"Terrain: {reservation['terrain_name']}\n"
            f"Heure: {reservation['time_slot']}\n"
            f"Utilisateur: {reservation['user_name']}",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success = self.reservation_controller.cancel_reservation(reservation['id'])
                if success:
                    QMessageBox.information(self, "Succès", "Réservation supprimée avec succès!")
                    
                    # MISE À JOUR INSTANTANÉE COMPLÈTE
                    # Forcer la mise à jour instantanée des points rouges
                    self.calendar_view.calendar.force_red_dots_update()
                    
                    # Utiliser _refresh_data() de la vue calendrier principale
                    self.calendar_view._refresh_data()
                    
                    # 4. Notification globale
                    try:
                        from hybrid_main import app
                        if hasattr(app, 'notifications_service') and app.notifications_service:
                            app.notifications_service.notify_reservation_change()
                    except:
                        pass
                    
                    # Recharger toutes les données (méthode existante)
                    self._reload_all_data()
                else:
                    QMessageBox.warning(self, "Erreur", "Impossible de supprimer la réservation.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression: {e}")
    
    # Méthode _save_notes_only dupliquée supprimée - utiliser celle de HybridCalendarView
    
    def _add_new_reservation(self):
        """Ajouter une nouvelle réservation pour cette date"""
        dialog = AddReservationDialog(self.date, self.calendar_view, parent=self)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            # Recharger les données
            self._reload_all_data()
            print(f"✅ Nouvelle réservation ajoutée pour {self.date.toString()}")
    
    def _save_reservation_move(self, reservation, new_date, start_time, end_time, terrain_id, dialog):
        """Sauvegarder le déplacement d'une réservation"""
        try:
            # Créer les nouveaux datetime
            from datetime import datetime, time
            python_date = new_date.toPython()
            start_datetime = datetime.combine(python_date, start_time.toPython())
            end_datetime = datetime.combine(python_date, end_time.toPython())
            
            # Vérifier que user_id existe
            user_id = reservation['user_id'] if 'user_id' in reservation else None
            if user_id is None:
                QMessageBox.warning(self, "Erreur", "Impossible de déterminer l'utilisateur de la réservation.")
                return
                
            # Utiliser le contrôleur pour modifier la réservation
            self.reservation_controller.modify_reservation(
                reservation['id'], 
                user_id,
                terrain_id,
                start_datetime,
                end_datetime,
                reservation.get('notes', '')
            )
            
            QMessageBox.information(self, "Succès", "Réservation déplacée avec succès!")
            
            # MISE À JOUR INSTANTANÉE COMPLÈTE APRÈS DÉPLACEMENT
            # 1. Mettre à jour selected_date avec la NOUVELLE date
            self.calendar_view.selected_date = new_date
            
            # 2. Recharger les deux mois (ancien et nouveau) si différents
            old_start = reservation['start'] if isinstance(reservation['start'], datetime) else datetime.fromisoformat(reservation['start'])
            old_date = QDate(old_start.year, old_start.month, old_start.day)
            
            # Recharger l'ancien mois (pour enlever les points rouges si nécessaire)
            if old_date.month() != new_date.month() or old_date.year() != new_date.year():
                self.calendar_view.calendar._load_month_data(old_date.year(), old_date.month())
            
            # Recharger le nouveau mois (pour ajouter les points rouges)
            self.calendar_view.calendar._load_month_data(new_date.year(), new_date.month())
            
            # 3. Forcer la mise à jour visuelle complète des points rouges
            QApplication.processEvents()  # Traiter les événements
            self.calendar_view.calendar.updateCells()  # Recalculer les cellules
            self.calendar_view.calendar.repaint()      # Forcer le redessin des points rouges
            
            # 4. Actualiser toutes les listes
            self.calendar_view._update_reservation_lists()
            self.calendar_view._update_statistics()
            
            # 5. Notification globale
            try:
                from hybrid_main import app
                if hasattr(app, 'notifications_service') and app.notifications_service:
                    app.notifications_service.notify_reservation_change()
            except:
                pass
            
            # Fermer la modale
            dialog.accept()
            
            # Recharger toutes les données (sécurité)
            if hasattr(self, '_reload_all_data'):
                self._reload_all_data()
                

            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du déplacement: {e}")
    
    def _go_to_previous_day(self):
        """Naviguer vers le jour précédent"""
        try:
            # Calculer la date précédente
            previous_date = self.date.addDays(-1)
            self._navigate_to_date(previous_date)
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la navigation: {e}")
    
    def _go_to_next_day(self):
        """Naviguer vers le jour suivant"""
        try:
            # Calculer la date suivante
            next_date = self.date.addDays(1)
            self._navigate_to_date(next_date)
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la navigation: {e}")
    
    def _navigate_to_date(self, new_date):
        """Naviguer vers une nouvelle date"""
        try:
            # Mettre à jour la date
            self.date = new_date
            
            # Mettre à jour le titre de la fenêtre
            self.setWindowTitle(f"Gestion des réservations - {new_date.toString('dd/MM/yyyy')}")
            
            # Mettre à jour le label de date
            self.date_label.setText(f"📅 Réservations du {new_date.toString('dddd dd MMMM yyyy')}")
            
            # Recharger les réservations pour cette nouvelle date
            python_date = new_date.toPython()
            new_reservations = self.calendar_service.get_day_reservations(python_date)
            self.reservations = new_reservations
            
            # Actualiser la liste des réservations (avec préservation de sélection)
            self._load_reservations()
            
            # 🔧 FIX: Ne vider les détails que s'il n'y a pas de sélection active
            current_item = self.reservation_list.currentItem()
            if not current_item or not current_item.data(Qt.UserRole):
                self._clear_details_panel()
            # Si une sélection existe, _load_reservations() l'aura restaurée
            # et _on_reservation_selected() aura mis à jour les détails
            
            print(f"✅ Navigation terminée - {len(new_reservations)} réservation(s) trouvée(s)")
            
        except Exception as e:
            print(f"❌ Erreur lors de la navigation: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la navigation vers {new_date.toString()}: {e}")
    
    def _clear_details_panel(self):
        """Réinitialiser le panneau de détails à droite"""
        try:
            # 🔧 FIX: Au lieu de supprimer les widgets, juste réinitialiser leur contenu
            if hasattr(self, 'info_label'):
                self.info_label.setText("👈 Sélectionnez une réservation pour voir les détails")
            
            # Désactiver les boutons d'action
            if hasattr(self, 'selected_reservation'):
                self.selected_reservation = None
            
            self._enable_action_buttons(False)
            
            print("🔄 Panneau de détails réinitialisé (widgets préservés)")
            
        except Exception as e:
            print(f"❌ Erreur lors de la réinitialisation du panneau: {e}")


class AddReservationDialog(QDialog):
    """Dialog pour ajouter une nouvelle réservation"""
    
    def __init__(self, date, calendar_view, parent=None):
        super().__init__(parent)
        self.date = date
        self.calendar_view = calendar_view
        self.reservation_controller = ReservationController()
        
        self.setWindowTitle(f"Nouvelle réservation - {date.toString('dd/MM/yyyy')}")
        self.setModal(True)
        self.setFixedSize(500, 600)
        
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        """Configuration de l'interface"""
        layout = QFormLayout(self)
        
        # Titre
        title = QLabel(f"➕ Nouvelle réservation pour le {self.date.toString('dddd dd MMMM yyyy')}")
        title.setStyleSheet(f"""
            QLabel {{
                font-size: 16px;
                font-weight: bold;
                color: {FootballTheme.PRIMARY_DARK};
                padding: 15px;
                background: {FootballTheme.SURFACE};
                border-radius: 8px;
                border: 2px solid {FootballTheme.PRIMARY};
                margin-bottom: 20px;
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addRow(title)
        
        # Sélection utilisateur
        self.user_combo = QComboBox()
        self.user_combo.setEditable(True)
        self.user_combo.setStyleSheet(f"""
            QComboBox {{
                background: white;
                border: 2px solid {FootballTheme.PRIMARY_LIGHT};
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                min-height: 20px;
            }}
            QComboBox:focus {{
                border: 2px solid {FootballTheme.PRIMARY};
            }}
        """)
        layout.addRow("👤 Utilisateur:", self.user_combo)
        
        # Sélection terrain
        self.terrain_combo = QComboBox()
        self.terrain_combo.setStyleSheet(self.user_combo.styleSheet())
        layout.addRow("🏟️ Terrain:", self.terrain_combo)
        
        # Heure de début
        self.start_time = QTimeEdit()
        self.start_time.setTime(QTime(8, 0))  # 8h par défaut
        self.start_time.setDisplayFormat("HH:mm")
        self.start_time.setStyleSheet(f"""
            QTimeEdit {{
                background: white;
                border: 2px solid {FootballTheme.PRIMARY_LIGHT};
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                min-height: 20px;
            }}
        """)
        layout.addRow("🕐 Heure début:", self.start_time)
        
        # Heure de fin
        self.end_time = QTimeEdit()
        self.end_time.setTime(QTime(10, 0))  # 10h par défaut
        self.end_time.setDisplayFormat("HH:mm")
        self.end_time.setStyleSheet(self.start_time.styleSheet())
        layout.addRow("🕕 Heure fin:", self.end_time)
        
        # Notes
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        self.notes_edit.setPlaceholderText("Notes optionnelles...")
        self.notes_edit.setStyleSheet(f"""
            QTextEdit {{
                background: white;
                border: 2px solid {FootballTheme.PRIMARY_LIGHT};
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }}
        """)
        layout.addRow("📝 Notes:", self.notes_edit)
        
        # Boutons
        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Save).setText("✅ Créer la réservation")
        button_box.button(QDialogButtonBox.Cancel).setText("❌ Annuler")
        
        # Style des boutons
        button_box.button(QDialogButtonBox.Save).setStyleSheet(f"""
            QPushButton {{
                background-color: {FootballTheme.SUCCESS};
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 20px;
                border: none;
                border-radius: 6px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: #2E7D32;
            }}
        """)
        
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet(f"""
            QPushButton {{
                background-color: #9E9E9E;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 20px;
                border: none;
                border-radius: 6px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: #757575;
            }}
        """)
        
        button_box.accepted.connect(self._create_reservation)
        button_box.rejected.connect(self.reject)
        
        layout.addRow(button_box)
    
    def _load_data(self):
        """Charger les utilisateurs et terrains"""
        try:
            # Charger les utilisateurs
            from app.controllers.user_controller import UserController
            user_controller = UserController()
            users = user_controller.list_users()
            
            for user in users:
                self.user_combo.addItem(f"{user.username} ({user.email})", user.id)
            
            # Charger les terrains
            from app.controllers.terrain_controller import TerrainController
            terrain_controller = TerrainController()
            terrains = terrain_controller.list_terrains()
            
            for terrain in terrains:
                if terrain.active:
                    self.terrain_combo.addItem(f"{terrain.name} - {terrain.location}", terrain.id)
                    
            print(f"📊 Chargé {len(users)} utilisateurs et {self.terrain_combo.count()} terrains")
            
        except Exception as e:
            print(f"❌ Erreur chargement données: {e}")
            QMessageBox.warning(self, "Erreur", "Impossible de charger les données utilisateurs/terrains")
    
    def _create_reservation(self):
        """Créer la nouvelle réservation"""
        try:
            # Validation des champs
            if self.user_combo.currentData() is None:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un utilisateur")
                return
                
            if self.terrain_combo.currentData() is None:
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un terrain")
                return
            
            # Vérifier que l'heure de fin est après l'heure de début
            if self.end_time.time() <= self.start_time.time():
                QMessageBox.warning(self, "Erreur", "L'heure de fin doit être après l'heure de début")
                return
            
            # Créer les datetime
            from datetime import datetime
            python_date = self.date.toPython()
            start_datetime = datetime.combine(python_date, self.start_time.time().toPython())
            end_datetime = datetime.combine(python_date, self.end_time.time().toPython())
            
            # Créer la réservation
            user_id = self.user_combo.currentData()
            terrain_id = self.terrain_combo.currentData()
            notes = self.notes_edit.toPlainText().strip()
            
            print(f"🆕 Création réservation: User {user_id}, Terrain {terrain_id}, {start_datetime} -> {end_datetime}")
            
            success = self.reservation_controller.create_reservation(
                user_id, terrain_id, start_datetime, end_datetime, notes
            )
            
            if success:
                QMessageBox.information(self, "Succès", "Réservation créée avec succès!")
                
                # MISE À JOUR INSTANTANÉE COMPLÈTE APRÈS CRÉATION
                # 1. Mettre à jour selected_date avec la date de la nouvelle réservation
                self.calendar_view.selected_date = self.date
                
                # 2. Recharger le mois de la nouvelle réservation pour ajouter les points rouges
                self.calendar_view.calendar._load_month_data(self.date.year(), self.date.month())
                
                # 3. Forcer la mise à jour visuelle complète des points rouges
                QApplication.processEvents()  # Traiter les événements en attente
                self.calendar_view.calendar.updateCells()  # Recalculer toutes les cellules
                self.calendar_view.calendar.repaint()      # Forcer le redessin des points rouges
                
                # 4. Actualiser toutes les listes et statistiques
                self.calendar_view._update_reservation_lists()
                self.calendar_view._update_statistics()
                
                # 5. Notification globale
                try:
                    if hasattr(self.calendar_view, 'notifications_service') and self.calendar_view.notifications_service:
                        self.calendar_view.notifications_service.notify_reservation_change()
                except Exception as e:
                    print(f"⚠️ Erreur notification: {e}")
                
                self.accept()
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de créer la réservation (conflit possible)")
                
        except Exception as e:
            print(f"❌ Erreur création réservation: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création: {str(e)}")