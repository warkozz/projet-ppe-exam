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
-- admin123 -> $2b$12$LqGIyLIvKX8dM8H0qXWx7.FuQ7qcEgB7k8E6qc7P5F3jtLp1L2E8y
-- manager123 -> $2b$12$o4qzJw9X8Y0r4mRPD.Z2s.vWx7a8yTbT9iVhN6mKcHs5.LqZ3n1J7
-- user123 -> $2b$12$m8H4X0pY7n5F1aQ9kM2L6e.jW8dT3oKpS6vR9cH4nE2bQ7mL0yW5z
-- test123 -> $2b$12$k5G3v8P2nQ0sL4mD9aF7x.rK2yJ8wE5bH3vN6dM1oQ7cF9pX4hS2m

INSERT INTO users (username, password_hash, email, role, active) VALUES
('admin', '$2b$12$LqGIyLIvKX8dM8H0qXWx7.FuQ7qcEgB7k8E6qc7P5F3jtLp1L2E8y', 'admin@foot5.com', 'superadmin', 1),
('manager', '$2b$12$o4qzJw9X8Y0r4mRPD.Z2s.vWx7a8yTbT9iVhN6mKcHs5.LqZ3n1J7', 'manager@foot5.com', 'admin', 1),
('user1', '$2b$12$m8H4X0pY7n5F1aQ9kM2L6e.jW8dT3oKpS6vR9cH4nE2bQ7mL0yW5z', 'user1@foot5.com', 'user', 1),
('test2', '$2b$12$k5G3v8P2nQ0sL4mD9aF7x.rK2yJ8wE5bH3vN6dM1oQ7cF9pX4hS2m', 'test2@foot5.com', 'user', 1),
('test3', '$2b$12$k5G3v8P2nQ0sL4mD9aF7x.rK2yJ8wE5bH3vN6dM1oQ7cF9pX4hS2m', 'test3@foot5.com', 'user', 1),
('test4', '$2b$12$k5G3v8P2nQ0sL4mD9aF7x.rK2yJ8wE5bH3vN6dM1oQ7cF9pX4hS2m', 'test4@foot5.com', 'user', 1),
('test5', '$2b$12$k5G3v8P2nQ0sL4mD9aF7x.rK2yJ8wE5bH3vN6dM1oQ7cF9pX4hS2m', 'test5@foot5.com', 'user', 1);

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