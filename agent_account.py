import streamlit as st
import utils
import read
import update

def show_profile():

    _ = utils.translate()

    st.header(_("Your Profile"))

    agent = read.agent()

    if agent is None:
        st.error(_("User not found"))
        return

    with st.form("profile_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input(_("Name"), value=agent["name"])
        lastname = col2.text_input(_("Lastname"), value=agent["lastname"])
        email = col1.text_input(_("Email"), value=agent["email"], disabled=True)
        phone = col2.text_input(_("Phone"), value=agent["phone"])
        company = col1.text_input(_("Company"), value=agent["company"])
        language_select = col2.selectbox(_("Language"), ['English', 'Français', 'Tiếng Việt'])
        if language_select == 'Français':
            language = 'fr'
        elif language_select == 'Tiếng Việt':
            language = 'vi'
        else:
            language = 'en'
        address = st.text_input(_("Address"), value=agent["address"])
        sourcing = st.text_area(_("Sourcing preferences"), value=agent["sourcing"])
        experience = st.number_input(_("Years of Experiences"), step=1, value=agent["experience"])
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
                "language": language,
                "isFirstLogin": "1"
            }           
            update.agent(agent_data)
