import requests
from typing import List, Dict, Any
from config import settings

DATASET_ID = "liste-des-marches-de-la-collectivite-parisienne"

def fetch_public_procurement_records(max_records: int = 1000, page_size: int = 100) -> List[Dict[str, Any]]:
    """
    Récupère jusqu'à max_records en paginant l'API
    avec un page_size (max 100).
    """
    base_url = settings.API_BASE_URL.rstrip("/")
    url = f"{base_url}/api/explore/v2.1/catalog/datasets/{DATASET_ID}/records"

    all_records: List[Dict[str, Any]] = []
    offset = 0
    page_size = min(page_size, 100)  # sécurité

    while len(all_records) < max_records:
        remaining = max_records - len(all_records)
        limit = min(page_size, remaining)

        params = {
            "limit": limit,
            "offset": offset,
            "order_by": "annee_de_notification"
        }

        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        chunk = data.get("results", [])

        if not chunk:
            break

        all_records.extend(chunk)
        offset += limit

    return all_records
