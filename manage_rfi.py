import streamlit as st
import pandas as pd
import read
import utils

def manage():
    _ = utils.translate()
    st.subheader(_("RFIs List"))

    with st.spinner(_("Loading RFIs...")):
        rfis = read.rfis()

    # Ensure RFIs are ordered by date (requestDueDate)
    rfis_sorted = sorted(rfis, key=lambda x: x.get('requestDueDate', ''), reverse=False)

    # Prepare data for the dataframe
    data = {
        "Title": [],
        "Reference": [],
        "Due Date": [],
        "PDF Link": []
    }

    # Populate the data for the table
    for rfi in rfis_sorted:
        title = rfi.get('title', 'Untitled RFI')
        reference = rfi.get('reference', 'No Reference')
        request_date = rfi.get('requestDueDate', 'No Due Date')
        
        # Create a link to the PDF file for each RFI (this is a placeholder link)
        pdf_url = f"https://your-pdf-hosting.com/RFI_{reference}.pdf"  # Adjust this to the actual location
        
        # Append the data to the list
        data["Title"].append(title)
        data["Reference"].append(reference)
        data["Due Date"].append(request_date)
        data["PDF Link"].append(pdf_url)

    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame in Streamlit
    st.dataframe(df)

    # Optionally log event
    # utils.log_event("RFI Dataframe Viewed")




'''
{
  "_id": "9i91d384nNixRcxB3S0L",
  "title": "Request for Accessory Components",
  "reference": "RFI-2024-002",
  "location": "Hanoi, Vietnam",
  "rp_name": "Tran Thi B",
  "rp_company": "XYZ Accessories Co.",
  "rp_position": "Head of Design",
  "rp_mail": "tranthib@xyzaccessories.vn",
  "rp_phone": "+84 987 654 321",
  "requestDate": "2024-08-02",
  "requestDueDate": "2024-08-16",
  "information": "Seeking information on the availability and pricing of accessory components like zippers and buttons.",
  "client": "ABC Garments Ltd.",
  "suppliers": [
    "Home Textiles VN"
  ],
  "comments": "Interested in bulk purchasing options."
}
'''