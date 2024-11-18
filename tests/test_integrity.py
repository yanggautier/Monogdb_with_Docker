import unittest
from pymongo import MongoClient
import pandas as pd
import numpy as np
from typing import List, Dict, Any
import os

# from dotenv import load_dotenv
# load_dotenv()

class DataIntegrityTest(unittest.TestCase):
    def setUp(self):
        # Chemin vers le fichier CSV source
        self.csv_path = os.getenv("INPUT_DATA_PATH")
        
        # Connexion à la base MongoDB cible
        self.client_target = MongoClient(os.getenv('MONGODB_URI'))
        self.db_target = self.client_target[os.getenv('MONGO_INITDB_DATABASE')]
        self.collection_target = self.db_target[os.getenv('COLLECTION')]
        
        # Charger les données CSV
        self.df_source = pd.read_csv(self.csv_path)
        
        # Convertir les types de données pandas en types Python standards
        self.df_source = self.df_source.replace({np.nan: None})

    def tearDown(self):
        self.client_target.close()

    def get_csv_schema(self) -> Dict[str, str]:
        """Extraire le schéma du DataFrame source"""
        schema = {}
        for column, dtype in self.df_source.dtypes.items():
            # Convertir les types pandas en types Python
            if pd.api.types.is_integer_dtype(dtype):
                schema[column] = 'int'
            elif pd.api.types.is_float_dtype(dtype):
                schema[column] = 'float'
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                schema[column] = 'datetime'
            elif pd.api.types.is_bool_dtype(dtype):
                schema[column] = 'bool'
            else:
                schema[column] = 'str'
        return schema

    def get_mongo_schema(self) -> Dict[str, str]:
        """Extraire le schéma de la collection MongoDB"""
        sample_doc = self.collection_target.find_one()
        if not sample_doc:
            return {}
            
        schema = {}
        def extract_type(value):
            if value is None:
                return 'null'
            elif isinstance(value, dict):
                return 'object'
            elif isinstance(value, bool):
                return 'bool'
            elif isinstance(value, int):
                return 'int'
            elif isinstance(value, float):
                return 'float'
            elif isinstance(value, str):
                return 'str'
            return type(value).__name__
        
        for field, value in sample_doc.items():
            if field != '_id':
                schema[field] = extract_type(value)
        return schema

    def test_file_existence(self):
        """Vérifier que le fichier CSV existe"""
        self.assertTrue(
            os.path.exists(self.csv_path),
            f"Le fichier CSV {self.csv_path} n'existe pas"
        )

    def test_column_presence(self):
        """Vérifier que toutes les colonnes sont présentes après migration"""
        csv_columns = set(self.df_source.columns)
        mongo_schema = self.get_mongo_schema()
        mongo_columns = set(mongo_schema.keys())
        
        self.assertEqual(
            csv_columns,
            mongo_columns,
            "Les colonnes ne correspondent pas entre le CSV et MongoDB"
        )

    def test_data_types(self):
        """Vérifier que les types de données sont cohérents"""
        csv_schema = self.get_csv_schema()
        mongo_schema = self.get_mongo_schema()
        
        for column in csv_schema:
            csv_type = csv_schema[column]
            mongo_type = mongo_schema[column]
            
            # Vérification de compatibilité des types
            if csv_type in ['int', 'float'] and mongo_type in ['int', 'float']:
                # Les types numériques sont compatibles
                continue 
            
            self.assertEqual(
                csv_type,
                mongo_type,
                f"Le type de la colonne {column} ne correspond pas"
            )

    def test_record_count(self):
        """Vérifier que le nombre d'enregistrements est identique"""
        csv_count = len(self.df_source)
        mongo_count = self.collection_target.count_documents({})
        
        self.assertEqual(
            csv_count,
            mongo_count,
            "Le nombre d'enregistrements ne correspond pas"
        )

    def test_duplicates(self):
        """Vérifier les doublons"""
        def get_csv_duplicates(df, columns=None):
            if columns is None:
                columns = df.columns.tolist()
            return len(df[df.duplicated(subset=columns, keep=False)])

        def get_mongo_duplicates(collection, fields=None):
            if fields is None:
                sample_doc = collection.find_one()
                fields = [field for field in sample_doc.keys() if field != '_id']
            
            pipeline = [
                {"$group": {
                    "_id": {field: f"${field}" for field in fields},
                    "count": {"$sum": 1}
                }},
                {"$match": {"count": {"$gt": 1}}}
            ]
            duplicates = list(collection.aggregate(pipeline))
            total_duplicates = sum(doc['count'] for doc in duplicates)
            return total_duplicates

        # Comparer les doublons en excluant l'_id MongoDB
        csv_duplicates = get_csv_duplicates(self.df_source)
        mongo_duplicates = get_mongo_duplicates(self.collection_target)
        
        self.assertEqual(
            csv_duplicates,
            mongo_duplicates,
            "Le nombre de doublons ne correspond pas"
        )

    def test_null_values(self):
        """Vérifier les valeurs nulles pour chaque colonne"""
        def count_csv_nulls(df):
            return df.isnull().sum().to_dict()

        def count_mongo_nulls(collection):
            null_counts = {}
            for field in self.get_mongo_schema().keys():
                null_count = collection.count_documents({field: None})
                null_counts[field] = null_count
            return null_counts

        csv_nulls = count_csv_nulls(self.df_source)
        mongo_nulls = count_mongo_nulls(self.collection_target)
        
        # Comparer les valeurs nulles pour chaque colonne
        for column in csv_nulls:
            self.assertEqual(
                csv_nulls[column],
                mongo_nulls[column],
                f"Le nombre de valeurs nulles ne correspond pas pour la colonne {column}"
            )

if __name__ == '__main__':
    unittest.main()