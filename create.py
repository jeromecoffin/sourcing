import streamlit as st
import utils

def feedback(user_feedback):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    db.feedbacks.insert_one(user_feedback)
    st.success(_("Thanks for feedback!"))

def project(project_id, project_data):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    db.projects.insert_one({"_id": project_id, **project_data})
    st.success(_("Data successfully modified!"))
    utils.log_event("Nouveau Projet", details=project_data["title"])
    st.cache_data.clear()

def client(client_data):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    db.clients.insert_one(client_data)
    utils.log_event("Nouveau Client", details=client_data["email"])
    st.success(_("Customer Successfully Added"))
    st.cache_data.clear()

def rfi(rfi_data):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    db.rfis.insert_one(rfi_data)
    utils.log_event("Nouveau RFI", details=rfi_data["title"])
    st.success(_("Added New RFI"))
    st.cache_data.clear()

def rfq(rfq_data):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    db.rfqs.insert_one(rfq_data)
    utils.log_event("Ajouter RFQ", details=rfq_data["title"])
    st.success(_("RFQ Successfully Added!"))
    st.cache_data.clear()

def supplier(supplier_data):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    db.suppliers.insert_one(supplier_data)
    st.success(_("Supplier Successfully Added!"))
    utils.detect_and_split_comma_in_lists()
    st.cache_data.clear()