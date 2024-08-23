from datetime import datetime, timezone, timedelta
from pymongo import MongoClient
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO
import streamlit as st
import gettext
import os
import pandas as pd
import read
import update
import create
from bson.objectid import ObjectId

# Define a custom hash function for ObjectId
def hash_objectid(obj):
    return str(obj)

# Initializes MongoDB using configuration from Streamlit secrets.
def initialize_mongodb():
    client = MongoClient("mongodb://avanta:88888888@localhost:27017/sourcingmain")
    return client.sourcingmain

# Calculates various KPIs from MongoDB collections.
# Output dict (e.g kpis["total_projects"])
def calculate_kpis(user_id):

    total_rfis = read.rfis(user_id)

    total_sent_rfis = 0
    suppliersContacted = []

    for rfi in total_rfis:
        suppliersContacted = rfi["suppliers"]
        total_sent_rfis += len(suppliersContacted)


    return {
        "total_rfis": len(total_rfis),
        "total_sent_rfis": total_sent_rfis
    }

# Detects and splits comma-separated values in 'categories' and 'fields' fields for suppliers.
# Update the MongoDB documents
def detect_and_split_comma_in_lists():

    suppliers = read.suppliers

    for supplier in suppliers:
        supplier_data = supplier
        changed = False
        
        # Check and split 'categories' field if it contains comma
        if 'categories' in supplier_data and isinstance(supplier_data['categories'], list):
            updated_categories = []
            for categories in supplier_data['categories']:
                if ',' in categories:
                    updated_categories.extend([c.strip() for c in categories.split(',')])
                    changed = True
                else:
                    updated_categories.append(categories)
            if changed:
                supplier_data['categories'] = updated_categories
                update.categories(supplier, updated_categories)
        
        # Check and split 'fields' field if it contains comma
        if 'fields' in supplier_data and isinstance(supplier_data['fields'], list):
            updated_fields = []
            for field in supplier_data['fields']:
                if ',' in field:
                    updated_fields.extend([f.strip() for f in field.split(',')])
                    changed = True
                else:
                    updated_fields.append(field)
            if changed:
                supplier_data['fields'] = updated_fields
                update.fields(supplier, updated_fields)

        if changed:
            print(f"Document {supplier['_id']} updated successfully.")
    return changed

# Logs an event with a specific type and details to the MongoDB 'event_logs' collection.
def log_event(event_type, details=None):
    utc_plus_7 = timezone(timedelta(hours=7))
    event_data = {
        "event_type": event_type,
        "timestamp": datetime.now(utc_plus_7).strftime('%Y%m%d%H%M%S'),
        "details": details
    }
    create.log(event_data)

# Configures gettext for translations based on the user's language preference.
def translate(user_id):

    language = read.language(user_id)

    # Configurer le chemin des fichiers de traduction
    locales_dir = os.path.join(os.path.dirname(__file__), 'locales')

    # Configurer gettext pour utiliser les traductions françaises
    lang = language  # 'en' pour anglais, 'vi' pour vietnamien, 'fr' pour français
    gettext.bindtextdomain('messages', locales_dir)
    gettext.textdomain('messages')
    language = gettext.translation('messages', locales_dir, languages=[lang])
    language.install()
    return language.gettext


# Exports a list of suppliers to a CSV file for download.
def export_suppliers_to_csv_management(suppliers):
    _ = translate()
    df = pd.DataFrame(suppliers)
    csv = df.to_csv(index=False)
    st.download_button(label=_("Download CSV"), data=csv, file_name="suppliers_export.csv", mime="text/csv")


# Generates a PDF document (RFI or RFQ) based on provided data.
def generate_pdf(doc_type, doc_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    elements = []

    agent = read.agent()

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=2))
    
    title = Paragraph(f"<b>{doc_type} Document</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    subheader = Paragraph(f"Generated with Avanta Sourcing", styles['Normal'])
    elements.append(subheader)
    elements.append(Spacer(1, 12))

    headerData = [
        ["Title", Paragraph(doc_data['title'], styles['Normal'])],
        ["Reference", Paragraph(doc_data['reference'], styles['Normal'])],
        ["Location", Paragraph(doc_data['location'], styles['Normal'])],
    ]

    headerTable = Table(headerData, colWidths=[2.5 * inch, 4 * inch])
    headerTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(headerTable)
    elements.append(Spacer(1, 6))

    timelineData = [
        ["Request Date", Paragraph(doc_data['requestDate'], styles['Normal'])],
        ["Request Due Date", Paragraph(doc_data['requestDueDate'], styles['Normal'])],
    ]

    timelineTable = Table(timelineData, colWidths=[2.5 * inch, 4 * inch])
    timelineTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(timelineTable)
    elements.append(Spacer(1, 6))

    requestingHeaderData = Paragraph(f"REQUESTING PARTY INFORMATION", styles['Title'])
    elements.append(requestingHeaderData)
    elements.append(Spacer(1, 12))

    requestingData = [
        ["Requesting Party Name", Paragraph(agent['name'], styles['Normal'])],
        ["Requesting Party Lastname", Paragraph(agent['lastname'], styles['Normal'])],
        ["Requesting Party Address", Paragraph(agent['address'], styles['Normal'])],
        ["Requesting Party Email", Paragraph(agent['email'], styles['Normal'])],
        ["Requesting Party Phone", Paragraph(agent['phone'], styles['Normal'])],
    ]

    requestingTable = Table(requestingData, colWidths=[2.5 * inch, 4 * inch])
    requestingTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(requestingTable)
    elements.append(Spacer(1, 6))

    generalInformationData = Paragraph(f"GENERAL INFORMATION", styles['Title'])
    elements.append(generalInformationData)
    elements.append(Spacer(1, 12))

    supplierNameData = [["SUPPLIER NAME", Paragraph('', styles['Normal'])]]

    supplierNameTable = Table(supplierNameData, colWidths=[2.5 * inch, 4 * inch])
    supplierNameTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(supplierNameTable)
    elements.append(Spacer(1, 6))

    supplierContactData= [
        ["CONTACT DETAILS INFORMATION", Paragraph('', styles['Normal'])],
        ["Address", Paragraph('', styles['Normal'])],
        ["City", Paragraph('', styles['Normal'])],
        ["Province", Paragraph('', styles['Normal'])],
        ["ZIP Code", Paragraph('', styles['Normal'])],
        ["Contact Person", Paragraph('', styles['Normal'])],
        ["Job Title", Paragraph('', styles['Normal'])],
        ["email", Paragraph('', styles['Normal'])],
        ["Phone Number", Paragraph('', styles['Normal'])],
        ["Fax Number", Paragraph('', styles['Normal'])],
        ["Website", Paragraph('', styles['Normal'])],
    ]

    supplierContactTable = Table(supplierContactData, colWidths=[2.5 * inch, 4 * inch])
    supplierContactTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(supplierContactTable)
    elements.append(Spacer(1, 6))

    businessInformationData= [
        ["BUSINESS INFORMATION", Paragraph('', styles['Normal'])],
        ["Which year your company was founded?", Paragraph('', styles['Normal'])],
        ["Ownership", Paragraph('', styles['Normal'])],
        ["Capital in million VND", Paragraph('', styles['Normal'])],
        ["What is the workfloor size.", Paragraph('', styles['Normal'])],
        ["How many employees do you have?", Paragraph('', styles['Normal'])],
        ["Do you have export license?", Paragraph('', styles['Normal'])],
        ["% of turnover exported to UE, USA, Others", Paragraph('', styles['Normal'])]
    ]

    businessInformationTable = Table(businessInformationData, colWidths=[2.5 * inch, 4 * inch])
    businessInformationTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(businessInformationTable)
    elements.append(Spacer(1, 6))

    productInformationData= [
        ["PRODUCT INFORMATION", Paragraph('', styles['Normal'])],
        ["Product Name", Paragraph('', styles['Normal'])],
        ["Quantity", Paragraph('', styles['Normal'])],
        ["Material", Paragraph('', styles['Normal'])],
        ["Size", Paragraph('', styles['Normal'])],
        ["Color", Paragraph('', styles['Normal'])],
        ["Accessory", Paragraph('', styles['Normal'])],
        ["Packaging", Paragraph('', styles['Normal'])],
        ["Carton Size (LxWxH)", Paragraph('', styles['Normal'])],
    ]

    productInformationTable = Table(productInformationData, colWidths=[2.5 * inch, 4 * inch])
    productInformationTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(productInformationTable)
    elements.append(Spacer(1, 6))

    logisticsInformationData= [
        ["LOGISTICS INFORMATION", Paragraph('', styles['Normal'])],
        ["Product Name", Paragraph('', styles['Normal'])],
        ["Quantity", Paragraph('', styles['Normal'])],
        ["Weight per Carton", Paragraph('', styles['Normal'])],
        ["FOB port", Paragraph('', styles['Normal'])],
        ["Delivery Time", Paragraph('', styles['Normal'])],
        ["Payment Term", Paragraph('', styles['Normal'])],
        ["Other", Paragraph('', styles['Normal'])]
    ]

    logisticsInformationTable = Table(logisticsInformationData, colWidths=[2.5 * inch, 4 * inch])
    logisticsInformationTable.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(logisticsInformationTable)
    elements.append(Spacer(1, 6))

    if doc_type == "RFI":
        information = Paragraph(f"<b>Information:</b><br/>{doc_data['information']}", styles['Normal'])
        elements.append(information)
    elif doc_type == "RFQ":
        quotationContent = Paragraph(f"<b>Quotation:</b><br/>{doc_data['quotationContent']}", styles['Normal'])
        elements.append(quotationContent)
        
    elements.append(Spacer(1, 6))

    comment = Paragraph(f"<b>Comment:</b><br/>{doc_data['comments']}", styles['Normal'])
    elements.append(comment)

    doc.build(elements)
    buffer.seek(0)
    return buffer