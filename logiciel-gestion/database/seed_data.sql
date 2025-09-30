DELETE FROM reservations;
DELETE FROM users;
DELETE FROM terrains;

INSERT INTO users (id, username, password_hash, email, is_admin) VALUES
(7, 'admin', '$2b$12$w1QwQwQwQwQwQwQwQwQwQeQwQwQwQwQwQwQwQwQwQwQwQwQw', 'admin@local', true),
(8, 'rayane', '$2b$12$e1RrRrRrRrRrRrRrRrRrReRrRrRrRrRrRrRrRrRrRrRrRrRr', 'rayane@local', false);

INSERT INTO terrains (id, name, location, active) VALUES
(1, 'Terrain A','Salle Centrale', true),
(2, 'Terrain B','Salle Nord', true);

INSERT INTO reservations (user_id, terrain_id, start, end, status) VALUES
(7,1,'2025-10-03 18:00:00','2025-10-03 19:00:00','confirmed'),
(8,2,'2025-10-04 18:00:00','2025-10-04 19:00:00','confirmed');