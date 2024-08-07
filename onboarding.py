import streamlit as st
from pymongo import MongoClient
import utils
import get
import pandas as pd

def show_onboarding():
    
    _ = utils.translate()

    st.header(_("Customer Onboarding"))

    with st.form("onboarding_form", clear_on_submit=True):
        company = st.text_input(_("Company"))
        name = st.text_input(_("Contact Name"))
        col1, col2 = st.columns(2)
        email = col1.text_input(_("Email"))
        phone = col2.text_input(_("Phone"))
        address = st.text_input(_("Address"))
        notes = st.text_area(_("Notes"))
        submit = st.form_submit_button(_("Save"))

        if submit:
            client_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "address": address,
                "company": company,
                "notes": notes
            }
            # Connect to MongoDB
            db = utils.initialize_mongodb()


            db.clients.insert_one(client_data)
            utils.log_event("Nouveau Client", details=email)
            st.success(_("Customer Successfully Added"))
            st.cache_data.clear()

    # Assuming get_clients() returns a list of dictionaries with client data
    clients = get.get_clients()

    # Extracting the client data into a pandas DataFrame
    df = pd.DataFrame(clients)

    # Displaying the DataFrame as an interactive table
    st.subheader(_("Customer List"))
    st.dataframe(df, hide_index=True, use_container_width=True)
