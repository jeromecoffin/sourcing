import streamlit as st
from firebase_admin import firestore, initialize_app
import pandas as pd
from datetime import datetime
from io import StringIO

def manage_suppliers():
    st.sidebar.title("Gestion des Fournisseurs")
    doc_type = st.sidebar.radio("Choisissez un type de document", ("Liste", "Ajouter un Fournisseur"), label_visibility="hidden")
    selected_categories = st.sidebar.multiselect("Filtrer par catégories de produit", options=get_distinct_values("category"))
    selected_fields = st.sidebar.multiselect("Filtrer par domaines d'activité", options=get_distinct_values("fields"))

    if doc_type == "Liste":
        # Display list of suppliers
        suppliers = get_suppliers(selected_categories, selected_fields)
        st.subheader("Liste des Fournisseurs")

        if suppliers:
            suppliers_df = pd.DataFrame(suppliers)
            suppliers_df = suppliers_df.sort_values(by=['company', 'name'])

            columns_order = ['company', 'name', 'email', 'address', 'category', 'fields', 'rate', 'id']
            suppliers_df = suppliers_df[columns_order]

            edited_df = st.data_editor(suppliers_df, hide_index=True)

            if st.button("Enregistrer les modifications"):
                for index, row in edited_df.iterrows():
                    supplier_id = row['id']
                    updated_data = row.to_dict()
                    del updated_data['id']  # Remove 'id' before updating
                    update_supplier(supplier_id, updated_data)
                st.success("Modifications enregistrées avec succès!")
        
        # Export functionality
        if st.button("Exporter les Fournisseurs"):
            export_suppliers_to_csv(suppliers)

    elif doc_type == "Ajouter un Fournisseur":
        # Form to add a new supplier
        with st.form("add_supplier_form"):
            company = st.text_input("Nom de l'entreprise")
            name = st.text_input("Nom du fournisseur")
            email = st.text_input("Email")
            address = st.text_input("Adresse")
            categories = st.multiselect("Categories", options=get_distinct_values("category"))
            new_category = st.text_input("Ajouter une nouvelle catégorie")
            if new_category:
                categories.append(new_category)

            fields = st.multiselect("Domaines d'activité", options=get_distinct_values("fields"))
            new_field = st.text_input("Ajouter un nouveau domaine d'activité")
            if new_field:
                fields.append(new_field)

            rate = st.slider("Évaluation", 0, 10, 5)
            submit = st.form_submit_button("Ajouter Fournisseur")

            if submit:
                supplier_data = {
                    "company": company,
                    "name": name,
                    "email": email,
                    "address": address,
                    "category": categories,
                    "fields": fields,
                    "rate": rate,
                    "created_at": datetime.now()
                }

                db = firestore.client()
                db.collection("suppliers").add(supplier_data)

                st.success("Fournisseur ajouté avec succès!")

def update_supplier(supplier_id, supplier_data):
    db = firestore.client()
    supplier_ref = db.collection("suppliers").document(supplier_id)
    supplier_ref.update(supplier_data)

def get_suppliers(selected_categories, selected_fields):
    db = firestore.client()
    suppliers_ref = db.collection("suppliers")
    suppliers = []
    for doc in suppliers_ref.stream():
        supplier = doc.to_dict()
        supplier['id'] = doc.id  # Ajout de l'ID du document
        if (not selected_categories or set(supplier.get('category', [])).intersection(set(selected_categories))) and \
           (not selected_fields or set(supplier.get('fields', [])).intersection(set(selected_fields))):
            suppliers.append(supplier)
    return suppliers

def export_suppliers_to_csv(suppliers):
    df = pd.DataFrame(suppliers)
    csv = df.to_csv(index=False)
    st.download_button(label="Télécharger CSV", data=csv, file_name="suppliers_export.csv", mime="text/csv")

def get_distinct_values(field_name):
    db = firestore.client()
    suppliers_ref = db.collection("suppliers")
    values = set()
    for doc in suppliers_ref.stream():
        supplier = doc.to_dict()
        if field_name in supplier:
            for value in supplier[field_name]:
                values.add(value)
    return list(values)

if __name__ == "__main__":
    manage_suppliers()
