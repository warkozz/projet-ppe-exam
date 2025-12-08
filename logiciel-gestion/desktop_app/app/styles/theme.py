# theme.py - Thème moderne pour l'application Football Manager
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor

class FootballTheme:
    """Thème moderne pour l'application de gestion de football"""
    
    # Couleurs principales
    PRIMARY = "#1B5E20"      # Vert football foncé
    PRIMARY_LIGHT = "#4CAF50" # Vert football clair
    PRIMARY_DARK = "#0D3B0F"  # Vert très foncé
    
    # Couleurs secondaires
    SECONDARY = "#FFC107"     # Jaune/orange (couleur arbitre)
    ACCENT = "#FF5722"        # Rouge (cartons, alertes)
    
    # Couleurs neutres (fond gris très clair, doux pour les yeux)
    SURFACE = "#f8f9fa"       # Gris très clair pour les surfaces
    BACKGROUND = "#f5f6fa"    # Gris très clair légèrement teinté pour le fond
    CARD = "#ffffff"          # Blanc pour les cartes (contraste avec le fond)
    
    # Couleurs de texte
    TEXT_PRIMARY = "#1b5e20"  # Vert foncé principal
    TEXT_SECONDARY = "#2e7d32" # Vert moyen pour texte secondaire
    TEXT_HINT = "#757575"     # Gris foncé pour hints (meilleur contraste)
    
    # États
    SUCCESS = "#4CAF50"       # Vert pour succès
    WARNING = "#FF9800"       # Orange pour avertissements
    ERROR = "#F44336"         # Rouge pour erreurs
    INFO = "#2196F3"          # Bleu pour informations
    
    # Gradients
    FIELD_GRADIENT = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #66BB6A, stop:1 #4CAF50)"
    
    @classmethod
    def get_main_stylesheet(cls) -> str:
        """Retourne le stylesheet principal de l'application"""
        return f"""
        /* =============================================================================
           FOOTBALL MANAGER - THEME PRINCIPAL
        ============================================================================= */
        
        QMainWindow {{
            background: {cls.BACKGROUND};
            color: {cls.TEXT_PRIMARY};
        }}
        
        /* Widgets de base */
        QWidget {{
            background: {cls.BACKGROUND};
            color: {cls.TEXT_PRIMARY};
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            font-size: 14px;
        }}
        
        /* Conteneurs principaux */
        .main-container {{
            background: {cls.SURFACE};
            border-radius: 12px;
            padding: 24px;
            margin: 8px;
        }}
        
        .card {{
            background: {cls.CARD};
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 4px;
        }}
        
        .field-card {{
            background: {cls.FIELD_GRADIENT};
            border: 2px solid {cls.PRIMARY};
            border-radius: 12px;
            padding: 20px;
            color: {cls.TEXT_PRIMARY};
        }}
        
        /* Titres et headers */
        .app-title {{
            font-size: 28px;
            font-weight: bold;
            color: {cls.PRIMARY};
            margin: 0px 0px 24px 0px;
            text-align: center;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            color: {cls.PRIMARY_DARK};
            margin: 16px 0px 12px 0px;
            padding-bottom: 8px;
            border-bottom: 2px solid {cls.PRIMARY_LIGHT};
        }}
        
        .card-title {{
            font-size: 16px;
            font-weight: 600;
            color: {cls.TEXT_PRIMARY};
            margin-bottom: 12px;
        }}
        
        /* Boutons modernes */
        QPushButton {{
            background: {cls.PRIMARY};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 14px;
            min-height: 16px;
        }}
        
        QPushButton:hover {{
            background: {cls.PRIMARY_LIGHT};
        }}
        
        QPushButton:pressed {{
            background: {cls.PRIMARY_DARK};
        }}
        
        QPushButton:disabled {{
            background: #BDBDBD;
            color: #757575;
        }}
        
        .btn-secondary {{
            background: {cls.SECONDARY};
            color: {cls.TEXT_PRIMARY};
        }}
        
        .btn-secondary:hover {{
            background: #FFD54F;
        }}
        
        .btn-danger {{
            background: {cls.ERROR};
        }}
        
        .btn-danger:hover {{
            background: #E57373;
        }}
        
        .btn-success {{
            background: {cls.SUCCESS};
        }}
        
        .btn-success:hover {{
            background: #66BB6A;
        }}
        
        /* Champs de saisie modernes */
        QLineEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox {{
            background: {cls.CARD};
            border: 2px solid #E0E0E0;
            border-radius: 6px;
            padding: 12px 16px;
            font-size: 14px;
            color: {cls.TEXT_PRIMARY};
            selection-background-color: {cls.PRIMARY_LIGHT};
        }}
        
        QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus, QSpinBox:focus {{
            border: 2px solid {cls.PRIMARY};
            background: #F8FFF8;
        }}
        
        QLineEdit:hover, QComboBox:hover, QDateEdit:hover, QTimeEdit:hover, QSpinBox:hover {{
            border: 2px solid {cls.PRIMARY_LIGHT};
        }}
        
        QComboBox::drop-down {{
            border: none;
            background: {cls.PRIMARY_LIGHT};
            border-radius: 4px;
            margin: 2px;
        }}
        
        QComboBox::down-arrow {{
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiPgo8cGF0aCBkPSJNMSAxTDYgNkwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            width: 12px;
            height: 8px;
        }}
        
        /* Zone de texte */
        QTextEdit {{
            background: {cls.CARD};
            border: 2px solid #E0E0E0;
            border-radius: 6px;
            padding: 12px;
            font-size: 14px;
            color: {cls.TEXT_PRIMARY};
            selection-background-color: {cls.PRIMARY_LIGHT};
        }}
        
        QTextEdit:focus {{
            border: 2px solid {cls.PRIMARY};
            background: #F8FFF8;
        }}
        
        /* Listes modernes */
        QListWidget {{
            background: {cls.CARD};
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            padding: 4px;
            outline: none;
        }}
        
        QListWidget::item {{
            background: transparent;
            border: none;
            border-radius: 4px;
            padding: 12px 16px;
            margin: 2px 0px;
            color: {cls.TEXT_PRIMARY};
        }}
        
        QListWidget::item:selected {{
            background: {cls.PRIMARY};
            color: white;
        }}
        
        QListWidget::item:hover {{
            background: {cls.PRIMARY_LIGHT};
            color: white;
        }}
        
        /* Tableaux */
        QTableWidget {{
            background: {cls.CARD};
            border: 1px solid #E0E0E0;
            border-radius: 6px;
            gridline-color: #F0F0F0;
            selection-background-color: {cls.PRIMARY_LIGHT};
        }}
        
        QTableWidget::item {{
            padding: 12px 8px;
            border: none;
        }}
        
        QHeaderView::section {{
            background: {cls.PRIMARY};
            color: white;
            font-weight: 600;
            padding: 12px 8px;
            border: none;
            border-right: 1px solid {cls.PRIMARY_DARK};
        }}
        
        QHeaderView::section:first {{
            border-top-left-radius: 6px;
        }}
        
        QHeaderView::section:last {{
            border-top-right-radius: 6px;
            border-right: none;
        }}
        
        /* Checkbox avec style football */
        QCheckBox {{
            spacing: 8px;
            color: {cls.TEXT_PRIMARY};
            font-size: 14px;
        }}
        
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border: 2px solid {cls.PRIMARY};
            border-radius: 4px;
            background: {cls.CARD};
        }}
        
        QCheckBox::indicator:checked {{
            background: {cls.PRIMARY};
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiPgo8cGF0aCBkPSJNMSA0LjVMNCA3LjVMMTEgMSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPHN2Zz4K);
        }}
        
        QCheckBox::indicator:hover {{
            border: 2px solid {cls.PRIMARY_LIGHT};
            background: #F8FFF8;
        }}
        
        /* Radio buttons */
        QRadioButton {{
            spacing: 8px;
            color: {cls.TEXT_PRIMARY};
            font-size: 14px;
        }}
        
        QRadioButton::indicator {{
            width: 20px;
            height: 20px;
            border: 2px solid {cls.PRIMARY};
            border-radius: 10px;
            background: {cls.CARD};
        }}
        
        QRadioButton::indicator:checked {{
            background: {cls.PRIMARY};
            border: 6px solid {cls.CARD};
            background-clip: content-box;
        }}
        
        /* Labels */
        QLabel {{
            color: {cls.TEXT_PRIMARY};
            font-size: 14px;
        }}
        
        .label-secondary {{
            color: {cls.TEXT_SECONDARY};
            font-size: 12px;
        }}
        
        .label-hint {{
            color: {cls.TEXT_HINT};
            font-size: 12px;
            font-style: italic;
        }}
        
        /* Status badges */
        .status-active {{
            background: {cls.SUCCESS};
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 12px;
        }}
        
        .status-inactive {{
            background: {cls.ERROR};
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 12px;
        }}
        
        .status-pending {{
            background: {cls.WARNING};
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 12px;
        }}
        
        /* Scrollbars */
        QScrollBar:vertical {{
            background: #F0F0F0;
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background: {cls.PRIMARY_LIGHT};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {cls.PRIMARY};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* Pas d'animations CSS car non supportées par Qt */
        """