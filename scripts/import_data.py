import pandas as pd
from pymongo import MongoClient
import json
import os
from datetime import datetime
from bson import ObjectId, Decimal128

def insert_data(file_path, mongodb_uri, db_name, collection_name):
    df = pd.read_csv(file_path)

    # Connexion à MongoDB
    client = MongoClient(mongodb_uri)
    db = client[db_name]

    collections = ['patient', 'medical', 'admission', 'billing']

    # Initiation de variable pour compter le nombre de patients migrés        
    insert_count = 0

    for _, row in df.iterrows():
        try:
            # Insertion de patient
            patient = {
                "name": row['Name'],
                "age": int(row['Age']),
                "gender": row['Gender'],
                "bloodType": row['Blood Type']
            }
            patient_result = db.patient.insert_one(patient)
            patient_id = patient_result.inserted_id

            # Insertion données médicales
            medical = {
                "patientId": patient_id,
                "condition": row['Medical Condition'],
                "medication": row['Medication'],
                "testResults": row['Test Results'],
                "doctor": row['Doctor']
            }
            db.medical.insert_one(medical)

            # Insertion admission
            admission = {
                "patientId": patient_id,
                "dateOfAdmission": datetime.strptime(row['Date of Admission'], '%Y-%m-%d'),
                "dischargeDate": datetime.strptime(row['Discharge Date'], '%Y-%m-%d') if pd.notna(row['Discharge Date']) else None,
                "admissionType": row['Admission Type'],
                "roomNumber": int(row['Room Number']),
                "hospital": row['Hospital']
            }
            db.admission.insert_one(admission)

            # Insertion facturation
            billing = {
                "patientId": patient_id,
                "insuranceProvider": row['Insurance Provider'],
                "amount": Decimal128(str(row['Billing Amount']))  # Conversion en Decimal128
            }
            db.billing.insert_one(billing)
            
            insert_count += 1

        except Exception as e:
            print(f"Erreur lors de l'insertion de la ligne {insert_count + 1}: {e}")
            continue
    
    print(f"{insert_count} patients insérés avec leurs données associées")

    # Vérification des insertions
    print("\nStatistiques des collections:")
    for collection_name in collections:
        count = db[collection_name].count_documents({})
        print(f"Collection {collection_name}: {count} documents")
    
    client.close()


if __name__ == "__main__":
    file_path = os.getenv("INPUT_DATA_PATH")
    mongodb_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGO_INITDB_DATABASE")
    collection_name = os.getenv("COLLECTION")

    try:
        insert_data(file_path, mongodb_uri, db_name, collection_name)
    except Exception as e:
        print(f"Erreur lors de l'insertion : {e}")


    


