import streamlit as st
from firebase_admin import firestore, initialize_app
import pandas as pd
from datetime import datetime
from io import StringIO
import utils

def manage_suppliers():

    _ = utils.translate()

    st.sidebar.title(_("Suppliers Management"))
    doc_type = st.sidebar.radio(_("Select Type of Document"), (_("List"), _("New Supplier")), label_visibility="hidden")

    if doc_type == _("List"):
        # Display list of suppliers
        st.subheader(_("Suppliers List"))
        col1, col2 = st.columns(2)
        selected_categories = col1.multiselect(_("Filter by Product Category"), options=get_distinct_values("category"))
        selected_fields = col2.multiselect(_("Filter by Field of Activity"), options=get_distinct_values("fields"))

        with st.spinner(_("Loading Suppliers...")):
            suppliers = get_suppliers(selected_categories, selected_fields)
        
        if suppliers:
            suppliers_df = pd.DataFrame(suppliers)
            suppliers_df = suppliers_df.sort_values(by=['company', 'name'])

            # Define columns to display, excluding 'id'
            columns_to_display = ['company', 'name', 'email', 'address', 'category', 'fields', 'rate']
            suppliers_df = suppliers_df[columns_to_display]

            # Display the data editor
            edited_df = st.data_editor(suppliers_df, hide_index=True, use_container_width=True)

            if st.button(_("Save edits")):
                utils.log_event("modifier fournisseur")
                for index, row in edited_df.iterrows():
                    supplier_id = suppliers[index]['id']  # Get id from original suppliers list
                    updated_data = row.to_dict()
                    update_supplier(supplier_id, updated_data)
                st.success(_("Successfully Saved Edits!"))
        
        # Export functionality
        if st.button(_("Export List")):
            utils.log_event("Exporter la Liste de Fournisseurs")
            export_suppliers_to_csv(suppliers)

    elif doc_type == _("Add Suppliers"):
        # Form to add a new supplier
        with st.spinner(_("Loading Suppliers...")):
            with st.form("add_supplier_form", clear_on_submit=True):
                company = st.text_input(_("Company Name"))
                name = st.text_input(_("Contact Name"))
                email = st.text_input("Email")
                address = st.text_input(_("Address"))
                categories = st.multiselect(_("Categories (Garments, Accessoiries, Home Textiles...)"), options=get_distinct_values("category"))
                new_category = st.text_input(_("Add new Categories (separated by ,)"))
                if new_category:
                    categories.append(new_category)

                fields = st.multiselect(_("Fields of Activity (Dyeing, Importing, Knitting...)"), options=get_distinct_values("fields"))
                new_field = st.text_input(_("Add now fields of activity (separated by ,)"))
                if new_field:
                    fields.append(new_field)

                rate = st.slider("Évaluation", 0, 10, 5)
                submit = st.form_submit_button(_("Add Supplier"))

                if submit:
                    utils.log_event("Nouveau Fournisseur", details=name)
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

                    st.success(_("Supplier Successfully Added!"))

                    utils.detect_and_split_comma_in_lists()
                    st.cache_data.clear()

def update_supplier(supplier_id, supplier_data):
    db = firestore.client()
    supplier_ref = db.collection("suppliers").document(supplier_id)
    supplier_ref.update(supplier_data)

@st.cache_data(ttl=3600)
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
    _ = utils.translate()
    df = pd.DataFrame(suppliers)
    csv = df.to_csv(index=False)
    st.download_button(label=_("Download CSV"), data=csv, file_name="suppliers_export.csv", mime="text/csv")

@st.cache_data(ttl=3600)
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
