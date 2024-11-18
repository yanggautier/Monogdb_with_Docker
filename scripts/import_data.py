import pandas as pd
from pymongo import MongoClient
import json
import os


def insert_data(file_path, mongodb_uri, db_name, collection_name):
    df = pd.read_csv(file_path)
    # Convertir le DataFrame Pandas à  une list de dictionaries
    records = json.loads(df.to_json(orient='records'))
    
    # Connecter à MongoDB
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Si la collection n'est pas vide, on supprime la collection et recréer
    if collection.count_documents({}) == 0:
        try: 
            collection.drop()
            collection = db[collection_name]
        except Exception as e:
            return e

    # Insertions des données
    result = collection.insert_many(records)
    print(f" {len(result.inserted_ids)} documents insérés")
    client.close()


if __name__ == "__main__":
    file_path = os.getenv("INPUT_DATA_PATH")
    mongodb_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGO_INITDB_DATABASE")
    collection_name = os.getenv("COLLECTION")
    insert_data(file_path, mongodb_uri, db_name, collection_name)


    


