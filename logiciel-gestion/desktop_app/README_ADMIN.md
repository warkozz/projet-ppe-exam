# Création et gestion des comptes administrateurs (superadmin, admin, user)

## Rôles disponibles
- **superadmin** : accès total à toutes les fonctionnalités (gestion utilisateurs, terrains, réservations)
- **admin** : gestion des terrains et réservations uniquement
- **user** : consultation uniquement

## Création d'un superadmin via script Python

1. Activez l'environnement virtuel :
   ```powershell
   .venv\Scripts\activate
   ```
2. Placez-vous dans le dossier `desktop_app`.
3. Lancez le script :
   ```powershell
   python create_superadmin.py
   ```
   Cela crée un utilisateur :
   - Nom d'utilisateur : **Administrateur**
   - Mot de passe : **admin123**
   - Email : administateur@local
   - Rôle : superadmin

## Création d'autres comptes
- Utilisez l'interface "Gestion utilisateurs" (accessible uniquement au superadmin) pour créer des comptes admin ou user.
- Vous pouvez aussi insérer directement dans la base via phpMyAdmin ou un script SQL.

## Connexion
- Depuis l'écran de connexion, entrez le nom d'utilisateur et le mot de passe.
- Le rôle détermine les droits d'accès dans l'application.

## Déconnexion
- Utilisez le bouton "Déconnexion" pour changer d'utilisateur sans fermer l'application.

---
Pour toute question, contactez l'équipe projet.
