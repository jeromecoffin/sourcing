import streamlit as st
import pandas as pd
import read
import utils
import webbrowser
import urllib.parse
import update
import generateXlsx


def send_rfi(user_id):
    _ = utils.translate(user_id)

    rfis = read.rfis(user_id)
    listrfi = []
    for rfi in rfis:
        rfititle = rfi["title"]
        rfiref = rfi["reference"]
        textbox = rfititle + " - " + rfiref
        listrfi.append(textbox)

    select = st.selectbox(_("Send RFI:"), listrfi)

    select_title = select.split(' -')[0]

    rfi_details = [d for d in rfis if d["title"] == select_title]
    rfi_details = rfi_details[0] if rfi_details else None

    # Check if 'suppliers' key exists in rfi_details, if not, initialize it as a list
    if "suppliers" not in rfi_details or rfi_details["suppliers"] is None:
        rfi_details["suppliers"] = []

    agent = read.agent_id(user_id)

    supplierName = st.text_input(_("To supplier name:"))

    supplierMail = st.text_input(_("at supplier mail address:"))

    send = st.button(_("Send RFI"))

    if send:

        file_name = storexlsx(user_id, agent["username"], rfi_details, supplierName)
        rfi_link = supplierMail + "=" + file_name
        rfi_details["suppliers"].append(rfi_link)

        file_link = file_name

        # Email components
        recipient = supplierMail
        subject = "RFI"
        body = (f'Dear {supplierName},\n'
                'I hope this message finds you well.\n'
                'We are currently evaluating potential suppliers and would appreciate your assistance in completing a RFI.'
                'To streamline the process, we have prepared an online Excel sheet where you can provide the necessary details regarding your offerings.\n\n'
                'Please use the link below to access and fill out the RFI:\n\n'
                f'{file_link}\n\n'
                'Thank you for your time and cooperation. We look forward to receiving your response.\n'
                'Regards,\n'
                f'{agent["lastname"]} {agent["name"]}\n'
                f'{agent["email"]}\n'
                f'{agent["phone"]}'
            )
        
        # Encode the subject and body to be URL-safe
        subject = urllib.parse.quote(subject)
        body = urllib.parse.quote(body)
        
        # Construct the mailto link
        mailto_link = f"mailto:{recipient}?subject={subject}&body={body}"
        
        # Open the default mail client with the mailto link
        webbrowser.open(mailto_link)

        update.rfi(rfi_details) #a mettre à la fin à cause du rerun

def storexlsx(user_id, username, rfi_data, supplierName):

    file_name = "/Users/jeromecoffin/" + username + rfi_data["reference"] + supplierName + ".xlsx"
    generateXlsx.generate_xlsx_rfi(user_id, rfi_data, file_name)
    return file_name

