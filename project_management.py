import streamlit as st
import utils
import read
import update
from datetime import datetime
import create


# Function to show project details
def show_project_details(project):

    _ = utils.translate()

    st.divider()

    st.write(_("Title:"), project['title'])
    st.write(_("Customer:"), project['client'])

    clients = read.clients()
    client = [d for d in clients if d["name"] == project['client']]
    client = client[0] if client else None
    if client:
        with st.expander(_("Customer Data:")):
            for key, value in client.items():
                st.code(f"{key}: {value}")

    st.divider()

    st.write("RFI:", project['rfi'])
    if project['rfi'] == _("empty"):
        rfis = read.rfis()
        rfistitle = [rfi["title"] for rfi in rfis]
        rfistitle.insert(0, _("empty"))
        rfi = st.selectbox(_("Chose one RFI:"), rfistitle)
        rfis = read.rfis()
        rfi_details = [d for d in rfis if d["title"] == project['rfi']]
        rfi_details = rfi_details[0] if rfi_details else None
    else:
        rfis = read.rfis()
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
        rfqs = read.rfqs()
        rfqstitle = [rfq["title"] for rfq in rfqs]
        rfqstitle.insert(0, _("empty"))
        rfq = st.selectbox(_("Chose one RFQ:"), rfqstitle)
        rfqs = read.rfqs()
        rfq_details = [d for d in rfqs if d["title"] == project['rfq']]
        rfq_details = rfq_details[0] if rfq_details else None
    else:
        rfqs = read.rfqs()
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
        update.project(project_data)
        

# Function to manage projects
def manage_projects():

    _ = utils.translate()

    st.sidebar.title(_("Project Management"))
    doc_type = st.sidebar.radio(_("Select Document Type"), (_("Projects"), _("New Project")), label_visibility="hidden")

    if doc_type == _("Projects"):
        st.header(_("Projects Management"))
        
        st.header(_("Existing Project"))
        projects = read.projects()
        
        if projects:
            project_names = [project['title'] for project in projects]
            selected_project_name = st.selectbox(_("Select a Project"), project_names)
            selected_project = next(project for project in projects if project['title'] == selected_project_name)
            
            show_project_details(selected_project)
        else:
            st.write(_("No Project Created"))
            
    elif doc_type == _("New Project"):
        new_projects()

def new_projects():
    
    _ = utils.translate()
    
    st.header(_("Create New Project"))

    with st.spinner(_("Loading Form...")):
    
        with st.form(key='create_project_form', clear_on_submit=True):
            
            clients = read.clients()
            clientsname = [client["name"] for client in clients]
            rfis = read.rfis()
            rfistitle = [rfi["title"] for rfi in rfis]
            rfqs = read.rfqs()
            rfqstitle = [rfq["title"] for rfq in rfqs]
            suppliers = read.suppliers(None, None)
            suppliersCompany = [supplier["company"] for supplier in suppliers]
            rfistitle.insert(0, _("empty"))
            rfqstitle.insert(0, _("empty"))
            
            title = st.text_input(_("Project Title"))
            client = st.selectbox(_("Select Customer:"), clientsname)
            rfi = st.selectbox(_("Select RFI"), rfistitle)
            rfq = st.selectbox(_("Select RFQ:"), rfqstitle)
            suppliersProject = st.multiselect(_("Choose Suppliers"), suppliersCompany)
            suppliersProject.insert(0, _("empty"))
            
            submit_button = st.form_submit_button(label=_('Create Project'))
        
            if submit_button:

                project_id = f"project_{datetime.now().strftime('%Y%m%d%H%M%S')}"

                project_data = {
                    "title": title,
                    "client": client,
                    "suppliers": suppliersProject,
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
                create.project(project_id, project_data)

                
