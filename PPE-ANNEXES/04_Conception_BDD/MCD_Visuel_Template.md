# 🗃️ MCD Textuel Détaillé - Football Manager 5v5

## 📋 Notation Merise Complète

### Entités et Attributs

```
UTILISATEUR
├─ id (1,1) [Clé Primaire] 
├─ username (1,1) [Unique]
├─ password_hash (1,1)
├─ email (1,1) [Unique]
└─ role (1,1) [superadmin|gestionnaire|utilisateur]

TERRAIN  
├─ id (1,1) [Clé Primaire]
├─ name (1,1)
├─ location (0,1)
└─ active (1,1) [Boolean]

RESERVATION
├─ id (1,1) [Clé Primaire] 
├─ start (1,1) [DateTime]
├─ end (1,1) [DateTime]
└─ status (1,1) [pending|confirmed|cancelled]
```

### Relations Détaillées

```
UTILISATEUR ──(1,n)── EFFECTUE ──(0,n)── RESERVATION
    │                                         │
    └── Un utilisateur peut faire plusieurs   │
        réservations (cardinalité 1,n)       │
                                              │
TERRAIN ──(1,n)── CONCERNE ──(0,n)── RESERVATION
    │                                         │
    └── Un terrain peut avoir plusieurs       │
        réservations (cardinalité 1,n)       │
```

### Diagramme ASCII Art MCD

```
┌─────────────────┐              ┌─────────────────┐              ┌─────────────────┐
│   UTILISATEUR   │              │   RESERVATION   │              │    TERRAIN      │
├─────────────────┤              ├─────────────────┤              ├─────────────────┤
│ id (PK)         │              │ id (PK)         │              │ id (PK)         │
│ username (U)    │    (1,n)     │ user_id (FK)    │    (0,n)     │ name            │
│ password_hash   │──────────────│ terrain_id (FK) │──────────────│ location        │
│ email (U)       │   EFFECTUE   │ start           │  CONCERNE    │ active          │
│ role            │              │ end             │              │                 │
└─────────────────┘              │ status          │              └─────────────────┘
                                 └─────────────────┘

Légende:
(PK) = Primary Key
(FK) = Foreign Key  
(U) = Unique
(1,n) = Un vers plusieurs
(0,n) = Zéro vers plusieurs
```

### Contraintes d'Intégrité Détaillées

1. **Clés Primaires :**
   - UTILISATEUR.id : AUTO_INCREMENT, NOT NULL
   - TERRAIN.id : AUTO_INCREMENT, NOT NULL  
   - RESERVATION.id : AUTO_INCREMENT, NOT NULL

2. **Clés Étrangères :**
   - RESERVATION.user_id → UTILISATEUR.id (CASCADE)
   - RESERVATION.terrain_id → TERRAIN.id (CASCADE)

3. **Contraintes Unicité :**
   - UTILISATEUR.username : UNIQUE
   - UTILISATEUR.email : UNIQUE

4. **Contraintes Domaine :**
   - UTILISATEUR.role ∈ {superadmin, gestionnaire, utilisateur}
   - RESERVATION.status ∈ {pending, confirmed, cancelled}
   - TERRAIN.active ∈ {TRUE, FALSE}

5. **Contraintes Métier :**
   - RESERVATION.end > RESERVATION.start
   - Pas de chevauchement temporel sur même terrain
   - Utilisateur actif pour créer réservation
   - Terrain actif pour nouvelle réservation
```

## 🔗 Outils Recommandés pour Générer l'Image MCD :

1. **Draw.io (diagrams.net)** - Gratuit, en ligne
2. **Lucidchart** - Professionnel
3. **MySQL Workbench** - Génère automatiquement depuis la BDD
4. **PowerDesigner** - Outil professionnel Merise
5. **Visual Studio Code** + Extension "ERD Editor"

## 📐 Template pour Draw.io :

```
Étapes pour créer ton MCD visuel :
1. Aller sur draw.io
2. Choisir "Entity Relation" template
3. Créer 3 rectangles pour les entités
4. Ajouter les attributs dans chaque rectangle
5. Dessiner les relations avec les cardinalités
6. Exporter en PNG/JPG
```