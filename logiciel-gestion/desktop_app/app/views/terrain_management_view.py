from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QListWidget, QLineEdit, QLabel, QMessageBox, QFrame
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt
from app.controllers.terrain_controller import TerrainController

class TerrainManagementView(QWidget):
    def __init__(self):
        super().__init__()
        self.ctrl = TerrainController()
        self.selected_id = None
        self.setWindowTitle('Gestion des Terrains')
        self.setMinimumWidth(700)
        self.setStyleSheet("""
            QWidget { background: #f7f7fa; }
            QLabel.title { font-size: 22px; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }
            QLineEdit, QListWidget { font-size: 15px; }
            QPushButton { background: #2980b9; color: white; border-radius: 6px; padding: 6px 16px; font-weight: bold; }
            QPushButton:hover { background: #3498db; }
        """)
        self._build()
        self.load_terrains()

    def _build(self):
        layout = QVBoxLayout()
        # Titre principal
        title = QLabel('Gestion des Terrains')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Liste des terrains
        list_frame = QFrame()
        list_frame.setFrameShape(QFrame.StyledPanel)
        list_frame.setStyleSheet('QFrame { background: #fff; border-radius: 8px; padding: 12px; }')
        list_layout = QVBoxLayout(list_frame)
        list_label = QLabel('Liste des terrains')
        list_label.setFont(QFont('Arial', 16, QFont.Bold))
        list_layout.addWidget(list_label)
        self.list = QListWidget()
        self.list.setStyleSheet('QListWidget { background: #f8f8ff; border: 1px solid #dbeafe; }')
        self.list.itemSelectionChanged.connect(self.on_select)
        list_layout.addWidget(self.list)
        layout.addWidget(list_frame)

        # Formulaire terrain
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.StyledPanel)
        form_frame.setStyleSheet('QFrame { background: #eaf2fb; border-radius: 8px; padding: 12px; }')
        form_layout = QGridLayout(form_frame)
        self.name_input = QLineEdit(); self.name_input.setPlaceholderText('Nom du terrain')
        self.loc_input = QLineEdit(); self.loc_input.setPlaceholderText('Lieu')
        form_layout.addWidget(QLabel('Nom'), 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)
        form_layout.addWidget(QLabel('Lieu'), 1, 0)
        form_layout.addWidget(self.loc_input, 1, 1)
        layout.addWidget(form_frame)

        # Boutons action
        btns = QHBoxLayout()
        self.btn_add = QPushButton(QIcon(), 'Ajouter')
        self.btn_add.setToolTip('Ajouter un terrain')
        self.btn_add.clicked.connect(self.add_terrain)
        self.btn_update = QPushButton(QIcon(), 'Modifier')
        self.btn_update.setToolTip('Modifier le terrain sélectionné')
        self.btn_update.clicked.connect(self.update_terrain)
        self.btn_delete = QPushButton(QIcon(), 'Supprimer')
        self.btn_delete.setToolTip('Supprimer le terrain sélectionné')
        self.btn_delete.clicked.connect(self.delete_terrain)
        self.btn_toggle = QPushButton(QIcon(), 'Activer/Désactiver')
        self.btn_toggle.setToolTip('Activer ou désactiver le terrain sélectionné')
        self.btn_toggle.clicked.connect(self.toggle_terrain)
        btns.addWidget(self.btn_add)
        btns.addWidget(self.btn_update)
        btns.addWidget(self.btn_delete)
        btns.addWidget(self.btn_toggle)
        layout.addLayout(btns)

        self.setLayout(layout)

    def load_terrains(self):
        self.list.clear()
        for t in self.ctrl.list_terrains():
            status = 'Actif' if t.active else 'Inactif'
            self.list.addItem(f'{t.id} - {t.name} - {t.location or ""} - {status}')

    def on_select(self):
        items = self.list.selectedItems()
        if not items:
            self.selected_id = None
            self.name_input.clear()
            self.loc_input.clear()
            return
        txt = items[0].text()
        tid, name, loc, *_ = txt.split(' - ')
        self.selected_id = int(tid)
        self.name_input.setText(name)
        self.loc_input.setText(loc)

    def add_terrain(self):
        name = self.name_input.text().strip()
        loc = self.loc_input.text().strip()
        if not name:
            QMessageBox.warning(self, 'Erreur', 'Nom requis')
            return
        self.ctrl.create(name, loc)
        self.load_terrains()
        self.name_input.clear(); self.loc_input.clear()

    def update_terrain(self):
        if not self.selected_id:
            QMessageBox.warning(self, 'Erreur', 'Sélectionnez un terrain')
            return
        name = self.name_input.text().strip()
        loc = self.loc_input.text().strip()
        self.ctrl.update(self.selected_id, name=name, location=loc)
        self.load_terrains()
        # Reselect l'élément modifié pour rafraîchir le formulaire
        for i in range(self.list.count()):
            item = self.list.item(i)
            if item.text().startswith(f"{self.selected_id} -"):
                self.list.setCurrentItem(item)
                break

    def delete_terrain(self):
        if not self.selected_id:
            QMessageBox.warning(self, 'Erreur', 'Sélectionnez un terrain')
            return
        self.ctrl.delete(self.selected_id)
        self.load_terrains()
        self.selected_id = None
        self.name_input.clear(); self.loc_input.clear()

    def toggle_terrain(self):
        if not self.selected_id:
            QMessageBox.warning(self, 'Erreur', 'Sélectionnez un terrain')
            return
        t = [t for t in self.ctrl.list_terrains() if t.id == self.selected_id][0]
        self.ctrl.update(self.selected_id, active=not t.active)
        self.load_terrains()
