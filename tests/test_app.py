import os
import sys


CURRENT_DIR = os.path.dirname(__file__)
SRC_PATH = os.path.join(CURRENT_DIR, "..", "src")
sys.path.append(os.path.abspath(SRC_PATH))

from app import app  


def test_index_route():
    """
    Vérifie que la page principale répond en 200.
    """
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
