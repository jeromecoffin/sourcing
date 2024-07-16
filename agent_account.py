import streamlit as st
from firebase_admin import firestore
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities.hasher import Hasher


def show_profile():

    st.header("Profil de l'Agent")

    db = firestore.client()
    agent_ref = db.collection("agents").document("user")
    agent = agent_ref.get()

    with st.form("profile_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("Prénom", value=agent.to_dict()["name"])
        lastname = col2.text_input("Nom", value=agent.to_dict()["lastname"])
        email = col1.text_input("Email", value=agent.to_dict()["email"], disabled=True)
        phone = col2.text_input("Téléphone", value=agent.to_dict()["phone"])
        company = st.text_input("Entreprise", value=agent.to_dict()["company"])
        address = st.text_input("Adresse Pro", value=agent.to_dict()["address"])
        sourcing = st.text_area("Préférences de sourcing", value=agent.to_dict()["sourcing"])
        experience = st.number_input("Années d'Expérience", step=1, value=agent.to_dict()["experience"])
        submit = st.form_submit_button("Modifier")

        if submit:
            agent_data = {
                "name": name,
                "lastname": lastname,
                "email": email,
                "phone": phone,
                "company": company,
                "address": address,
                "sourcing": sourcing,
                "experience": experience,
            }

            db = firestore.client()
            agent_ref.update(agent_data)            
            st.success("Données modifiées avec succès!")
            st.rerun()
        