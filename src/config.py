import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    """
    Configuration de l'application (style 12-Factor App) :
    - tout vient des variables d'environnement
    - aucune info sensible ou spécifique à un environnement n'est codée en dur
    """

    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://opendata.paris.fr")


    DB_HOST: str = os.getenv("DB_HOST", "localhost")  
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "root")
    DB_NAME: str = os.getenv("DB_NAME", "marches_publics")


settings = Settings()
