import streamlit as st
from firebase_admin import firestore

def manage_suppliers():
    st.header("Gestion des Fournisseurs")

    with st.form("add_supplier_form"):
        name = st.text_input("Nom du fournisseur")
        contact = st.text_input("Contact")
        product_offerings = st.text_area("Produits offerts")
        certifications = st.text_area("Certifications")
        past_performance = st.text_area("Historique des performances")
        submit = st.form_submit_button("Ajouter Fournisseur")

        if submit:
            supplier_data = {
                "name": name,
                "contact": contact,
                "product_offerings": product_offerings,
                "certifications": certifications,
                "past_performance": past_performance
            }
            db = firestore.client()
            db.collection("suppliers").add(supplier_data)
            st.success("Fournisseur ajouté avec succès!")

    suppliers = get_suppliers()
    st.subheader("Liste des Fournisseurs")
    for supplier in suppliers:
        st.write(supplier)

def get_suppliers():
    db = firestore.client()
    suppliers_ref = db.collection("suppliers")
    suppliers = [doc.to_dict() for doc in suppliers_ref.stream()]
    return suppliers
