from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from app.controllers.user_controller import UserController

class UserManagementView(QWidget):
    def __init__(self):
        super().__init__()
        self.ctrl = UserController()
        self._build()
        self.load_users()

    def _build(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Gestion des utilisateurs'))
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['ID', 'Nom', 'Email', 'Rôle'])
        layout.addWidget(self.table)
        btns = QHBoxLayout()
        btn_add = QPushButton('Ajouter')
        btn_add.clicked.connect(self.add_user)
        btn_edit = QPushButton('Modifier')
        btn_edit.clicked.connect(self.edit_user)
        btn_del = QPushButton('Supprimer')
        btn_del.clicked.connect(self.delete_user)
        btns.addWidget(btn_add)
        btns.addWidget(btn_edit)
        btns.addWidget(btn_del)
        layout.addLayout(btns)
        self.setLayout(layout)

    def load_users(self):
        users = self.ctrl.list_users()
        self.table.setRowCount(0)
        for user in users:
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
