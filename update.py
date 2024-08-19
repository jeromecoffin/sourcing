import streamlit as st
import utils

def agent(agent_data):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    db.agents.update_one({"_id": "user"}, {"$set": agent_data})            
    st.success(_("Data successfully modified!"))
    st.cache_data.clear() # clear cache for language
    st.rerun()

def project(project_data):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    db.projects.update_one({'_id': project['_id']}, {'$set': project_data})
    utils.log_event("Mettre à jour projet", project['title'])
    st.cache_data.clear()
    st.success(_("Project Successfully Updated"))

def categories(supplier, updated_categories):
    db = utils.initialize_mongodb()
    db.suppliers.update_one({'_id': supplier['_id']}, {'$set': {'categories': updated_categories}})

def fields(supplier, updated_fields):
    db = utils.initialize_mongodb()
    db.suppliers.update_one({'_id': supplier['_id']}, {'$set': {'fields': updated_fields}})

def rfi(rfi_data):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    db.rfis.update_one({"title": rfi_data["title"]}, {"$set": rfi_data})            
    st.success(_("Data successfully modified!"))
    st.cache_data.clear() # clear cache for language
    st.rerun()