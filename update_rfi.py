import streamlit as st
import utils
import read
import create
import update

def update_rfi_rfq():

    _ = utils.translate()

    st.write("RFI:")
    rfis = read.rfis()
    rfistitle = [rfi["title"] for rfi in rfis]
    rfi = st.selectbox(_("Chose one RFI:"), rfistitle)

    rfi_details = [d for d in rfis if d["title"] == rfi]
    rfi_details = rfi_details[0] if rfi_details else None

    with st.form("add_rfi_form", clear_on_submit=True):

        title = st.text_input(_("RFI Title"), value=rfi_details["title"])
        reference = st.text_input(_("Reference"), value=rfi_details["reference"])
        location = st.text_input(_("Location"), value=rfi_details["location"])

        st.divider()

        requestDate = st.text_input(_("Requesting Date"), value=rfi_details["requestDate"])
        requestDueDate = st.text_input(_("Deadline"), value=rfi_details["requestDueDate"])

        st.divider()
        
        productName = st.text_input(_("Product Name"), value=rfi_details["productName"])
        quantity = st.text_input(_("Quantity"), value=rfi_details["quantity"])
        material = st.text_input(_("Material"), value=rfi_details["material"])
        size = st.text_input(_("Size"), value=rfi_details["size"])
        color = st.text_input(_("Color"), value=rfi_details["color"])
        accessory = st.text_area(_("Accessory"), value=rfi_details["accessory"])
        packaging = st.text_input(_("Packaging"), value=rfi_details["packaging"])
        cartonSize = st.text_input(_("CartonSize"), value=rfi_details["cartonSize"])

        st.divider()

        information = st.text_area(_("Information"), value=rfi_details["information"])

        comment =  st.text_area(_("Comment"), value=rfi_details["comment"])

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
            update.rfi(rfi_data)