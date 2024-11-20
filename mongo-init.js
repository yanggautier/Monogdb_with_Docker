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
db.createCollection("patients");
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