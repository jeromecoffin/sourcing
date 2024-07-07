import streamlit as st
from firebase_admin import credentials, firestore, initialize_app

import onboarding
import account
import supplier_management
import rfi_rfq_management
import kpi_dashboard
import project_management
from utils import initialize_firebase

# Initialize Firebase
initialize_firebase()

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
    elif choice == "Gestion des Fournisseurs":
        supplier_management.manage_suppliers()
    elif choice == "RFI/RFQ":
        rfi_rfq_management.manage_rfi_rfq()
    elif choice == "Gestion des Projets":
        project_management.manage_projects()        

if __name__ == "__main__":
    main()
