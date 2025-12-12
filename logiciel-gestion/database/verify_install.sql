-- Script de vérification de la base de données foot5
-- À exécuter dans phpMyAdmin pour vérifier l'installation

USE foot5;

-- Vérifier l'existence des tables
SELECT 
    'Tables créées' as status,
    COUNT(*) as nombre_tables
FROM information_schema.tables 
WHERE table_schema = 'foot5';

-- Vérifier les utilisateurs
SELECT 
    'Utilisateurs' as type,
    COUNT(*) as total,
    COUNT(CASE WHEN role = 'superadmin' THEN 1 END) as superadmins,
    COUNT(CASE WHEN role = 'admin' THEN 1 END) as admins,
    COUNT(CASE WHEN role = 'user' THEN 1 END) as users
FROM users;

-- Vérifier les terrains
SELECT 
    'Terrains' as type,
    COUNT(*) as total,
    COUNT(CASE WHEN active = 1 THEN 1 END) as actifs,
    COUNT(CASE WHEN active = 0 THEN 1 END) as inactifs
FROM terrains;

-- Vérifier les réservations
SELECT 
    'Réservations' as type,
    COUNT(*) as total,
    COUNT(CASE WHEN status = 'confirmed' THEN 1 END) as confirmées,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as en_attente,
    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as annulées
FROM reservations;

-- Lister les utilisateurs administrateurs
SELECT 
    username,
    email,
    role,
    active,
    created_at
FROM users 
WHERE role IN ('superadmin', 'admin')
ORDER BY role DESC, username;

-- Informations de connexion pour test
SELECT 
    '=== INFORMATIONS DE CONNEXION ===' as info
UNION ALL
SELECT 'Superadmin: admin / admin123'
UNION ALL  
SELECT 'Manager: manager / manager123'
UNION ALL
SELECT 'Utilisateur: user1 / user123'
UNION ALL
SELECT '⚠️ Changez ces mots de passe en production!';