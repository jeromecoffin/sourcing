import streamlit as st
import utils
from bson.objectid import ObjectId

# Define a custom hash function for ObjectId
def hash_objectid(obj):
    return str(obj)

# Access in app, generateXlsx, send_rfi, settings, utils
@st.cache_data(ttl=3600)
def agent(username):

    db = utils.initialize_mongodb()
    collection = db.users
    agent = collection.find_one({"username": username})
    return agent

# Access in generateXlsx, send_rfi, settings, utils
@st.cache_data(ttl=3600, hash_funcs={ObjectId: hash_objectid})
def agent_id(user_id):

    db = utils.initialize_mongodb()
    collection = db.users
    agent = collection.find_one({"_id": user_id})
    return agent

# Access in manage_rfi, send_rfis, utils
# Pas de cache car besoin de relire après send et pas possible de clear cache ou rerun, sinon le lien disparait tout de suite
#@st.cache_data(ttl=3600, hash_funcs={ObjectId: hash_objectid})
def rfis(user_id):

    # Get the list of RFI ObjectIds associated with the user
    list_rfis = list(agent_id(user_id)["rfi_ids"])
    db = utils.initialize_mongodb()

    # Find RFIs that have an _id in the list_rfis
    rfis = list(db.rfis.find({"_id": {"$in": list_rfis}}, {'_id': 0}))
    return rfis

# Access in utils
@st.cache_data(ttl=3600, hash_funcs={ObjectId: hash_objectid})
def language(user_id):

    try:
        db = utils.initialize_mongodb()
        agent = db.users.find_one({'_id': user_id}, {'_id': 0, 'language': 1})

        if agent and 'language' in agent:
            return agent['language']
        else:
            return "en"
        
    except Exception as e:
        print(f"Error: {e}")
        return "en"

# Access in app
def isFirstLogin(user_id):

    db = utils.initialize_mongodb()
    agent = db.users.find_one({'_id': user_id}, {'_id': 0, 'isFirstLogin': 1})
    return agent['isFirstLogin'] if agent else None

