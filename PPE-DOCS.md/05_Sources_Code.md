# Code Source — Liens GitHub
## Projet PPE Foot5 — BTS SIO SLAM

**Étudiant :** Hakim Rayane  
**Date :** Mars 2026

---

## Liens vers les Dépôts

### Application Légère — Web Client
**URL :** https://github.com/warkozz/projet-ppe-foot5-web  
**Branche principale :** `develop`  
**Langage dominant :** TypeScript (77%) + Python (20%)

### Application Lourde — Admin Desktop
**URL :** https://github.com/warkozz/projet-ppe-exam  
**Branche principale :** `main`  
**Langage dominant :** Python 100%

---

## Structure des Dépôts

### Appli Légère (`projet-ppe-foot5-web`)

```
projet-ppe-foot5-web/
│
├── backend/                         # API FastAPI (Python)
│   ├── main.py                      # Point d'entrée
│   ├── app/
│   │   ├── models/                  # Modèles SQLAlchemy
│   │   │   ├── user.py
│   │   │   ├── terrain.py
│   │   │   └── reservation.py
│   │   ├── routes/                  # Endpoints REST
│   │   │   ├── auth.py
│   │   │   ├── terrains.py
│   │   │   └── reservations.py
│   │   ├── schemas/                 # Validation Pydantic
│   │   ├── services/                # Logique métier
│   │   └── utils/                   # JWT, hashing, config
│   ├── test_api.py                  # Tests fonctionnels API
│   ├── test_logic.py                # Tests logique métier
│   └── requirements.txt
│
├── frontend/                        # App React (TypeScript)
│   └── src/
│       ├── pages/                   # Pages de l'application
│       │   ├── Home.tsx
│       │   ├── Login.tsx
│       │   ├── Register.tsx
│       │   ├── Terrains.tsx
│       │   ├── Reservation.tsx
│       │   ├── MonEspace.tsx
│       │   └── Profile.tsx
│       ├── components/              # Composants réutilisables
│       ├── contexts/                # AuthContext
│       ├── services/                # api.ts (Axios)
│       └── types/                   # Interfaces TypeScript
│
└── docs/                            # Documentation projet
    ├── BACKEND_API.md               # Doc technique API complète
    ├── BACKEND_STATUS.md            # État des fonctionnalités
    └── PROJECT_HISTORY.md           # Historique du développement
```

### Appli Lourde (`projet-ppe-exam`)

```
projet-ppe-exam/
│
├── logiciel-gestion/
│   ├── database/                    # Scripts SQL
│   │   ├── schema_mysql.sql         # Schéma complet
│   │   ├── seed_data_mysql_fixed.sql# Données de test
│   │   └── verify_install.sql       # Script de vérification
│   │
│   ├── desktop_app/                 # Application Python/PySide6
│   │   ├── hybrid_main.py           # Point d'entrée
│   │   ├── requirements.txt
│   │   ├── app/
│   │   │   ├── config.py            # Configuration
│   │   │   ├── models/              # Modèles SQLAlchemy
│   │   │   │   ├── db.py
│   │   │   │   ├── user.py
│   │   │   │   ├── terrain.py
│   │   │   │   └── reservation.py
│   │   │   ├── controllers/         # Logique métier
│   │   │   │   ├── auth_controller.py
│   │   │   │   ├── user_controller.py
│   │   │   │   ├── terrain_controller.py
│   │   │   │   └── reservation_controller.py
│   │   │   ├── views/               # Interfaces PySide6
│   │   │   │   ├── login_view.py
│   │   │   │   └── hybrid/
│   │   │   │       ├── dashboard_view.py
│   │   │   │       ├── user_view.py
│   │   │   │       ├── terrain_view.py
│   │   │   │       ├── reservation_view.py
│   │   │   │       └── calendar_view.py
│   │   │   ├── services/            # Services (calendrier, etc.)
│   │   │   ├── styles/              # Thème Material Design
│   │   │   └── utils/               # hashing bcrypt
│   │   └── run.bat                  # Script de démarrage Windows
│   │
│   └── documentation/
│       ├── technical_documentation.md
│       └── user_manual.md
│
└── PPE-ANNEXES/                     # Documents PPE (étapes 1-10)
    ├── 01_Introduction_Projet.md
    ├── 02_Maquettes_UI.md
    ├── 03_Cahier_Charges.md
    ├── 04_Conception_BDD/
    ├── 05_Planification.md
    ├── 06_Developpement.md
    ├── 07_Tests.md
    ├── 08_Documentation.md
    ├── 09_Rendu_Final.md
    └── 10_Evaluation.md
```

---

## Métriques du Code

### Appli Lourde (Desktop)

| Métrique | Valeur |
|---|---|
| Lignes de code Python | ~9 000 lignes |
| Nombre de modules | 15+ |
| Nombre de classes | 25+ |
| Méthodes documentées | 100+ |
| Conformité PEP8 | ✅ |
| Type hints | 95% |
| Couverture de tests | 87% |

### Appli Légère (Web)

| Métrique | Valeur |
|---|---|
| Langage principal | TypeScript 77% |
| Backend Python | 20% |
| Endpoints API | 20+ |
| Tests API | pytest + requests |
| Documentation | Swagger auto-générée |

---

## Cloner et Tester

### Appli Légère
```bash
git clone https://github.com/warkozz/projet-ppe-foot5-web.git
cd projet-ppe-foot5-web/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# → Swagger : http://localhost:8000/docs

cd ../frontend
npm install ; npm start
# → App React : http://localhost:3000
```

### Appli Lourde
```bash
git clone https://github.com/warkozz/projet-ppe-exam.git
cd projet-ppe-exam/logiciel-gestion/desktop_app
pip install -r requirements.txt
python hybrid_main.py
```

---

## Informations Techniques Clés

| Élément | Valeur |
|---|---|
| Auteur | Hakim Rayane (warkozz) |
| Profil GitHub | https://github.com/warkozz |
| Formation | BTS SIO SLAM |
| Période de développement | Décembre 2025 – Mars 2026 |
| Base de données | MySQL `foot5` — XAMPP |
| Système d'exploitation | Windows |

---

*Hakim Rayane — BTS SIO SLAM — PPE Foot5 — Mars 2026*
