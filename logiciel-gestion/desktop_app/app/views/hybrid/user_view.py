# user_view.py - Vue hybride de gestion des utilisateurs
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QListWidget, 
    QComboBox, QLineEdit, QLabel, QMessageBox, QCheckBox, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
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

class HybridUserView(QWidget):
    """Vue hybride de gestion des utilisateurs"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ctrl = UserController()
        self.selected_id = None
        
        self.setWindowTitle('Gestion des Utilisateurs - Version Hybride')
        self.setMinimumSize(900, 600)
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
            QPushButton {{
                background: #4caf50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: #45a049;
            }}
            QLineEdit, QTextEdit, QComboBox {{
                background: white;
                border: 2px solid #c8e6c9;
                border-radius: 4px;
                padding: 6px;
                color: #1b5e20;
            }}
            QListWidget {{
                background: white;
                border: 2px solid #c8e6c9;
                border-radius: 4px;
                color: #1b5e20;
                selection-background-color: #e8f5e8;
            }}
            QCheckBox {{
                color: #1b5e20;
                font-weight: bold;
                background: transparent;
            }}
        """)
        
        self._build()
        
    def _build(self):
        """Construction de l'interface"""
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel('👤 Gestion des Utilisateurs')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1b5e20;
                background: #e8f5e8;
                padding: 15px;
                margin: 10px;
                border-radius: 8px;
                border: 2px solid #4caf50;
            }
        """)
        layout.addWidget(title)
        
        # Liste des utilisateurs
        layout.addWidget(QLabel('📋 Liste des utilisateurs'))
        self.users_list = QListWidget()
        layout.addWidget(self.users_list)
        
        # Formulaire
        layout.addWidget(QLabel('➕ Formulaire utilisateur'))
        form_layout = QGridLayout()
        
        form_layout.addWidget(QLabel('👤 Nom d\'utilisateur:'), 0, 0)
        self.username_edit = QLineEdit()
        form_layout.addWidget(self.username_edit, 0, 1)
        
        form_layout.addWidget(QLabel('✉️ Email:'), 0, 2)
        self.email_edit = QLineEdit()
        form_layout.addWidget(self.email_edit, 0, 3)
        
        form_layout.addWidget(QLabel('🔑 Mot de passe:'), 1, 0)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_edit, 1, 1)
        
        form_layout.addWidget(QLabel('👑 Rôle:'), 1, 2)
        self.role_cb = QComboBox()
        self.role_cb.addItems(['user', 'admin', 'superadmin'])
        form_layout.addWidget(self.role_cb, 1, 3)
        
        self.active_cb = HoverButton('✅ Compte actif', '👤')
        self.active_cb.setCheckable(True)
        self.active_cb.setChecked(True)
        self._update_active_button_text()
        form_layout.addWidget(self.active_cb, 2, 0, 1, 2)
        
        layout.addLayout(form_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        self.btn_back = HoverButton('Retour au Dashboard', '🔙')
        buttons_layout.addWidget(self.btn_back)
        buttons_layout.addStretch()
        
        self.btn_add = HoverButton('Ajouter', '➕')
        self.btn_modify = HoverButton('Modifier', '✏️')
        self.btn_delete = HoverButton('Supprimer', '🗑️')
        self.btn_clear = HoverButton('Nettoyer', '🧹')
        
        buttons_layout.addWidget(self.btn_add)
        buttons_layout.addWidget(self.btn_modify)
        buttons_layout.addWidget(self.btn_delete)
        buttons_layout.addWidget(self.btn_clear)
        
        layout.addLayout(buttons_layout)
        
        # Connecter les événements
        self._connect_events()
        self._load_data()
        
    def _connect_events(self):
        """Connexion des événements"""
        self.btn_add.clicked.connect(self.add_user)
        self.btn_modify.clicked.connect(self.modify_user)
        self.btn_delete.clicked.connect(self.delete_user)
        self.btn_clear.clicked.connect(self.clear_form)
        self.users_list.itemClicked.connect(self.on_selection_changed)
        self.active_cb.clicked.connect(self._on_active_toggled)
        
    def _load_data(self):
        """Charge la liste des utilisateurs"""
        try:
            users = self.ctrl.list_users()
            self.users_list.clear()
            
            if not users:
                self.users_list.addItem("Aucun utilisateur trouvé")
                print("⚠️ Aucun utilisateur dans la base")
                return
                
            for user in users:
                status = "✅" if user.active else "❌"
                role_icon = "👑" if user.role == 'superadmin' else "🔑" if user.role == 'admin' else "👤"
                item_text = f"[{user.id}] {status} {role_icon} {user.username} ({user.role})"
                if user.email:
                    item_text += f" - {user.email}"
                self.users_list.addItem(item_text)
            print(f"✅ {len(users)} utilisateurs chargés")
        except Exception as e:
            print(f"❌ Erreur chargement utilisateurs: {e}")
            self.users_list.clear()
            self.users_list.addItem(f"❌ Erreur: {str(e)}")
            
    def on_selection_changed(self, item):
        """Gestion de la sélection"""
        try:
            # Extraire l'ID de l'utilisateur
            text = item.text()
            self.selected_id = int(text.split(']')[0].split('[')[1])
            
            # Charger les données de l'utilisateur sélectionné
            users = self.ctrl.list_users()
            user = next((u for u in users if u.id == self.selected_id), None)
            
            if user:
                self.username_edit.setText(user.username)
                self.email_edit.setText(user.email or "")
                self.password_edit.clear()  # Ne pas afficher le mot de passe
                self.role_cb.setCurrentText(user.role)
                self.active_cb.setChecked(user.active)
                print(f"✅ Utilisateur sélectionné: {user.username} (actif: {user.active})")
        except Exception as e:
            print(f"❌ Erreur sélection: {e}")
            
    def add_user(self):
        """Ajouter un nouvel utilisateur"""
        try:
            username = self.username_edit.text().strip()
            email = self.email_edit.text().strip()
            password = self.password_edit.text().strip()
            role = self.role_cb.currentText()
            active = self.active_cb.isChecked()
            
            if not username or not password:
                QMessageBox.warning(self, "Erreur", "Le nom d'utilisateur et le mot de passe sont obligatoires")
                return
            
            if len(password) < 3:
                QMessageBox.warning(self, "Erreur", "Le mot de passe doit contenir au moins 3 caractères")
                return
                
            result = self.ctrl.create_user(username, email or None, password, role, active)
            if result:
                status_text = "actif" if active else "inactif"
                QMessageBox.information(self, "Succès", f"Utilisateur '{username}' ajouté avec succès ({status_text})")
                self._load_data()
                self.clear_form()
                print(f"✅ Utilisateur créé: {username} ({role}, actif: {active})")
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la création de l'utilisateur")
        except Exception as e:
            error_msg = str(e)
            if "Nom d'utilisateur déjà utilisé" in error_msg:
                QMessageBox.warning(self, "Erreur", f"Le nom d'utilisateur '{username}' est déjà utilisé")
            elif "Email déjà utilisé" in error_msg:
                QMessageBox.warning(self, "Erreur", f"L'email '{email}' est déjà utilisé par un autre utilisateur")
            elif "déjà utilisé" in error_msg:
                QMessageBox.warning(self, "Erreur", error_msg)
            else:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la création: {error_msg}")
            print(f"❌ Erreur création utilisateur: {e}")
            
    def modify_user(self):
        """Modifier l'utilisateur sélectionné"""
        if not self.selected_id:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un utilisateur")
            return
            
        try:
            username = self.username_edit.text().strip()
            email = self.email_edit.text().strip()
            password = self.password_edit.text().strip()
            role = self.role_cb.currentText()
            active = self.active_cb.isChecked()
            
            if not username:
                QMessageBox.warning(self, "Erreur", "Le nom d'utilisateur est obligatoire")
                return
            
            if password and len(password) < 3:
                QMessageBox.warning(self, "Erreur", "Le mot de passe doit contenir au moins 3 caractères")
                return
                
            # Préparer les données à modifier
            update_data = {'username': username, 'email': email or None, 'role': role, 'active': active}
            if password:
                update_data['password'] = password
            
            result = self.ctrl.update_user(self.selected_id, **update_data)
            if result:
                status_text = "actif" if active else "inactif"
                QMessageBox.information(self, "Succès", f"Utilisateur modifié avec succès ({status_text})")
                self._load_data()
                self.clear_form()
                print(f"✅ Utilisateur modifié: {username} (actif: {active})")
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la modification")
        except Exception as e:
            error_msg = str(e)
            if "introuvable" in error_msg:
                QMessageBox.warning(self, "Erreur", "Utilisateur introuvable")
            elif "Nom d'utilisateur déjà utilisé" in error_msg:
                QMessageBox.warning(self, "Erreur", f"Le nom d'utilisateur '{username}' est déjà utilisé par un autre utilisateur")
            elif "Email déjà utilisé" in error_msg:
                QMessageBox.warning(self, "Erreur", f"L'email '{email}' est déjà utilisé par un autre utilisateur")
            elif "déjà utilisé" in error_msg:
                QMessageBox.warning(self, "Erreur", error_msg)
            else:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la modification: {error_msg}")
            print(f"❌ Erreur modification: {e}")
            
    def delete_user(self):
        """Supprimer l'utilisateur sélectionné"""
        if not self.selected_id:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un utilisateur")
            return
        
        # Vérifier qu'on ne supprime pas l'admin principal
        users = self.ctrl.list_users()
        user_to_delete = next((u for u in users if u.id == self.selected_id), None)
        
        if user_to_delete and user_to_delete.role == 'superadmin':
            QMessageBox.warning(self, "Erreur", "Impossible de supprimer le super administrateur")
            return
            
        reply = QMessageBox.question(
            self, "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer l'utilisateur '{user_to_delete.username if user_to_delete else 'inconnu'}' ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.ctrl.delete_user(self.selected_id)
                QMessageBox.information(self, "Succès", "Utilisateur supprimé avec succès")
                self._load_data()
                self.clear_form()
                print(f"✅ Utilisateur supprimé: ID {self.selected_id}")
            except Exception as e:
                error_msg = str(e)
                if "introuvable" in error_msg:
                    QMessageBox.warning(self, "Erreur", "Utilisateur introuvable")
                else:
                    QMessageBox.critical(self, "Erreur", f"Erreur: {error_msg}")
                print(f"❌ Erreur suppression: {e}")
                
    def _update_active_button_text(self):
        """Met à jour le texte du bouton selon son état"""
        if self.active_cb.isChecked():
            self.active_cb.setText('✅ Compte actif')
        else:
            self.active_cb.setText('❌ Compte inactif')
            
    def _on_active_toggled(self):
        """Gère le changement d'état du bouton"""
        self._update_active_button_text()

    def clear_form(self):
        """Vider le formulaire"""
        self.username_edit.clear()
        self.email_edit.clear()
        self.password_edit.clear()
        self.role_cb.setCurrentIndex(0)
        self.active_cb.setChecked(True)
        self._update_active_button_text()
        self.selected_id = None