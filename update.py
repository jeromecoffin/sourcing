import streamlit as st
import utils

def agent(agent_data):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    db.agents.update_one({"user_id": "user"}, {"$set": agent_data})            
    st.success(_("Data successfully modified!"))
    st.cache_data.clear() # clear cache for language
    st.experimental_rerun()

def project(project_data):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    db.projects.update_one({'_id': project['_id']}, {'$set': project_data})
    utils.log_event("Mettre à jour projet", project['title'])
    st.cache_data.clear()
    st.success(_("Project Successfully Updated"))