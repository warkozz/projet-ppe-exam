from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from app.views.login_view import LoginView
from app.views.dashboard_view import DashboardView

class FootApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Foot5 - Gestion interne')
        self.resize(1000, 700)
        self._container = QWidget()
        self.setCentralWidget(self._container)
        self._layout = QVBoxLayout()
        self._container.setLayout(self._layout)

        # start with login
        self.login_view = LoginView(on_login=self._on_login)
        self._layout.addWidget(self.login_view)

    def _on_login(self, user):
        # Nettoie le layout avant d'ajouter le dashboard
        while self._layout.count():
            item = self._layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        self.dashboard = DashboardView(user)
        self._layout.addWidget(self.dashboard)
