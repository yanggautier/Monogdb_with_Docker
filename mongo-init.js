db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

// Create application user with more permissions
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
    ]
});

// Create the collections you need
db.createCollection("patients");
db.createCollection("test_collection");  // Add this if you need this collection

// Optional: Create any necessary indexes
db.patients.createIndex({ "patientId": 1 }, { unique: true });

// Additional permissions for specific collections
db.grantRolesToUser(
    process.env.MONGO_APP_USER,
    [
        { role: "readWrite", db: process.env.MONGO_INITDB_DATABASE }
    ]
);