from typing import List, Dict, Any
import pymysql
from pymysql.cursors import DictCursor
from config import settings


def get_connection():
    return pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        cursorclass=DictCursor,
        charset="utf8mb4",
        autocommit=True,
    )


def init_db():
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS marches_publics (
        id INT AUTO_INCREMENT PRIMARY KEY,
        annee_notification INT,
        num_marche VARCHAR(50),
        objet_du_marche TEXT,
        nature_du_marche VARCHAR(50),
        fournisseur_nom VARCHAR(255),
        fournisseur_siret VARCHAR(20),
        fournisseur_code_postal VARCHAR(10),
        fournisseur_ville VARCHAR(100),
        montant_min DECIMAL(15,2),
        montant_max DECIMAL(15,2),
        date_notification DATETIME NULL,
        date_debut DATETIME NULL,
        date_fin DATETIME NULL,
        duree_marche_jours INT,
        perimetre_financier VARCHAR(50),
        categorie_achat_cle VARCHAR(20),
        categorie_achat_texte VARCHAR(255)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(create_table_sql)
    finally:
        conn.close()


def insert_records(records: List[Dict[str, Any]]):
    if not records:
        return

    sql = """
    INSERT INTO marches_publics (
        annee_notification,
        num_marche,
        objet_du_marche,
        nature_du_marche,
        fournisseur_nom,
        fournisseur_siret,
        fournisseur_code_postal,
        fournisseur_ville,
        montant_min,
        montant_max,
        date_notification,
        date_debut,
        date_fin,
        duree_marche_jours,
        perimetre_financier,
        categorie_achat_cle,
        categorie_achat_texte
    )
    VALUES (
        %(annee_notification)s,
        %(num_marche)s,
        %(objet_du_marche)s,
        %(nature_du_marche)s,
        %(fournisseur_nom)s,
        %(fournisseur_siret)s,
        %(fournisseur_code_postal)s,
        %(fournisseur_ville)s,
        %(montant_min)s,
        %(montant_max)s,
        %(date_notification)s,
        %(date_debut)s,
        %(date_fin)s,
        %(duree_marche_jours)s,
        %(perimetre_financier)s,
        %(categorie_achat_cle)s,
        %(categorie_achat_texte)s
    );
    """

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.executemany(sql, records)
    finally:
        conn.close()
