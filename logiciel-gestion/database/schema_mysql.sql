-- Script MySQL pour la base de données foot5
CREATE DATABASE IF NOT EXISTS foot5;
USE foot5;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  role ENUM('superadmin', 'admin', 'user') NOT NULL DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS terrains (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  location VARCHAR(200),
  active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS reservations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  terrain_id INT,
  start DATETIME NOT NULL,
  end DATETIME NOT NULL,
  status VARCHAR(20) DEFAULT 'confirmed',
  notes VARCHAR(250),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (terrain_id) REFERENCES terrains(id) ON DELETE CASCADE
);
