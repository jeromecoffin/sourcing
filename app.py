import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
        "due_date": datetime.datetime.combine(due_date, datetime.datetime.min.time()),
        "user_id": user_id,
        "creation_date": datetime.datetime.now(),
        "status": "Open"
    })

def add_rfq(title, content, due_date, budget, user_id):
    doc_ref = db.collection("rfqs").document()
    doc_ref.set({
        "title": title,
        "content": content,
        "due_date": datetime.datetime.combine(due_date, datetime.datetime.min.time()),
        "budget": budget,
        "user_id": user_id,
        "creation_date": datetime.datetime.now(),
        "status": "Open"
    })

def format_firestore_timestamp(timestamp):
    if isinstance(timestamp, datetime.datetime):
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp

def get_rfis():
    rfis_ref = db.collection("rfis")
    docs = rfis_ref.stream()
    rfis = []
    for doc in docs:
        data = doc.to_dict()
        data['due_date'] = format_firestore_timestamp(data['due_date'])
        data['creation_date'] = format_firestore_timestamp(data['creation_date'])
        rfis.append(data)
    return rfis

def get_rfqs():
    rfqs_ref = db.collection("rfqs")
    docs = rfqs_ref.stream()
    rfqs = []
    for doc in docs:
        data = doc.to_dict()
        data['due_date'] = format_firestore_timestamp(data['due_date'])
        data['creation_date'] = format_firestore_timestamp(data['creation_date'])
        rfqs.append(data)
    return rfqs

# Générer un PDF pour RFI ou RFQ
def generate_pdf(doc_type, doc_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 50, f"{doc_type} Document")
    p.drawString(100, height - 70, f"Title: {doc_data['title']}")
    p.drawString(100, height - 90, f"Content: {doc_data['content']}")
    p.drawString(100, height - 110, f"Due Date: {doc_data['due_date']}")
    p.drawString(100, height - 130, f"User ID: {doc_data['user_id']}")
    p.drawString(100, height - 150, f"Creation Date: {doc_data['creation_date']}")
    if doc_type == "RFQ":
        p.drawString(100, height - 170, f"Budget: {doc_data['budget']}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

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
def main():
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
                pdf = generate_pdf("RFI", rfi)
                st.download_button(label="Télécharger en PDF", data=pdf, file_name=f"RFI_{rfi['title']}.pdf")

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
                pdf = generate_pdf("RFQ", rfq)
                st.download_button(label="Télécharger en PDF", data=pdf, file_name=f"RFQ_{rfq['title']}.pdf")

    elif choice == "Tableau de Bord":
        st.header("Tableau de Bord - KPI")

        kpis = calculate_kpis()
        st.subheader("Indicateurs Clés de Performance")
        for kpi, value in kpis.items():
            st.metric(label=kpi, value=value)

if __name__ == "__main__":
    main()
