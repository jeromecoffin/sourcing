import streamlit as st
import pandas as pd
from datetime import datetime
import utils
import read
import create

def manage_suppliers():

    _ = utils.translate()

    st.sidebar.title(_("Suppliers Management"))
    doc_type = st.sidebar.radio(_("Select Type of Document"), (_("List"), _("New Supplier")), label_visibility="hidden")

    # Connect to MongoDB
    db = utils.initialize_mongodb()

    if doc_type == _("List"):
        # Display list of suppliers
        st.subheader(_("Suppliers List"))
        col1, col2 = st.columns(2)
        selected_categories = col1.multiselect(_("Filter by Product Category"), options=read.distinct_values_management("categories"))
        selected_fields = col2.multiselect(_("Filter by Field of Activity"), options=read.distinct_values_management("fields"))

        with st.spinner(_("Loading Suppliers...")):
            suppliers = read.suppliers(selected_categories, selected_fields)
        
        if suppliers:
            suppliers_df = pd.DataFrame(suppliers)
            suppliers_df = suppliers_df.sort_values(by=['company', 'name'])

            # Define columns to display, excluding 'id'
            columns_to_display = ['company', 'name', 'email', 'address', 'categories', 'fields', 'rate', 'remove']
            suppliers_df = suppliers_df[columns_to_display]

            # Display the data editor
            edited_df = st.data_editor(suppliers_df, hide_index=True, use_container_width=True)
            
            if st.button(_("Save edits")):
                utils.log_event("modifier fournisseur")
                for index, row in edited_df.iterrows():
                    supplier_id = suppliers[index]['_id']  # Get id from original suppliers list
                    updated_data = row.to_dict()
                    db.suppliers.update_one({'_id': supplier_id}, {'$set': updated_data})
                st.cache_data.clear()
                st.success(_("Successfully Saved Edits!"))
                st.rerun()

        
        # Export functionality
        if st.button(_("Export List")):
            utils.log_event("Exporter la Liste de Fournisseurs")
            utils.export_suppliers_to_csv_management(suppliers)

    elif doc_type == _("New Supplier"):
        # Form to add a new supplier
        with st.spinner(_("Loading Suppliers...")):
            with st.form("add_supplier_form", clear_on_submit=True):
                company = st.text_input(_("Company Name"))
                name = st.text_input(_("Contact Name"))
                email = st.text_input("Email")
                address = st.text_input(_("Address"))
                categories = st.multiselect(_("Categories (Garments, Accessories, Home Textiles...)"), options=read.distinct_values_management("categories"))
                new_categories = st.text_input(_("Add new Categories (separated by ,)"))
                if new_categories:
                    categories.extend([cat.strip() for cat in new_categories.split(',')])

                fields = st.multiselect(_("Fields of Activity (Dyeing, Importing, Knitting...)"), options=read.distinct_values_management("fields"))
                new_field = st.text_input(_("Add new fields of activity (separated by ,)"))
                if new_field:
                    fields.extend([field.strip() for field in new_field.split(',')])

                rate = st.slider("Évaluation", 0, 10, 5)
                submit = st.form_submit_button(_("Add Supplier"))

                if submit:
                    utils.log_event("Nouveau Fournisseur", details=name)
                    supplier_data = {
                        "company": company,
                        "name": name,
                        "email": email,
                        "address": address,
                        "categories": categories,
                        "fields": fields,
                        "rate": rate,
                        "remove": False,
                        "created_at": datetime.now()
                    }
                    create.supplier(supplier_data)

                    
