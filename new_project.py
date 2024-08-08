import streamlit as st
import utils
from datetime import datetime
import read
import create

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

                
