from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from app.controllers.auth_controller import AuthController
class LoginView(QWidget):
    def __init__(self, on_login):
        super().__init__(); self.on_login = on_login; self.auth = AuthController(); self._build()
    def _build(self):
        layout = QVBoxLayout(); self.user_input = QLineEdit(); self.user_input.setPlaceholderText('username')
        self.pass_input = QLineEdit(); self.pass_input.setPlaceholderText('password'); self.pass_input.setEchoMode(QLineEdit.Password)
        btn_login = QPushButton('Se connecter'); btn_login.clicked.connect(self.try_login)
        layout.addWidget(QLabel('Connexion')); layout.addWidget(self.user_input); layout.addWidget(self.pass_input); layout.addWidget(btn_login)
        self.setLayout(layout)
    def try_login(self):
        u = self.user_input.text().strip(); p = self.pass_input.text().strip()
        user = self.auth.login(u,p)
        if user: self.on_login(user)
        else: QMessageBox.warning(self,'Erreur','Identifiants invalides')
