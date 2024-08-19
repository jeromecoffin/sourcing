import streamlit as st
import utils
import read
import create

def create_rfi_rfq():

    _ = utils.translate()

    st.sidebar.title(_("RFI Management"))

    with st.form("add_rfi_form", clear_on_submit=True):

        title = st.text_input(_("RFI Title"))
        reference = st.text_input(_("Reference"))
        location = st.text_input(_("Location"))

        st.divider()

        requestDate = st.text_input(_("Requesting Date"))
        requestDueDate = st.text_input(_("Deadline"))

        st.divider()
        
        productName = st.text_input(_("Product Name"))
        quantity = st.text_input(_("Quantity"))
        material = st.text_input(_("Material"))
        size = st.text_input(_("Size"))
        color = st.text_input(_("Color"))
        accessory = st.text_area(_("Accessory"))
        packaging = st.text_input(_("Packaging"))
        cartonSize = st.text_input(_("CartonSize"))

        st.divider()

        information = st.text_area(_("Information"))

        comment =  st.text_area(_("Comment"))

        submit = st.form_submit_button(_("Submit RFI"))

        if submit:
            rfi_data = {
                "title": title,
                "reference": reference,
                "location": location,
                "requestDate": requestDate,
                "requestDueDate": requestDueDate,
                "productName": productName,
                "quantity": quantity,
                "material": material,
                "size": size,
                "color": color,
                "accessory": accessory,
                "packaging": packaging,
                "cartonSize": cartonSize,
                "information": information,
                "comment": comment
            }
            create.rfi(rfi_data)