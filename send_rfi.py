import streamlit as st
import pandas as pd
import read
import utils
import webbrowser
import urllib.parse
import update

def send_rfi():
    _ = utils.translate()

    rfis = read.rfis()
    listrfi = []
    for rfi in rfis:
        rfititle = rfi["title"]
        rfiref = rfi["reference"]
        textbox = rfititle + " - " + rfiref
        listrfi.append(textbox)

    select = st.selectbox(_("Send RFI:"), listrfi)

    select_title = select.split(' ')[0]

    rfi_details = [d for d in rfis if d["title"] == select_title]
    rfi_details = rfi_details[0] if rfi_details else None

    if "suppliers" not in rfi_details:
        rfi_details["suppliers"] = []

    agent = read.agent()

    supplierName = st.text_input(_("To supplier name:"))

    supplierMail = st.text_input(_("at supplier mail address:"))

    send = st.button(_("Send RFI"))

    if send:
        
        rfi_details["suppliers"].append(supplierMail)
        update.rfi(rfi_details)

        # Email components
        recipient = supplierMail
        subject = "RFI"
        body = f'Please find the link to RFI to fill. \n\n http://www.avanta-sourcing.com \n\n Regards, \n {agent["lastname"]} {agent["name"]} \n {agent["email"]} \n {agent["phone"]}'
        
        # Encode the subject and body to be URL-safe
        subject = urllib.parse.quote(subject)
        body = urllib.parse.quote(body)
        
        # Construct the mailto link
        mailto_link = f"mailto:{recipient}?subject={subject}&body={body}"
        
        # Open the default mail client with the mailto link
        webbrowser.open(mailto_link)

        st.cache_data.clear()
