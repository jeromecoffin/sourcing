import streamlit as st
from firebase_admin import firestore
import utils

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
            db = firestore.client()
            db.collection("clients").add(client_data)
            utils.log_event("Nouveau Client", details=email)
            st.success(_("Customer Successfully Added"))
            st.cache_data.clear()

    clients = get_clients()
    st.subheader(_("Customer List"))
    for client in clients:
        st.write(client)

@st.cache_data(ttl=3600)
def get_clients():
    db = firestore.client()
    clients_ref = db.collection("clients")
    clients = [doc.to_dict() for doc in clients_ref.stream()]
    return clients