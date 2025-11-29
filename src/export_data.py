import json
import os
from analysis import (
    montant_par_annee,
    montant_par_nature,
    top_fournisseurs,
    nb_marches_par_annee,
    montant_par_perimetre,
)

OUTPUT_DIR = "web/data"


def export_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1) Montant total par année
    data = montant_par_annee()
    out = [{"annee": row[0], "montant": float(row[1])} for row in data]
    with open(f"{OUTPUT_DIR}/montant_par_annee.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4)

    # 2) Nombre de marchés par année
    data = nb_marches_par_annee()
    out = [{"annee": row[0], "nb_marches": int(row[1])} for row in data]
    with open(f"{OUTPUT_DIR}/nb_marches_par_annee.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4)

    # 3) Montant total par nature de marché
    data = montant_par_nature()
    out = [{"nature": row[0], "montant": float(row[1])} for row in data]
    with open(f"{OUTPUT_DIR}/montant_par_nature.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4)

    # 4) Top 10 fournisseurs par montant
    data = top_fournisseurs()
    out = [{"fournisseur": row[0], "montant": float(row[1])} for row in data]
    with open(f"{OUTPUT_DIR}/top_fournisseurs.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4)

    # 5) Montant total par périmètre financier
    data = montant_par_perimetre()
    out = [{"perimetre": row[0], "montant": float(row[1])} for row in data]
    with open(f"{OUTPUT_DIR}/montant_par_perimetre.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4)

    print("Fichiers exportés dans web/data/")
