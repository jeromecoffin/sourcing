import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Vérifiez si Firebase n'est pas déjà initialisé
if not firebase_admin._apps:
    # Initialiser Firebase
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Gestion des contacts fournisseurs
def add_supplier(name, email, phone, address):
    doc_ref = db.collection("suppliers").document()
    doc_ref.set({
        "name": name,
        "email": email,
        "phone": phone,
        "address": address
    })

def get_suppliers():
    suppliers_ref = db.collection("suppliers")
    docs = suppliers_ref.stream()
    return [doc.to_dict() for doc in docs]

# Gestion des documents RFI/RFQ
def add_rfi(title, content, due_date, user_id):
    doc_ref = db.collection("rfis").document()
    doc_ref.set({
        "title": title,
        "content": content,
        "due_date": due_date,
        "user_id": user_id,
        "creation_date": datetime.datetime.now(),
        "status": "Open"
    })

def add_rfq(title, content, due_date, budget, user_id):
    doc_ref = db.collection("rfqs").document()
    doc_ref.set({
        "title": title,
        "content": content,
        "due_date": due_date,
        "budget": budget,
        "user_id": user_id,
        "creation_date": datetime.datetime.now(),
        "status": "Open"
    })

def get_rfis():
    rfis_ref = db.collection("rfis")
    docs = rfis_ref.stream()
    return [doc.to_dict() for doc in docs]

def get_rfqs():
    rfqs_ref = db.collection("rfqs")
    docs = rfqs_ref.stream()
    return [doc.to_dict() for doc in docs]

# Tableau de bord (KPI)
def calculate_kpis():
    suppliers = get_suppliers()
    rfis = get_rfis()
    rfqs = get_rfqs()

    kpis = {
        "total_suppliers": len(suppliers),
        "total_rfis": len(rfis),
        "total_rfqs": len(rfqs),
        "avg_rfi_response_time": 0,  # Placeholder
        "avg_rfq_response_time": 0,  # Placeholder
        # Ajoutez d'autres KPI ici
    }
    return kpis

# Interface Streamlit
st.title("Plateforme SaaS pour les Agents de Sourcing")

st.sidebar.title("Navigation")
choice = st.sidebar.selectbox("Menu", ["Accueil", "Gestion des Contacts", "Documents RFI/RFQ", "Tableau de Bord"])

if choice == "Accueil":
    st.header("Bienvenue sur la Plateforme SaaS pour les Agents de Sourcing")
    st.write("Cette plateforme permet de gérer les contacts fournisseurs, les documents RFI/RFQ, et de suivre les KPI clés.")

elif choice == "Gestion des Contacts":
    st.header("Gestion des Contacts Fournisseurs")

    with st.form("add_supplier_form"):
        name = st.text_input("Nom du Fournisseur")
        email = st.text_input("Email du Fournisseur")
        phone = st.text_input("Téléphone du Fournisseur")
        address = st.text_input("Adresse du Fournisseur")
        submit = st.form_submit_button("Ajouter Fournisseur")

    if submit:
        add_supplier(name, email, phone, address)
        st.success("Fournisseur ajouté avec succès!")

    suppliers = get_suppliers()
    st.subheader("Liste des Fournisseurs")
    for supplier in suppliers:
        st.write(supplier)

elif choice == "Documents RFI/RFQ":
    st.header("Gestion des Documents RFI/RFQ")

    doc_type = st.radio("Type de Document", ["RFI", "RFQ"])

    if doc_type == "RFI":
        with st.form("add_rfi_form"):
            title = st.text_input("Titre du RFI")
            content = st.text_area("Contenu du RFI")
            due_date = st.date_input("Date Limite de Réponse")
            user_id = st.text_input("ID Utilisateur")
            submit = st.form_submit_button("Ajouter RFI")

        if submit:
            add_rfi(title, content, due_date, user_id)
            st.success("RFI ajouté avec succès!")

        rfis = get_rfis()
        st.subheader("Liste des RFIs")
        for rfi in rfis:
            st.write(rfi)

    elif doc_type == "RFQ":
        with st.form("add_rfq_form"):
            title = st.text_input("Titre du RFQ")
            content = st.text_area("Contenu du RFQ")
            due_date = st.date_input("Date Limite de Réponse")
            budget = st.number_input("Budget Estimé")
            user_id = st.text_input("ID Utilisateur")
            submit = st.form_submit_button("Ajouter RFQ")

        if submit:
            add_rfq(title, content, due_date, budget, user_id)
            st.success("RFQ ajouté avec succès!")

        rfqs = get_rfqs()
        st.subheader("Liste des RFQs")
        for rfq in rfqs:
            st.write(rfq)

elif choice == "Tableau de Bord":
    st.header("Tableau de Bord - KPI")

    kpis = calculate_kpis()
    st.subheader("Indicateurs Clés de Performance")
    for kpi, value in kpis.items():
        st.metric(label=kpi, value=value)
