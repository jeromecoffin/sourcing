import streamlit as st
import utils

@st.cache_data(ttl=3600)
def agent():
    db = utils.initialize_mongodb()
    collection = db.agents
    agent = collection.find_one({"_id": "user"})
    return agent

@st.cache_data(ttl=3600)
def projects():
    db = utils.initialize_mongodb()
    projects = list(db.projects.find())
    for project in projects:
        project['doc_id'] = str(project['_id'])  # Add the document ID
        del project['_id']
    return projects

@st.cache_data(ttl=3600)
def rfis():
    db = utils.initialize_mongodb()
    rfis = list(db.rfis.find({}, {'_id': 0}))
    return rfis

@st.cache_data(ttl=3600)
def rfqs():
    db = utils.initialize_mongodb()
    rfqs = list(db.rfqs.find({}, {'_id': 0}))
    return rfqs

@st.cache_data(ttl=3600)
def clients():
    db = utils.initialize_mongodb()
    clients = list(db.clients.find({}, {'_id': 0}))
    return clients

@st.cache_data(ttl=3600)
def suppliers(selected_categories, selected_fields):
    query = {}
    if selected_categories:
        query['categories'] = {'$in': selected_categories}
    if selected_fields:
        query['fields'] = {'$in': selected_fields}
    query['remove'] = False
    #print(f"Query: {query}")
    db = utils.initialize_mongodb()
    suppliers = list(db.suppliers.find(query, {'_id': 0}))
    return suppliers

@st.cache_data(ttl=3600)
def language():
    try:
        db = utils.initialize_mongodb()
        agent = db.agents.find_one({'_id': 'user'}, {'_id': 0, 'language': 1})
        if agent and 'language' in agent:
            return agent['language']
        else:
            return "en"
    except Exception as e:
        print(f"Error: {e}")
        return "en"

def isFirstLogin():
    db = utils.initialize_mongodb()
    agent = db.agents.find_one({'_id': 'user'}, {'_id': 0, 'isFirstLogin': 1})
    return agent['isFirstLogin'] if agent else None

# Retrieves distinct values for a specific field from the MongoDB 'suppliers' collection.
@st.cache_data(ttl=3600)
def distinct_values_management(field_name):
    db = utils.initialize_mongodb()
    values = db.suppliers.distinct(field_name)
    return values
