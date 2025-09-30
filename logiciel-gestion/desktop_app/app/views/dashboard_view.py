from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget
from app.controllers.terrain_controller import TerrainController
class DashboardView(QWidget):
    def __init__(self, user):
        super().__init__(); self.user = user; self.terrain_ctrl = TerrainController(); self._build()
    def _build(self):
        layout = QVBoxLayout(); layout.addWidget(QLabel(f'Bienvenue {self.user.username}'))
        self.terrain_list = QListWidget(); btn = QPushButton('Rafraichir'); btn.clicked.connect(self.load_terrains)
        layout.addWidget(self.terrain_list); layout.addWidget(btn); self.setLayout(layout); self.load_terrains()
    def load_terrains(self):
        self.terrain_list.clear()
        for t in self.terrain_ctrl.list_terrains():
            self.terrain_list.addItem(f"{t.id} - {t.name} - {'Actif' if t.active else 'Inactif'}")
