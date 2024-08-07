import streamlit as st
from pymongo import MongoClient
import utils
import new_project
import get
import pandas as pd


# Function to show project details
def show_project_details(project):

    _ = utils.translate()

    st.divider()

    st.write(_("Title:"), project['title'])
    st.write(_("Customer:"), project['client'])

    clients = get.get_clients()
    client = [d for d in clients if d["name"] == project['client']]
    client = client[0] if client else None
    if client:
        with st.expander(_("Customer Data:")):
            for key, value in client.items():
                st.code(f"{key}: {value}")

    st.divider()

    st.write("RFI:", project['rfi'])
    if project['rfi'] == _("empty"):
        rfis = get.get_rfis()
        rfistitle = [rfi["title"] for rfi in rfis]
        rfistitle.insert(0, _("empty"))
        rfi = st.selectbox(_("Chose one RFI:"), rfistitle)
        rfis = get.get_rfis()
        rfi_details = [d for d in rfis if d["title"] == project['rfi']]
        rfi_details = rfi_details[0] if rfi_details else None
    else:
        rfis = get.get_rfis()
        rfi_details = [d for d in rfis if d["title"] == project['rfi']]
        rfi_details = rfi_details[0] if rfi_details else None
        rfi = project['rfi']
    if rfi_details:
        with st.expander(_("RFI Data :")):
            for key, value in rfi_details.items():
                st.code(f"{key}: {value}")
    else:
        st.write(_("No RFI Selected"))

    st.divider()

    st.write("RFQ:", project['rfq'])
    if project['rfq'] == _("empty"):
        rfqs = get.get_rfqs()
        rfqstitle = [rfq["title"] for rfq in rfqs]
        rfqstitle.insert(0, _("empty"))
        rfq = st.selectbox(_("Chose one RFQ:"), rfqstitle)
        rfqs = get.get_rfqs()
        rfq_details = [d for d in rfqs if d["title"] == project['rfq']]
        rfq_details = rfq_details[0] if rfq_details else None
    else:
        rfqs = get.get_rfqs()
        rfq_details = [d for d in rfqs if d["title"] == project['rfq']]
        rfq_details = rfq_details[0] if rfq_details else None
        rfq = project['rfq']
    if rfq_details:
        with st.expander(_("RFQ Data:")):
            for key, value in rfq_details.items():
                st.code(f"{key}: {value}")
    else:
        st.write(_("No RFQ Selected"))

    st.divider()

    try:
        suppliers = project.get('suppliers', [])
        supplier = st.selectbox(_("Final Supplier:"), suppliers)
        st.write(_("Final Supplier:"), supplier)
    except:
        st.error(_("Error in supplier project management"))

    submit = st.button(_("Save"))

    if submit:
        project_data = {
            "title": project['title'],
            "client": project['client'],
            "suppliers": suppliers,
            "supplier_final": supplier,
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

        # Connect to MongoDB
        db = utils.initialize_mongodb()

        # Update the project in MongoDB
        db.projects.update_one({'_id': project['_id']}, {'$set': project_data})
        utils.log_event("Mettre à jour projet", project['title'])
        st.cache_data.clear()
        st.success(_("Project Successfully Updated"))

# Function to manage projects
def manage_projects():

    _ = utils.translate()

    st.sidebar.title(_("Project Management"))
    doc_type = st.sidebar.radio(_("Select Document Type"), (_("Projects"), _("New Project")), label_visibility="hidden")

    if doc_type == _("Projects"):
        st.header(_("Projects Management"))
        
        st.header(_("Existing Project"))
        projects = get.get_projects()
        
        if projects:
            project_names = [project['title'] for project in projects]
            selected_project_name = st.selectbox(_("Select a Project"), project_names)
            selected_project = next(project for project in projects if project['title'] == selected_project_name)
            
            show_project_details(selected_project)
        else:
            st.write(_("No Project Created"))
            
    elif doc_type == _("New Project"):
        new_project.new_projects()

# Define other necessary utility functions here
def update_project(project_id, project_data):
    # Connect to MongoDB
    db = utils.initialize_mongodb()

    # Update the project in MongoDB
    db.projects.update_one({'_id': project_id}, {'$set': project_data})
