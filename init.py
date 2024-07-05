import firebase_admin
from firebase_admin import credentials, firestore

# Initialiser Firebase
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Ajouter des données de base
def initialize_data():
    # Fournisseurs de base
    suppliers = [
        {"name": "Supplier A", "email": "suppliera@example.com", "phone": "+1234567890", "address": "123 Street, City, Country"},
        {"name": "Supplier B", "email": "supplierb@example.com", "phone": "+0987654321", "address": "456 Avenue, City, Country"}
    ]

    # Documents RFI de base
    rfis = [
        {"title": "RFI 1", "content": "Request for information 1", "due_date": "2023-07-31", "user_id": "user1", "creation_date": "2023-07-01", "status": "Open"},
        {"title": "RFI 2", "content": "Request for information 2", "due_date": "2023-08-15", "user_id": "user2", "creation_date": "2023-07-01", "status": "Open"}
    ]

    # Documents RFQ de base
    rfqs = [
        {"title": "RFQ 1", "content": "Request for quotation 1", "due_date": "2023-07-20", "budget": 10000, "user_id": "user1", "creation_date": "2023-07-01", "status": "Open"},
        {"title": "RFQ 2", "content": "Request for quotation 2", "due_date": "2023-08-05", "budget": 20000, "user_id": "user2", "creation_date": "2023-07-01", "status": "Open"}
    ]

    # Ajouter les fournisseurs à Firebase
    for supplier in suppliers:
        db.collection("suppliers").add(supplier)

    # Ajouter les RFIs à Firebase
    for rfi in rfis:
        db.collection("rfis").add(rfi)

    # Ajouter les RFQs à Firebase
    for rfq in rfqs:
        db.collection("rfqs").add(rfq)

    print("Initial data added to Firebase.")

# Initialiser les données
initialize_data()
