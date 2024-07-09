import streamlit as st
import utils
from datetime import datetime
from firebase_admin import firestore

def create_project(title, client, details, fournisseur, rfi, rfq):
    db = firestore.client()
    project_id = f"project_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    project_data = {
        "title": title,
        "client": client,
        "details": details,
        "fournisseur": fournisseur,
        "rfi": rfi,
        "rfq": rfq,
        "kpis": {
            "response_time": 0,
            "cost": 0,
            "performance": 0,
            "on_time_deliveries": 0,
            "late_deliveries": 0
        }
    }
    db.collection("projects").document(project_id).set(project_data)
    return project_data

def new_projects():
    utils.initialize_firebase()
    
    st.header("Créer un Nouveau Projet")
    
    with st.form(key='create_project_form'):
        
        clients = utils.get_clients()
        rfi_options = utils.get_rfis()
        rfq_options = utils.get_rfqs()
        fournisseurs = utils.get_suppliers()
        rfi_options.insert(0, "vide")
        rfq_options.insert(0, "vide")
        
        title = st.text_input("Titre du Projet")
        client = st.selectbox("Sélectionnez un Client:", clients)
        sourcingTypes = ["Garments", "Furnitures"]
        rfi = st.selectbox("Sélectionnez un RFI:", rfi_options)
        rfq = st.selectbox("Sélectionnez un RFQ:", rfq_options)
        details = st.multiselect("Préférences de Sourcing", sourcingTypes)
        fournisseur = st.multiselect("Sélectionnez les Fournisseurs:", fournisseurs)
        
        submit_button = st.form_submit_button(label='Créer le Projet')
    
        if submit_button:
            project = create_project(title, client, details, fournisseur, rfi, rfq)
            st.success("Projet créé avec succès!")
            st.write(project)
    