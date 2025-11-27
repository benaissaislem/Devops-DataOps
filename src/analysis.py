import pymysql
from config import settings

def get_connection():
    return pymysql.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        autocommit=True,
        charset="utf8mb4"
    )

def montant_par_annee():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT annee_notification, SUM(montant_max)
        FROM marches_publics
        GROUP BY annee_notification
        ORDER BY annee_notification;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def montant_par_nature():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT nature_du_marche, SUM(montant_max)
        FROM marches_publics
        GROUP BY nature_du_marche
        ORDER BY SUM(montant_max) DESC;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def top_fournisseurs(limit=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT fournisseur_nom, SUM(montant_max)
        FROM marches_publics
        GROUP BY fournisseur_nom
        ORDER BY SUM(montant_max) DESC
        LIMIT %s;
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows



def nb_marches_par_annee():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT annee_notification, COUNT(*)
        FROM marches_publics
        GROUP BY annee_notification
        ORDER BY annee_notification;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def duree_moyenne_par_nature():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT nature_du_marche, AVG(duree_marche_jours)
        FROM marches_publics
        WHERE duree_marche_jours IS NOT NULL
        GROUP BY nature_du_marche;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def montant_par_perimetre():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT perimetre_financier, SUM(montant_max)
        FROM marches_publics
        GROUP BY perimetre_financier
        ORDER BY SUM(montant_max) DESC;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

