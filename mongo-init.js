db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

// Création d'utilisateur d'application avec des permissions 
db.createUser({
    user: process.env.MONGO_APP_USER,
    pwd: process.env.MONGO_APP_PASSWORD,
    roles: [
        {
            role: "readWrite",
            db: process.env.MONGO_INITDB_DATABASE
        },
        {
            role: "dbAdmin",
            db: process.env.MONGO_INITDB_DATABASE
        },
        {
            role: "readWrite",
            db: "test_database"
        },
        {
            role: "dbAdmin",
            db: "test_database"
        }
    ],
    mechanisms: ["SCRAM-SHA-256"]  // Utilise SHA-256 pour le hachage
});

// Création des collections qu'on a besoin
db.createCollection("patients",{
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["name", "age", "gender", "admissionDate"],
            properties: {
                name: {
                    bsonType: "string",
                    description: "Patient's full name"
                },
                age: {
                    bsonType: "int",
                    minimum: 0,
                    maximum: 120
                },
                gender: {
                    bsonType: "string",
                    enum: ["Male", "Female", "Other"]
                },
                bloodType: {
                    bsonType: "string",
                    pattern: "^(A|B|AB|O)[+-]$"
                },
                medicalCondition: {
                    bsonType: "string"
                },
                admissionDate: {
                    bsonType: "date"
                },
                doctor: {
                    bsonType: "string"
                },
                hospital: {
                    bsonType: "string"
                },
                insuranceProvider: {
                    bsonType: "string"
                },
                billingAmount: {
                    bsonType: "decimal"
                },
                roomNumber: {
                    bsonType: "int",
                    minimum: 1
                },
                admissionType: {
                    bsonType: "string",
                    enum: ["Emergency", "Scheduled", "Transfer"]
                },
                dischargeDate: {
                    bsonType: "date"
                },
                medication: {
                    bsonType: "string"
                },
                testResults: {
                    bsonType: "string"
                }
            }
        }
    }
});

db.createCollection("test_collection");  // La collection pour faire des  

// Optional: Create any necessary indexes
db.patients.createIndex({ "patientId": 1 }, { unique: true });

// Ajout des rôls pour des collections spécifiques
db.grantRolesToUser(
    process.env.MONGO_APP_USER,
    [
        { role: "readWrite", db: process.env.MONGO_INITDB_DATABASE }
    ]
);