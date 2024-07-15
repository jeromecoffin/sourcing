import streamlit as st
import utils
from datetime import datetime
import firebase_admin
from firebase_admin import firestore
import new_project
from google.cloud.firestore_v1.base_query import FieldFilter

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

@st.cache_data(ttl=3600)
def get_rfi_details(rfi_id):
    db = firestore.client()
    rfi_ref = db.collection("rfis").where(filter=FieldFilter("title", "==", rfi_id))
    rfi = rfi_ref.get()
    return rfi[0].to_dict() if rfi else {}

@st.cache_data(ttl=3600)
def get_rfq_details(rfq_id):
    db = firestore.client()
    rfq_ref = db.collection("rfqs").where(filter=FieldFilter("title", "==", rfq_id))
    rfq = rfq_ref.get()
    return rfq[0].to_dict() if rfq else {}

@st.cache_data(ttl=3600)
def get_clients_details(client_name):
    db = firestore.client()
    client_ref = db.collection("clients").where(filter=FieldFilter("name", "==", client_name))
    client = client_ref.get()
    return client[0].to_dict() if client else {}

def update_project(doc_id, project_data):
    db = firestore.client()
    project_ref = db.collection("projects").document(doc_id)
    project_ref.update(project_data)

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

    st.write("RFI :", project['rfi'])
    rfi = project['rfi']
    if project['rfi'] == "vide":
        rfi_options = utils.get_rfis()
        rfi_options.insert(0, "vide")
        rfi = st.selectbox("Sélectionnez une RFI:", rfi_options)
        rfi_details = get_rfi_details(rfi)
    else:
        rfi_details = get_rfi_details(project['rfi'])
    if rfi_details:
        with st.expander("Détails du RFI :"):
            for key, value in rfi_details.items():
                st.code(f"{key}: {value}")
    else:
        st.write("Aucun détail RFI disponible.")

    st.divider()

    st.write("RFQ :", project['rfq'])
    rfq = project['rfq']
    if project['rfq'] == "vide":
        rfq_options = utils.get_rfqs()
        rfq_options.insert(0, "vide")
        rfq = st.selectbox("Sélectionnez une RFQ:", rfq_options)
        rfq_details = get_rfq_details(rfq)
    else:
        rfq_details = get_rfq_details(project['rfq'])
    if rfq_details:
        with st.expander("Détails du RFQ :"):
            for key, value in rfq_details.items():
                st.code(f"{key}: {value}")
    else:
        st.write("Aucun détail RFQ disponible.")

    st.divider()

    suppliers = []
    suppliers = project['fournisseurs']
    supplier = st.selectbox("Fournisseur Final :", project['fournisseurs'])
    st.write("Fournisseur Final : ", supplier)

    submit = st.button("Enregistrer les modifications")

    if submit:
        project_data = {
            "title": project['title'],
            "client": project['client'],
            "fournisseurs": suppliers,
            "fournisseur_final": supplier,  
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

        # Update the project in Firestore
        update_project(project['doc_id'], project_data)

        st.success("Projet modifié avec succès!")

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

if __name__ == "__main__":
    manage_projects()
