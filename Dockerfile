# Image de base Python légère
FROM python:3.11-slim

# Réglages de base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Répertoire de travail dans le container
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'app
COPY src ./src
COPY web ./web

# Exposer le port Flask
EXPOSE 5000

# Commande de lancement de Flask
CMD ["python", "src/app.py"]
