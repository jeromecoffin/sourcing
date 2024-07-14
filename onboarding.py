import streamlit as st
from firebase_admin import firestore

def show_onboarding():
    
    st.header("Onboarding Client")

    with st.form("onboarding_form"):
        name = st.text_input("Nom")
        email = st.text_input("Email")
        company = st.text_input("Entreprise")
        notes = st.text_area("Notes")
        submit = st.form_submit_button("Enregistrer")

        if submit:
            client_data = {
                "name": name,
                "email": email,
                "company": company,
                "notes": notes
            }
            db = firestore.client()
            db.collection("clients").add(client_data)
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