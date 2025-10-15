from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QFrame, QLineEdit, QCheckBox
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
from app.controllers.user_controller import UserController

class UserManagementView(QWidget):
    def __init__(self):
        super().__init__()
        self.ctrl = UserController()
        self.setWindowTitle('Gestion des Utilisateurs')
        self.setMinimumWidth(800)
        self.setStyleSheet("""
            QWidget { background: #f7f7fa; }
            QLabel.title { font-size: 22px; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }
            QTableWidget { font-size: 15px; background: #f8f8ff; border: 1px solid #dbeafe; }
            QPushButton { background: #2980b9; color: white; border-radius: 6px; padding: 6px 16px; font-weight: bold; }
            QPushButton:hover { background: #3498db; }
        """)
        self._build()
        self.load_users()

    def _build(self):
        layout = QVBoxLayout()
        # Titre principal
        title = QLabel('Gestion des Utilisateurs')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Filtres avancés
        filter_frame = QFrame()
        filter_frame.setFrameShape(QFrame.StyledPanel)
        filter_frame.setStyleSheet('QFrame { background: #eaf2fb; border-radius: 8px; padding: 12px; }')
        filter_layout = QHBoxLayout(filter_frame)
        self.search_input = QLineEdit(); self.search_input.setPlaceholderText('Rechercher un utilisateur...')
        self.show_all_cb = QCheckBox('Afficher tous les utilisateurs')
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.show_all_cb)
        layout.addWidget(filter_frame)

        # Table des utilisateurs
        table_frame = QFrame()
        table_frame.setFrameShape(QFrame.StyledPanel)
        table_frame.setStyleSheet('QFrame { background: #fff; border-radius: 8px; padding: 12px; }')
        table_layout = QVBoxLayout(table_frame)
        table_label = QLabel('Liste des utilisateurs')
        table_label.setFont(QFont('Arial', 16, QFont.Bold))
        table_layout.addWidget(table_label)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['ID', 'Nom', 'Email', 'Rôle'])
        self.table.setStyleSheet('QTableWidget { background: #f8f8ff; border: 1px solid #dbeafe; }')
        table_layout.addWidget(self.table)
        layout.addWidget(table_frame)

        # Boutons action
        btns = QHBoxLayout()
        btn_add = QPushButton(QIcon(), 'Ajouter')
        btn_add.setToolTip('Ajouter un utilisateur')
        btn_add.clicked.connect(self.add_user)
        btn_edit = QPushButton(QIcon(), 'Modifier')
        btn_edit.setToolTip('Modifier l\'utilisateur sélectionné')
        btn_edit.clicked.connect(self.edit_user)
        btn_del = QPushButton(QIcon(), 'Supprimer')
        btn_del.setToolTip('Supprimer l\'utilisateur sélectionné')
        btn_del.clicked.connect(self.delete_user)
        btns.addWidget(btn_add)
        btns.addWidget(btn_edit)
        btns.addWidget(btn_del)
        layout.addLayout(btns)

        self.setLayout(layout)
        # Connexion des signaux de filtre
        self.search_input.returnPressed.connect(self.load_users)
        self.show_all_cb.stateChanged.connect(self.load_users)

    def load_users(self):
        users = self.ctrl.list_users()
        search_text = self.search_input.text().strip().lower()
        show_all = self.show_all_cb.isChecked()
        self.table.setRowCount(0)
        for user in users:
            if not show_all:
                # Filtre par recherche
                if search_text and search_text not in user.username.lower() and search_text not in user.email.lower():
                    continue
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.table.setItem(row, 1, QTableWidgetItem(user.username))
            self.table.setItem(row, 2, QTableWidgetItem(user.email))
            self.table.setItem(row, 3, QTableWidgetItem(user.role))

    def add_user(self):
        from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox
        dialog = QDialog(self)
        dialog.setWindowTitle('Ajouter un utilisateur')
        form = QFormLayout(dialog)
        username = QLineEdit()
        email = QLineEdit()
        password = QLineEdit(); password.setEchoMode(QLineEdit.Password)
        role = QComboBox(); role.addItems(['superadmin', 'admin', 'user'])
        form.addRow('Nom d\'utilisateur', username)
        form.addRow('Email', email)
        form.addRow('Mot de passe', password)
        form.addRow('Rôle', role)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        form.addRow(buttons)
        def submit():
            try:
                self.ctrl.create_user(username.text().strip(), email.text().strip(), password.text(), role.currentText())
                self.load_users()
                dialog.accept()
                QMessageBox.information(self, 'Succès', 'Utilisateur ajouté')
            except Exception as e:
                QMessageBox.warning(self, 'Erreur', str(e))
        buttons.accepted.connect(submit)
        buttons.rejected.connect(dialog.reject)
        dialog.exec()

    def edit_user(self):
        from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QDialogButtonBox
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Erreur', 'Sélectionnez un utilisateur')
            return
        user_id = int(self.table.item(row, 0).text())
        username_val = self.table.item(row, 1).text()
        email_val = self.table.item(row, 2).text()
        role_val = self.table.item(row, 3).text()
        dialog = QDialog(self)
        dialog.setWindowTitle('Modifier utilisateur')
        form = QFormLayout(dialog)
        username = QLineEdit(username_val)
        email = QLineEdit(email_val)
        password = QLineEdit(); password.setEchoMode(QLineEdit.Password)
        role = QComboBox(); role.addItems(['superadmin', 'admin', 'user']); role.setCurrentText(role_val)
        form.addRow('Nom d\'utilisateur', username)
        form.addRow('Email', email)
        form.addRow('Nouveau mot de passe (laisser vide pour ne pas changer)', password)
        form.addRow('Rôle', role)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        form.addRow(buttons)
        def submit():
            try:
                kwargs = {
                    'username': username.text().strip(),
                    'email': email.text().strip(),
                    'role': role.currentText()
                }
                if password.text():
                    kwargs['password'] = password.text()
                self.ctrl.update_user(user_id, **kwargs)
                self.load_users()
                dialog.accept()
                QMessageBox.information(self, 'Succès', 'Utilisateur modifié')
            except Exception as e:
                QMessageBox.warning(self, 'Erreur', str(e))
        buttons.accepted.connect(submit)
        buttons.rejected.connect(dialog.reject)
        dialog.exec()

    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Erreur', 'Sélectionnez un utilisateur')
            return
        user_id = int(self.table.item(row, 0).text())
        try:
            self.ctrl.delete_user(user_id)
            self.load_users()
            QMessageBox.information(self, 'Succès', 'Utilisateur supprimé')
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', str(e))
