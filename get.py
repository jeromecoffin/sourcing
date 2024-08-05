from firebase_admin import firestore
import streamlit as st

# Retrieves all RFIs from the Firestore 'rfis' collection.
# Output : List dict all RFI 
@st.cache_data(ttl=3600)
def get_rfis():
    db = firestore.client()
    rfis_ref = db.collection("rfis")
    rfis = [doc.to_dict() for doc in rfis_ref.stream()]
    return rfis

# Retrieves all RFQs from the Firestore 'rfqs' collection.
# Output : List dict all RFQ 
@st.cache_data(ttl=3600)
def get_rfqs():
    db = firestore.client()
    rfqs_ref = db.collection("rfqs")
    rfqs = [doc.to_dict() for doc in rfqs_ref.stream()]
    return rfqs

# Retrieves the language preference for the user from the Firestore 'agents' collection.
# Output : en, vi ou fr
@st.cache_data(ttl=3600)
def get_language():
    db = firestore.client()
    agent_ref = db.collection("agents").document("user")
    agent = agent_ref.get()
    return agent.to_dict()["language"]

# Retrieves all projects from the Firestore 'projects' collection.
# Output : List of dict of all projects
@st.cache_data(ttl=3600)
def get_projects():
    db = firestore.client()
    projects_ref = db.collection("projects")
    projects = []
    for doc in projects_ref.stream():
        project = doc.to_dict()
        project['doc_id'] = doc.id  # Add the document ID
        projects.append(project)
    return projects

# Retrieves onboarding information for clients from the Firestore 'clients' collection.
# Output : List of dict of all clients
@st.cache_data(ttl=3600)
def get_clients():
    db = firestore.client()
    clients_ref = db.collection("clients")
    clients = [doc.to_dict() for doc in clients_ref.stream()]
    return clients

# Retrieves suppliers from Firestore 'suppliers' collection based on selected categories and fields.
# Input : List categories and list fields
# Output : List dict supplier filtered
@st.cache_data(ttl=3600)
def get_suppliers(selected_categories, selected_fields):
    db = firestore.client()
    suppliers_ref = db.collection("suppliers")
    suppliers = []
    for doc in suppliers_ref.stream():
        supplier = doc.to_dict()
        supplier['id'] = doc.id  # Ajout de l'ID du document
        if (not selected_categories or set(supplier.get('categories', [])).intersection(set(selected_categories))) and \
           (not selected_fields or set(supplier.get('fields', [])).intersection(set(selected_fields))):
            suppliers.append(supplier)
    return suppliers

# Retrieves distinct values for a specific field from the Firestore 'suppliers' collection.
@st.cache_data(ttl=3600)
def get_distinct_values_management(field_name):
    db = firestore.client()
    suppliers_ref = db.collection("suppliers")
    values = set()
    for doc in suppliers_ref.stream():
        supplier = doc.to_dict()
        if field_name in supplier:
            for value in supplier[field_name]:
                values.add(value)
    return list(values)