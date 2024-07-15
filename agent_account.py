import streamlit as st
from firebase_admin import firestore

def show_profile():

    st.header("Profil de l'Agent")

    with st.form("profile_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("Prénom")
        lastname = col2.text_input("Nom")
        email = col1.text_input("Email")
        phone = col2.text_input("Téléphone")
        company = st.text_input("Entreprise")
        address = st.text_input("Adresse Pro")
        preferences = st.text_area("Préférences de sourcing")
        experience = st.number_input("Années d'Expérience", step=1)
        password = st.text_input("Mot de Passe")
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
