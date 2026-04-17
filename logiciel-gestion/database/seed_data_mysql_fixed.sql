-- Football Manager 5v5 - Données initiales MySQL
-- Version 2.0 avec mots de passe bcrypt valides

USE foot5;

-- Nettoyer les données existantes
DELETE FROM reservations;
DELETE FROM users;
DELETE FROM terrains;

-- ===================================
-- UTILISATEURS PAR DÉFAUT
-- ===================================
-- Mots de passe hachés avec bcrypt (rounds=12)
-- admin123 -> $2b$12$L0dGQLuqMqzGT8OUyum9ru1rk.nlvFlGok6LS1cB95tLvqnFFYBNm
-- manager123 -> $2b$12$41Lc8LqWEiRfPrET3iwztuO/7P3PcFy/cQYHuD7KPMn6Ufsyy5MRy
-- user123 -> $2b$12$0k80SQvxIS1K.xm3endGY.kvgScGOWucXVfGBbZyNVgkHgMT5ezi2
-- test123 -> $2b$12$YvIaViHm1zGvLENozWjyV.KksQ/lGeBX1P2fxw/f25eiH8lgJoZpe

INSERT INTO users (username, password_hash, email, role, active) VALUES
('admin', '$2b$12$L0dGQLuqMqzGT8OUyum9ru1rk.nlvFlGok6LS1cB95tLvqnFFYBNm', 'admin@foot5.com', 'superadmin', 1),
('manager', '$2b$12$41Lc8LqWEiRfPrET3iwztuO/7P3PcFy/cQYHuD7KPMn6Ufsyy5MRy', 'manager@foot5.com', 'admin', 1),
('user1', '$2b$12$0k80SQvxIS1K.xm3endGY.kvgScGOWucXVfGBbZyNVgkHgMT5ezi2', 'user1@foot5.com', 'user', 1),
('test2', '$2b$12$YvIaViHm1zGvLENozWjyV.KksQ/lGeBX1P2fxw/f25eiH8lgJoZpe', 'test2@foot5.com', 'user', 1),
('test3', '$2b$12$YvIaViHm1zGvLENozWjyV.KksQ/lGeBX1P2fxw/f25eiH8lgJoZpe', 'test3@foot5.com', 'user', 1),
('test4', '$2b$12$YvIaViHm1zGvLENozWjyV.KksQ/lGeBX1P2fxw/f25eiH8lgJoZpe', 'test4@foot5.com', 'user', 1),
('test5', '$2b$12$YvIaViHm1zGvLENozWjyV.KksQ/lGeBX1P2fxw/f25eiH8lgJoZpe', 'test5@foot5.com', 'user', 1);

-- ===================================
-- TERRAINS PAR DÉFAUT
-- ===================================
INSERT INTO terrains (name, location, active) VALUES
('Terrain A', 'Salle Centrale', 1),
('Terrain B', 'Salle Nord', 1),
('Terrain C', 'Salle Sud', 1),
('Terrain D', 'Salle Est', 1),
('Terrain E', 'Salle Ouest', 1),
('Terrain F', 'Salle Annexe', 0);  -- Terrain inactif pour test

-- ===================================
-- RÉSERVATIONS D'EXEMPLE
-- ===================================
-- Note: Adaptez les dates selon vos besoins de test
INSERT INTO reservations (user_id, terrain_id, start, end, status, notes) VALUES
(1, 1, '2025-12-12 14:00:00', '2025-12-12 16:00:00', 'confirmed', 'Match amical équipe A'),
(2, 2, '2025-12-12 18:00:00', '2025-12-12 20:00:00', 'confirmed', 'Entraînement équipe B'),
(3, 1, '2025-12-13 10:00:00', '2025-12-13 12:00:00', 'pending', 'Tournoi junior'),
(4, 3, '2025-12-13 14:00:00', '2025-12-13 16:00:00', 'confirmed', 'Match test'),
(5, 2, '2025-12-14 16:00:00', '2025-12-14 18:00:00', 'confirmed', 'Entraînement senior');

-- ===================================
-- INFORMATIONS DE CONNEXION
-- ===================================
-- Superadmin: admin / admin123
-- Manager: manager / manager123
-- Utilisateur: user1 / user123
-- Utilisateurs test: test2-test5 / test123

SELECT 'Base de données initialisée avec succès!' as message;
SELECT COUNT(*) as nombre_utilisateurs FROM users;
SELECT COUNT(*) as nombre_terrains FROM terrains;
SELECT COUNT(*) as nombre_reservations FROM reservations;