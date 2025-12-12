-- Football Manager 5v5 - Schéma Base de Données MySQL/MariaDB
-- Version 2.0 - Compatible avec la version hybride Material Design

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS foot5 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE foot5;

-- ===================================
-- TABLE: users
-- Gestion des utilisateurs avec système de rôles étendu
-- ===================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(120) UNIQUE,  -- Nullable pour permettre des utilisateurs sans email
    role ENUM('user', 'admin', 'superadmin') NOT NULL DEFAULT 'user',
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_active (active)
) ENGINE=InnoDB;

-- ===================================
-- TABLE: terrains
-- Gestion des terrains avec système actif/inactif
-- ===================================
CREATE TABLE IF NOT EXISTS terrains (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200),  -- Description/emplacement du terrain
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_name (name),
    INDEX idx_active (active)
) ENGINE=InnoDB;

-- ===================================
-- TABLE: reservations
-- Gestion des réservations avec statuts et contraintes
-- ===================================
CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    terrain_id INT NOT NULL,
    start DATETIME NOT NULL,
    end DATETIME NOT NULL,
    status ENUM('active', 'cancelled', 'completed') DEFAULT 'active',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (terrain_id) REFERENCES terrains(id) ON DELETE CASCADE,
    
    INDEX idx_user_id (user_id),
    INDEX idx_terrain_id (terrain_id),
    INDEX idx_start_time (start),
    INDEX idx_status (status),
    INDEX idx_reservation_period (start, end),
    
    -- Contrainte pour éviter les chevauchements sur le même terrain
    UNIQUE KEY unique_terrain_time (terrain_id, start, end)
) ENGINE=InnoDB;

-- ===================================
-- DONNÉES INITIALES
-- ===================================

-- Insertion de terrains d'exemple
INSERT IGNORE INTO terrains (name, location, active) VALUES
('Terrain Central', 'Terrain principal avec éclairage', TRUE),
('Terrain Nord', 'Terrain secondaire, pelouse synthétique', TRUE),
('Terrain Sud', 'Petit terrain d\'entraînement', TRUE),
('Terrain Ouest', 'Terrain en rénovation', FALSE);

-- ===================================
-- VUES UTILES
-- ===================================

-- Vue pour les réservations avec détails utilisateur et terrain
CREATE OR REPLACE VIEW reservation_details AS
SELECT 
    r.id,
    r.start,
    r.end,
    r.status,
    r.notes,
    u.username,
    u.email,
    u.role,
    t.name as terrain_name,
    t.location as terrain_location,
    t.active as terrain_active
FROM reservations r
JOIN users u ON r.user_id = u.id
JOIN terrains t ON r.terrain_id = t.id;

-- Vue pour les statistiques du dashboard
CREATE OR REPLACE VIEW dashboard_stats AS
SELECT 
    (SELECT COUNT(*) FROM users WHERE active = TRUE) as active_users,
    (SELECT COUNT(*) FROM terrains WHERE active = TRUE) as active_terrains,
    (SELECT COUNT(*) FROM reservations 
     WHERE status = 'active' 
     AND DATE(start) = CURDATE()) as today_reservations,
    (SELECT COUNT(*) FROM reservations 
     WHERE status = 'active') as total_active_reservations;
