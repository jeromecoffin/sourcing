import streamlit as st
import utils
import read
import create

def add_text_input_field():
    """Function to add a new text input field."""
    st.session_state.additional_fields.append("")

def remove_text_input_field():
    """Function to remove the last text input field."""
    if st.session_state.additional_fields:
        st.session_state.additional_fields.pop()


def create_rfi():

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

        information = st.text_area(_("Information"))

        comment =  st.text_area(_("Comment"))

        st.divider()

        # Dynamic input fields section
        st.subheader("Additional Information")
        
        # Display current dynamic input fields
        for idx, value in enumerate(st.session_state.additional_fields):
            st.session_state.additional_fields[idx] = st.text_input(f"Additional Field {idx+1}", value=value, key=f"input_{idx}")

        suppliers = []

        submit = st.form_submit_button(_("Submit RFI"))

        if submit:
            rfi_data = {
                "title": title,
                "reference": reference,
                "location": location,
                "requestDate": requestDate,
                "requestDueDate": requestDueDate,
                "additional_fields": st.session_state.additional_fields,
                "information": information,
                "comment": comment,
                "suppliers": suppliers
            }
            create.rfi(rfi_data)
    col1, col2, col3 = st.columns(3)
    # Add and Remove buttons to manage dynamic inputs (outside the form)
    col1.button("Add Another Field", on_click=add_text_input_field)
    col2.button("Remove Last Field", on_click=remove_text_input_field)