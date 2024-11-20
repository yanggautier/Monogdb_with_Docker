# MongoDB Dockerized Application avec Tests Python

Application de traitement de données utilisant MongoDB dans un conteneur Docker, 
accompagnée de tests unitaires en Python avec pymongo,
elle importe les données qui sont dans un fichier en format csv dans une collection de la base de données NoSQL Mongodb(service dans un container Docker) 
et puis extraire les données qui se trouve dans la collection dans un fichier en formation json.

## Fonctionnalités

Configuration MongoDB via Docker-compose
Import de données CSV vers JSON

Tests unitaires pour:
- Connexion à MongoDB
- Opérations CRUD
- Intégrité des données

Export des données au format JSON

## Technologies

- Docker & Docker-compose
- MongoDB
- Python (pymongo)
- unittest
- pandas

## Structure

```
project/
        ├── Dockerfile
        ├── README.md
        ├── docker-compose.yml
        ├── mongo-init.js
        ├── requirements.txt
        ├── .env
        ├── data
        │   ├── healthcare_dataset.csv
        │   └── healthcare_dataset.json
        ├── scripts
        │   ├── export_data.py
        │   └── import_data.py
        └── tests
            ├── test_connection.py
            ├── test_integrity.py
            └── test_operation.py
```

## Installation

1. Modifier le `.env.sample` en fichier `.env`
2. Mettre les valeurs des variables d'environnement dans le fichier `.env`

Utiliser la commande pour lancer le programme
```bash
docker-compose up -d
```

Suppression des containers des services qui se trouve le docker-compose ainsi que les volumes
```bash
docker-compose down -v
```

## Rôle

- Le rôle `root` est le super-administrateur dans MongoDB, il est le rôle le plus puissant dans MongoDB. 
  Voici ses caractéristiques principales :

    Privilèges accordés :
    - Accès total à toutes les ressources
    - Gestion complète des utilisateurs et rôles
    - Accès à toutes les bases de données
    - Administration complète du cluster
    - Possibilité de réaliser des opérations de maintenance

    Ici nous l'avons crée ce rôle au moment de création de container de service MongoDB

- Le rôle `dbAdmin` permet de gérer les collections (créer, supprimer et modifier) et gérer les index, 
  on l'a attribué à l'utilisateur dans le script d'initialisation de base de données mongodb.

- Le rôle `dbAdmin` permet de lecture et d'écriture de données, 
  on l'a attribué à l'utilisateur dans le script d'initialisation de base de données mongodb.

## Authentification

Les nom d'utilisateur et mot de passe sont définis dans le fichier `.env`
On utilise ces 2 paramètres dans l'uri `MONGODB_URI`  pour connecter à Mongodb