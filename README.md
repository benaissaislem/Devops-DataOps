# Analyse des Marchés Publics – Ville de Paris

### Projet DevOps/Data – Test Technique

**Réalisé par : Islem Ben Aissa – Ingénieure Cloud & DevOps**


# 0. Source des données & choix du thème

Dans le cadre de ce test technique, j’ai choisi un thème à partir des jeux de données publics fournis par la Ville de Paris.

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

#  3. Structure du repository

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

### ✔ Collecte des données

`api_client.py` interroge l’API OpenData Paris pour récupérer les marchés publics.

### ✔ Nettoyage & transformation

`processing.py` :

* normalisation des colonnes
* filtrage des années
* extraction des KPI
* génération des fichiers JSON pour le dashboard

### ✔ Stockage MySQL

`loader.py` :

* création de la base `airquality`
* création de la table `marches_publics`
* insertion des données nettoyées

### ✔ API Flask

`app.py` :

* route `/` qui sert le dashboard
* exposition des données JSON depuis `web/data/`

---

# 📌 5. Explication du Frontend (Dashboard)

Dashboard statique :

* **HTML/CSS** pour la mise en page
* **Chart.js** pour les graphiques
* **JavaScript** pour charger les JSON produits par Python

Les KPI affichés :

1. Montant total par année
2. Nombre de marchés par année
3. Répartition par nature de marché
4. Top 10 fournisseurs
5. Montant total par périmètre financier

 Résultat : une interface propre, moderne et responsive.

---

# 6. Conteneurisation (Docker)

### ✔ Dockerfile (Flask)

* Python 3.11 slim
* Installation des dépendances
* Copie du code
* Exposition du port 5000
* Commande `python src/app.py`

### ✔ docker-compose.yml

2 services :

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

Un volume MySQL assure la persistance des données.

---

# 7. CI – Tests automatisés (GitHub Actions)

Workflow `.github/workflows/tests.yml` :

* Checkout du code
* Setup Python
* Installation des dépendances
* Lancement de `pytest`

 Le test vérifie que la route `/` de Flask répond correctement (**200 OK**).

Cela garantit la stabilité minimale de l’application.

---

#  8. Comment exécuter le projet

### 👉 1. Cloner le repo

```
git clone https://github.com/benaissaislem/Devops-DataOps.git
cd Devops-DataOps
```

###  2. Lancer Docker Compose

```
docker compose up --build
```

###  3. Ouvrir l'application

[http://127.0.0.1:5000](http://127.0.0.1:5000)

###  4. Arrêter l'environnement

```
docker compose down
```

---

# 📌 9. Screenshots du résultat final

###  Dashboard final

*(capture complète que tu as fournie)*

![Dashboard](./web/dashboard_full.png) *(Tu renommeras l'image et tu la mettras dans le repo si tu veux.)*

### 💾 Base MySQL (Workbench)

<img width="1918" height="976" alt="image" src="https://github.com/user-attachments/assets/d26ba40a-cf04-41e0-9732-4916fc6a7b0c" />


---

# 10. Choix techniques & justification

| Technologie                   | Rôle             | Justification                             |
| ----------------------------- | ---------------- | ----------------------------------------- |
| **Python (requests, pandas)** | ETL              | Fiable, rapide, maîtrise totale           |
| **MySQL 8**                   | Stockage durable | Stable & largement utilisé en entreprise  |
| **Flask**                     | Serveur léger    | Simple, rapide, adapté au test technique  |
| **Chart.js**                  | Visualisation    | Graphiques modernes et faciles à intégrer |
| **Docker**                    | Reproductibilité | Pipeline portable & standard DevOps       |
| **Docker Compose**            | Orchestration    | Multi-services cohérents                  |
| **Pytest**                    | QA               | Tester l'app ↑ crédibilité                |
| **GitHub Actions**            | CI               | Automatisation & standard entreprise      |



---

# 12. Auteur

**Islem Ben Aissa**
Ingénieure Cloud & DevOps
📧 [benaissa.isslem@gmail.com](mailto:benaissa.isslem@gmail.com)
🔗 [https://www.linkedin.com/in/islem-b-aissa](https://www.linkedin.com/in/islem-b-aissa)






