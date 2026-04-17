-- ============================================================
--  PPE INSTALL - Football Manager 5v5
--  Script complet prêt à l'emploi pour présentation jury
--  À importer dans phpMyAdmin (base : foot5)
--  Date : Avril 2026
-- ============================================================

-- ============================================================
--  1. CRÉATION DE LA BASE DE DONNÉES
-- ============================================================
DROP DATABASE IF EXISTS foot5;
CREATE DATABASE foot5
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE foot5;

-- ============================================================
--  2. TABLES
-- ============================================================

CREATE TABLE users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email         VARCHAR(120) UNIQUE,
    role          ENUM('user','admin','superadmin') NOT NULL DEFAULT 'user',
    active        BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_role     (role),
    INDEX idx_active   (active)
) ENGINE=InnoDB;

CREATE TABLE terrains (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    location   VARCHAR(200),
    active     BOOLEAN DEFAULT TRUE,
    price      DECIMAL(10,2) DEFAULT 0.00,
    capacity   INT DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name   (name),
    INDEX idx_active (active)
) ENGINE=InnoDB;

CREATE TABLE reservations (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    terrain_id  INT NOT NULL,
    start       DATETIME NOT NULL,
    end         DATETIME NOT NULL,
    status      ENUM('pending','confirmed','cancelled') DEFAULT 'pending',
    notes       TEXT,
    total_cost  DECIMAL(10,2) DEFAULT 0.00,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)    REFERENCES users(id)    ON DELETE CASCADE,
    FOREIGN KEY (terrain_id) REFERENCES terrains(id) ON DELETE CASCADE,
    INDEX idx_user_id   (user_id),
    INDEX idx_terrain_id(terrain_id),
    INDEX idx_start     (start),
    INDEX idx_status    (status)
) ENGINE=InnoDB;

-- ============================================================
--  3. VUES UTILES (dashboard + détails réservations)
-- ============================================================

CREATE OR REPLACE VIEW reservation_details AS
SELECT
    r.id,
    r.start,
    r.end,
    r.status,
    r.notes,
    r.total_cost,
    u.username,
    u.email,
    u.role,
    t.name     AS terrain_name,
    t.location AS terrain_location,
    t.active   AS terrain_active
FROM reservations r
JOIN users    u ON r.user_id    = u.id
JOIN terrains t ON r.terrain_id = t.id;

CREATE OR REPLACE VIEW dashboard_stats AS
SELECT
    (SELECT COUNT(*) FROM users        WHERE active = TRUE)                                         AS active_users,
    (SELECT COUNT(*) FROM terrains     WHERE active = TRUE)                                         AS active_terrains,
    (SELECT COUNT(*) FROM reservations WHERE status IN ('pending','confirmed')
                                         AND DATE(start) = CURDATE())                               AS today_reservations,
    (SELECT COUNT(*) FROM reservations WHERE status IN ('pending','confirmed'))                     AS total_active_reservations;

-- ============================================================
--  4. UTILISATEURS
--  Mots de passe bcrypt (rounds=12) générés depuis le projet
--  admin     -> admin123
--  manager   -> manager123
--  user1     -> user123
--  alice/bob/charlie/diana/eve -> user123
--  test123   -> test123
-- ============================================================

INSERT INTO users (username, password_hash, email, role, active) VALUES
-- SUPERADMIN
('admin',
 '$2b$12$L0dGQLuqMqzGT8OUyum9ru1rk.nlvFlGok6LS1cB95tLvqnFFYBNm',
 'admin@foot5.com', 'superadmin', 1),

-- ADMIN / MANAGER
('manager',
 '$2b$12$41Lc8LqWEiRfPrET3iwztuO/7P3PcFy/cQYHuD7KPMn6Ufsyy5MRy',
 'manager@foot5.com', 'admin', 1),

-- UTILISATEURS STANDARD (pour tester les réservations)
('user1',
 '$2b$12$0k80SQvxIS1K.xm3endGY.kvgScGOWucXVfGBbZyNVgkHgMT5ezi2',
 'user1@foot5.com', 'user', 1),

('alice',
 '$2b$12$0k80SQvxIS1K.xm3endGY.kvgScGOWucXVfGBbZyNVgkHgMT5ezi2',
 'alice@foot5.com', 'user', 1),

('bob',
 '$2b$12$0k80SQvxIS1K.xm3endGY.kvgScGOWucXVfGBbZyNVgkHgMT5ezi2',
 'bob@foot5.com', 'user', 1),

('charlie',
 '$2b$12$0k80SQvxIS1K.xm3endGY.kvgScGOWucXVfGBbZyNVgkHgMT5ezi2',
 'charlie@foot5.com', 'user', 1),

('diana',
 '$2b$12$0k80SQvxIS1K.xm3endGY.kvgScGOWucXVfGBbZyNVgkHgMT5ezi2',
 'diana@foot5.com', 'user', 1),

-- COMPTE INACTIF (pour tester la gestion des comptes désactivés)
('inactif',
 '$2b$12$YvIaViHm1zGvLENozWjyV.KksQ/lGeBX1P2fxw/f25eiH8lgJoZpe',
 'inactif@foot5.com', 'user', 0);

-- ============================================================
--  5. TERRAINS
-- ============================================================

INSERT INTO terrains (name, location, active, price, capacity) VALUES
('Terrain A - Central',   'Salle Principale - Rez-de-chaussée',  1, 30.00, 10),
('Terrain B - Nord',      'Salle Nord - Pelouse synthétique',     1, 25.00, 10),
('Terrain C - Sud',       'Salle Sud - Éclairage LED',           1, 25.00, 10),
('Terrain D - Est',       'Annexe Est - Intérieur chauffé',      1, 20.00, 10),
('Terrain E - VIP',       'Salle VIP - Vestiaires privatifs',    1, 50.00, 10),
('Terrain F - Rénovation','Terrain en cours de rénovation',      0, 0.00,  10);

-- ============================================================
--  6. RÉSERVATIONS DE DÉMONSTRATION
--  Couvre : aujourd'hui, demain, semaine prochaine,
--           statuts confirmed / pending / cancelled
-- ============================================================

-- ---- AUJOURD'HUI ----
INSERT INTO reservations (user_id, terrain_id, start, end, status, notes, total_cost) VALUES
(3, 1,
 DATE_FORMAT(NOW(), '%Y-%m-%d 09:00:00'),
 DATE_FORMAT(NOW(), '%Y-%m-%d 11:00:00'),
 'confirmed', 'Match amical - équipe user1 vs alice', 60.00),

(4, 2,
 DATE_FORMAT(NOW(), '%Y-%m-%d 11:00:00'),
 DATE_FORMAT(NOW(), '%Y-%m-%d 13:00:00'),
 'confirmed', 'Entraînement Alice FC', 50.00),

(5, 3,
 DATE_FORMAT(NOW(), '%Y-%m-%d 14:00:00'),
 DATE_FORMAT(NOW(), '%Y-%m-%d 16:00:00'),
 'pending',   'Tournoi interne - en attente de validation', 50.00),

(6, 1,
 DATE_FORMAT(NOW(), '%Y-%m-%d 18:00:00'),
 DATE_FORMAT(NOW(), '%Y-%m-%d 20:00:00'),
 'confirmed', 'Soirée Charlie United', 60.00),

-- ---- DEMAIN ----
(3, 4,
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 1 DAY), '%Y-%m-%d 10:00:00'),
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 1 DAY), '%Y-%m-%d 12:00:00'),
 'confirmed', 'Réservation demain - user1', 40.00),

(4, 5,
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 1 DAY), '%Y-%m-%d 15:00:00'),
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 1 DAY), '%Y-%m-%d 17:00:00'),
 'pending',   'Alice - terrain VIP demain', 100.00),

-- ---- CETTE SEMAINE ----
(5, 2,
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 2 DAY), '%Y-%m-%d 09:00:00'),
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 2 DAY), '%Y-%m-%d 11:00:00'),
 'confirmed', 'Bob Morning Cup', 50.00),

(6, 3,
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 3 DAY), '%Y-%m-%d 16:00:00'),
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 3 DAY), '%Y-%m-%d 18:00:00'),
 'confirmed', 'Finale Charlie vs Diana', 50.00),

(7, 1,
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 4 DAY), '%Y-%m-%d 20:00:00'),
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 4 DAY), '%Y-%m-%d 22:00:00'),
 'pending',   'Diana - soirée nocturne', 60.00),

-- ---- SEMAINE PROCHAINE ----
(3, 5,
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 7 DAY), '%Y-%m-%d 10:00:00'),
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 7 DAY), '%Y-%m-%d 12:00:00'),
 'confirmed', 'Tournoi mensuel - phase de groupes', 100.00),

(4, 2,
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 8 DAY), '%Y-%m-%d 14:00:00'),
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL 8 DAY), '%Y-%m-%d 16:00:00'),
 'confirmed', 'Demi-finale Alice FC', 50.00),

-- ---- ANNULÉES (pour tester le filtre) ----
(5, 3,
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -2 DAY), '%Y-%m-%d 10:00:00'),
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -2 DAY), '%Y-%m-%d 12:00:00'),
 'cancelled', 'Annulée - terrain indisponible', 0.00),

(6, 4,
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -1 DAY), '%Y-%m-%d 18:00:00'),
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -1 DAY), '%Y-%m-%d 20:00:00'),
 'cancelled', 'Annulée - équipe absente', 0.00),

-- ---- PASSÉES CONFIRMÉES (historique) ----
(3, 1,
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -7 DAY), '%Y-%m-%d 09:00:00'),
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -7 DAY), '%Y-%m-%d 11:00:00'),
 'confirmed', 'Match passé semaine dernière', 60.00),

(4, 2,
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -5 DAY), '%Y-%m-%d 14:00:00'),
 DATE_FORMAT(DATE_ADD(NOW(), INTERVAL -5 DAY), '%Y-%m-%d 16:00:00'),
 'confirmed', 'Entraînement passé', 50.00);

-- ============================================================
--  7. VÉRIFICATION FINALE
-- ============================================================

SELECT '========================================' AS '';
SELECT '   INSTALLATION PPE - RÉCAPITULATIF     ' AS '';
SELECT '========================================' AS '';

SELECT 'UTILISATEURS' AS section,
    COUNT(*) AS total,
    SUM(role = 'superadmin') AS superadmins,
    SUM(role = 'admin')      AS admins,
    SUM(role = 'user')       AS users,
    SUM(active = 0)          AS inactifs
FROM users;

SELECT 'TERRAINS' AS section,
    COUNT(*)         AS total,
    SUM(active = 1)  AS actifs,
    SUM(active = 0)  AS inactifs
FROM terrains;

SELECT 'RÉSERVATIONS' AS section,
    COUNT(*)                       AS total,
    SUM(status = 'confirmed')      AS confirmées,
    SUM(status = 'pending')        AS en_attente,
    SUM(status = 'cancelled')      AS annulées
FROM reservations;

SELECT '========================================' AS '';
SELECT '   COMPTES DE CONNEXION POUR LE JURY    ' AS '';
SELECT '========================================' AS '';
SELECT '  Superadmin : admin     / admin123     ' AS '';
SELECT '  Admin      : manager   / manager123   ' AS '';
SELECT '  Utilisateur: user1     / user123      ' AS '';
SELECT '  Utilisateur: alice     / user123      ' AS '';
SELECT '  Compte OFF : inactif   / test123      ' AS '';
SELECT '========================================' AS '';
SELECT '  ✅ Base de données prête pour le jury !' AS '';
SELECT '========================================' AS '';
