import streamlit as st
import datetime
from firebase_admin import firestore
import utils


def manage_rfi_rfq():

    st.sidebar.title("RFI/RFQ Management")
    doc_type = st.sidebar.radio("Choisissez un type de document", ("RFI", "RFQ"))

    if doc_type == "RFI":

        with st.form("add_rfi_form", clear_on_submit=True):

            title = st.text_input("Titre du RFI")
            reference = st.text_input("Ref")
            location = st.text_input("Location")
            clients = utils.get_clients()
            selected_client = st.selectbox("Choisissez le client:", clients)

            st.divider()
            st.write("Partie Requérante")
            rp_name = st.text_input("Nom")
            rp_company = st.text_input("Entreprise")
            rp_position = st.text_input("Rôle")
            rp_mail = st.text_input("email")
            rp_phone = st.text_input("Téléphone")
            st.divider()

            requestDate = st.text_input("Date de la demande")
            requestDueDate = st.text_input("Date d'échéance")
            information = st.text_area("Informations de la Demande")
            
            suppliers = utils.get_suppliers()
            selected_suppliers = st.multiselect("Choisissez les Fournisseurs:", suppliers)
            
            comments = st.text_area("Commentaires Supplémentaires")
            submit = st.form_submit_button("Ajouter RFI")

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
                st.success("RFI ajouté avec succès!")
                st.cache_data.clear()

        st.subheader("Liste des RFIs")
        with st.spinner("Chargement des RFIs..."):
            rfis = get_rfis()
        for rfi in rfis:
            st.write(rfi)
            if st.button(f"Télécharger {rfi['title']} en PDF"):
                pdf = utils.generate_pdf("RFI", rfi)
                utils.log_event("Télécharger RFI", details=rfi['title'])
                st.download_button(
                    label="Télécharger en PDF",
                    data=pdf,
                    file_name=f"RFI_{rfi['title']}.pdf",
                    mime="application/pdf"
                )
    elif doc_type == "RFQ":

        with st.form("add_rfq_form", clear_on_submit=True):

            title = st.text_input("Titre du RFQ")
            reference = st.text_input("Ref")
            location = st.text_input("Location")

            clients = utils.get_clients()
            selected_client = st.selectbox("Choisissez le client:", clients)

            rfis = utils.get_rfis()
            selected_rfis = st.selectbox("Choisissez une RFI:", rfis)
            
            st.divider()
            st.write("Partie Requérante")
            rp_name = st.text_input("Nom")
            rp_company = st.text_input("Entreprise")
            rp_position = st.text_input("Rôle")
            rp_mail = st.text_input("email")
            rp_phone = st.text_input("Téléphone")
            st.divider()

            requestDate = st.text_input("Date de la demande")
            requestDueDate = st.text_input("Date d'échéance")
            quotationContent = st.text_area("Contenu du Devis")
            
            suppliers = utils.get_suppliers()
            selected_suppliers = st.multiselect("Choisissez les Fournisseurs:", suppliers)
            
            comments = st.text_area("Commentaires Supplémentaires")
            submit = st.form_submit_button("Ajouter RFQ")

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
                st.success("RFQ ajouté avec succès!")
                st.cache_data.clear()

        st.subheader("Liste des RFQs")
        with st.spinner("Chargement des RFQs..."):
            rfqs = get_rfqs()
        for rfq in rfqs:
            st.write(rfq)
            if st.button(f"Télécharger {rfq['title']} en PDF"):
                pdf = utils.generate_pdf("RFQ", rfq)
                utils.log_event("Télécharger RFQ", details=rfq['title'])
                st.download_button(
                    label="Télécharger en PDF",
                    data=pdf,
                    file_name=f"RFQ_{rfq['title']}.pdf",
                    mime="application/pdf"
                )

@st.cache_data(ttl=3600)
def get_rfis():
    db = firestore.client()
    rfis_ref = db.collection("rfis")
    rfis = [doc.to_dict() for doc in rfis_ref.stream()]
    return rfis

@st.cache_data(ttl=3600)
def get_rfqs():
    db = firestore.client()
    rfqs_ref = db.collection("rfqs")
    rfqs = [doc.to_dict() for doc in rfqs_ref.stream()]
    return rfqs
