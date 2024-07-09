import streamlit as st
import utils
from datetime import datetime
import firebase_admin
from firebase_admin import firestore
import new_project

def get_projects():
    db = firestore.client()
    projects_ref = db.collection("projects")
    projects = projects_ref.get()
    return [project.to_dict() for project in projects]

def get_rfi_details(rfi_id):
    db = firestore.client()
    rfi_ref = db.collection("rfis").where("title", "==", rfi_id)
    rfi = rfi_ref.get()
    return rfi[0].to_dict() if rfi else {}

def get_rfq_details(rfq_id):
    db = firestore.client()
    rfq_ref = db.collection("rfqs").where("title", "==", rfq_id)
    rfq = rfq_ref.get()
    return rfq[0].to_dict() if rfq else {}

def get_clients_details(client_name):
    db = firestore.client()
    client_ref = db.collection("clients").where("name", "==", client_name)
    client = client_ref.get()
    return client[0].to_dict() if client else {}

def show_project_details(project):
    st.divider()
    st.write("Titre :", project['title'])
    st.write("Client :", project['client'])
    client_details = get_clients_details(project['client'])
    if client_details:
        with st.expander("Informations Client"):
            for key, value in client_details.items():
                st.code(f"{key}: {value}")
    st.divider()
    st.write("KPIs :")
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
    st.write("RFI :", project['rfi'])
    rfi_details = get_rfi_details(project['rfi'])
    if rfi_details:
        with st.expander("Détails du RFI :"):
            for key, value in rfi_details.items():
                st.code(f"{key}: {value}")
    else:
        st.write("Aucun détail RFI disponible.")
    st.divider()
    st.write("RFQ :", project['rfq'])
    rfq_details = get_rfq_details(project['rfq'])
    if rfq_details:
        with st.expander("Détails du RFQ :"):
            for key, value in rfq_details.items():
                st.code(f"{key}: {value}")
    else:
        st.write("Aucun détail RFQ disponible.")
    st.divider()
    st.write("Fournisseur Final :", project['fournisseur'])
    st.divider()

def manage_projects():
    utils.initialize_firebase()

    st.sidebar.title("Project Management")
    doc_type = st.sidebar.radio("Choisissez un type de document", ("Projets", "Nouveau Projet"), label_visibility="hidden")

    if doc_type == "Projets":
        st.header("Gestion des Projets")
        
        st.header("Projets Existants")
        projects = get_projects()
        
        if projects:
            project_names = [project['title'] for project in projects]
            selected_project_name = st.selectbox("Sélectionnez un Projet:", project_names)
            selected_project = next(project for project in projects if project['title'] == selected_project_name)
            
            show_project_details(selected_project)
        else:
            st.write("Aucun projet disponible.")
    elif doc_type == "Nouveau Projet":
        new_project.new_projects()
