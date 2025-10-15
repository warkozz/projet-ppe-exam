from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QListWidget, QComboBox, QDateEdit, QLabel, QMessageBox, QTextEdit, QCheckBox, QFrame
)
from PySide6.QtGui import QIcon, QFont, QColor, QPalette
from PySide6.QtCore import QDateTime, QDate, Qt
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
        self.setWindowTitle('Gestion des Réservations')
        self.setMinimumWidth(900)
        self.setStyleSheet("""
            QWidget { background: #f7f7fa; }
            QLabel.title { font-size: 22px; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }
            QComboBox, QDateEdit, QTextEdit, QListWidget { font-size: 15px; }
            QPushButton { background: #2980b9; color: white; border-radius: 6px; padding: 6px 16px; font-weight: bold; }
            QPushButton:hover { background: #3498db; }
            QCheckBox { font-size: 15px; }
        """)
        self._build()
    def _populate_slots(self):
        self.slot_cb.clear()
        # Créneaux horaires typiques (modifiable)
        slots = [
            (8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20)
        ]
        for s in slots:
            label = f"{s[0]:02d}h - {s[1]:02d}h"
            self.slot_cb.addItem(label, s)

    def _build(self):
        layout = QVBoxLayout()
        # Titre principal
        title = QLabel('Gestion des Réservations')
        title.setObjectName('title')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Filtres avancés
        filter_frame = QFrame()
        filter_frame.setFrameShape(QFrame.StyledPanel)
        filter_frame.setStyleSheet('QFrame { background: #eaf2fb; border-radius: 8px; padding: 12px; }')
        filter_layout = QGridLayout(filter_frame)
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
        self.btn_filter = QPushButton(QIcon(), 'Filtrer')
        self.btn_filter.setToolTip('Appliquer les filtres')
        filter_layout.addWidget(QLabel('Utilisateur'), 0, 0)
        filter_layout.addWidget(self.user_cb, 0, 1)
        filter_layout.addWidget(self.show_all_cb, 0, 2)
        filter_layout.addWidget(QLabel('Du'), 1, 0)
        filter_layout.addWidget(self.date_from, 1, 1)
        filter_layout.addWidget(QLabel('au'), 1, 2)
        filter_layout.addWidget(self.date_to, 1, 3)
        filter_layout.addWidget(self.btn_filter, 1, 4)
        layout.addWidget(filter_frame)

        # Liste des réservations
        list_frame = QFrame()
        list_frame.setFrameShape(QFrame.StyledPanel)
        list_frame.setStyleSheet('QFrame { background: #fff; border-radius: 8px; padding: 12px; }')
        list_layout = QVBoxLayout(list_frame)
        list_label = QLabel('Liste des réservations')
        list_label.setFont(QFont('Arial', 16, QFont.Bold))
        list_layout.addWidget(list_label)
        self.list = QListWidget()
        self.list.setStyleSheet('QListWidget { background: #f8f8ff; border: 1px solid #dbeafe; }')
        self.list.itemSelectionChanged.connect(self.on_select)
        list_layout.addWidget(self.list)
        layout.addWidget(list_frame)

        # Formulaire réservation
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.StyledPanel)
        form_frame.setStyleSheet('QFrame { background: #eaf2fb; border-radius: 8px; padding: 12px; }')
        form_layout = QGridLayout(form_frame)
        self.terrain_cb = QComboBox()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat('yyyy-MM-dd')
        self.date_edit.setCalendarPopup(True)
        self.slot_cb = QComboBox()
        self._populate_slots()
        self.notes = QTextEdit()
        self.notes.setPlaceholderText('Notes (optionnel)')
        form_layout.addWidget(QLabel('Terrain'), 0, 0)
        form_layout.addWidget(self.terrain_cb, 0, 1)
        form_layout.addWidget(QLabel('Date'), 1, 0)
        form_layout.addWidget(self.date_edit, 1, 1)
        form_layout.addWidget(QLabel('Créneau'), 2, 0)
        form_layout.addWidget(self.slot_cb, 2, 1)
        form_layout.addWidget(QLabel('Notes'), 3, 0)
        form_layout.addWidget(self.notes, 3, 1, 1, 3)
        layout.addWidget(form_frame)

        # Boutons action
        btns = QHBoxLayout()
        self.btn_add = QPushButton(QIcon(), 'Ajouter')
        self.btn_add.setToolTip('Ajouter une nouvelle réservation')
        self.btn_add.clicked.connect(self.add_reservation)
        self.btn_modify = QPushButton(QIcon(), 'Modifier')
        self.btn_modify.setToolTip('Modifier la réservation sélectionnée')
        self.btn_modify.clicked.connect(self.modify_reservation)
        self.btn_cancel = QPushButton(QIcon(), 'Annuler réservation')
        self.btn_cancel.setToolTip('Annuler la réservation sélectionnée')
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
        self.show_all_cb.stateChanged.connect(self.load_reservations)

    def load_users_terrains(self):
        self.user_cb.clear()
        users = self.user_ctrl.list_users()
        for u in users:
            self.user_cb.addItem(f"{u.username}", u.id)
        self.user_cb.setCurrentIndex(-1)

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
            self.user_cb.setCurrentIndex(-1)
            self.terrain_cb.setCurrentIndex(-1)
            self.date_edit.setDate(QDate.currentDate())
            self.slot_cb.setCurrentIndex(-1)
            self.notes.clear()
            return
        txt = items[0].text()
        # Format attendu: '{id} - {user_str} - {terrain_str} - {start} à {end}'
        parts = txt.split(' - ')
        if len(parts) < 4:
            self.selected_id = None
            return
        rid = parts[0]
        self.selected_id = int(rid)
        # Recherche la réservation dans la base
        reservations = self.ctrl.get_reservations()
        for r in reservations:
            if r.id == self.selected_id:
                idx_user = self.user_cb.findData(r.user_id)
                if idx_user >= 0:
                    self.user_cb.setCurrentIndex(idx_user)
                idx_terrain = self.terrain_cb.findData(r.terrain_id)
                if idx_terrain >= 0:
                    self.terrain_cb.setCurrentIndex(idx_terrain)
                self.date_edit.setDate(QDate(r.start.year, r.start.month, r.start.day))
                slot_tuple = (r.start.hour, r.end.hour)
                idx_slot = self.slot_cb.findData(slot_tuple)
                if idx_slot >= 0:
                    self.slot_cb.setCurrentIndex(idx_slot)
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
