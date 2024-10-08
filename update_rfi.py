import streamlit as st
import utils
import read
import update

# NOT USED ANYMORE
# Might be useful later

def update_rfi(user_id):

    _ = utils.translate(user_id)

    st.write("RFI:")

    rfis = read.rfis(user_id)
    rfistitle = [rfi["title"] for rfi in rfis]
    rfi = st.selectbox(_("Chose one RFI:"), rfistitle)

    rfi_details = [d for d in rfis if d["title"] == rfi]
    rfi_details = rfi_details[0] if rfi_details else None

    additional_fields = []

    with st.form("add_rfi_form", clear_on_submit=True):

        title = st.text_input(_("RFI Title"), value=rfi_details["title"])
        reference = st.text_input(_("Reference"), value=rfi_details["reference"])

        st.divider()

        requestDate = st.text_input(_("Requesting Date"), value=rfi_details["requestDate"])
        requestDueDate = st.text_input(_("Deadline"), value=rfi_details["requestDueDate"])

        st.divider()
        
        for idx, x in enumerate(rfi_details["additional_fields"]):
            field = st.text_input("field{}".format(idx), value=x)
            additional_fields.append(field)

        st.divider()

        information = st.text_area(_("Information"), value=rfi_details["information"])

        comment =  st.text_area(_("Comment"), value=rfi_details["comment"])

        submit = st.form_submit_button(_("Submit RFI"))

        if submit:
            rfi_data = {
                "title": title,
                "reference": reference,
                "requestDate": requestDate,
                "requestDueDate": requestDueDate,
                "additional_fields": additional_fields,
                "information": information,
                "comment": comment
            }
            update.rfi(user_id, rfi_data) 