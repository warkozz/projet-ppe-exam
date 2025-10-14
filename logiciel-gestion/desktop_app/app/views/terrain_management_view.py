from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QMessageBox
from app.controllers.terrain_controller import TerrainController

class TerrainManagementView(QWidget):
    def __init__(self):
        super().__init__()
        self.ctrl = TerrainController()
        self.selected_id = None
        self._build()
        self.load_terrains()

    def _build(self):
        layout = QVBoxLayout()
        self.list = QListWidget()
        self.list.itemSelectionChanged.connect(self.on_select)
        layout.addWidget(QLabel('Liste des terrains'))
        layout.addWidget(self.list)

        form = QHBoxLayout()
        self.name_input = QLineEdit(); self.name_input.setPlaceholderText('Nom')
        self.loc_input = QLineEdit(); self.loc_input.setPlaceholderText('Lieu')
        form.addWidget(self.name_input)
        form.addWidget(self.loc_input)
        layout.addLayout(form)

        btns = QHBoxLayout()
        self.btn_add = QPushButton('Ajouter')
        self.btn_add.clicked.connect(self.add_terrain)
        self.btn_update = QPushButton('Modifier')
        self.btn_update.clicked.connect(self.update_terrain)
        self.btn_delete = QPushButton('Supprimer')
        self.btn_delete.clicked.connect(self.delete_terrain)
        self.btn_toggle = QPushButton('Activer/Désactiver')
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
