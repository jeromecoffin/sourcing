from pymongo import MongoClient
import streamlit as st

# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client.sourcingmain

# Retrieves all RFIs from the MongoDB 'rfis' collection.
# Output: List of dicts of all RFI
@st.cache_data(ttl=3600)
def get_rfis():
    rfis = list(db.rfis.find({}, {'_id': 0}))
    return rfis

# Retrieves all RFQs from the MongoDB 'rfqs' collection.
# Output: List of dicts of all RFQ
@st.cache_data(ttl=3600)
def get_rfqs():
    rfqs = list(db.rfqs.find({}, {'_id': 0}))
    return rfqs

# Retrieves the language preference for the user from the MongoDB 'agents' collection.
# Output: 'en', 'vi' or 'fr'
@st.cache_data(ttl=3600)
def get_language():
    try:
        agent = db.agents.find_one({'_id': 'user'}, {'_id': 0, 'language': 1})
        if agent and 'language' in agent:
            return agent['language']
        else:
            return "en"
    except Exception as e:
        print(f"Error: {e}")
        return "en"

# Retrieves the isFirstLogin status for the user from the MongoDB 'agents' collection.
def get_isFirstLogin():
    agent = db.agents.find_one({'_id': 'user'}, {'_id': 0, 'isFirstLogin': 1})
    return agent['isFirstLogin'] if agent else None

# Retrieves all projects from the MongoDB 'projects' collection.
# Output: List of dicts of all projects
@st.cache_data(ttl=3600)
def get_projects():
    projects = list(db.projects.find({}, {'_id': 1}))
    for project in projects:
        project['doc_id'] = str(project['_id'])  # Add the document ID
        del project['_id']
    return projects

# Retrieves onboarding information for clients from the MongoDB 'clients' collection.
# Output: List of dicts of all clients
@st.cache_data(ttl=3600)
def get_clients():
    clients = list(db.clients.find({}, {'_id': 0}))
    return clients

# Retrieves suppliers from MongoDB 'suppliers' collection based on selected categories and fields.
# Input: List of categories and list of fields
# Output: List of dicts of filtered suppliers
@st.cache_data(ttl=3600)
def get_suppliers(selected_categories, selected_fields):
    query = {}
    if selected_categories:
        query['categories'] = {'$in': selected_categories}
    if selected_fields:
        query['fields'] = {'$in': selected_fields}
    query['remove'] = False
    suppliers = list(db.suppliers.find(query, {'_id': 0}))
    return suppliers

# Retrieves distinct values for a specific field from the MongoDB 'suppliers' collection.
@st.cache_data(ttl=3600)
def get_distinct_values_management(field_name):
    values = db.suppliers.distinct(field_name)
    return values
