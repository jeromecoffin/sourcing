import streamlit as st
import datetime
from firebase_admin import firestore
from utils import generate_pdf

def manage_rfi_rfq():
    st.sidebar.title("RFI/RFQ Management")
    doc_type = st.sidebar.radio("Choisissez un type de document", ("RFI", "RFQ"))

    if doc_type == "RFI":
        with st.form("add_rfi_form"):
            title = st.text_input("Titre du RFI")
            description = st.text_area("Description")
            due_date = st.date_input("Date Limite de Réponse")
            specifications = st.text_area("Spécifications Techniques")
            quality_standards = st.text_input("Normes de Qualité")
            production_capacity = st.text_input("Capacité de Production")
            delivery_timeframes = st.text_input("Délais de Livraison")
            estimated_costs = st.text_input("Coûts Estimés")
            payment_terms = st.text_input("Conditions de Paiement")
            required_documentation = st.text_area("Documentation Requise")
            certifications = st.text_input("Certifications Requises")
            delivery_terms = st.text_input("Conditions de Livraison")
            delivery_address = st.text_input("Adresse de Livraison")
            samples_required = st.checkbox("Échantillons Requis")
            user_id = st.text_input("ID Utilisateur")
            main_contact = st.text_input("Contact Principal")
            comments = st.text_area("Commentaires Supplémentaires")
            submit = st.form_submit_button("Ajouter RFI")

            if submit:
                rfi_data = {
                    "title": title,
                    "description": description,
                    "due_date": datetime.datetime.combine(due_date, datetime.datetime.min.time()),
                    "specifications": specifications,
                    "quality_standards": quality_standards,
                    "production_capacity": production_capacity,
                    "delivery_timeframes": delivery_timeframes,
                    "estimated_costs": estimated_costs,
                    "payment_terms": payment_terms,
                    "required_documentation": required_documentation,
                    "certifications": certifications,
                    "delivery_terms": delivery_terms,
                    "delivery_address": delivery_address,
                    "samples_required": samples_required,
                    "user_id": user_id,
                    "main_contact": main_contact,
                    "comments": comments
                }
                db = firestore.client()
                db.collection("rfis").add(rfi_data)
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
            description = st.text_area("Description")
            due_date = st.date_input("Date Limite de Réponse")
            quantity = st.number_input("Quantité", min_value=1)
            sizes = st.text_input("Tailles")
            colors = st.text_input("Couleurs")
            materials = st.text_input("Matériaux")
            technical_drawings = st.text_area("Dessin Technique / Spécifications")
            samples_required = st.checkbox("Échantillons Requis")
            quality_standards = st.text_input("Normes de Qualité")
            delivery_terms = st.text_input("Conditions de Livraison")
            delivery_address = st.text_input("Adresse de Livraison")
            budget = st.number_input("Budget Estimé", min_value=0.0, step=0.01)
            payment_terms = st.text_input("Conditions de Paiement")
            delivery_date = st.date_input("Date de Livraison Souhaitée")
            documentation = st.text_area("Documentation Requise")
            user_id = st.text_input("ID Utilisateur")
            main_contact = st.text_input("Contact Principal")
            comments = st.text_area("Commentaires Supplémentaires")
            submit = st.form_submit_button("Ajouter RFQ")

            if submit:
                rfq_data = {
                    "title": title,
                    "description": description,
                    "due_date": datetime.datetime.combine(due_date, datetime.datetime.min.time()),
                    "quantity": quantity,
                    "sizes": sizes,
                    "colors": colors,
                    "materials": materials,
                    "technical_drawings": technical_drawings,
                    "samples_required": samples_required,
                    "quality_standards": quality_standards,
                    "delivery_terms": delivery_terms,
                    "delivery_address": delivery_address,
                    "budget": budget,
                    "payment_terms": payment_terms,
                    "delivery_date": datetime.datetime.combine(delivery_date, datetime.datetime.min.time()),
                    "documentation": documentation,
                    "user_id": user_id,
                    "main_contact": main_contact,
                    "comments": comments
                }
                db = firestore.client()
                db.collection("rfqs").add(rfq_data)
                st.success("RFQ ajouté avec succès!")

        rfqs = get_rfqs()
        st.subheader("Liste des RFQs")
        for rfq in rfqs:
            st.write(rfq)
            pdf = generate_pdf("RFQ", rfq)
            st.download_button(label="Télécharger en PDF", data=pdf, file_name=f"RFQ_{rfq['title']}.pdf")

def get_rfis():
    db = firestore.client()
    rfis_ref = db.collection("rfis")
    rfis = [doc.to_dict() for doc in rfis_ref.stream()]
    return rfis

def get_rfqs():
    db = firestore.client()
    rfqs_ref = db.collection("rfqs")
    rfqs = [doc.to_dict() for doc in rfqs_ref.stream()]
    return rfqs
