import streamlit as st
import pandas as pd
import read
import utils

def show_dashboard(user_id):
    
    _ = utils.translate(user_id)

    st.header(_("Dashboard"))

    kpis = utils.calculate_kpis(user_id)
    col1, col2 = st.columns(2)
    col1.metric(label=_("RFI Templates"), value=kpis["total_rfis"])
    col2.metric(label=_("RFIs Sent"), value=kpis["total_sent_rfis"])

@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):

    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

def list_rfis(user_id):

    _ = utils.translate(user_id)
    st.subheader(_("RFI Templates"))

    with st.spinner(_("Loading RFIs...")):
        rfis = read.rfis(user_id)

    # Ensure RFIs are ordered by date (requestDueDate)
    rfis_sorted = sorted(rfis, key=lambda x: x.get('requestDueDate', ''), reverse=False)

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

    df = pd.DataFrame(data)

    try:

        pagination = st.container()

        bottom_menu = st.columns((4, 1, 1))

        with bottom_menu[2]:
            batch_size = st.selectbox("Page Size", options=[10, 20, 50], key="rfis")
        with bottom_menu[1]:
            total_pages = (
                int((len(df) / batch_size)+1) if int((len(df) / batch_size)+1) > 0 else 1
            )
            current_page = st.number_input(
                "Page", min_value=1, max_value=total_pages, step=1, key="numberrfis"
            )
        with bottom_menu[0]:
            st.markdown(f"Page **{current_page}** of **{total_pages}** ")

        pages = split_frame(df, batch_size)
        pagination.dataframe(data=pages[current_page - 1], use_container_width=True, hide_index=True)

    except Exception as e:
        st.error("No RFI to display.")



def list_suppliers(user_id):

    _ = utils.translate(user_id)
    
    st.subheader(_("RFIs Sent"))

    with st.spinner(_("Loading RFIs...")):
        rfis = read.rfis(user_id)

    # Ensure RFIs are ordered by date (requestDueDate)
    rfis_sorted = sorted(rfis, key=lambda x: x.get('requestDueDate', ''), reverse=False)

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
    
    df = pd.DataFrame(supplier_data)

    try:

        pagination = st.container()

        bottom_menu = st.columns((4, 1, 1))

        with bottom_menu[2]:
            batch_size = st.selectbox("Page Size", options=[10, 20, 50], key="suppliers")
        with bottom_menu[1]:
            total_pages = (
                int((len(df) / batch_size)+1) if int((len(df) / batch_size)+1) > 0 else 1
            )
            current_page = st.number_input(
                "Page", min_value=1, max_value=total_pages, step=1, key="numbersuppliers"
            )
        with bottom_menu[0]:
            st.markdown(f"Page **{current_page}** of **{total_pages}** ")

        pages = split_frame(df, batch_size)
        pagination.dataframe(data=pages[current_page - 1], use_container_width=True, hide_index=True)

    except Exception as e:
        st.error("No RFI to display.")

