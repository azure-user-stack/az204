-- Script pour activer SQL Server Authentication (Mode mixte)
-- Fichier: enable_sql_authentication.sql
-- ATTENTION: Ce script nécessite des privilèges administrateur

USE master;
GO

-- Activer le mode mixte (Windows + SQL Server Authentication)
EXEC xp_instance_regwrite 
    N'HKEY_LOCAL_MACHINE', 
    N'Software\Microsoft\MSSQLServer\MSSQLServer', 
    N'LoginMode', 
    REG_DWORD, 
    2;  -- 1 = Windows Auth only, 2 = Mixed Mode

-- Créer l'utilisateur avec les bonnes permissions
IF NOT EXISTS(SELECT * FROM sys.server_principals WHERE name = 'incident_user')
BEGIN
    CREATE LOGIN incident_user WITH PASSWORD = 'MotDePasse123!', 
    CHECK_POLICY = OFF, CHECK_EXPIRATION = OFF;
    PRINT 'Login incident_user créé avec succès';
END
ELSE
BEGIN
    -- Modifier le mot de passe si le login existe
    ALTER LOGIN incident_user WITH PASSWORD = 'MotDePasse123!';
    PRINT 'Mot de passe du login incident_user mis à jour';
END

-- S'assurer que le login n'est pas désactivé
ALTER LOGIN incident_user ENABLE;

PRINT '⚠️  IMPORTANT: Vous devez redémarrer le service SQL Server pour que les changements prennent effet !';
PRINT '💡 Commande PowerShell: Restart-Service "MSSQL$SQLEXPRESS"';