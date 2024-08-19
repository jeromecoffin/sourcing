import streamlit as st
import utils
import read
import pandas as pd
import create

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
            create.client(client_data)

    # Extracting the client data into a pandas DataFrame
    df = pd.DataFrame(read.clients())

    # Displaying the DataFrame as an interactive table
    st.subheader(_("Customer List"))
    st.dataframe(df, hide_index=True, use_container_width=True)
