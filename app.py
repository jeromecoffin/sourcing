import streamlit as st
from firebase_admin import credentials, firestore, initialize_app

import onboarding
import account
import supplier_management
import rfi_rfq_management
import kpi_dashboard
from utils import initialize_firebase

# Initialize Firebase
initialize_firebase()

def main():
    st.sidebar.title("Menu")
    menu = ["Accueil", "Profil", "Onboarding", "Gestion des Fournisseurs", "RFI/RFQ", "Tableau de Bord"]
    choice = st.sidebar.selectbox("Choisissez une option", menu)

    if choice == "Accueil":
        st.title("Bienvenue sur la plateforme de sourcing")
    elif choice == "Profil":
        account.show_profile()
    elif choice == "Onboarding":
        onboarding.show_onboarding()
    elif choice == "Gestion des Fournisseurs":
        supplier_management.manage_suppliers()
    elif choice == "RFI/RFQ":
        rfi_rfq_management.manage_rfi_rfq()
    elif choice == "Tableau de Bord":
        kpi_dashboard.show_dashboard()

if __name__ == "__main__":
    main()
