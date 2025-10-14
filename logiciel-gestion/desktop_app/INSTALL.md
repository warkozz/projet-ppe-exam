# Installation et Lancement de l'Application de Gestion

## Prérequis

- **Python 3.13+** (recommandé : utiliser un environnement virtuel)
- **PostgreSQL** (pour la base de données)
- **CMake** et un compilateur C++ (pour la partie C++ du moteur de réservation)
- **pip** (installé avec Python)

## Installation

### 1. Cloner le dépôt
```sh
git clone <url-du-repo>
cd projet-ppe-exam/logiciel-gestion/desktop_app
```

### 2. Créer et activer un environnement virtuel Python
```sh
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/Mac
```

### 3. Installer les dépendances Python
```sh
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
Copiez le fichier `.env.example` en `.env` et adaptez les valeurs (notamment la connexion à la base PostgreSQL).

### 5. Installer et configurer la base de données
- Créez une base PostgreSQL.
- Exécutez les scripts SQL dans `../database/schema_postgres.sql` puis `../database/seed_data.sql` pour créer les tables et insérer les données de test.

### 6. Compiler le moteur C++ (optionnel, si besoin de performances)
Assurez-vous d'avoir **CMake** et un compilateur C++ installés.
```sh
cd ../cpp
cmake -S . -B build
cmake --build build
```

## Lancement de l'application

Depuis le dossier `desktop_app` :

```sh
.venv\Scripts\activate  # Windows
python app/main.py
```

Ou utilisez le script :
```sh
run.bat  # Windows
./run.sh # Linux/Mac
```

## Dépannage
- Si `cmake` n'est pas reconnu, installez-le et ajoutez-le à votre PATH : https://cmake.org/download/
- Vérifiez que PostgreSQL est bien démarré et accessible.
- Pour tout problème de dépendances Python, relancez `pip install -r requirements.txt`.

## Structure du projet
- `app/` : code source Python (MVC)
- `cpp/` : moteur de réservation C++
- `database/` : scripts SQL
- `documentation/` : docs techniques et utilisateur

---
Pour toute question, consultez la documentation ou contactez l'équipe projet.
