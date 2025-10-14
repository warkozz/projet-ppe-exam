from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QComboBox, QDateEdit, QLabel, QMessageBox, QTextEdit
from PySide6.QtWidgets import QLineEdit, QCheckBox
from PySide6.QtCore import QDateTime, QDate
from app.controllers.reservation_controller import ReservationController
from app.controllers.terrain_controller import TerrainController
from app.controllers.user_controller import UserController
from datetime import datetime

class ReservationManagementView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ctrl = ReservationController()
        self.user_ctrl = UserController()
        self.terrain_ctrl = TerrainController()
        self.selected_id = None
        self._build()
    def _populate_slots(self):
        self.slot_cb.clear()
        # Ajoutez ici la logique pour remplir les créneaux si besoin

    def _build(self):
        layout = QVBoxLayout()
        # Filtres avancés
        filter_layout = QHBoxLayout()
        self.user_cb = QComboBox()
        self.user_cb.setEditable(True)
        self.user_cb.setInsertPolicy(QComboBox.NoInsert)
        self.user_cb.setPlaceholderText('Sélectionner ou rechercher un utilisateur...')
        self.show_all_cb = QCheckBox('Afficher toutes les réservations')
        self.date_from = QDateEdit(QDate.currentDate())
        self.date_from.setDisplayFormat('yyyy-MM-dd')
        self.date_from.setCalendarPopup(True)
        self.date_to = QDateEdit(QDate.currentDate())
        self.date_to.setDisplayFormat('yyyy-MM-dd')
        self.date_to.setCalendarPopup(True)
        filter_layout.addWidget(self.user_cb)
        filter_layout.addWidget(self.show_all_cb)
        filter_layout.addWidget(QLabel('Du'))
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(QLabel('au'))
        filter_layout.addWidget(self.date_to)
        self.btn_filter = QPushButton('Filtrer')
        filter_layout.addWidget(self.btn_filter)
        layout.addLayout(filter_layout)

        self.list = QListWidget()
        self.list.itemSelectionChanged.connect(self.on_select)
        layout.addWidget(QLabel('Liste des réservations'))
        layout.addWidget(self.list)

        form = QHBoxLayout()
        self.terrain_cb = QComboBox()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat('yyyy-MM-dd')
        self.date_edit.setCalendarPopup(True)
        self.slot_cb = QComboBox()
        self._populate_slots()
        self.notes = QTextEdit()
        self.notes.setPlaceholderText('Notes')
        form.addWidget(self.terrain_cb)
        form.addWidget(self.date_edit)
        form.addWidget(self.slot_cb)
        form.addWidget(self.notes)
        layout.addLayout(form)

        btns = QHBoxLayout()
        self.btn_add = QPushButton('Ajouter')
        self.btn_add.clicked.connect(self.add_reservation)
        self.btn_modify = QPushButton('Modifier')
        self.btn_modify.clicked.connect(self.modify_reservation)
        self.btn_cancel = QPushButton('Annuler réservation')
        self.btn_cancel.clicked.connect(self.cancel_reservation)
        btns.addWidget(self.btn_add)
        btns.addWidget(self.btn_modify)
        btns.addWidget(self.btn_cancel)
        layout.addLayout(btns)

        self.setLayout(layout)
        self.load_users_terrains()
        self.date_edit.dateChanged.connect(self.update_terrains_avail)
        self.slot_cb.currentIndexChanged.connect(self.update_terrains_avail)
        self.update_terrains_avail()
        # Connexion des signaux de filtre
        self.btn_filter.clicked.connect(self.load_reservations)
        self.user_cb.lineEdit().returnPressed.connect(self.load_reservations)

    def load_users_terrains(self):
        self.user_cb.clear()
        users = self.user_ctrl.list_users()
        for u in users:
            self.user_cb.addItem(u.username, u.id)

    def modify_reservation(self):
        if not self.selected_id:
            QMessageBox.warning(self, 'Erreur', 'Sélectionnez une réservation à modifier')
            return
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
            self.ctrl.modify_reservation(self.selected_id, user_id, terrain_id, start, end, notes)
            self.load_reservations()
            self.update_terrains_avail()
            # Reselect the modified reservation in the list
            for i in range(self.list.count()):
                item = self.list.item(i)
                if item.text().startswith(f"{self.selected_id} -"):
                    self.list.setCurrentItem(item)
                    break
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', str(e))
    def update_terrains_avail(self):
        # Affiche seulement les terrains disponibles pour la date/créneau sélectionné
        from app.services.cpp_bridge import check_conflict
        from app.models.db import SessionLocal
        date = self.date_edit.date().toPython()
        slot = self.slot_cb.currentData()
        self.terrain_cb.clear()
        if not slot:
            return
        start = datetime(date.year, date.month, date.day, slot[0], 0, 0)
        end = datetime(date.year, date.month, date.day, slot[1], 0, 0)
        db = SessionLocal()
        try:
            for t in self.terrain_ctrl.list_terrains():
                if not t.active:
                    continue
                try:
                    conflict = check_conflict(db, t.id, start, end)
                except Exception:
                    conflict = False
                label = f'{t.id} - {t.name}'
                self.terrain_cb.addItem(label, t.id)
                idx = self.terrain_cb.count()-1
                if conflict:
                    self.terrain_cb.model().item(idx).setEnabled(False)
        finally:
            db.close()

    def on_select(self):
        items = self.list.selectedItems()
        if not items:
            self.selected_id = None
            return
        txt = items[0].text()
        # Format attendu: '{id} - {user_str} - {terrain_str} - {start} à {end}'
        parts = txt.split(' - ')
        if len(parts) < 4:
            self.selected_id = None
            return
        rid = parts[0]
        self.selected_id = int(rid)
        # Remplit le formulaire avec les infos de la réservation sélectionnée
        # Recherche la réservation dans la liste
        now = datetime.now()
        reservations = self.ctrl.get_reservations(date_from=now)
        for r in reservations:
            if r.id == self.selected_id:
                # Utilisateur
                idx_user = self.user_cb.findData(r.user_id)
                if idx_user >= 0:
                    self.user_cb.setCurrentIndex(idx_user)
                # Terrain
                idx_terrain = self.terrain_cb.findData(r.terrain_id)
                if idx_terrain >= 0:
                    self.terrain_cb.setCurrentIndex(idx_terrain)
                # Date
                self.date_edit.setDate(QDate(r.start.year, r.start.month, r.start.day))
                # Créneau
                slot_tuple = (r.start.hour, r.end.hour)
                idx_slot = self.slot_cb.findData(slot_tuple)
                if idx_slot >= 0:
                    self.slot_cb.setCurrentIndex(idx_slot)
                # Notes
                self.notes.setPlainText(r.notes or '')
                break

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
            self.update_terrains_avail()
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', str(e))

    def cancel_reservation(self):
        if not self.selected_id:
            QMessageBox.warning(self, 'Erreur', 'Sélectionnez une réservation')
            return
        try:
            self.ctrl.cancel_reservation(self.selected_id)
            self.load_reservations()
            self.update_terrains_avail()
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', str(e))

    def load_reservations(self):
        self.list.clear()
        try:
            reservations = self.ctrl.get_reservations()
            user_id = self.user_cb.currentData()
            terrain_id = self.terrain_cb.currentData()
            show_all = self.show_all_cb.isChecked()
            search_text = self.user_cb.currentText().strip().lower() if self.user_cb.isEditable() else ''
            for r in reservations:
                if getattr(r, 'status', None) == 'cancelled':
                    continue
                user = getattr(r, 'user', None)
                user_str = user.username if user else str(r.user_id)
                # Filtrage par recherche utilisateur
                if search_text and search_text not in user_str.lower():
                    continue
                if not show_all:
                    if user_id and r.user_id != user_id:
                        continue
                    if terrain_id and r.terrain_id != terrain_id:
                        continue
                start = r.start.strftime('%Y-%m-%d %H:%M')
                end = r.end.strftime('%H:%M')
                terrain = getattr(r, 'terrain', None)
                terrain_str = terrain.name if terrain else str(r.terrain_id)
                self.list.addItem(f'{r.id} - {user_str} - {terrain_str} - {start} à {end}')
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', f'Impossible de charger les réservations: {e}')
