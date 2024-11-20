import pandas as pd
from pymongo import MongoClient
import json
import os
from datetime import datetime
# from dotenv import load_dotenv



def export_to_json(collection, output_file):
    """
    Exporte une collection MongoDB vers un fichier JSON
    """
    data = list(collection.find({}, {'_id': 0}))
    
    # Gestion des types datetime pour la sérialisation JSON
    def datetime_handler(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=datetime_handler)

    return f"Données exportées vers {output_file}"


if __name__ == "__main__":
    # Connexion à la base de données
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client[os.getenv("MONGO_INITDB_DATABASE")]
    collection = db[os.getenv("COLLECTION")]
    export_to_json(collection, os.getenv("OUTPUT_DATA_PATH"))