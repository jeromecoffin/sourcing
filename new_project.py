import streamlit as st
import utils
from datetime import datetime
from firebase_admin import firestore

def create_project(title, client, fournisseurs, rfi, rfq):

    db = firestore.client()

    project_id = f"project_{datetime.now().strftime('%Y%m%d%H%M%S')}"

    project_data = {
        "title": title,
        "client": client,
        "fournisseurs": fournisseurs,
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

    _ = utils.translate()
    
    st.header(_("Create New Project"))

    with st.spinner(_("Loading Form...")):
    
        with st.form(key='create_project_form', clear_on_submit=True):
            
            clients = utils.get_clients()
            rfi_options = utils.get_rfis()
            rfq_options = utils.get_rfqs()
            fournisseurs = utils.get_suppliers()
            rfi_options.insert(0, _("empty"))
            rfq_options.insert(0, _("empty"))
            
            title = st.text_input(_("Project Title"))
            client = st.selectbox(_("Select Customer:"), clients)
            rfi = st.selectbox(_("Select RFI"), rfi_options)
            rfq = st.selectbox(_("Select RFQ:"), rfq_options)
            fournisseursProject = st.multiselect(_("Choose Suppliers"), fournisseurs)
            fournisseursProject.insert(0, _("empty"))
            
            submit_button = st.form_submit_button(label=_('Create Project'))
        
            if submit_button:
                project = create_project(title, client, fournisseursProject, rfi, rfq)
                st.success(_("Data successfully modified!"))
                utils.log_event("Nouveau Projet", details=title)
                st.cache_data.clear()
                st.write(project)

        