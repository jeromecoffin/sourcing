import streamlit as st
from firebase_admin import credentials, firestore, initialize_app
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

import onboarding
import account
import supplier_management
import rfi_rfq_management
import kpi_dashboard
import project_management
from utils import initialize_firebase

# Initialize Firebase
initialize_firebase()

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
        menu = ["Tableau de Bord", "Onboarding", "Gestion des Projets", "Gestion des Fournisseurs", "Profil", "RFI/RFQ"]
        choice = st.sidebar.selectbox("Choisissez une option", menu)

        if choice == "Tableau de Bord":
            kpi_dashboard.show_dashboard()
        elif choice == "Profil":
            account.show_profile()
        elif choice == "Onboarding":
            onboarding.show_onboarding()
        elif choice == "Gestion des Projets":
            project_management.manage_projects() 
        elif choice == "Gestion des Fournisseurs":
            supplier_management.manage_suppliers()
        elif choice == "RFI/RFQ":
            rfi_rfq_management.manage_rfi_rfq()

    if __name__ == "__main__":
        main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
