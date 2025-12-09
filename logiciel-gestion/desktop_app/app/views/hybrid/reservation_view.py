# reservation_view.py - Vue hybride réservations - garde les fonctionnalités qui marchent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QListWidget, 
    QComboBox, QDateEdit, QLabel, QMessageBox, QTextEdit, QCheckBox, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import QDate, Qt
from app.controllers.reservation_controller import ReservationController
from app.controllers.terrain_controller import TerrainController
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
from app.styles.theme import FootballTheme
from datetime import datetime

class HybridReservationView(QWidget):
    """Vue hybride des réservations - reprend les fonctionnalités qui marchent avec un design moderne"""
    
    def __init__(self, parent=None, notifications_service=None):
        super().__init__(parent)
        self.ctrl = ReservationController()
        self.user_ctrl = UserController() 
        self.terrain_ctrl = TerrainController()
        self.selected_id = None
        self.notifications_service = notifications_service  # Service pour notifier les autres vues
        
        self.setWindowTitle('Gestion des Réservations - Version Hybride')
        self.setMinimumSize(1000, 700)
        
        # Style simple et clean
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
            QLineEdit, QTextEdit, QComboBox, QDateEdit {{
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
        
        # Titre principal avec marges correctes
        title = QLabel('🏆 Gestion des Réservations')
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

        # Filtres
        layout.addWidget(QLabel('🔍 Filtres de recherche'))
        filter_layout = QGridLayout()
        
        # Filtres sur une grille simple
        filter_layout.addWidget(QLabel('👤 Utilisateur:'), 1, 0)
        self.user_cb = QComboBox()
        self.user_cb.setEditable(True)
        filter_layout.addWidget(self.user_cb, 1, 1)
        
        filter_layout.addWidget(QLabel('🏟️ Terrain:'), 1, 2)
        self.terrain_cb = QComboBox()
        filter_layout.addWidget(self.terrain_cb, 1, 3)
        
        filter_layout.addWidget(QLabel('📅 Du:'), 2, 0)
        self.date_from = QDateEdit(QDate.currentDate())
        self.date_from.setDisplayFormat('dd/MM/yyyy')
        self.date_from.setButtonSymbols(QDateEdit.NoButtons)
        self.date_from.setStyleSheet("""
            QDateEdit {
                background: white;
                border: 2px solid #c8e6c9;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: #1b5e20;
            }
            QDateEdit:focus {
                border: 2px solid #4caf50;
                background: #f8fff8;
            }
        """)
        filter_layout.addWidget(self.date_from, 2, 1)
        
        filter_layout.addWidget(QLabel('📅 Au:'), 2, 2)
        self.date_to = QDateEdit(QDate.currentDate())
        self.date_to.setDisplayFormat('dd/MM/yyyy')
        self.date_to.setButtonSymbols(QDateEdit.NoButtons)
        self.date_to.setStyleSheet("""
            QDateEdit {
                background: white;
                border: 2px solid #c8e6c9;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: #1b5e20;
            }
            QDateEdit:focus {
                border: 2px solid #4caf50;
                background: #f8fff8;
            }
        """)
        filter_layout.addWidget(self.date_to, 2, 3)
        
        # Bouton toggle pour afficher toutes les réservations
        self.show_all_cb = HoverButton('📊 Mes réservations', '🔄')
        self.show_all_cb.setCheckable(True)
        self.show_all_cb.setChecked(False)
        self._update_show_all_button_text()
        filter_layout.addWidget(self.show_all_cb, 3, 0, 1, 2)
        
        # Boutons avec style vert standard
        self.btn_filter = HoverButton('Filtrer', '🔍')
        self.btn_reset = HoverButton('Reset', '🔄')
        filter_layout.addWidget(self.btn_filter, 3, 2)
        filter_layout.addWidget(self.btn_reset, 3, 3)
        
        layout.addLayout(filter_layout)

        # Liste des réservations
        layout.addWidget(QLabel('📋 Liste des réservations'))
        self.reservations_list = QListWidget()
        layout.addWidget(self.reservations_list)

        # Formulaire
        layout.addWidget(QLabel('➕ Formulaire de réservation'))
        form_layout = QGridLayout()
        
        # Champs du formulaire
        form_layout.addWidget(QLabel('👤 Client:'), 1, 0)
        self.form_user_cb = QComboBox()
        self.form_user_cb.setEditable(True)
        form_layout.addWidget(self.form_user_cb, 1, 1)
        
        form_layout.addWidget(QLabel('🏟️ Terrain:'), 1, 2)
        self.terrain_form_cb = QComboBox()
        form_layout.addWidget(self.terrain_form_cb, 1, 3)
        
        form_layout.addWidget(QLabel('📅 Date:'), 2, 0)
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setDisplayFormat('dd/MM/yyyy')
        self.date_edit.setButtonSymbols(QDateEdit.NoButtons)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                background: white;
                border: 2px solid #c8e6c9;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: #1b5e20;
            }
            QDateEdit:focus {
                border: 2px solid #4caf50;
                background: #f8fff8;
            }
        """)
        form_layout.addWidget(self.date_edit, 2, 1)
        
        form_layout.addWidget(QLabel('⏰ Créneau:'), 2, 2)
        self.slot_cb = QComboBox()
        self._populate_slots()
        form_layout.addWidget(self.slot_cb, 2, 3)
        
        form_layout.addWidget(QLabel('📝 Notes:'), 3, 0)
        self.notes = QTextEdit()
        self.notes.setMaximumHeight(60)
        form_layout.addWidget(self.notes, 3, 1, 1, 3)
        
        layout.addLayout(form_layout)

        # Boutons
        buttons_layout = QHBoxLayout()
        
        # Bouton retour avec style cohérent
        self.btn_back = HoverButton('Retour au Dashboard', '🔙')
        self.btn_back.setMinimumHeight(40)
        buttons_layout.addWidget(self.btn_back)
        
        buttons_layout.addStretch()
        
        # Tous les boutons avec taille uniforme
        self.btn_add = HoverButton('Ajouter', '➕')
        self.btn_add.setToolTip('Ajouter une réservation')
        self.btn_add.setMinimumHeight(40)
        buttons_layout.addWidget(self.btn_add)
        
        self.btn_modify = HoverButton('Modifier', '✏️')
        self.btn_modify.setToolTip('Modifier la réservation sélectionnée')
        self.btn_modify.setMinimumHeight(40)
        buttons_layout.addWidget(self.btn_modify)
        
        self.btn_cancel = HoverButton('Annuler', '❌')
        self.btn_cancel.setToolTip('Annuler la réservation sélectionnée')
        self.btn_cancel.setMinimumHeight(40)
        buttons_layout.addWidget(self.btn_cancel)
        
        self.btn_clear = HoverButton('Nettoyer', '🧹')
        self.btn_clear.setToolTip('Nettoyer le formulaire')
        self.btn_clear.setMinimumHeight(40)
        buttons_layout.addWidget(self.btn_clear)
        
        layout.addLayout(buttons_layout)
        
        # Ajout d'un espacement final
        layout.addStretch()
        
        # CONNECTER LES ÉVÉNEMENTS - REPRENDRE L'ANCIEN
        self._connect_events()
        self._load_initial_data()
        
    def _populate_slots(self):
        """REPRIS DE L'ANCIEN - FONCTIONNE"""
        self.slot_cb.clear()
        slots = [
            (8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20)
        ]
        for s in slots:
            label = f"{s[0]:02d}h - {s[1]:02d}h"
            self.slot_cb.addItem(label, s)
            
    def _connect_events(self):
        """Connexions des événements"""
        # Événements de filtrage
        self.btn_filter.clicked.connect(self.load_reservations)
        self.btn_reset.clicked.connect(self.reset_filters)
        self.show_all_cb.clicked.connect(self._on_show_all_toggled)
        
        # Événements du formulaire
        self.btn_add.clicked.connect(self.add_reservation)
        self.btn_modify.clicked.connect(self.modify_reservation)
        self.btn_cancel.clicked.connect(self.cancel_reservation)
        self.btn_clear.clicked.connect(self.clear_form)
        
        # Sélection dans la liste
        self.reservations_list.itemClicked.connect(self.on_selection_changed)
    
    def _update_show_all_button_text(self):
        """Met à jour le texte du bouton selon son état"""
        if self.show_all_cb.isChecked():
            self.show_all_cb.setText('🌍 Toutes les réservations')
        else:
            self.show_all_cb.setText('📊 Mes réservations')
            
    def _on_show_all_toggled(self):
        """Gère le changement d'état du bouton"""
        self._update_show_all_button_text()
        self.load_reservations()

    def clear_form(self):
        """Nettoie le formulaire"""
        self.form_user_cb.setCurrentIndex(-1)
        self.terrain_form_cb.setCurrentIndex(-1)
        self.date_edit.setDate(QDate.currentDate())
        self.slot_cb.setCurrentIndex(-1)
        self.notes.clear()
        self.selected_id = None
        self.show_all_cb.setChecked(False)
        self._update_show_all_button_text()
        
    def _load_initial_data(self):
        """Charge les données initiales - REPRIS DE L'ANCIEN"""
        try:
            # Charger les utilisateurs pour les filtres et formulaire
            self.user_cb.clear()
            self.user_cb.addItem("Tous", None)
            self.form_user_cb.clear()
            users = self.user_ctrl.list_users()
            for user in users:
                self.user_cb.addItem(user.username, user.id)
                self.form_user_cb.addItem(user.username, user.id)
                
            # Charger les terrains pour filtre et formulaire
            terrains = self.terrain_ctrl.list_terrains()
            
            # Filtre terrain
            self.terrain_cb.clear()
            self.terrain_cb.addItem("Tous", None)
            
            # Formulaire terrain
            self.terrain_form_cb.clear()
            
            for terrain in terrains:
                if terrain.active:
                    self.terrain_cb.addItem(f"{terrain.id} - {terrain.name}", terrain.id)
                    self.terrain_form_cb.addItem(f"{terrain.id} - {terrain.name}", terrain.id)
                    
            # Charger les réservations
            self.load_reservations()
            
            print("✅ Données initiales chargées avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement initial: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur de chargement: {str(e)}")
    
    # MÉTHODES FONCTIONNELLES REPRISES DE L'ANCIEN SYSTÈME
    def load_reservations(self):
        """REPRISE EXACTE DE L'ANCIEN - FONCTIONNE"""
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
                
                # Logique de filtrage
                should_show = False
                
                if show_all:
                    should_show = True
                else:
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
                    
                    # Filtrage par dates
                    if should_show:
                        date_from = self.date_from.date().toPython()
                        date_to = self.date_to.date().toPython()
                        reservation_date = r.start.date()
                        
                        if reservation_date < date_from or reservation_date > date_to:
                            should_show = False
                
                # Ajouter la réservation si elle doit être affichée
                if should_show:
                    start = r.start.strftime('%Y-%m-%d %H:%M')
                    end = r.end.strftime('%H:%M')
                    terrain = getattr(r, 'terrain', None)
                    terrain_str = terrain.name if terrain else str(r.terrain_id)
                    self.reservations_list.addItem(f'{r.id} - {user_str} - {terrain_str} - {start} à {end}')
                    count_filtered += 1
            
            # Affichage stats
            mode = "TOUTES" if show_all else "FILTRÉES"
            print(f"📊 {count_filtered}/{count_total} réservations {mode} affichées")
                
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', f'Impossible de charger les réservations: {e}')
            print(f"❌ Erreur de chargement: {e}")
        
    def reset_filters(self):
        """Reset des filtres"""
        self.user_cb.setCurrentIndex(0)
        self.terrain_cb.setCurrentIndex(0)
        self.show_all_cb.setChecked(False)
        self.date_from.setDate(QDate.currentDate())
        self.date_to.setDate(QDate.currentDate())
        self.load_reservations()
        
    def update_terrains_avail(self):
        """Mise à jour des terrains disponibles - REPRIS DE L'ANCIEN"""
        try:
            date = self.date_edit.date().toPython()
            slot = self.slot_cb.currentData()
            self.terrain_form_cb.clear()
            
            if not slot:
                return
                
            start = datetime(date.year, date.month, date.day, slot[0], 0, 0)
            end = datetime(date.year, date.month, date.day, slot[1], 0, 0)
            
            # Version simplifiée sans cpp_bridge qui peut poser problème
            for t in self.terrain_ctrl.list_terrains():
                if not t.active:
                    continue
                    
                label = f'{t.id} - {t.name}'
                self.terrain_form_cb.addItem(label, t.id)
                
                # TODO: Ajouter vérification de conflit si besoin
                
        except Exception as e:
            print(f"Erreur mise à jour terrains: {e}")
    
    def add_reservation(self):
        """Ajout de réservation - REPRIS DE L'ANCIEN"""
        try:
            user_id = self.form_user_cb.currentData() if self.form_user_cb.currentData() else None
            if not user_id:
                QMessageBox.warning(self, 'Erreur', 'Sélectionnez un utilisateur')
                return
            terrain_id = self.terrain_form_cb.currentData()
            date = self.date_edit.date().toPython()
            slot = self.slot_cb.currentData()
            notes = self.notes.toPlainText().strip()
            
            if not terrain_id or not slot:
                QMessageBox.warning(self, 'Erreur', 'Sélectionnez un terrain et un créneau')
                return
                
            start = datetime(date.year, date.month, date.day, slot[0], 0, 0)
            end = datetime(date.year, date.month, date.day, slot[1], 0, 0)
            
            try:
                result = self.ctrl.create_reservation(user_id, terrain_id, start, end, notes)
                if result:
                    QMessageBox.information(self, 'Succès', 'Réservation créée avec succès')
                    self.load_reservations()
                    self.update_terrains_avail()
                    
                    # Notifier les autres vues (comme le calendrier)
                    if self.notifications_service:
                        self.notifications_service.notify_reservation_change()
                else:
                    QMessageBox.warning(self, 'Erreur', 'La création a échoué')
            except Exception as e:
                QMessageBox.critical(self, 'Erreur', f'Erreur lors de la création: {str(e)}')
            
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', str(e))
        
    def modify_reservation(self):
        """Modification de réservation - REPRIS DE L'ANCIEN"""
        if not self.selected_id:
            QMessageBox.warning(self, 'Erreur', 'Sélectionnez une réservation')
            return
            
        try:
            user_id = self.form_user_cb.currentData() if self.form_user_cb.currentData() else None
            if not user_id:
                QMessageBox.warning(self, 'Erreur', 'Sélectionnez un utilisateur')
                return
            terrain_id = self.terrain_form_cb.currentData()
            date = self.date_edit.date().toPython()
            slot = self.slot_cb.currentData()
            notes = self.notes.toPlainText().strip()
            
            if not terrain_id or not slot:
                QMessageBox.warning(self, 'Erreur', 'Sélectionnez un terrain et un créneau')
                return
                
            start = datetime(date.year, date.month, date.day, slot[0], 0, 0)
            end = datetime(date.year, date.month, date.day, slot[1], 0, 0)
            
            try:
                success = self.ctrl.modify_reservation(self.selected_id, user_id, terrain_id, start, end, notes)
                if success:
                    QMessageBox.information(self, 'Succès', 'Réservation modifiée avec succès')
                    self.load_reservations()
                    
                    # Notifier les autres vues (comme le calendrier)
                    if self.notifications_service:
                        self.notifications_service.notify_reservation_change()
                else:
                    QMessageBox.warning(self, 'Erreur', 'La modification a échoué')
            except Exception as e:
                QMessageBox.critical(self, 'Erreur', f'Erreur lors de la modification: {str(e)}')
            
            # Resélectionner l'élément modifié
            for i in range(self.reservations_list.count()):
                item = self.reservations_list.item(i)
                if item.text().startswith(f"{self.selected_id} -"):
                    self.reservations_list.setCurrentItem(item)
                    break
                    
        except Exception as e:
            QMessageBox.warning(self, 'Erreur', str(e))
        
    def cancel_reservation(self):
        """Annulation de réservation - REPRIS DE L'ANCIEN"""
        if not self.selected_id:
            QMessageBox.warning(self, 'Erreur', 'Sélectionnez une réservation')
            return
            
        reply = QMessageBox.question(
            self, 'Confirmation',
            'Êtes-vous sûr de vouloir annuler cette réservation ?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                try:
                    success = self.ctrl.cancel_reservation(self.selected_id)
                    if success:
                        QMessageBox.information(self, 'Succès', 'Réservation annulée')
                        self.load_reservations()
                        self.update_terrains_avail()
                        
                        # Notifier les autres vues (comme le calendrier)
                        if self.notifications_service:
                            self.notifications_service.notify_reservation_change()
                    else:
                        QMessageBox.warning(self, 'Erreur', 'L\'annulation a échoué')
                except Exception as e:
                    QMessageBox.critical(self, 'Erreur', f'Erreur lors de l\'annulation: {str(e)}')
            except Exception as e:
                QMessageBox.warning(self, 'Erreur', str(e))
    
    def on_selection_changed(self):
        """Gestion de la sélection - REPRIS DE L'ANCIEN"""
        items = self.reservations_list.selectedItems()
        if not items:
            self.selected_id = None
            self.user_cb.setCurrentIndex(0)
            self.terrain_form_cb.setCurrentIndex(0)
            self.date_edit.setDate(QDate.currentDate())
            self.slot_cb.setCurrentIndex(0)
            self.notes.clear()
            return
            
        txt = items[0].text()
        parts = txt.split(' - ')
        if len(parts) < 4:
            self.selected_id = None
            return
            
        rid = parts[0]
        self.selected_id = int(rid)
        
        # Recherche la réservation dans la base
        try:
            reservations = self.ctrl.get_reservations()
            for r in reservations:
                if r.id == self.selected_id:
                    # Utilisateur
                    idx_user = self.user_cb.findData(r.user_id)
                    if idx_user >= 0:
                        self.user_cb.setCurrentIndex(idx_user)
                        
                    # Terrain
                    idx_terrain = self.terrain_form_cb.findData(r.terrain_id)
                    if idx_terrain >= 0:
                        self.terrain_form_cb.setCurrentIndex(idx_terrain)
                        
                    # Date
                    self.date_edit.setDate(QDate(r.start.year, r.start.month, r.start.day))
                    
                    # Slot
                    slot_tuple = (r.start.hour, r.end.hour)
                    idx_slot = self.slot_cb.findData(slot_tuple)
                    if idx_slot >= 0:
                        self.slot_cb.setCurrentIndex(idx_slot)
                        
                    # Notes
                    self.notes.setPlainText(r.notes or '')
                    break
                    
        except Exception as e:
            print(f"Erreur lors de la sélection: {e}")