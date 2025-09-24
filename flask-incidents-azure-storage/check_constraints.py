#!/usr/bin/env python3
"""
Script pour vérifier les contraintes de la base de données
"""

import os
import pyodbc
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def check_database_constraints():
    """Vérifier les contraintes de la base de données"""
    try:
        # Configuration de la connexion
        connection_string = f"""
        DRIVER={{ODBC Driver 18 for SQL Server}};
        SERVER={os.getenv('AZURE_SQL_SERVER')};
        DATABASE={os.getenv('AZURE_SQL_DATABASE')};
        UID={os.getenv('AZURE_SQL_USERNAME')};
        PWD={os.getenv('AZURE_SQL_PASSWORD')};
        Encrypt=yes;
        TrustServerCertificate=no;
        Connection Timeout=30;
        """
        
        print("🔍 Connexion à Azure SQL Database...")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # 1. Vérifier les contraintes CHECK sur la table incidents
        print("\n📋 Contraintes CHECK sur la table incidents:")
        check_constraints_query = """
        SELECT 
            cc.CONSTRAINT_NAME,
            cc.CHECK_CLAUSE
        FROM INFORMATION_SCHEMA.CHECK_CONSTRAINTS cc
        INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE ctu
            ON cc.CONSTRAINT_NAME = ctu.CONSTRAINT_NAME
        WHERE ctu.TABLE_NAME = 'incidents'
        """
        
        cursor.execute(check_constraints_query)
        constraints = cursor.fetchall()
        
        for constraint in constraints:
            print(f"   Contrainte: {constraint[0]}")
            print(f"   Règle: {constraint[1]}")
            print()
        
        # 2. Vérifier les valeurs existantes dans la colonne severite
        print("\n📊 Valeurs existantes dans la colonne 'severite':")
        existing_values_query = """
        SELECT DISTINCT severite, COUNT(*) as count
        FROM incidents 
        GROUP BY severite
        ORDER BY count DESC
        """
        
        cursor.execute(existing_values_query)
        existing_values = cursor.fetchall()
        
        for value in existing_values:
            print(f"   '{value[0]}' - {value[1]} incident(s)")
        
        # 3. Vérifier la structure de la table
        print("\n🏗️ Structure de la table incidents:")
        structure_query = """
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            CHARACTER_MAXIMUM_LENGTH,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'incidents'
        ORDER BY ORDINAL_POSITION
        """
        
        cursor.execute(structure_query)
        columns = cursor.fetchall()
        
        for col in columns:
            nullable = "NULL" if col[2] == "YES" else "NOT NULL"
            length = f"({col[3]})" if col[3] else ""
            default = f"DEFAULT {col[4]}" if col[4] else ""
            print(f"   {col[0]}: {col[1]}{length} {nullable} {default}")
        
        cursor.close()
        conn.close()
        print("\n✅ Vérification terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    check_database_constraints()