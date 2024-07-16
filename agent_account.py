import streamlit as st
from firebase_admin import firestore
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities.hasher import Hasher
import utils


def show_profile():

    _ = utils.translate()

    st.header(_("Your Profile"))

    db = firestore.client()
    agent_ref = db.collection("agents").document("user")
    agent = agent_ref.get()

    with st.form("profile_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input(_("Name"), value=agent.to_dict()["name"])
        lastname = col2.text_input(_("Lastname"), value=agent.to_dict()["lastname"])
        email = col1.text_input(_("Email"), value=agent.to_dict()["email"], disabled=True)
        phone = col2.text_input(_("Phone"), value=agent.to_dict()["phone"])
        company = col1.text_input(_("Company"), value=agent.to_dict()["company"])
        language = col2.selectbox(_("Language"), ['en', 'fr', 'vi'])
        address = st.text_input(_("Address"), value=agent.to_dict()["address"])
        sourcing = st.text_area(_("Sourcing preferences"), value=agent.to_dict()["sourcing"])
        experience = st.number_input(_("Years of Experiences"), step=1, value=agent.to_dict()["experience"])
        submit = st.form_submit_button(_("Submit changes"))

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
                "language": language
            }

            db = firestore.client()
            agent_ref.update(agent_data)            
            st.success(_("Data successfully modified!"))
            st.rerun()
        