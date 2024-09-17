import streamlit as st
import utils
import create

def add_text_input_field():
    """Function to add a new text input field."""
    st.session_state.additional_fields.append("")

def remove_text_input_field():
    """Function to remove the last text input field."""
    if st.session_state.additional_fields:
        st.session_state.additional_fields.pop()

def create_rfi(user_id):

    _ = utils.translate(user_id)

    with st.form("add_rfi_form", clear_on_submit=True):

        title = st.text_input(_("RFI Title"))
        reference = st.text_input(_("Reference"))

        st.divider()

        requestDate = st.text_input(_("Requesting Date"))
        requestDueDate = st.text_input(_("Deadline"))

        st.divider()

        information = st.text_area(_("Project Information"))

        comment =  st.text_area(_("Comment"))

        st.divider()

        # Dynamic input fields section
        st.subheader(_("Additional Information"))
        st.caption(_("Select Add Another Field button to add specific question to the supplier."))
        
        # Display current dynamic input fields
        for idx, value in enumerate(st.session_state.additional_fields):
            st.session_state.additional_fields[idx] = st.text_input(f"Additional Request {idx+1}", value=value, key=f"input_{idx}")

        suppliers = []

        submit = st.form_submit_button(_("Submit RFI"))

        if submit:
            rfi_data = {
                "title": title,
                "reference": reference,
                "requestDate": requestDate,
                "requestDueDate": requestDueDate,
                "additional_fields": st.session_state.additional_fields,
                "information": information,
                "comment": comment,
                "suppliers": suppliers
            }
            create.rfi(user_id, rfi_data)
            st.session_state.additional_fields = []
            st.rerun()

    col1, col2, col3 = st.columns(3)
    # Add and Remove buttons to manage dynamic inputs (outside the form)
    col1.button(_("Add Request Field"), on_click=add_text_input_field)
    col2.button(_("Remove Last Request Field"), on_click=remove_text_input_field)