-- Script de création de base de données et utilisateur
-- Fichier: setup_database.sql

-- =============================================
-- Création de la base de données IncidentsReseau
-- =============================================
USE master;
GO

-- Supprimer la base si elle existe déjà (optionnel)
IF EXISTS(SELECT * FROM sys.databases WHERE name = 'IncidentsReseau')
BEGIN
    ALTER DATABASE IncidentsReseau SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE IncidentsReseau;
END
GO

-- Créer la nouvelle base de données
CREATE DATABASE IncidentsReseau;
GO

-- =============================================
-- Création de l'utilisateur incident_user
-- =============================================

-- Créer le login au niveau serveur
IF NOT EXISTS(SELECT * FROM sys.server_principals WHERE name = 'incident_user')
BEGIN
    CREATE LOGIN incident_user WITH PASSWORD = 'MotDePasse123!', 
    CHECK_POLICY = OFF, CHECK_EXPIRATION = OFF;
END
GO

-- Basculer vers la nouvelle base de données
USE IncidentsReseau;
GO

-- Créer l'utilisateur dans la base de données
IF NOT EXISTS(SELECT * FROM sys.database_principals WHERE name = 'incident_user')
BEGIN
    CREATE USER incident_user FOR LOGIN incident_user;
END
GO

-- Attribuer les rôles nécessaires
ALTER ROLE db_datareader ADD MEMBER incident_user;    -- Lecture des données
ALTER ROLE db_datawriter ADD MEMBER incident_user;    -- Écriture des données
ALTER ROLE db_ddladmin ADD MEMBER incident_user;      -- Création/modification de tables
GO

-- =============================================
-- Création de la table incidents
-- =============================================
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='incidents' AND xtype='U')
BEGIN
    CREATE TABLE incidents (
        id INT IDENTITY(1,1) PRIMARY KEY,
        titre NVARCHAR(200) NOT NULL,
        severite NVARCHAR(50) NOT NULL,
        date_incident DATETIME2 NOT NULL DEFAULT GETDATE()
    );
END
GO

-- =============================================
-- Insertion de données d'exemple
-- =============================================
IF NOT EXISTS (SELECT * FROM incidents)
BEGIN
    INSERT INTO incidents (titre, severite, date_incident) VALUES 
    ('Panne serveur principal', 'Critique', '2025-09-20 14:30:00'),
    ('Latence élevée sur le réseau', 'Moyenne', '2025-09-21 09:15:00'),
    ('Connexion intermittente WiFi', 'Faible', '2025-09-22 16:45:00'),
    ('Échec authentification VPN', 'Élevée', '2025-09-23 08:20:00'),
    ('Surcharge bande passante', 'Moyenne', '2025-09-23 11:10:00');
END
GO

-- =============================================
-- Vérification des créations
-- =============================================
PRINT '✅ Base de données créée : IncidentsReseau';
PRINT '✅ Utilisateur créé : incident_user';
PRINT '✅ Table créée : incidents';

-- Afficher les informations de connexion
PRINT '🔗 Paramètres de connexion :';
PRINT '   Serveur: localhost\SQLEXPRESS';
PRINT '   Base: IncidentsReseau';
PRINT '   Utilisateur: incident_user';
PRINT '   Mot de passe: MotDePasse123!';

-- Compter les incidents insérés
SELECT COUNT(*) AS 'Nombre d''incidents créés' FROM incidents;

-- Afficher les incidents
SELECT * FROM incidents ORDER BY date_incident DESC;