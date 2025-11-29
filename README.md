# Analyse des Marchés Publics – Ville de Paris

### Projet DevOps/Data – Test Technique  
**Réalisé par : Islem Ben Aissa – Ingénieure Cloud & DevOps**

---

#  0. Source des données & choix du thème

Dans le cadre du test technique, les candidates et candidats doivent sélectionner un thème parmi les jeux de données mis à disposition par la Ville de Paris :

 **Plateforme OpenData officielle :**  
https://opendata.paris.fr/pages/home/

La plateforme propose des centaines de datasets couvrant :  
- commerce  
- culture  
- environnement  
- mobilité  
- finances publiques  
- infrastructures  
- services urbains, etc.

##  Thème choisi : *Finances publiques – Marchés publics de la Ville de Paris*

J’ai choisi d’analyser les **marchés publics** car ce dataset :

- est structuré (années, montants, fournisseurs…)  
- permet de calculer des KPI réels et concrets  
- a des enjeux pertinents : dépenses publiques, transparence, budget  
- se prête parfaitement à la construction d’un pipeline Data → API → Dashboard  

###  Dataset utilisé  
**Marchés publics de la Ville de Paris (2013–2016)**  
Ce dataset comprend :  
- année de notification  
- numéro du marché  
- objet  
- nature du marché (services, travaux, fournitures)  
- fournisseur  
- montants notifiés  
- périmètre financier  


---

# 1. Présentation du projet

Ce projet consiste à réaliser **une application complète de data visualisation**, basée sur les données OpenData Paris relatives aux *marchés publics* (2013–2016).  
L’objectif est de démontrer une **maîtrise globale du pipeline Data + compétences DevOps** :

* Collecte de données brutes  
* Nettoyage & transformation  
* Stockage dans une base MySQL  
* Exposition via API Flask  
* Dashboard statique HTML/CSS + Chart.js  
* Conteneurisation Docker  
* Orchestration multi-services via Docker Compose  
* Tests automatisés avec Pytest  
* CI GitHub Actions  


---

# 2. Architecture générale

###  Architecture technique (schéma ASCII)

```
                             +--------------------+
                             |   OpenData Paris   |
                             |  (marchés publics) |
                             +---------+----------+
                                       |
                                       v
                         +-----------------------------+
                         |   Traitement Python (ETL)   |
                         | loader.py / processing.py   |
                         +---------------+-------------+
                                         |
                                         v
                          +-----------------------------+
                          |        MySQL (Docker)       |
                          |   Table : marches_publics   |
                          +---------------+-------------+
                                         |
                                         v
                         +-----------------------------+
                         |         Flask API           |
                         |   Génération JSON / API     |
                         +---------------+-------------+
                                         |
                                         v
                    +---------------------------------------+
                    |       Dashboard HTML / CSS / JS       |
                    |  Charts (5 KPI) — Chart.js + JSON     |
                    +---------------------------------------+
```

---

# 3. Structure du repository

```
air-quality-project/
│
├── src/
│   ├── api_client.py        → Récupération API OpenData
│   ├── loader.py            → Chargement MySQL
│   ├── processing.py        → Calcul KPI + JSON
│   ├── analysis.py          → Analyse des datasets
│   ├── app.py               → Flask (serveur web)
│   ├── config.py            → Variables + config MySQL
│   └── main.py              → Script principal (pipeline)
│
├── web/
│   ├── index.html           → Dashboard
│   ├── scripts.js           → Affichage des graphiques
│   ├── styles.css           → UI/UX
│   └── data/*.json          → KPI générés automatiquement
│
├── tests/
│   └── test_app.py          → Test de la route /
│
├── docker-compose.yml       → Multi-services (web + DB)
├── Dockerfile               → Build de l'app Flask
├── requirements.txt         → Dépendances Python
└── README.md                → Documentation 
```

---

# 4. Explication du Backend

##  Collecte des données  
`api_client.py` interroge l’API OpenData Paris pour récupérer les marchés publics.

##  Nettoyage & transformation  
`processing.py` :  
* normalisation des colonnes  
* filtrage des années  
* extraction des KPI  
* génération des fichiers JSON pour le dashboard  

##  Stockage MySQL  
`loader.py` :  
* création de la base `airquality`  
* création de la table `marches_publics`  
* insertion des données nettoyées  

##  API Flask  
`app.py` :  
* route `/` qui sert le dashboard  
* exposition des fichiers JSON depuis `web/data/`  

---

# 5. Explication du Frontend (Dashboard)

Dashboard statique développé avec :  
* **HTML/CSS** pour la mise en page  
* **Chart.js** pour les visualisations  
* **JavaScript** pour charger dynamiquement les données JSON  

### KPI affichés  
 Montant total par année  
 Nombre de marchés par année  
 Répartition par nature de marché  
 Top 10 fournisseurs  
 Montant total par périmètre financier  

---

# 6. Conteneurisation (Docker)

##  Dockerfile  
Le Dockerfile construit l’image du service `marches-web` :

* Basé sur **Python 3.11 slim** (léger et optimisé)
* Installation des dépendances via `requirements.txt`
* Copie du code applicatif (`src/` + `web/`)
* Définition du dossier de travail `/app`
* Exposition du port **5000**
* Commande finale : `python src/app.py`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY web ./web

EXPOSE 5000

CMD ["python", "src/app.py"]
```
Ce conteneur héberge l'API Flask ainsi que la partie dashboard (HTML/JS/CSS).

Commande de lancement : 
```
python src/app.py
```

##  docker-compose.yml  
Deux services sont orchestrés :

* marches-db → MySQL 8 (base de données)

* marches-web → Flask + génération des JSON

Le fichier docker-compose.yml gère :

* le réseau interne

* les variables d’environnement via .env

* l'ordre de démarrage (depends_on)

* un volume persistant MySQL (db_data)

```
db:
  image: mysql:8.0
  environment:
    MYSQL_ROOT_PASSWORD: root
    MYSQL_DATABASE: airquality

web:
  build: .
  depends_on: [db]
  ports: ["5000:5000"]
  env_file: .env
```
##  Visualisation des conteneurs (Docker Desktop)
Après exécution de :
```
docker compose up --build
```
Les trois composants du projet tournent correctement :

* marches-db → MySQL

* marches-web → Flask

* marches-publics-project → Stack Docker Compose

Voici l’affichage dans Docker Desktop :

<img width="1907" height="738" alt="image" src="https://github.com/user-attachments/assets/59db63b4-9198-472c-860a-89360daf5a66" />

---

# 7. CI – Tests automatisés (GitHub Actions)

Un workflow simple exécutant :  
✔ Checkout du code  
✔ Setup Python  
✔ Installation des dépendances  
✔ Lancement de `pytest`

Le test valide que la route `/` retourne bien **200 OK**, garantissant un fonctionnement minimal de l’API.

---

# 8. Comment exécuter le projet

##  Cloner le repo  
```
git clone https://github.com/benaissaislem/Devops-DataOps.git
cd Devops-DataOps
```

##  Lancer Docker Compose  
```
docker compose up --build
```

##  Ouvrir l'application  
http://127.0.0.1:5000

##  Arrêter l'environnement  
```
docker compose down
```

---

# 9. Screenshots du résultat final

### Dashboard final  
<img width="1917" height="981" alt="image" src="https://github.com/user-attachments/assets/d3f5e084-63be-4267-b59a-fd9cb97df6db" />


### Vue MySQL Workbench  
<img width="1918" height="1018" alt="image" src="https://github.com/user-attachments/assets/efa55b8e-fa23-4a3f-861d-348b642dac96" />


---

# 10. Choix techniques & justification

| Technologie | Rôle | Justification |
|------------|------|---------------|
| **Python (requests, pandas)** | ETL | Rapidité, flexibilité, maîtrise totale |
| **MySQL 8** | Stockage | Base stable et utilisée en production |
| **Flask** | API légère | Simple, efficace, parfait pour un test |
| **Chart.js** | Visualisation | Graphiques interactifs, moderne |
| **Docker** | Reproductibilité | Standard DevOps, portable |
| **Docker Compose** | Orchestration | Multi-services facile à déployer |
| **Pytest** | Tests | Assure un minimum de qualité logicielle |
| **GitHub Actions** | CI | Automatisation fiable et standard |

---








