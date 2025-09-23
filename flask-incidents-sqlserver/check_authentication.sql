-- Script pour vérifier et activer SQL Server Authentication
-- Fichier: check_authentication.sql

-- Vérifier le mode d'authentification actuel
SELECT 
    CASE SERVERPROPERTY('IsIntegratedSecurityOnly') 
        WHEN 1 THEN 'Windows Authentication uniquement'
        WHEN 0 THEN 'Mode mixte (Windows + SQL Server Authentication)'
    END AS 'Mode d''authentification';

-- Lister tous les logins existants
SELECT 
    name AS 'Login Name',
    type_desc AS 'Type',
    is_disabled AS 'Désactivé',
    create_date AS 'Date création'
FROM sys.server_principals 
WHERE type IN ('S', 'U')  -- S = SQL Login, U = Windows User
ORDER BY name;