-- create DB and tables (run as postgres user)
CREATE DATABASE foot5;
\c foot5
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  is_admin BOOLEAN DEFAULT FALSE
);
CREATE TABLE terrains (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  location VARCHAR(200),
  active BOOLEAN DEFAULT TRUE
);
CREATE TABLE reservations (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  terrain_id INTEGER REFERENCES terrains(id) ON DELETE CASCADE,
  start TIMESTAMP NOT NULL,
  end TIMESTAMP NOT NULL,
  status VARCHAR(20) DEFAULT 'confirmed',
  notes VARCHAR(250)
);
