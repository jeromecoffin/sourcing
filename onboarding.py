import streamlit as st
from firebase_admin import firestore

def show_onboarding():
    st.header("Onboarding Client")

    with st.form("onboarding_form"):
        name = st.text_input("Nom")
        email = st.text_input("Email")
        company = st.text_input("Entreprise")
        preferences = st.text_area("Préférences de sourcing")
        submit = st.form_submit_button("Enregistrer")

        if submit:
            client_data = {
                "name": name,
                "email": email,
                "company": company,
                "preferences": preferences
            }
            db = firestore.client()
            db.collection("clients").add(client_data)
            st.success("Client inscrit avec succès!")

    clients = get_clients()
    st.subheader("Liste des Clients")
    for client in clients:
        st.write(client)

def get_clients():
    db = firestore.client()
    clients_ref = db.collection("clients")
    clients = [doc.to_dict() for doc in clients_ref.stream()]
    return clients