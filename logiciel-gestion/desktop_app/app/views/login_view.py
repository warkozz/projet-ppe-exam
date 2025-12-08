from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont
from app.controllers.auth_controller import AuthController
from app.styles.theme import FootballTheme

class HoverButton(QPushButton):
    """Bouton avec effet hover personnalisé - identique aux autres pages"""
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
                font-size: 15px;
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
                font-size: 15px;
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

class LoginView(QWidget):
    def __init__(self, on_login):
        super().__init__()
        self.on_login = on_login
        self.auth = AuthController()
        self._build()
        
    def _build(self):
        # Style moderne avec Material Design
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e8f5e9, stop:1 #f1f8e9);
                color: #1b5e20;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #1b5e20;
                font-size: 28px;
                font-weight: bold;
                padding: 25px;
                background: transparent;
            }
            QLineEdit {
                background: white;
                border: 2px solid #c8e6c9;
                border-radius: 8px;
                padding: 15px;
                font-size: 16px;
                color: #1b5e20;
                margin: 8px;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #4caf50;
                background: #f8fff8;
            }
            QLineEdit:hover {
                border: 2px solid #66BB6A;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Titre avec style amélioré
        title = QLabel('⚽ Football Manager 5v5')
        title.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title.setStyleSheet("color: #1b5e20; margin-bottom: 30px;")
        layout.addWidget(title)
        
        subtitle = QLabel('Connexion à votre espace')
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setStyleSheet("color: #2e7d32; font-size: 18px; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Champs de saisie
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText('Nom d\'utilisateur')
        layout.addWidget(self.user_input)
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText('Mot de passe')
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)
        
        # Bouton de connexion avec style uniforme
        btn_login = HoverButton('Se connecter', '🚀')
        btn_login.clicked.connect(self.try_login)
        layout.addWidget(btn_login)
        
        self.setLayout(layout)
        
    def try_login(self):
        u = self.user_input.text().strip()
        p = self.pass_input.text().strip()
        user = self.auth.login(u, p)
        if user:
            self.on_login(user)
        else:
            QMessageBox.warning(self, 'Erreur', 'Identifiants invalides')
