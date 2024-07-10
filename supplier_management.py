import streamlit as st
from firebase_admin import firestore, initialize_app
import pandas as pd
from datetime import datetime
import random

def manage_suppliers():

    st.sidebar.title("Gestion des Fournisseurs")
    doc_type = st.sidebar.radio("Choisissez un type de document", ("Liste", "Ajouter un Fournisseur"), label_visibility="hidden")
    
    if doc_type == "Liste":

        # Display list of suppliers
        suppliers = get_suppliers()
        st.subheader("Liste des Fournisseurs")

        df = pd.DataFrame(
        {
            ".": [[random.randint(0, 5000) for _ in range(30)] for _ in range(1)]
        }
        )

        for supplier in suppliers:
            col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 2, 3, 3, 2, 2])
            
            with col1:
                try:
                    st.write(supplier['name'])
                except KeyError:
                    st.write("Non Renseigné")
            
            with col2:
                st.metric(label="", value="5", delta="3")
            
            with col3:
                try:
                    st.write(supplier['product_offerings'])
                except KeyError:
                    st.write("Garments, Furnitures")
            
            with col4:
                st.dataframe(
                    df,
                    column_config={
                        ".": st.column_config.LineChartColumn(
                            y_min=0, y_max=5000
                        )
                    },
                    hide_index=True,
                )
            
            with col5:
                st.selectbox("contact", ("Contacts", "Jimmy W.", "Théo FL"), key=random.randint(0, 10000), label_visibility="hidden")
            
            with col6:
                if st.button(f"Modif", key=f"update_{supplier['id']}"):
                    st.session_state['supplier_to_update'] = supplier['id']
                    st.rerun()
            
            with col7:
                if st.button(f"Supp", key=f"delete_{supplier['id']}"):
                    delete_supplier(supplier['id'])
                    st.rerun()

            st.markdown("---")
        
        # Import and export functionality
        st.subheader("Import/Export des Fournisseurs")
        if st.button("Exporter les Fournisseurs"):
            export_suppliers_to_csv(suppliers)
        uploaded_file = st.file_uploader("Importer les Fournisseurs", type=["csv"])
        if uploaded_file:
            import_suppliers_from_csv(uploaded_file)
            st.success("Fournisseurs importés avec succès!")

    elif doc_type == "Ajouter un Fournisseur":

        # Form to add a new supplier
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
                    "past_performance": past_performance,
                    "created_at": datetime.now()
                }

                db = firestore.client()
                db.collection("suppliers").add(supplier_data)

                st.success("Fournisseur ajouté avec succès!")

def get_suppliers():
    db = firestore.client()
    suppliers_ref = db.collection("suppliers")
    suppliers = []
    for doc in suppliers_ref.stream():
        supplier = doc.to_dict()
        supplier['id'] = doc.id  # Ajout de l'ID du document
        suppliers.append(supplier)
    return suppliers


def update_supplier(supplier_id):

    st.header(f"Modifier le Fournisseur: {supplier_id}")

    db = firestore.client()
    supplier_ref = db.collection("suppliers").document(supplier_id)
    supplier = supplier_ref.get().to_dict()
    
    with st.form("update_supplier_form"):
        try:
            name = st.text_input("Nom du fournisseur", supplier['name'])
        except:
            name = st.text_input("Nom du fournisseur")
        try:
            email = st.text_input("Email", supplier['email'])
        except:
            email = st.text_input("Email")
        try:
            product_offerings = st.text_area("Produits offerts", supplier['product_offerings'])
        except:
            product_offerings = st.text_area("Produits offerts")
        try:
            certifications = st.text_area("Certifications", supplier['certifications'])
        except:
            certifications = st.text_area("Certifications")
        try:
            past_performance = st.text_area("Historique des performances", supplier['past_performance'])
        except:
            past_performance = st.text_area("Historique des performances")
        submit = st.form_submit_button("Mettre à jour Fournisseur")

        if submit:
            supplier_data = {
                "name": name,
                "email": email,
                "product_offerings": product_offerings,
                "certifications": certifications,
                "past_performance": past_performance
            }
            
            supplier_ref.update(supplier_data)

            st.success("Fournisseur mis à jour avec succès!")

def delete_supplier(supplier_id):
    db = firestore.client()
    supplier_ref = db.collection("suppliers").document(supplier_id)
    supplier_ref.delete()
    st.success("Fournisseur supprimé avec succès!")

def export_suppliers_to_csv(suppliers):
    df = pd.DataFrame(suppliers)
    df.to_csv("suppliers_export.csv", index=False)
    st.download_button("Télécharger CSV", "suppliers_export.csv")

def import_suppliers_from_csv(file):
    df = pd.read_csv(file)
    db = firestore.client()
    for index, row in df.iterrows():
        supplier_data = {
            "name": row["name"],
            "contact": row["contact"],
            "product_offerings": row["product_offerings"],
            "certifications": row["certifications"],
            "past_performance": row["past_performance"],
            "created_at": datetime.now()
        }
        db.collection("suppliers").add(supplier_data)

if __name__ == "__main__":
    manage_suppliers()
