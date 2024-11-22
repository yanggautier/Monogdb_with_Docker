import pandas as pd
from pymongo import MongoClient
import json
import os
from datetime import datetime
from bson import ObjectId, Decimal128

# from dotenv import load_dotenv

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, Decimal128):
            return float(obj.to_decimal())
        return json.JSONEncoder.default(self, obj)
    

def export_to_json(db, output_file):
    """
    Exporte une collection MongoDB vers un fichier JSON
    """

    # Initialisation du dictionnaire pour stocker toutes les données
    all_data = []

    patients = db.patient.find({})
    
    for patient in patients:
        patient_id = patient['_id']
        
        # Récupération des données médicales associées
        medical_data = db.medical.find_one({"patientId": patient_id})
        # Récupération des données d'admission
        admission_data = db.admission.find_one({"patientId": patient_id})
        # Récupération des données de facturation
        billing_data = db.billing.find_one({"patientId": patient_id})
        
        # Construction de l'objet patient complet
        patient_complete = {
            "patient": {
                "name": patient.get('name'),
                "age": patient.get('age'),
                "gender": patient.get('gender'),
                "bloodType": patient.get('bloodType'),
                "medical": {
                    "condition": medical_data.get('condition') if medical_data else None,
                    "medication": medical_data.get('medication') if medical_data else None,
                    "testResults": medical_data.get('testResults') if medical_data else None,
                    "doctor": medical_data.get('doctor') if medical_data else None
                },
                "admission": {
                    "dateOfAdmission": admission_data.get('dateOfAdmission') if admission_data else None,
                    "dischargeDate": admission_data.get('dischargeDate') if admission_data else None,
                    "admissionType": admission_data.get('admissionType') if admission_data else None,
                    "roomNumber": admission_data.get('roomNumber') if admission_data else None,
                    "hospital": admission_data.get('hospital') if admission_data else None
                },
                "billing": {
                    "insuranceProvider": billing_data.get('insuranceProvider') if billing_data else None,
                    "amount": billing_data.get('amount') if billing_data else None
                }
            }
        }
        
        all_data.append(patient_complete)
    
    print(f"Nombre de ligne de patient dans la variable str{len(all_data)}")

    # Écriture dans le fichier JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, cls=JSONEncoder, ensure_ascii=False, indent=2)
    print(f"Exportation réussie ! {len(all_data)} patients exportés vers {output_file}")


if __name__ == "__main__":
    # Connexion à la base de données
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client[os.getenv("MONGO_INITDB_DATABASE")]
    try:
        export_to_json(db, os.getenv("OUTPUT_DATA_PATH"))
    except Exception as e:
        print(f"Erreur lors de l'exportation : {e}")
    finally:
        client.close()