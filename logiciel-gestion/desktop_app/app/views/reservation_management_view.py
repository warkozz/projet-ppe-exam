from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QComboBox, QDateEdit, QLabel, QMessageBox, QTextEdit
from PySide6.QtCore import QDateTime, QDate
from app.controllers.reservation_controller import ReservationController
from app.controllers.terrain_controller import TerrainController
from app.controllers.user_controller import UserController
from datetime import datetime

class ReservationManagementView(QWidget):
    def load_users_terrains(self):
        self.user_cb.clear()
        for u in self.user_ctrl.list_users():
            self.user_cb.addItem(f'{u.id} - {u.username}', u.id)
        self.terrain_cb.clear()
        for t in self.terrain_ctrl.list_terrains():
            if t.active:
                self.terrain_cb.addItem(f'{t.id} - {t.name}', t.id)
    def _populate_slots(self):
        self.slot_cb.clear()
        for h in range(9, 23, 2):
            start = f"{h:02d}:00"
            end = f"{h+2:02d}:00"
            self.slot_cb.addItem(f"{start} - {end}", (h, h+2))
    def __init__(self):
        super().__init__()
        self.ctrl = ReservationController()
        self.terrain_ctrl = TerrainController()
        self.user_ctrl = UserController()
        self.selected_id = None
        self._build()
        self.load_reservations()

    def _build(self):
        layout = QVBoxLayout()
        self.list = QListWidget()
        self.list.itemSelectionChanged.connect(self.on_select)
        layout.addWidget(QLabel('Liste des réservations'))
        layout.addWidget(self.list)

        form = QHBoxLayout()
        self.user_cb = QComboBox()
        self.terrain_cb = QComboBox()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat('yyyy-MM-dd')
        self.date_edit.setCalendarPopup(True)
        self.slot_cb = QComboBox()
        self._populate_slots()
        self.notes = QTextEdit()
        self.notes.setPlaceholderText('Notes')
        form.addWidget(self.user_cb)
        form.addWidget(self.terrain_cb)
        form.addWidget(self.date_edit)
        form.addWidget(self.slot_cb)
        form.addWidget(self.notes)
        layout.addLayout(form)

        btns = QHBoxLayout()
        self.btn_add = QPushButton('Ajouter')
        self.btn_add.clicked.connect(self.add_reservation)
        self.btn_cancel = QPushButton('Annuler réservation')
        self.btn_cancel.clicked.connect(self.cancel_reservation)
        btns.addWidget(self.btn_add)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)
        self.setLayout(layout)
        self.load_users_terrains()
        self.date_edit.dateChanged.connect(self.update_terrains_avail)
        self.slot_cb.currentIndexChanged.connect(self.update_terrains_avail)
        self.update_terrains_avail()
    def update_terrains_avail(self):
        # Affiche seulement les terrains disponibles pour la date/créneau sélectionné
        from app.services.cpp_bridge import check_conflict
        date = self.date_edit.date().toPython()
        slot = self.slot_cb.currentData()
        self.terrain_cb.clear()
        if not slot:
            return
        start = datetime(date.year, date.month, date.day, slot[0], 0, 0)
        end = datetime(date.year, date.month, date.day, slot[1], 0, 0)
        for t in self.terrain_ctrl.list_terrains():
            if not t.active:
                continue
            try:
                conflict = check_conflict(self.ctrl.db, t.id, start, end) if hasattr(self.ctrl, 'db') else False
            except Exception:
                conflict = False
            label = f'{t.id} - {t.name}'
            self.terrain_cb.addItem(label, t.id)
            idx = self.terrain_cb.count()-1
            if conflict:
                self.terrain_cb.model().item(idx).setEnabled(False)

    def on_select(self):
        items = self.list.selectedItems()
        if not items:
            self.selected_id = None
            return
        txt = items[0].text()
        rid, *_ = txt.split(' - ')
        self.selected_id = int(rid)

    def add_reservation(self):
        user_id = self.user_cb.currentData()
        terrain_id = self.terrain_cb.currentData()
        date = self.date_edit.date().toPython()
        slot = self.slot_cb.currentData()
        notes = self.notes.toPlainText().strip()
        if not user_id or not terrain_id or not slot:
            QMessageBox.warning(self, 'Erreur', 'Sélectionnez un utilisateur, un terrain et un créneau')
            return
        start = datetime(date.year, date.month, date.day, slot[0], 0, 0)
        end = datetime(date.year, date.month, date.day, slot[1], 0, 0)
        try:
            self.ctrl.create_reservation(user_id, terrain_id, start, end, notes)
            self.load_reservations()
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', str(e))

    def cancel_reservation(self):
        if not self.selected_id:
            QMessageBox.warning(self, 'Erreur', 'Sélectionnez une réservation')
            return
        try:
            self.ctrl.cancel_reservation(self.selected_id)
            self.load_reservations()
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', str(e))
