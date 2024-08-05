import streamlit as st
from firebase_admin import firestore
import utils
import get

def manage_rfi_rfq():

    _ = utils.translate()

    st.sidebar.title(_("RFI/RFQ Management"))
    doc_type = st.sidebar.radio(_("Chose a type of document"), ("RFI", "RFQ"))

    if doc_type == "RFI":

        with st.form("add_rfi_form", clear_on_submit=True):

            title = st.text_input(_("RFI Title"))
            reference = st.text_input(_("Reference"))
            location = st.text_input(_("Location"))
            clients = get.get_clients()
            clientsname = [client["name"] for client in clients]
            selected_client = st.selectbox(_("Select a Client:"), clientsname)

            st.divider()
            st.write(_("Requesting Party"))
            rp_name = st.text_input(_("Name"))
            rp_company = st.text_input(_("Company"))
            rp_position = st.text_input(_("Position"))
            rp_mail = st.text_input(_("email"))
            rp_phone = st.text_input(_("Phone"))
            st.divider()

            requestDate = st.text_input(_("Requesting Date"))
            requestDueDate = st.text_input(_("Deadline"))
            information = st.text_area(_("Requesting Information"))
            
            suppliers = get.get_suppliers(None, None)
            suppliersCompany = [supplier["company"] for supplier in suppliers]
            selected_suppliers = st.multiselect(_("Select Suppliers"), suppliersCompany)
            
            comments = st.text_area(_("Additional Comments"))
            submit = st.form_submit_button(_("Submit RFI"))

            if submit:
                rfi_data = {
                    "title": title,
                    "reference": reference,
                    "location": location,
                    "rp_name": rp_name,
                    "rp_company": rp_company,
                    "rp_position": rp_position,
                    "rp_mail": rp_mail,
                    "rp_phone": rp_phone,
                    "requestDate": requestDate,
                    "requestDueDate": requestDueDate,
                    "information": information,
                    "client": selected_client,
                    "suppliers": selected_suppliers,
                    "comments": comments
                }

                db = firestore.client()
                db.collection("rfis").add(rfi_data)
                utils.log_event("Nouveau RFI", details=title)
                st.success(_("Added New RFI"))
                st.cache_data.clear()

        st.subheader(_("RFIs List"))
        with st.spinner(_("Loading RFIs...")):
            rfis = get.get_rfis()
        for rfi in rfis:
            titleExpender = rfi['title'] + " - " + rfi['reference']
            with st.expander(titleExpender):
                for key, value in rfi.items():
                    st.code(f"{key}: {value}")
                if st.button(_("Download") + " " + rfi['title'] + _(" in PDF")):
                    pdf = utils.generate_pdf("RFI", rfi)
                    utils.log_event("Télécharger RFI", details=rfi['title'])
                    st.download_button(
                        label=_("Download PDF"),
                        data=pdf,
                        file_name=f"RFI_{rfi['title']}.pdf",
                        mime="application/pdf"
                    )
    elif doc_type == "RFQ":

        with st.form("add_rfq_form", clear_on_submit=True):

            title = st.text_input(_("RFQ Title"))
            reference = st.text_input(_("Reference"))
            location = st.text_input(_("Location"))

            clients = get.get_clients()
            clientsname = [client["name"] for client in clients]
            selected_client = st.selectbox(_("Select Customer:"), clientsname)

            rfis = get.get_rfis()
            rfistitle = [rfi["title"] for rfi in rfis]
            selected_rfis = st.selectbox(_("Select RFI:"), rfistitle)
            
            st.divider()
            st.write(_("Requesting Party"))
            rp_name = st.text_input(_("Name"))
            rp_company = st.text_input(_("Company"))
            rp_position = st.text_input(_("Position"))
            rp_mail = st.text_input(_("email"))
            rp_phone = st.text_input(_("Phone"))
            st.divider()

            requestDate = st.text_input(_("Requesting Date"))
            requestDueDate = st.text_input(_("Deadline"))
            quotationContent = st.text_area(_("Quotation Content"))
            
            suppliers = get.get_suppliers(None, None)
            suppliersCompany = [supplier["company"] for supplier in suppliers]
            selected_suppliers = st.multiselect(_("Select Suppliers:"), suppliersCompany)
            
            comments = st.text_area(_("Comments"))
            submit = st.form_submit_button(_("Submit RFQ"))

            if submit:
                rfq_data = {
                    "title": title,
                    "rfi": selected_rfis,
                    "reference": reference,
                    "location": location,
                    "rp_name": rp_name,
                    "rp_company": rp_company,
                    "rp_position": rp_position,
                    "rp_mail": rp_mail,
                    "rp_phone": rp_phone,
                    "requestDate": requestDate,
                    "requestDueDate": requestDueDate,
                    "quotationContent": quotationContent,
                    "client": selected_client,
                    "suppliers": selected_suppliers,
                    "comments": comments
                }

                db = firestore.client()
                db.collection("rfqs").add(rfq_data)

                utils.log_event("Ajouter RFQ", details=title)
                st.success(_("RFQ Successfully Added!"))
                st.cache_data.clear()

        st.subheader(_("RFQs List"))
        with st.spinner(_("RFQs Loading...")):
            rfqs = get.get_rfqs()
        for rfq in rfqs:
            titleExpender = rfq['title'] + " - " + rfq['reference']
            with st.expander(titleExpender):
                for key, value in rfq.items():
                    st.code(f"{key}: {value}")
                if st.button(_("Download") + " " + rfq['title'] + _(" in PDF")):
                    pdf = utils.generate_pdf("RFQ", rfq)
                    utils.log_event(_("Download RFQ"), details=rfq['title'])
                    st.download_button(
                        label=_("Download PDF"),
                        data=pdf,
                        file_name=f"RFQ_{rfq['title']}.pdf",
                        mime="application/pdf"
                    )


