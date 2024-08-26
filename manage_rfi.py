import streamlit as st
import pandas as pd
import read
import utils

def show_dashboard(user_id):
    
    _ = utils.translate(user_id)

    st.header(_("Dashboard"))
    kpis = utils.calculate_kpis(user_id)
    col1, col2, col3 = st.columns(3)
    col1.metric(label=_("Total Number of RFIs"), value=kpis["total_rfis"])
    col2.metric(label=_("RFIs Sent"), value=kpis["total_sent_rfis"])
    col3.metric(label=_("RFIs Received"), value=kpis["total_sent_rfis"])

def list_rfis(user_id):
    _ = utils.translate(user_id)
    st.subheader(_("RFIs List"))

    with st.spinner(_("Loading RFIs...")):
        rfis = read.rfis(user_id)

    # Ensure RFIs are ordered by date (requestDueDate)
    rfis_sorted = sorted(rfis, key=lambda x: x.get('requestDueDate', ''), reverse=False)

    # Prepare data for the dataframe
    data = {
        "Title": [],
        "Reference": [],
        "Due Date": [],
        "Suppliers Contacted": [],
    }

    # Populate the data for the table
    for rfi in rfis_sorted:
        title = rfi.get('title', 'Untitled RFI')
        reference = rfi.get('reference', 'No Reference')
        suppliersContacted = rfi.get('suppliers')
        request_date = rfi.get('requestDueDate', 'No Due Date')
        
        # Append the data to the list
        data["Title"].append(title)
        data["Reference"].append(reference)
        data["Due Date"].append(request_date)
        data["Suppliers Contacted"].append(len(suppliersContacted))

    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame in Streamlit
    st.dataframe(df)

    # Optionally log event
    # utils.log_event("RFI Dataframe Viewed")
import pandas as pd
import streamlit as st
import utils
import read

def list_suppliers(user_id):
    _ = utils.translate(user_id)
    st.subheader(_("Suppliers List"))

    with st.spinner(_("Loading RFIs...")):
        rfis = read.rfis(user_id)

    # Ensure RFIs are ordered by date (requestDueDate)
    rfis_sorted = sorted(rfis, key=lambda x: x.get('requestDueDate', ''), reverse=False)

    # Prepare data for the dataframe
    supplier_data = {
        "Supplier Name": [],
        "Title": [],
        "Reference": [],
        "Due Date": [],
        "Sheet Link": []
    }

    for rfi in rfis_sorted:
        for s in rfi.get("suppliers", []):
            title = rfi.get('title', 'Untitled RFI')
            reference = rfi.get('reference', 'No Reference')
            request_date = rfi.get('requestDueDate', 'No Due Date')
            supplier = str(s).partition("=")[0]
            
            # Create a link to the XLSX file for each RFI
            sheet_url = str(s).partition("=")[2]
            
            # Append the data to the list
            supplier_data["Title"].append(title)
            supplier_data["Reference"].append(reference)
            supplier_data["Due Date"].append(request_date)
            supplier_data["Supplier Name"].append(supplier)
            supplier_data["Sheet Link"].append(sheet_url)
    
    # Convert to DataFrame
    df = pd.DataFrame(supplier_data)

    # Display the DataFrame in Streamlit
    st.dataframe(df)


