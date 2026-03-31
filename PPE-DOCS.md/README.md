# PPE-DOCS — Documentation Exam PPE
## Projet Foot5 — BTS SIO SLAM

**Étudiant :** Hakim Rayane  
**Date :** Mars 2026  
**Contexte :** Dossier de rendu pour l'examen PPE (Projet Personnel Encadré)

---

> **Phrase à retenir pour l'oral :**  
> *"Le projet Foot5 repose sur une architecture composée de deux applications complémentaires : une application web destinée aux clients et une application lourde destinée à l'administration, partageant une base de données commune."*

---

## Structure du Dossier

```
PPE-DOCS/
├── README.md                          ← Ce fichier (index)
│
├── 01_Tableau_Synthese.md             ← Vue synthétique des 2 projets
├── 02_Dossier_Principal_Commun.md     ← Contexte + BDD + Architecture globale
├── 03_Application_Legere_Web.md       ← Application web (React + FastAPI)
├── 04_Application_Lourde_Admin.md     ← Application desktop (Python + PySide6)
└── 05_Sources_Code.md                 ← Liens GitHub + structure des dépôts
```

---

## Plan du Dossier

| # | Document | Contenu |
|---|---|---|
| **01** | [Tableau de Synthèse](01_Tableau_Synthese.md) | Vue comparative des 2 applications |
| **02** | [Dossier Principal Commun](02_Dossier_Principal_Commun.md) | Contexte Foot5, BDD commune (MCD/MLD/SQL), architecture globale |
| **03** | [Application Légère — Web](03_Application_Legere_Web.md) | React + FastAPI, fonctionnalités client, sécurité JWT, tests |
| **04** | [Application Lourde — Admin](04_Application_Lourde_Admin.md) | PySide6 desktop, gestion admin, MVC, sécurité, tests |
| **05** | [Code Source](05_Sources_Code.md) | Liens GitHub, structure dépôts, métriques code |

---

## Résumé du Projet

### Ce que tu as construit

Le projet Foot5 est une **plateforme complète de gestion de terrains de football 5v5** composée de deux applications complémentaires.

**Application Légère (Web) — côté CLIENT**
- Accessible via navigateur, sans installation
- Inscription, connexion, réservation de terrain en ligne
- Historique des réservations ("Mon Espace")
- Stack : React + TypeScript + Tailwind + FastAPI + MySQL
- GitHub : https://github.com/warkozz/projet-ppe-foot5-web

**Application Lourde (Desktop) — côté ADMIN**
- Interface native installée sur le poste admin
- Gestion complète : utilisateurs, terrains, réservations
- Calendrier interactif, tableau de bord, multi-rôles
- Stack : Python + PySide6 (Qt6) + SQLAlchemy + MySQL
- GitHub : https://github.com/warkozz/projet-ppe-exam

**Point fort : une seule BDD MySQL `foot5` partagée entre les deux apps.**

---

*Hakim Rayane — BTS SIO SLAM — PPE Foot5 — Mars 2026*
