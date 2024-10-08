import streamlit as st
import read
import utils
import update
import generateXlsx
import nextcloud
from datetime import datetime
import pyshorteners

def storexlsx(user_id, username, rfi_data, supplierName):

    now = datetime.now()
    date = now.strftime("%Y%m%d%H%M")

    file_name = str(user_id) + "/" + rfi_data["reference"] + "/" + supplierName + date + ".xlsx"

    xlsx_data = generateXlsx.generate_xlsx_rfi(user_id, rfi_data, file_name)

    nextcloud.create_file(xlsx_data, file_name)

    return file_name

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

        send = st.button(_("Link RFI"))

        if send:

            try:

                with st.spinner(_('Generating link...')):

                    # Generate file and store in NextCloud
                    file_name = storexlsx(user_id, agent["username"], rfi_details, supplierName)

                    # Create a short share link
                    file_link = nextcloud.sharelink(file_name)
                    file_link = file_link.replace("http://nginx-server:8443", "https://www.rfi.avanta-sourcing.com:8443")
                    short_url = pyshorteners.Shortener().tinyurl.short(file_link)

                    # Store supplier email and url in mongo
                    rfi_link = supplierMail + "=" + short_url
                    rfi_details["suppliers"].append(rfi_link)

                # Email components
                #recipient = supplierMail
                #subject = "RFI"
                body = (f'{short_url}')

                # Encode the subject and body to be URL-safe
                #subject = urllib.parse.quote(subject)
                #encode_body = urllib.parse.quote(body)
                
                st.text(body)
                st.warning(_("Each generated link is unique and can only be shared with one supplier. To share your RFI template with a different supplier, generate a new link."))
                
                # Construct the mailto link
                #mailto_link = f"mailto:{recipient}?subject={subject}&body={encode_body}"
                
                # Open the default mail client with the mailto link
                #webbrowser.open(mailto_link)

                # Pas possible de clear cache et rerun, sinon le lien disparairait tout de suite
                # Desactiver cache de read rfi
                update.rfi(user_id, rfi_details)

            except Exception as e:
                st.error(e)
    else:
        st.write(_("Create your first RFI to send it."))
