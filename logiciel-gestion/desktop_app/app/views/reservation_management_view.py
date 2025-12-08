from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QListWidget, QComboBox, QDateEdit, 
    QLabel, QMessageBox, QTextEdit, QCheckBox, QListWidgetItem, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import QDate, Qt
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
        # Style simple harmonisé avec les autres pages
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
        
        # Titre simple
        layout.addWidget(QLabel('Gestion des Réservations'))
        
        # Filtres simples
        layout.addWidget(QLabel('Utilisateur:'))
        self.user_cb = QComboBox()
        self.user_cb.setEditable(True)
        layout.addWidget(self.user_cb)
        
        layout.addWidget(QLabel('Terrain:'))
        self.terrain_cb = QComboBox()
        layout.addWidget(self.terrain_cb)
        
        self.show_all_cb = QCheckBox('Afficher toutes les réservations')
        layout.addWidget(self.show_all_cb)
        
        layout.addWidget(QLabel('Du:'))
        self.date_from = QDateEdit(QDate.currentDate())
        self.date_from.setDisplayFormat('yyyy-MM-dd')
        layout.addWidget(self.date_from)
        
        layout.addWidget(QLabel('Au:'))
        self.date_to = QDateEdit(QDate.currentDate())
        self.date_to.setDisplayFormat('yyyy-MM-dd')
        layout.addWidget(self.date_to)
        
        self.btn_filter = QPushButton('Filtrer')
        layout.addWidget(self.btn_filter)
        
        self.btn_reset = QPushButton('Reset')
        layout.addWidget(self.btn_reset)

        # Liste des réservations
        layout.addWidget(QLabel('Liste des réservations'))
        self.reservations_list = QListWidget()
        layout.addWidget(self.reservations_list)

        # Formulaire réservation
        layout.addWidget(QLabel('Terrain:'))
        layout.addWidget(self.terrain_cb)
        
        layout.addWidget(QLabel('Date:'))
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat('yyyy-MM-dd')
        layout.addWidget(self.date_edit)
        
        layout.addWidget(QLabel('Créneau:'))
        self.slot_cb = QComboBox()
        self._populate_slots()
        layout.addWidget(self.slot_cb)
        
        layout.addWidget(QLabel('Notes:'))
        self.notes = QTextEdit()
        layout.addWidget(self.notes)

        # Boutons
        self.btn_add = QPushButton('Ajouter')
        self.btn_add.clicked.connect(self.add_reservation)
        layout.addWidget(self.btn_add)
        
        self.btn_modify = QPushButton('Modifier')
        self.btn_modify.clicked.connect(self.modify_reservation)
        layout.addWidget(self.btn_modify)
        
        self.btn_cancel = QPushButton('Annuler réservation')
        self.btn_cancel.clicked.connect(self.cancel_reservation)
        layout.addWidget(self.btn_cancel)

        self.setLayout(layout)
        self.load_users_terrains()
        
        # Connexions simples
        self.btn_filter.clicked.connect(self.load_reservations)
        self.btn_reset.clicked.connect(self.reset_filters)
        self.show_all_cb.stateChanged.connect(self.on_show_all_changed)
        self.reservations_list.itemSelectionChanged.connect(self.on_select)
        
        self.load_reservations()

    def load_users_terrains(self):
        self.user_cb.clear()
        users = self.user_ctrl.list_users()
        for u in users:
            self.user_cb.addItem(f"{u.username}", u.id)
        self.user_cb.setCurrentIndex(-1)
        
        self.terrain_cb.clear()
        terrains = self.terrain_ctrl.list_terrains()
        for t in terrains:
            if t.active:
                self.terrain_cb.addItem(f"{t.name}", t.id)
        self.terrain_cb.setCurrentIndex(-1)

    def on_show_all_changed(self):
        """Gère le changement d'état de la checkbox"""
        if self.show_all_cb.isChecked():
            self.show_all_cb.setText("Afficher toutes les réservations (Activé)")
        else:
            self.show_all_cb.setText("Afficher toutes les réservations")
        
        self.load_reservations()

    
    def reset_filters(self):
        """Réinitialise tous les filtres"""
        self.user_cb.setCurrentIndex(-1)
        self.terrain_cb.setCurrentIndex(-1)
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_to.setDate(QDate.currentDate().addDays(30))
        self.show_all_cb.setChecked(False)
        self.show_all_cb.setText("Afficher toutes les réservations")
        self.load_reservations()
    


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
            for i in range(self.reservations_list.count()):
                item = self.reservations_list.item(i)
                if item.text().startswith(f"{self.selected_id} -"):
                    self.reservations_list.setCurrentItem(item)
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
        items = self.reservations_list.selectedItems()
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
        self.reservations_list.clear()
        try:
            reservations = self.ctrl.get_reservations()
            user_id = self.user_cb.currentData()
            terrain_id = self.terrain_cb.currentData()
            show_all = self.show_all_cb.isChecked()
            search_text = self.user_cb.currentText().strip().lower() if self.user_cb.isEditable() else ''
            
            count_total = 0
            count_filtered = 0
            
            for r in reservations:
                count_total += 1
                # Toujours ignorer les réservations annulées
                if getattr(r, 'status', None) == 'cancelled':
                    continue
                
                user = getattr(r, 'user', None)
                user_str = user.username if user else str(r.user_id)
                
                # Logique de filtrage corrigée avec dates
                should_show = False
                
                if show_all:
                    # Si "Afficher toutes" est coché, montrer toutes les réservations
                    should_show = True
                else:
                    # Sinon, appliquer les filtres
                    should_show = True
                    
                    # Filtrage par recherche utilisateur
                    if search_text and search_text not in user_str.lower():
                        should_show = False
                        
                    # Filtrage par utilisateur sélectionné
                    if should_show and user_id and r.user_id != user_id:
                        should_show = False
                        
                    # Filtrage par terrain sélectionné
                    if should_show and terrain_id and r.terrain_id != terrain_id:
                        should_show = False
                    
                    # 🆕 Filtrage par dates
                    if should_show:
                        date_from = self.date_from.date().toPython()
                        date_to = self.date_to.date().toPython()
                        reservation_date = r.start.date()
                        
                        if reservation_date < date_from or reservation_date > date_to:
                            should_show = False
                
                # Ajouter la réservation seulement si elle doit être affichée
                if should_show:
                    start = r.start.strftime('%Y-%m-%d %H:%M')
                    end = r.end.strftime('%H:%M')
                    terrain = getattr(r, 'terrain', None)
                    terrain_str = terrain.name if terrain else str(r.terrain_id)
                    self.reservations_list.addItem(f'{r.id} - {user_str} - {terrain_str} - {start} à {end}')
                    count_filtered += 1
            
            # Debug : afficher les stats dans la console
            mode = "TOUTES" if show_all else "FILTRÉES"
            date_from = self.date_from.date().toPython()
            date_to = self.date_to.date().toPython()
            print(f"📊 {count_filtered}/{count_total} réservations {mode} affichées")
            print(f"   🔸 User: {user_id if user_id else 'Tous'} | Terrain: {terrain_id if terrain_id else 'Tous'}")
            print(f"   📅 Période: {date_from.strftime('%d/%m/%Y')} → {date_to.strftime('%d/%m/%Y')}")
                
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', f'Impossible de charger les réservations: {e}')
            print(f"❌ Erreur de chargement: {e}")
