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

    _ = utils.translate()

    st.divider()

    st.write(_("Title:"), project['title'])

    st.write(_("Customer:"), project['client'])
    client_details = get_clients_details(project['client'])
    if client_details:
        with st.expander(_("Customer Data:")):
            for key, value in client_details.items():
                st.code(f"{key}: {value}")

    st.divider()

    st.write("RFI:", project['rfi'])
    rfi = project['rfi']
    if project['rfi'] == _("empty"):
        rfi_options = utils.get_rfis()
        rfi_options.insert(0, _("empty"))
        rfi = st.selectbox(_("Chose one RFI:"), rfi_options)
        rfi_details = get_rfi_details(rfi)
    else:
        rfi_details = get_rfi_details(project['rfi'])
    if rfi_details:
        with st.expander(_("RFI Data :")):
            for key, value in rfi_details.items():
                st.code(f"{key}: {value}")
    else:
        st.write(_("No RFI Selected"))

    st.divider()

    st.write("RFQ:", project['rfq'])
    rfq = project['rfq']
    if project['rfq'] == _("empty"):
        rfq_options = utils.get_rfqs()
        rfq_options.insert(0, _("empty"))
        rfq = st.selectbox(_("Chose one RFQ:"), rfq_options)
        rfq_details = get_rfq_details(rfq)
    else:
        rfq_details = get_rfq_details(project['rfq'])
    if rfq_details:
        with st.expander(_("RFQ Data:")):
            for key, value in rfq_details.items():
                st.code(f"{key}: {value}")
    else:
        st.write(_("No RFQ Selected"))

    st.divider()

    suppliers = []
    suppliers = project['fournisseurs']
    supplier = st.selectbox(_("Final Supplier:"), project['fournisseurs'])
    st.write(_("Final Supplier:"), supplier)

    submit = st.button(_("Save"))

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
        utils.log_event("Mettre à jour projet", project['title'])
        st.success(_("Project Successfully Updated"))

def manage_projects():

    _ = utils.translate()

    utils.initialize_firebase()

    st.sidebar.title(_("Project Management"))
    doc_type = st.sidebar.radio(_("Select Document Type"), (_("Projects"), _("New Project")), label_visibility="hidden")

    if doc_type == _("Projects"):
        st.header(_("Projects Management"))
        
        st.header(_("Existing Project"))
        projects = get_projects()
        
        if projects:
            project_names = [project['title'] for project in projects]
            selected_project_name = st.selectbox(_("Select a Project"), project_names)
            selected_project = next(project for project in projects if project['title'] == selected_project_name)
            
            show_project_details(selected_project)
        else:
            st.write(_("No Project Created"))
            
    elif doc_type == _("New Project"):
        new_project.new_projects()

if __name__ == "__main__":
    manage_projects()
