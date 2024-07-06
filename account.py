import streamlit as st
from firebase_admin import firestore

def show_profile():
    st.header("Profil de l'Agent")

    with st.form("profile_form"):
        name = st.text_input("Nom")
        email = st.text_input("Email")
        company = st.text_input("Entreprise")
        preferences = st.text_area("Préférences de sourcing")
        submit = st.form_submit_button("S'inscrire")

        if submit:
            agent_data = {
                "name": name,
                "email": email,
                "company": company,
                "preferences": preferences
            }
            db = firestore.client()
            db.collection("agents").add(agent_data)
            st.success("Agent inscrit avec succès!")
