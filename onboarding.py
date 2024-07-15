import streamlit as st
from firebase_admin import firestore
import utils

def show_onboarding():
    
    st.header("Onboarding Client")

    with st.form("onboarding_form", clear_on_submit=True):
        company = st.text_input("Entreprise")
        name = st.text_input("Nom du contact")
        col1, col2 = st.columns(2)
        email = col1.text_input("Email")
        phone = col2.text_input("Téléphone")
        address = st.text_input("Adresse")
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Enregistrer")

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
            st.success("Client inscrit avec succès!")
            st.cache_data.clear()

    clients = get_clients()
    st.subheader("Liste des Clients")
    for client in clients:
        st.write(client)

@st.cache_data(ttl=3600)
def get_clients():
    db = firestore.client()
    clients_ref = db.collection("clients")
    clients = [doc.to_dict() for doc in clients_ref.stream()]
    return clients