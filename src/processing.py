from typing import Dict, Any, Optional
from datetime import datetime


def _to_float(value: Any) -> Optional[float]:
    if value in (None, "", "NA"):
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _to_int(value: Any) -> Optional[int]:
    if value in (None, "", "NA"):
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _to_datetime(value: Any) -> Optional[datetime]:
    if not value:
        return None
    # format typique : "2021-05-06"
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None



def normalize_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforme un record brut de l'API en dict prêt pour insertion DB.
    """
    return {
        "annee_notification": _to_int(raw.get("annee_de_notification")),
        "num_marche": raw.get("num_marche"),
        "objet_du_marche": raw.get("objet_du_marche"),
        "nature_du_marche": raw.get("nature_du_marche"),
        "fournisseur_nom": raw.get("fournisseur_nom"),
        "fournisseur_siret": raw.get("fournisseur_siret"),
        "fournisseur_code_postal": raw.get("fournisseur_code_postal"),
        "fournisseur_ville": raw.get("fournisseur_ville"),
        "montant_min": _to_float(raw.get("montant_min")),
        "montant_max": _to_float(raw.get("montant_max")),
        "date_notification": _to_datetime(raw.get("date_de_notification")),
        "date_debut": _to_datetime(raw.get("date_de_debut")),
        "date_fin": _to_datetime(raw.get("date_de_fin")),
        "duree_marche_jours": _to_int(raw.get("duree_du_marche_en_jours")),
        "perimetre_financier": raw.get("perimetre_financier"),
        "categorie_achat_cle": raw.get("categorie_d_achat_cle"),
        "categorie_achat_texte": raw.get("categorie_d_achat_texte"),
    }


