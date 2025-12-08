# dashboard_view.py - Dashboard hybride combinant ancien fonctionnel + nouveau design
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, 
    QListWidget, QFrame, QScrollArea, QSplitter
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from app.controllers.terrain_controller import TerrainController
from app.controllers.reservation_controller import ReservationController
from app.controllers.user_controller import UserController
from app.styles.theme import FootballTheme

class HoverButton(QPushButton):
    """Bouton avec effet hover personnalisé"""
    def __init__(self, text, icon="", parent=None):
        super().__init__(f"{icon} {text}" if icon else text, parent)
        self.base_style = f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {FootballTheme.PRIMARY}, stop:1 {FootballTheme.PRIMARY_DARK});
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
                margin: 5px;
            }}
        """
        self.hover_style = f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {FootballTheme.PRIMARY_LIGHT}, stop:1 {FootballTheme.PRIMARY});
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
                margin: 5px;
            }}
        """
        self.setStyleSheet(self.base_style)
    
    def enterEvent(self, event):
        self.setStyleSheet(self.hover_style)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.setStyleSheet(self.base_style)
        super().leaveEvent(event)

class ModernCard(QFrame):
    """Carte moderne simplifiée"""
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setStyleSheet(f"""
            QFrame#card {{
                background: {FootballTheme.CARD};
                border: 1px solid {FootballTheme.TEXT_HINT};
                border-radius: 12px;
                padding: 16px;
                margin: 8px;
            }}
            QLabel {{
                color: {FootballTheme.TEXT_PRIMARY};
                font-size: 14px;
            }}
            QPushButton {{
                background: {FootballTheme.PRIMARY};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
                min-height: 32px;
            }}
            QPushButton:hover {{
                background: {FootballTheme.SUCCESS};
            }}
            QPushButton:pressed {{
                background: {FootballTheme.ACCENT};
            }}
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 12, 12, 12)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 8px;")
            self.layout.addWidget(title_label)

class StatsCard(ModernCard):
    """Carte de statistiques moderne mais simple"""
    def __init__(self, title, value, icon="", parent=None):
        super().__init__(parent=parent)
        
        # Layout horizontal pour icon + contenu
        content_layout = QHBoxLayout()
        
        # Contenu textuel
        text_layout = QVBoxLayout()
        
        value_label = QLabel(str(value))
        value_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1b5e20;
        """)
        text_layout.addWidget(value_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            color: #2e7d32;
        """)
        text_layout.addWidget(title_label)
        
        content_layout.addLayout(text_layout)
        
        # Icon si fourni
        if icon:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 32px;")
            content_layout.addWidget(icon_label)
            
        self.layout.addLayout(content_layout)
        
        # Style avec couleur de fond claire
        self.setStyleSheet(f"""
            StatsCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e8f5e9, stop:1 #c8e6c9);
                border: 2px solid {FootballTheme.PRIMARY};
                border-radius: 12px;
                padding: 20px;
            }}
        """)

class HybridDashboardView(QWidget):
    """Dashboard hybride - fonctionnalités anciennes + design moderne"""
    
    def __init__(self, user, main_app):
        super().__init__()
        self.user = user
        self.main_app = main_app  # Référence pour naviguer
        self.terrain_ctrl = TerrainController()
        self.reservation_ctrl = ReservationController()
        self.user_ctrl = UserController()
        
        self._setup_ui()
        self._load_data()
        
        # Actualisation auto
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._load_data)
        self.refresh_timer.start(60000)  # 1 minute
        
    def _setup_ui(self):
        """Interface utilisateur hybride"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header avec info utilisateur et déconnexion
        header_layout = QHBoxLayout()
        
        welcome_label = QLabel(f"⚽ Bienvenue {self.user.username} ({self.user.role})")
        welcome_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {FootballTheme.PRIMARY};
            padding: 10px;
        """)
        header_layout.addWidget(welcome_label)
        
        header_layout.addStretch()
        
        logout_btn = HoverButton("Déconnexion", "🚪")
        logout_btn.clicked.connect(self._logout)
        # Utilise le style HoverButton par défaut avec les couleurs vertes
        header_layout.addWidget(logout_btn)
        
        main_layout.addLayout(header_layout)
        
        # Stats en haut
        stats_layout = QGridLayout()
        stats_layout.setSpacing(16)
        
        # Statistiques basiques - FONCTIONNELLES
        try:
            terrains = self.terrain_ctrl.list_terrains()
            active_terrains = len([t for t in terrains if t.active])
            
            reservations = self.reservation_ctrl.get_reservations() 
            from datetime import date
            today_reservations = len([
                r for r in reservations 
                if r.start.date() == date.today() and getattr(r, 'status', 'active') != 'cancelled'
            ])
            
            users = self.user_ctrl.list_users() if self.user.role in ['admin', 'superadmin'] else []
        except:
            active_terrains = 0
            today_reservations = 0
            users = []
        
        # Cartes de stats
        terrains_card = StatsCard("Terrains actifs", active_terrains, "⚽")
        stats_layout.addWidget(terrains_card, 0, 0)
        
        reservations_card = StatsCard("Réservations aujourd'hui", today_reservations, "📅")
        stats_layout.addWidget(reservations_card, 0, 1)
        
        if self.user.role in ['admin', 'superadmin']:
            users_card = StatsCard("Utilisateurs", len(users), "👥")
            stats_layout.addWidget(users_card, 0, 2)
        
        main_layout.addLayout(stats_layout)
        
        # Splitter pour diviser en sections
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Section gauche : Actions et navigation - FONCTIONNELLES
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Actions rapides
        actions_card = ModernCard("⚡ Actions rapides")
        actions_layout = QVBoxLayout()
        
        # Gestion des réservations - TOUJOURS accessible
        reservations_btn = HoverButton("Gestion des réservations", "📋")
        reservations_btn.clicked.connect(self._open_reservations)
        actions_layout.addWidget(reservations_btn)
        
        # Gestion terrains - ADMIN/SUPERADMIN
        if self.user.role in ['admin', 'superadmin']:
            terrains_btn = HoverButton("Gestion des terrains", "⚽")
            terrains_btn.clicked.connect(self._open_terrains)
            actions_layout.addWidget(terrains_btn)
        
        # Gestion utilisateurs - SUPERADMIN seulement
        if self.user.role == 'superadmin':
            users_btn = HoverButton("Gestion des utilisateurs", "👥")
            users_btn.clicked.connect(self._open_users)
            actions_layout.addWidget(users_btn)
        
        actions_card.layout.addLayout(actions_layout)
        left_layout.addWidget(actions_card)
        
        left_layout.addStretch()
        splitter.addWidget(left_widget)
        
        # Section droite : Liste des terrains - FONCTIONNELLE (comme l'ancien)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        terrains_card = ModernCard("⚽ Terrains disponibles")
        terrains_layout = QVBoxLayout()
        
        self.terrain_list = QListWidget()
        self.terrain_list.setMinimumHeight(300)

        terrains_layout.addWidget(self.terrain_list)
        
        # Style CSS avec correction uniquement de la couleur du texte sélectionné
        self.terrain_list.setStyleSheet(f"""
            QListWidget {{
                background: {FootballTheme.SURFACE};
                border: 1px solid {FootballTheme.TEXT_HINT};
                border-radius: 8px;
                padding: 8px;
            }}
            QListWidget::item {{
                padding: 12px;
                border-radius: 6px;
                margin: 3px;
                border: 1px solid transparent;
                font-size: 14px;
                font-weight: 500;
                color: {FootballTheme.PRIMARY_DARK};
            }}
            QListWidget::item:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e8f5e9, stop:1 #c8e6c9);
                border: 1px solid {FootballTheme.PRIMARY};
                color: {FootballTheme.PRIMARY_DARK};
                font-weight: bold;
            }}
            QListWidget::item:selected {{
                color: white;
                font-weight: bold;
            }}
            QListWidget::item:selected:hover {{
                color: white;
                font-weight: bold;
            }}
        """)
        
        # Forcer seulement la couleur du texte sélectionné avec la palette
        from PySide6.QtGui import QPalette, QColor
        palette = self.terrain_list.palette()
        palette.setColor(QPalette.HighlightedText, QColor('white'))
        self.terrain_list.setPalette(palette)
        
        refresh_btn = HoverButton("Actualiser", "🔄")
        refresh_btn.clicked.connect(self._load_data)
        terrains_layout.addWidget(refresh_btn)
        
        terrains_card.layout.addLayout(terrains_layout)
        right_layout.addWidget(terrains_card)
        
        splitter.addWidget(right_widget)
        
        # Ratio 40/60
        splitter.setSizes([400, 600])
        main_layout.addWidget(splitter)
        
    def _load_data(self):
        """Charge les données - FONCTIONNEL (reprend l'ancien)"""
        try:
            # Charger les terrains
            self.terrain_list.clear()
            terrains = self.terrain_ctrl.list_terrains()
            
            for terrain in terrains:
                status = "🟢 Actif" if terrain.active else "🔴 Inactif"
                item_text = f"{terrain.id} - {terrain.name} - {status}"
                self.terrain_list.addItem(item_text)
                
            print(f"✅ {len(terrains)} terrains chargés")
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des terrains: {e}")
            self.terrain_list.addItem("❌ Erreur de chargement")
    
    def _open_reservations(self):
        """Ouvre la gestion des réservations - FONCTIONNELLE"""
        try:
            from app.views.hybrid.reservation_view import HybridReservationView
            reservations_view = HybridReservationView()
            
            # Ajouter le bouton retour
            reservations_view.btn_back.clicked.connect(lambda: self.main_app.go_back_to_dashboard())
            
            # Navigation dans la même fenêtre
            if hasattr(self.main_app, 'show_view'):
                self.main_app.show_view(reservations_view)
            else:
                reservations_view.show()
                
        except Exception as e:
            print(f"❌ Erreur ouverture réservations: {e}")
    

    
    def _open_terrains(self):
        """Ouvre la gestion des terrains - FONCTIONNELLE"""
        try:
            from app.views.hybrid.terrain_view import HybridTerrainView
            terrain_view = HybridTerrainView()
            
            # Ajouter bouton retour
            terrain_view.btn_back.clicked.connect(lambda: self.main_app.go_back_to_dashboard())
            
            if hasattr(self.main_app, 'show_view'):
                self.main_app.show_view(terrain_view)
            else:
                terrain_view.show()
                
        except Exception as e:
            print(f"❌ Erreur ouverture terrains: {e}")
    
    def _open_users(self):
        """Ouvre la gestion des utilisateurs - FONCTIONNELLE"""
        try:
            from app.views.hybrid.user_view import HybridUserView
            user_view = HybridUserView()
            
            # Ajouter bouton retour
            user_view.btn_back.clicked.connect(lambda: self.main_app.go_back_to_dashboard())
            
            if hasattr(self.main_app, 'show_view'):
                self.main_app.show_view(user_view)
            else:
                user_view.show()
                
        except Exception as e:
            print(f"❌ Erreur ouverture utilisateurs: {e}")
    
    def _logout(self):
        """Déconnexion - FONCTIONNELLE"""
        from PySide6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self, 'Déconnexion',
            'Êtes-vous sûr de vouloir vous déconnecter ?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Arrêter le timer
            if hasattr(self, 'refresh_timer'):
                self.refresh_timer.stop()
                
            # Retourner au login
            print("👋 Déconnexion...")
            self.main_app.current_user = None
            self.main_app._show_login()