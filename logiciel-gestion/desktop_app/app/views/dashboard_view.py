from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget
from app.controllers.terrain_controller import TerrainController
class DashboardView(QWidget):
    def __init__(self, user):
        super().__init__(); self.user = user; self.terrain_ctrl = TerrainController(); self._build()
    def _build(self):
        from PySide6.QtWidgets import QApplication
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f'Bienvenue {self.user.username} ({self.user.role})'))
        btn_logout = QPushButton('Déconnexion')
        btn_logout.clicked.connect(self.logout)
        layout.addWidget(btn_logout)
        # Superadmin : gestion utilisateurs, admin : gestion terrains/réservations, user : consultation
        if getattr(self.user, 'role', 'user') == 'superadmin':
            btn_users = QPushButton('Gestion utilisateurs')
            btn_users.clicked.connect(self.open_user_management)
            layout.addWidget(btn_users)
        if getattr(self.user, 'role', 'user') in ['superadmin', 'admin']:
            btn_terrains = QPushButton('Gestion terrains')
            btn_terrains.clicked.connect(self.open_terrain_management)
            layout.addWidget(btn_terrains)
            btn_reserv = QPushButton('Gestion réservations')
            btn_reserv.clicked.connect(self.open_reservation_management)
            layout.addWidget(btn_reserv)
        self.terrain_list = QListWidget()
        btn = QPushButton('Rafraichir')
        btn.clicked.connect(self.load_terrains)
        layout.addWidget(self.terrain_list)
        layout.addWidget(btn)
        self.setLayout(layout)
        self.load_terrains()
    def logout(self):
        # Nettoie le layout du parent et affiche le login
        from app.views.login_view import LoginView
        parent = self.parentWidget()
        while parent and not hasattr(parent, '_layout'):
            parent = parent.parentWidget()
        if parent and hasattr(parent, '_layout'):
            layout = parent._layout
            # Supprime tous les widgets du layout (dashboard, boutons, etc.)
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            # Ajoute le login
            login_view = LoginView(on_login=parent._on_login)
            layout.addWidget(login_view)
            parent.login_view = login_view
            def show_on_login(user):
                parent._on_login(user)
            login_view.on_login = show_on_login
            return
        # Superadmin : gestion utilisateurs, admin : gestion terrains/réservations, user : consultation
        if getattr(self.user, 'role', 'user') == 'superadmin':
            btn_users = QPushButton('Gestion utilisateurs')
            btn_users.clicked.connect(self.open_user_management)
            layout.addWidget(btn_users)
        # Admin et superadmin : gestion terrains/réservations (à compléter plus tard)
        if getattr(self.user, 'role', 'user') in ['superadmin', 'admin']:
            btn_terrains = QPushButton('Gestion terrains')
            btn_terrains.clicked.connect(self.open_terrain_management)
            layout.addWidget(btn_terrains)
            btn_reserv = QPushButton('Gestion réservations')
            btn_reserv.clicked.connect(self.open_reservation_management)
            layout.addWidget(btn_reserv)
        # Tous : consultation des terrains
        self.terrain_list = QListWidget()
        btn = QPushButton('Rafraichir')
        btn.clicked.connect(self.load_terrains)
        layout.addWidget(self.terrain_list)
        layout.addWidget(btn)
        self.setLayout(layout)
        self.load_terrains()

    def open_terrain_management(self):
        # À implémenter : vue de gestion des terrains
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, 'Info', 'Gestion des terrains à venir')

    def open_reservation_management(self):
        # À implémenter : vue de gestion des réservations
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, 'Info', 'Gestion des réservations à venir')

    def open_user_management(self):
        from app.views.user_management_view import UserManagementView
        self.umw = UserManagementView()
        self.umw.show()
    def load_terrains(self):
        self.terrain_list.clear()
        for t in self.terrain_ctrl.list_terrains():
            self.terrain_list.addItem(f"{t.id} - {t.name} - {'Actif' if t.active else 'Inactif'}")
