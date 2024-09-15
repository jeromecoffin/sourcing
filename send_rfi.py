import streamlit as st
import pandas as pd
import read
import utils
import webbrowser
import urllib.parse
import update
import generateXlsx
import nextcloud
from datetime import datetime
import time


def send_rfi(user_id):
    _ = utils.translate(user_id)

    rfis = read.rfis(user_id)
    if rfis:
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

            with st.spinner(_('Generating link...')):

                file_name = storexlsx(user_id, agent["username"], rfi_details, supplierName)
                file_link = nextcloud.sharelink(file_name)
                rfi_link = supplierMail + "=" + file_link
                rfi_details["suppliers"].append(rfi_link)

            # Email components
            recipient = supplierMail
            subject = "RFI"
            body = (f'{file_link}')

            # Encode the subject and body to be URL-safe
            subject = urllib.parse.quote(subject)
            encode_body = urllib.parse.quote(body)
            
            st.text(body)
            
            # Construct the mailto link
            #mailto_link = f"mailto:{recipient}?subject={subject}&body={encode_body}"
            
            # Open the default mail client with the mailto link
            #webbrowser.open(mailto_link)

            update.rfi(rfi_details) #a mettre à la fin à cause du rerun
    else:
        st.write(_("Create your first RFI to send it."))

def storexlsx(user_id, username, rfi_data, supplierName):
    now = datetime.now()
    date = now.strftime("%Y%m%d%H%M")
    file_name = str(user_id) + "/" + rfi_data["reference"] + "/" + supplierName + date + ".xlsx"
    xlsx_data = generateXlsx.generate_xlsx_rfi(user_id, rfi_data, file_name)
    nextcloud.create_file(xlsx_data, file_name)
    return file_name

