# Application Légère — Web Client
## Foot5 Extension Web — BTS SIO SLAM

**Étudiant :** Hakim Rayane  
**Date :** Mars 2026  
**Dépôt :** https://github.com/warkozz/projet-ppe-foot5-web

---

## 1. Présentation

L'application web Foot5 est l'**interface cliente** du système de gestion de terrains de football 5v5. Elle permet à n'importe quel joueur d'accéder à la plateforme depuis son navigateur, sans installation, et de réserver un créneau en quelques clics.

### Caractéristiques principales
- Interface **responsive** accessible depuis tout navigateur
- **Aucune installation** requise côté client
- Synchronisation en temps réel avec la base de données partagée
- Inscription en ligne autonome
- Calcul automatique du coût de la réservation

### Statut du projet
| Composant | Statut |
|---|---|
| Backend API (FastAPI) | Terminé ✅ |
| Frontend React | Terminé ✅ |
| Tests API | Terminés ✅ |
| Documentation | Complète ✅ |

---

## 2. Fonctionnalités

### 2.1 Authentification et Gestion du Profil

| Fonctionnalité | Description |
|---|---|
| **Inscription** | Création d'un compte avec username, email, mot de passe |
| **Connexion** | Authentification JWT, token valide 30 minutes |
| **Mon Profil** | Consultation et modification des informations personnelles |
| **Changer le mot de passe** | Modification sécurisée avec vérification de l'ancien mot de passe |
| **Renouveler le token** | Renouvellement automatique de session |

**Endpoints d'authentification :**
```
POST /api/auth/register    — Inscription
POST /api/auth/login       — Connexion
GET  /api/auth/me          — Profil utilisateur
PUT  /api/auth/me          — Modifier profil
PUT  /api/auth/me/password — Changer mot de passe
POST /api/auth/refresh     — Renouveler token
```

### 2.2 Réservation de Terrain

Le parcours de réservation se déroule en **3 étapes** :

**Étape 1 — Choisir un terrain**
- Liste des terrains actifs avec nom, localisation, tarif/h, format (5v5, 7v7…)
- Affichage du prix et de la capacité dynamiquement

**Étape 2 — Sélectionner un créneau**
- Vérification en temps réel des créneaux disponibles
- Affichage du planning complet du terrain pour le jour choisi
- Détection automatique des conflits

**Étape 3 — Confirmer**
- Affichage du coût total calculé automatiquement (durée × tarif horaire)
- Confirmation avec possibilité d'ajouter une note
- Création de la réservation avec statut `pending`

**Règle métier :** quota de **2 réservations maximum par semaine** (7 jours glissants, configurable)

**Endpoints de réservation :**
```
GET    /api/reservations                              — Mes réservations
POST   /api/reservations                              — Créer (quota vérifié, coût calculé)
GET    /api/reservations/{id}                         — Détail
PUT    /api/reservations/{id}                         — Modifier
DELETE /api/reservations/{id}                         — Annuler
GET    /api/reservations/availability/slots/{id}?date — Créneaux disponibles
GET    /api/reservations/availability/terrain/{id}?date — Planning complet
```

### 2.3 Mon Espace (Historique)

- Affichage de toutes ses réservations
- Filtres par **statut** : En attente / Confirmée / Annulée
- **Tri par date**
- Codes couleurs : 🟡 En attente, 🟢 Confirmée, 🔴 Annulée

### 2.4 Gestion des Terrains (rôle admin)

- Liste des terrains depuis l'API (public)
- Création, modification, suppression (admin)
- Activation / désactivation d'un terrain
- Consultation du format et du tarif

**Endpoints terrain :**
```
GET    /api/terrains             — Liste des terrains actifs (public)
GET    /api/terrains/{id}       — Détail d'un terrain
POST   /api/terrains            — Créer (admin)
PUT    /api/terrains/{id}       — Modifier (admin)
DELETE /api/terrains/{id}       — Supprimer (admin)
PATCH  /api/terrains/{id}/toggle-active — Activer/Désactiver (admin)
```

---

## 3. Technologies

### 3.1 Stack Technique

```
┌───────────────────────────────────────────────┐
│                  FRONTEND                     │
│  React 18 + TypeScript                        │
│  Tailwind CSS (responsive design)             │
│  Axios (appels HTTP vers l'API)               │
│  React Router DOM (navigation)                │
│  AuthContext (gestion état d'authentification)│
└───────────────────┬───────────────────────────┘
                    │ HTTP/REST (JSON)
                    ▼
┌───────────────────────────────────────────────┐
│                   BACKEND                     │
│  FastAPI (Python) — port 8000                 │
│  SQLAlchemy 2.0 (ORM)                         │
│  Pydantic (validation des données)            │
│  python-jose (JWT)                            │
│  bcrypt (hachage mots de passe)               │
│  pytest + requests (tests)                    │
└───────────────────┬───────────────────────────┘
                    │ SQLAlchemy
                    ▼
         Base MySQL "foot5" (partagée)
```

### 3.2 Versions et Dépendances

**Backend (`requirements.txt`) :**
```
fastapi
uvicorn
sqlalchemy
pymysql
python-jose[cryptography]
passlib[bcrypt]
pydantic
python-dotenv
pytest
requests
```

**Frontend (`package.json`) :**
```json
{
  "dependencies": {
    "react": "^18.x",
    "react-dom": "^18.x",
    "typescript": "^5.x",
    "react-router-dom": "^6.x",
    "axios": "^1.x",
    "tailwindcss": "^3.x"
  }
}
```

### 3.3 Architecture du Projet

```
projet-ppe-foot5-web/
├── backend/
│   ├── main.py                    # Point d'entrée FastAPI
│   ├── app/
│   │   ├── models/                # User, Terrain, Reservation (SQLAlchemy)
│   │   ├── routes/                # auth.py, terrains.py, reservations.py
│   │   ├── schemas/               # Validation Pydantic (entrées/sorties)
│   │   ├── services/              # Logique métier (quota, coût, conflits)
│   │   └── utils/                 # hashing.py, jwt.py, config.py
│   ├── test_api.py                # Tests fonctionnels API
│   ├── test_logic.py              # Tests logique métier
│   └── requirements.txt
└── frontend/
    └── src/
        ├── pages/                 # Accueil, Terrains, Réservation, Mon Espace, Profil
        ├── components/            # Navigation, Footer, Button, Badge, Alert…
        ├── contexts/              # AuthContext (état utilisateur global)
        ├── services/              # api.ts (toutes les fonctions Axios)
        └── types/                 # Interfaces TypeScript
```

### 3.4 Pattern Architectural

L'application web suit un pattern **REST API + SPA** :
- Le frontend React est un **single-page application** qui consomme l'API
- Le backend FastAPI expose des **endpoints REST** stateless
- La communication est **JSON over HTTP**
- L'authentification est **stateless via JWT**

---

## 4. Interfaces (Description)

### 4.0 Charte Graphique

| Élément | Valeur |
|---|---|
| Couleur primaire | #10B981 (Vert Emeraude — Tailwind emerald-500) |
| Couleur secondaire | #059669 (Vert Foncé — Tailwind emerald-600) |
| Couleur accent | #34D399 (Vert Clair — Tailwind emerald-400) |
| Fond principal | #FFFFFF (Blanc) |
| Fond secondaire | #F9FAFB (Gris très clair — Tailwind gray-50) |
| Texte principal | #111827 (Quasi-noir — Tailwind gray-900) |
| Texte secondaire | #6B7280 (Gris — Tailwind gray-500) |
| Erreur / Annulé | #EF4444 (Rouge — Tailwind red-500) |
| Succès / Confirmé | #10B981 (Vert — Tailwind emerald-500) |
| Attente | #F59E0B (Ambre — Tailwind amber-500) |
| Typographie | Inter / system-ui — 14–20px |
| Border-radius | 8px (cards), 6px (boutons), 4px (inputs) |
| Framework CSS | Tailwind CSS 3.x (utility-first) |

### 4.1 Page d'Accueil
- Présentation du service Foot5
- Boutons "Réserver" et "Se connecter"
- Liste des terrains disponibles (public)

### 4.2 Page de Connexion / Inscription
- Formulaire de connexion avec gestion des erreurs
- Lien vers l'inscription
- Messages d'erreur contextuels (identifiants incorrects, email déjà utilisé…)

### 4.3 Page Terrains
- Cards affichant chaque terrain :
  - Nom et localisation
  - Format (ex: "5v5 — 10 joueurs")
  - Tarif horaire (ex: "20€/h")
  - Statut (Actif / Inactif)
  - Bouton "Réserver"

### 4.4 Parcours de Réservation (3 étapes)
1. **Choix du terrain** : liste visuelle avec format et prix
2. **Choix du créneau** : sélection date + heure de début + durée + affichage coût estimé
3. **Confirmation** : récapitulatif avec coût total + champ notes + bouton confirmer

### 4.5 Mon Espace
- Tableau de l'historique des réservations
- Filtres par statut + tri par date
- Affichage du coût total de chaque réservation
- Bouton d'annulation si réservation en attente

### 4.6 Mon Profil
- Affichage des informations du compte
- Formulaire de modification (email, username)
- Formulaire de changement de mot de passe

### 4.7 Pages Légales
Pages CGU, Politique de confidentialité, Mentions légales

---

## 5. Sécurité

### 5.1 Authentification JWT

```
Client                     Serveur FastAPI
  │                              │
  │  POST /api/auth/login        │
  │ ────────────────────────────>│
  │  {username, password}        │
  │                              │ → vérifie bcrypt(password, hash)
  │  {access_token: "eyJ..."}    │
  │ <────────────────────────────│
  │                              │
  │  GET /api/reservations       │
  │  Authorization: Bearer eyJ...│
  │ ────────────────────────────>│
  │                              │ → valide JWT (expiration, signature)
  │  [{id:1, terrain:...}]       │
  │ <────────────────────────────│
```

- Token JWT signé (algorithme HS256)
- Expiration : 30 minutes
- Transmission via header `Authorization: Bearer <token>`

### 5.2 Contrôle d'Accès (RBAC)

| Route | Public | User | Admin |
|---|---|---|---|
| `GET /api/terrains` | ✅ | ✅ | ✅ |
| `POST /api/reservations` | ❌ | ✅ | ✅ |
| `GET /api/reservations` | ❌ | Ses resas | Toutes |
| `PATCH .../confirm` | ❌ | ❌ | ✅ |
| `POST /api/terrains` | ❌ | ❌ | ✅ |

### 5.3 Validation des Données

- **Pydantic** valide toutes les entrées API (types, longueurs, formats)
- **Validation email** : regex RFC 5322
- **Validation du mot de passe** : longueur minimum
- **Validation temporelle** : `end > start` obligatoire
- **Quota** : maximum 2 réservations par semaine (7 jours glissants)

### 5.4 Protection contre les Conflits

```python
# Détection de conflit (côté service)
def check_availability(terrain_id, start, end):
    conflicts = db.query(Reservation).filter(
        Reservation.terrain_id == terrain_id,
        Reservation.status.in_(['pending', 'confirmed']),
        Reservation.start < end,
        Reservation.end > start
    ).count()
    return conflicts == 0
```

---

## 6. Tests

### 6.1 Tests API (`test_api.py`)

| Test | Description | Résultat |
|---|---|---|
| `test_register` | Inscription nouvel utilisateur | ✅ |
| `test_login` | Connexion avec identifiants valides | ✅ |
| `test_login_invalid` | Connexion avec mauvais mdp | ✅ (401) |
| `test_get_profile` | Récupérer profil avec token | ✅ |
| `test_get_terrains` | Liste des terrains (public) | ✅ |
| `test_create_reservation` | Créer une réservation | ✅ |
| `test_conflict_detection` | Conflit sur même terrain/créneau | ✅ (409) |
| `test_quota_limit` | Dépassement quota 2/semaine | ✅ (429) |

### 6.2 Tests Logique Métier (`test_logic.py`)

| Test | Description | Résultat |
|---|---|---|
| `test_total_cost_calculation` | Coût = durée × tarif | ✅ |
| `test_time_overlap_detection` | Détection chevauchement | ✅ |
| `test_weekly_quota_logic` | Comptage réservations 7j glissants | ✅ |
| `test_bcrypt_hash_compatible` | Hash compatible app desktop | ✅ |

### 6.3 Documentation API Interactive

FastAPI génère automatiquement une documentation Swagger accessible sur :
```
http://localhost:8000/docs        ← Interface Swagger UI
http://localhost:8000/redoc       ← Interface ReDoc
```

---

## 7. Installation et Démarrage

### Prérequis
- Python 3.8+
- Node.js 18+ et npm
- MySQL avec la base `foot5` initialisée

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm start
# → http://localhost:3000
```

### Configuration (`.env`)
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=foot5
DB_USER=root
DB_PASSWORD=
JWT_SECRET_KEY=votre-cle-secrete
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
MAX_WEEKLY_RESERVATIONS=2
```

---

*Hakim Rayane — BTS SIO SLAM — PPE Foot5 — Mars 2026*
