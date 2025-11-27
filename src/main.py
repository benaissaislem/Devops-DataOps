# from analysis import montant_par_annee, montant_par_nature, top_fournisseurs
from analysis import (
    montant_par_annee,
    montant_par_nature,
    top_fournisseurs,
    nb_marches_par_annee,
    montant_par_perimetre,
)

from config import settings
from api_client import fetch_public_procurement_records
from processing import normalize_record
from loader import init_db, insert_records
from export_data import export_all


def main():
    print("App démarrée ")
    print("API_BASE_URL =", settings.API_BASE_URL)

    # 1) init DB
    print("Initialisation de la base MySQL...")
    init_db()
    print("OK \n")

    # 2) fetch API
    # print("Récupération des marchés publics...")
    # raw_records = fetch_public_procurement_records(limit=50)  # par ex. 200
    # print(f"Nombre de lignes récupérées : {len(raw_records)}")
    raw_records = fetch_public_procurement_records(max_records=5000)
    print(f"Nombre de lignes récupérées : {len(raw_records)}")


    # 3) normalisation
    normalized = [normalize_record(r) for r in raw_records]
    print(f"Nombre de lignes prêtes pour insertion : {len(normalized)}")

     

    # 4) insertion
    print("Insertion en base...")
    insert_records(normalized)
    print("Insertion terminée")

    print("\n=== Analyse : montant total par année ===")
    print(montant_par_annee())

    print("\n=== Analyse : montant total par nature de marché ===")
    print(montant_par_nature())

    print("\n=== Analyse : top 10 des fournisseurs par montant ===")
    print(top_fournisseurs(10))

    print("\n=== Analyse : nombre de marchés par année ===")
    print(nb_marches_par_annee())

    print("\n=== Analyse : montant par périmètre financier ===")
    print(montant_par_perimetre())


    print("\nExport des données d'analyse pour la dataviz...")
    export_all()
    print("Export terminé.")



if __name__ == "__main__":
    main()
