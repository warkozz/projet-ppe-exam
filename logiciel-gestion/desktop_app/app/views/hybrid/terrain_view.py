# terrain_view.py - Vue hybride de gestion des terrains
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QListWidget, 
    QComboBox, QLineEdit, QLabel, QMessageBox, QTextEdit, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from app.controllers.terrain_controller import TerrainController
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

class HybridTerrainView(QWidget):
    """Vue hybride de gestion des terrains"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ctrl = TerrainController()
        self.selected_id = None
        
        self.setWindowTitle('Gestion des Terrains - Version Hybride')
        self.setMinimumSize(900, 600)
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
            QLineEdit, QTextEdit, QComboBox {{
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
        """)
        
        self._build()
        
    def _build(self):
        """Construction de l'interface"""
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel('🏐️ Gestion des Terrains')
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
        
        # Liste des terrains
        layout.addWidget(QLabel('📋 Liste des terrains'))
        self.terrains_list = QListWidget()
        layout.addWidget(self.terrains_list)
        
        # Formulaire
        layout.addWidget(QLabel('➕ Formulaire terrain'))
        form_layout = QGridLayout()
        
        form_layout.addWidget(QLabel('🏟️ Nom:'), 0, 0)
        self.name_edit = QLineEdit()
        form_layout.addWidget(self.name_edit, 0, 1)
        
        # Bouton toggle pour actif/inactif
        self.active_cb = HoverButton('✅ Terrain actif', '🏟️')
        self.active_cb.setCheckable(True)
        self.active_cb.setChecked(True)
        self._update_active_button_text()
        form_layout.addWidget(self.active_cb, 0, 2, 1, 2)
        
        form_layout.addWidget(QLabel('📝 Description:'), 1, 0)
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        form_layout.addWidget(self.description_edit, 1, 1, 1, 3)
        
        layout.addLayout(form_layout)
        
        # Boutons
        buttons_layout = QHBoxLayout()
        self.btn_back = HoverButton('Retour au Dashboard', '🔙')
        buttons_layout.addWidget(self.btn_back)
        buttons_layout.addStretch()
        
        self.btn_add = HoverButton('Ajouter', '➕')
        self.btn_modify = HoverButton('Modifier', '✏️')
        self.btn_delete = HoverButton('Supprimer', '🗑️')
        self.btn_clear = HoverButton('Nettoyer', '🧹')
        
        buttons_layout.addWidget(self.btn_add)
        buttons_layout.addWidget(self.btn_modify)
        buttons_layout.addWidget(self.btn_delete)
        buttons_layout.addWidget(self.btn_clear)
        
        layout.addLayout(buttons_layout)
        
        # Connecter les événements
        self._connect_events()
        self._load_data()
        
    def _connect_events(self):
        """Connexion des événements"""
        self.btn_add.clicked.connect(self.add_terrain)
        self.btn_modify.clicked.connect(self.modify_terrain)
        self.btn_delete.clicked.connect(self.delete_terrain)
        self.btn_clear.clicked.connect(self.clear_form)
        self.terrains_list.itemClicked.connect(self.on_selection_changed)
        self.active_cb.clicked.connect(self._on_active_toggled)
        
    def _load_data(self):
        """Charge la liste des terrains"""
        try:
            terrains = self.ctrl.list_terrains()
            self.terrains_list.clear()
            for terrain in terrains:
                item_text = f"🏟️ {terrain.name}"
                if hasattr(terrain, 'location') and terrain.location:
                    item_text += f" - {terrain.location}"
                item_text += f" ({'✅' if terrain.active else '❌'})"
                
                # Créer l'item et stocker l'ID du terrain
                from PySide6.QtWidgets import QListWidgetItem
                item = QListWidgetItem(item_text)
                item.setData(256, terrain.id)  # Stocker l'ID pour la sélection
                self.terrains_list.addItem(item)
                
            print(f"✅ {len(terrains)} terrains chargés")
        except Exception as e:
            print(f"❌ Erreur chargement terrains: {e}")
            
    def on_selection_changed(self, item):
        """Gestion de la sélection - charge les données du terrain dans le formulaire"""
        try:
            # Récupérer l'ID du terrain stocké dans l'item
            terrain_id = item.data(256)  # Data role utilisé pour stocker l'ID
            if terrain_id:
                # Récupérer le terrain via le contrôleur
                terrain = self.ctrl.get_terrain_by_id(terrain_id)
                if terrain:
                    # Charger les données dans le formulaire
                    self.name_edit.setText(terrain.name)
                    self.description_edit.setPlainText(terrain.location or "")
                    # Définir le statut actif
                    self.active_cb.setChecked(terrain.active)
                    self._update_active_button_text()
                    # Sauvegarder l'ID pour les opérations de modification/suppression
                    self.selected_id = terrain_id
                    print(f"✅ Terrain '{terrain.name}' sélectionné et chargé dans le formulaire")
        except Exception as e:
            print(f"❌ Erreur lors de la sélection du terrain: {e}")
            QMessageBox.warning(self, 'Erreur', f'Erreur lors du chargement: {e}')
    
    def _update_active_button_text(self):
        """Met à jour le texte du bouton selon son état"""
        if self.active_cb.isChecked():
            self.active_cb.setText('✅ Terrain actif')
        else:
            self.active_cb.setText('❌ Terrain inactif')
            
    def _on_active_toggled(self):
        """Gère le changement d'état du bouton"""
        self._update_active_button_text()
            
    def add_terrain(self):
        """Ajouter un nouveau terrain"""
        try:
            name = self.name_edit.text().strip()
            description = self.description_edit.toPlainText().strip()
            active = self.active_cb.isChecked()
            
            if not name:
                QMessageBox.warning(self, "Erreur", "Le nom du terrain est obligatoire")
                return
                
            result = self.ctrl.create(name, description or None, active)
            if result:
                QMessageBox.information(self, "Succès", f"Terrain '{name}' ajouté avec succès")
                self._load_data()
                self.clear_form()
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la création du terrain")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {e}")
            
    def modify_terrain(self):
        """Modifier le terrain sélectionné"""
        if not self.selected_id:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un terrain")
            return
            
        try:
            name = self.name_edit.text().strip()
            description = self.description_edit.toPlainText().strip()
            active = self.active_cb.isChecked()
            
            if not name:
                QMessageBox.warning(self, "Erreur", "Le nom du terrain est obligatoire")
                return
                
            result = self.ctrl.update(self.selected_id, name=name, location=description or None, active=active)
            if result:
                QMessageBox.information(self, "Succès", "Terrain modifié avec succès")
                self._load_data()
                self.clear_form()
            else:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la modification")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {e}")
            
    def delete_terrain(self):
        """Supprimer le terrain sélectionné"""
        if not self.selected_id:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un terrain")
            return
            
        reply = QMessageBox.question(
            self, "Confirmation", 
            "Êtes-vous sûr de vouloir supprimer ce terrain ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                result = self.ctrl.delete(self.selected_id)
                if result:
                    QMessageBox.information(self, "Succès", "Terrain supprimé avec succès")
                    self._load_data()
                    self.clear_form()
                else:
                    QMessageBox.warning(self, "Erreur", "Erreur lors de la suppression")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur: {e}")
                
    def clear_form(self):
        """Nettoie le formulaire"""
        self.name_edit.clear()
        self.description_edit.clear()
        self.active_cb.setChecked(True)
        self._update_active_button_text()
        self.selected_id = None