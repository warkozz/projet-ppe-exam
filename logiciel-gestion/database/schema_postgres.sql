-- Football Manager 5v5 - Schéma Base de Données PostgreSQL
-- Version 2.0 - Aligné avec la version MySQL

-- Connexion à la base de données (exécuter en tant que postgres)
CREATE DATABASE foot5;
\c foot5

-- ===================================
-- TYPES ENUM
-- ===================================
CREATE TYPE role_enum AS ENUM ('superadmin', 'admin', 'user');
CREATE TYPE status_enum AS ENUM ('pending', 'confirmed', 'cancelled');

-- ===================================
-- TABLE: users
-- ===================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(120) UNIQUE,
    role role_enum NOT NULL DEFAULT 'user',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(active);

-- ===================================
-- TABLE: terrains
-- ===================================
CREATE TABLE terrains (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_terrains_name ON terrains(name);
CREATE INDEX idx_terrains_active ON terrains(active);

-- ===================================
-- TABLE: reservations
-- ===================================
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    terrain_id INTEGER NOT NULL REFERENCES terrains(id) ON DELETE CASCADE,
    start TIMESTAMP NOT NULL,
    "end" TIMESTAMP NOT NULL,
    status status_enum NOT NULL DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_reservation_time CHECK ("end" > start)
);

CREATE INDEX idx_reservations_user ON reservations(user_id);
CREATE INDEX idx_reservations_terrain ON reservations(terrain_id);
CREATE INDEX idx_reservations_start ON reservations(start);
CREATE INDEX idx_reservations_status ON reservations(status);

-- ===================================
-- DONNÉES INITIALES
-- ===================================
INSERT INTO terrains (name, location, active) VALUES
    ('Terrain Central', 'Terrain principal avec éclairage', TRUE),
    ('Terrain Nord', 'Terrain secondaire, pelouse synthétique', TRUE),
    ('Terrain Sud', 'Petit terrain d''entraînement', TRUE),
    ('Terrain Ouest', 'Terrain en rénovation', FALSE);
