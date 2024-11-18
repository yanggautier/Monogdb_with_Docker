from pymongo import MongoClient, errors
import os
import unittest

# from dotenv import load_dotenv
# load_dotenv()


class TestConnection(unittest.TestCase):
    def setUp(self):
            """Configuration initiale avant chaque test"""
            self.uri = os.getenv('MONGODB_URI')
            self.db_name = os.getenv('MONGO_INITDB_DATABASE')
            
    def test_real_connection(self):
        """Test d'une vraie connexion à MongoDB"""
        print("-------------------------- My test --------------------------")
        try:
            # Tentative de connexion
            client = MongoClient(self.uri, serverSelectionTimeoutMS=2000)

            # Force une connexion en exécutant une commande
            client.admin.command('ping')

            # Si on arrive ici, la connexion est réussie
            self.assertTrue(True)
            
        except errors.ConnectionFailure:
            self.fail("La connexion à MongoDB a échoué")
            
        finally:
            if 'client' in locals():
                client.close()
                
    def test_database_creation(self):
        """Test de création d'une base de données"""
        try:
            client = MongoClient(self.uri)
            db = client[self.db_name]
            
            # Création d'une collection pour tester
            collection = db.test_collection
            result = collection.insert_one({"test": "data"})
            
            # Vérification que l'insertion a fonctionné
            self.assertTrue(result.inserted_id is not None)
            
            # Nettoyage
            client.drop_database(self.db_name)
            
        finally:
            if 'client' in locals():
                client.close()


if __name__ == '__main__':
    unittest.main()