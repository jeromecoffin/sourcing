import streamlit as st
from firebase_admin import credentials, firestore, initialize_app
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import onboarding
import agent_account
import supplier_management
import rfi_rfq_management
import kpi_dashboard
import project_management
from utils import initialize_firebase

# Initialize Firebase
initialize_firebase()

st.set_page_config(layout="wide")

# Load config.yaml for authentication
with open('cred.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

user, authentication_status, username = authenticator.login('main', fields = {'Form name': 'login'})

if authentication_status:

    authenticator.logout('Logout', 'sidebar')
    st.sidebar.title(f"Welcome {user}")

    def main():

        st.sidebar.title("Menu")

        menu = ["Tableau de Bord", "Onboarding Client", "Gestion des Projets", "Gestion des Fournisseurs", "RFI/RFQ", "Mon Compte"]
        choice = st.sidebar.selectbox("Choisissez une option", menu)

        if choice == "Tableau de Bord":
            kpi_dashboard.show_dashboard()
            st.divider()
            with st.form("kpi_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder="Plus de KPI, autre info...")
                submit = st.form_submit_button("Envoyer")
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success("Merci pour votre retour !")
        elif choice == "Onboarding Client":
            onboarding.show_onboarding()
            st.divider()
            with st.form("onboarding_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder="Plus d'info client...")
                submit = st.form_submit_button("Envoyer")
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success("Merci pour votre retour !")
        elif choice == "Gestion des Projets":
            project_management.manage_projects()
            st.divider()
            with st.form("projets_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder="Ajouter un champs ; Plus de RFIs...")
                submit = st.form_submit_button("Envoyer")
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success("Merci pour votre retour !")
        elif choice == "Gestion des Fournisseurs":
            supplier_management.manage_suppliers()
            st.divider()
            with st.form("suppliers_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder="More/less fields if the new client form ; display other details in the list...")
                submit = st.form_submit_button("Envoyer")
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success("Merci pour votre retour !")
        elif choice == "RFI/RFQ":
            rfi_rfq_management.manage_rfi_rfq()
            st.divider()
            with st.form("documents_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder="Modify fields for RFI/RFQ...")
                submit = st.form_submit_button("Envoyer")
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success("Merci pour votre retour !")
        elif choice == "Mon Compte":
            agent_account.show_profile()
            st.divider()
            with st.form("documents_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder="Info sur la facturation...")
                submit = st.form_submit_button("Envoyer")
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success("Merci pour votre retour !")

    if __name__ == "__main__":
        main()

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
