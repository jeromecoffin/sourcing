import streamlit as st
import utils
from datetime import datetime
import firebase_admin
from firebase_admin import firestore

def get_projects():
    db = firestore.client()
    projects_ref = db.collection("projects")
    projects = projects_ref.get()
    return [project.to_dict() for project in projects]

def create_project(title, client, rfi, rfq, atelier):
    db = firestore.client()
    project_id = f"project_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    project_data = {
        "titre": title,
        "client": client,
        "rfi": rfi,
        "rfq": rfq,
        "atelier": atelier,
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

def get_rfi_details(rfi_id):
    db = firestore.client()
    rfi_ref = db.collection("rfis").where("title", "==", rfi_id)
    rfi = rfi_ref.get()
    return rfi[0].to_dict() if rfi else {}

def get_clients_details(client_name):
    db = firestore.client()
    client_ref = db.collection("clients").where("name", "==", client_name)
    client = client_ref.get()
    return client[0].to_dict() if client else {}

def show_project_details(project):
    st.divider()
    st.write("Titre:", project['title'])
    st.write("Client:", project['client'])
    client_details = get_clients_details(project['client'])
    if client_details:
        with st.expander("Informations Client"):
            for key, value in client_details.items():
                st.code(f"{key}: {value}")
    st.divider()
    st.write("KPIs:")
    col1, col2, col3 = st.columns(3)
    i=1
    for kpi, value in project['kpis'].items():
        if i == 1:
            col1.metric(label=kpi, value=value)
            i += 1
        elif i == 2:
            col2.metric(label=kpi, value=value)
            i += 1
        elif i == 3:
            col3.metric(label=kpi, value=value)
            i = 1
    st.divider()
    st.write("RFI:", project['rfi'])
    rfi_details = get_rfi_details(project['rfi'])
    if rfi_details:
        with st.expander("Détails du RFI:"):
            for key, value in rfi_details.items():
                st.code(f"{key}: {value}")
    else:
        st.write("Aucun détail RFI disponible.")
    st.divider()
    st.write("RFQ:", project['rfq'])
    st.divider()
    st.write("Atelier Choisi:", project['atelier'])
    st.divider()

def manage_projects():
    utils.initialize_firebase()
    
    st.header("Gestion des Projets")
    
    with st.form(key='create_project_form'):
        
        clients = utils.get_clients()
        rfi_options = utils.get_rfis()
        rfq_options = utils.get_rfqs()
        ateliers = utils.get_suppliers()
        
        title = st.text_input("Titre du Projet")
        client = st.selectbox("Sélectionnez un Client:", clients)
        rfi = st.selectbox("Sélectionnez un RFI:", rfi_options)
        rfq = st.selectbox("Sélectionnez un RFQ:", rfq_options)
        atelier = st.selectbox("Sélectionnez un Atelier:", ateliers)
        
        submit_button = st.form_submit_button(label='Créer le Projet')
    
        if submit_button:
            project = create_project(title, client, rfi, rfq, atelier)
            st.success("Projet créé avec succès!")
            st.write(project)
    
    st.header("Projets Existants")
    projects = get_projects()
    
    if projects:
        project_names = [project['client'] for project in projects]
        selected_project_name = st.selectbox("Sélectionnez un Projet:", project_names)
        selected_project = next(project for project in projects if project['client'] == selected_project_name)
        
        show_project_details(selected_project)
    else:
        st.write("Aucun projet disponible.")
