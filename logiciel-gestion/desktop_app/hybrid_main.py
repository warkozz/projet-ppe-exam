# hybrid_main.py - Version Material Design (Version Principale)
import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QIcon
from qt_material import apply_stylesheet

from app.views.login_view import LoginView
from app.views.hybrid.dashboard_view import HybridDashboardView

class GlobalNotificationService(QObject):
    """Service global de notifications pour synchroniser les vues"""
    reservation_data_changed = Signal()  # Signal émis quand les données de réservation changent
    
    def __init__(self):
        super().__init__()
        print("🔧 Service de notifications global initialisé")
    
    def notify_reservation_change(self):
        """Notifie tous les observateurs qu'une réservation a changé"""
        print("📡 Notification globale : données de réservation modifiées")
        self.reservation_data_changed.emit()

# Instance globale du service de notifications
global_notifications = GlobalNotificationService()

class MaterialFootballApp(QMainWindow):
    """Application avec Material Design moderne"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚽ Football Manager 5v5 - Material Design")
        self.setMinimumSize(1200, 800)
        self.current_user = None
        self.notifications = global_notifications  # Référence au service global
        
        # Widget central avec stack pour navigation
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self._layout = QVBoxLayout(self.central_widget)
        self._layout.setContentsMargins(0, 0, 0, 0)
        
        # Stack pour gérer les vues
        self.stack = QStackedWidget()
        self._layout.addWidget(self.stack)
        
        # Afficher le login au démarrage
        self._show_login()
        
    def _show_login(self):
        """Affiche la vue de connexion"""
        self.login_view = LoginView(on_login=self._on_login)
        self.stack.addWidget(self.login_view)
        self.stack.setCurrentWidget(self.login_view)
        
    def _on_login(self, user):
        """Gère la connexion réussie"""
        self.current_user = user
        print(f"✅ Connexion réussie : {user.username} ({user.role})")
        
        # Supprimer la vue de login
        self.stack.removeWidget(self.login_view)
        self.login_view.deleteLater()
        
        # Créer et afficher le dashboard hybride
        self.dashboard_view = HybridDashboardView(user, self)
        self.stack.addWidget(self.dashboard_view)
        self.stack.setCurrentWidget(self.dashboard_view)
        
    def show_view(self, view_widget):
        """Affiche une nouvelle vue"""
        # Vérifier si la vue est déjà dans la stack
        for i in range(self.stack.count()):
            if self.stack.widget(i) == view_widget:
                self.stack.setCurrentWidget(view_widget)
                return
        
        # Ajouter la nouvelle vue si elle n'existe pas
        self.stack.addWidget(view_widget)
        self.stack.setCurrentWidget(view_widget)
        
    def go_back_to_dashboard(self):
        """Retourne au dashboard sans supprimer les vues en cache"""
        # Simplement revenir au dashboard, garder les autres vues en cache
        self.stack.setCurrentWidget(self.dashboard_view)
        print("🔙 Retour au dashboard (vues conservées en cache)")

def main():
    app = QApplication(sys.argv)
    
    # Appliquer le thème Material Design (thème clair)
    apply_stylesheet(app, theme='light_teal.xml', extra={
        'primary_color': '#4CAF50',
        'secondary_color': '#2E7D32',
        'success_color': '#66BB6A',
        'warning_color': '#FF9800',
        'error_color': '#F44336',
        'info_color': '#2196F3',
        'font_family': 'Segoe UI',
        'font_size': '14px'
    })
    
    # Configuration pour les fonts
    from PySide6.QtGui import QFont
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = MaterialFootballApp()
    window.show()
    
    print("🏟️ Football Manager 5v5 - Version Material Design")
    print("🎨 Thème moderne avec Material Design")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()