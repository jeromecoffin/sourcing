from datetime import datetime, timezone, timedelta
from firebase_admin import credentials, firestore, initialize_app, _apps
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
import get

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
import get

# Initializes MongoDB using configuration from Streamlit secrets.
def initialize_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    return client.sourcingmain

# Calculates various KPIs from MongoDB collections.
# Output dict (e.g kpis["total_projects"])
@st.cache_data(ttl=3600)
def calculate_kpis():
    db = initialize_mongodb()

    total_projects = list(db.projects.find())
    total_suppliers = list(db.suppliers.find())
    total_clients = list(db.clients.find())
    total_rfis = list(db.rfis.find())
    total_rfqs = list(db.rfqs.find())

    now = datetime.now(timezone.utc)

    def get_date_safe(doc, field):
        date_str = doc.get(field)
        if isinstance(date_str, str):
            return datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
        elif isinstance(date_str, datetime):
            return date_str
        return now

    average_response_time_rfis = sum([(now - get_date_safe(rfi, "due_date")).days for rfi in total_rfis]) / len(total_rfis) if total_rfis else 0
    average_response_time_rfqs = sum([(now - get_date_safe(rfq, "due_date")).days for rfq in total_rfqs]) / len(total_rfqs) if total_rfqs else 0

    total_project_costs = sum([rfq.get("budget", 0) for rfq in total_rfqs])
    average_supplier_performance = sum([supplier.get("rating", 0) for supplier in total_suppliers]) / len(total_suppliers) if total_suppliers else 0

    on_time_deliveries = len([rfq for rfq in total_rfqs if get_date_safe(rfq, "delivery_date") <= get_date_safe(rfq, "due_date")])
    late_deliveries = len(total_rfqs) - on_time_deliveries

    samples_required = len([rfi for rfi in total_rfis if rfi.get("samples_required", False)])

    return {
        "total_projects": len(total_projects),
        "total_suppliers": len(total_suppliers),
        "total_clients": len(total_clients),
        "total_rfis": len(total_rfis),
        "total_rfqs": len(total_rfqs),
        "average_response_time_rfis": average_response_time_rfis,
        "average_response_time_rfqs": average_response_time_rfqs,
        "total_project_costs": total_project_costs,
        "average_supplier_performance": average_supplier_performance,
        "on_time_deliveries": on_time_deliveries,
        "late_deliveries": late_deliveries,
        "samples_required": samples_required
    }

# Detects and splits comma-separated values in 'categories' and 'fields' fields for suppliers.
# Update the MongoDB documents
def detect_and_split_comma_in_lists():
    db = initialize_mongodb()
    suppliers = db.suppliers.find()

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
                db.suppliers.update_one({'_id': supplier['_id']}, {'$set': {'categories': updated_categories}})
        
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
                db.suppliers.update_one({'_id': supplier['_id']}, {'$set': {'fields': updated_fields}})

        if changed:
            print(f"Document {supplier['_id']} updated successfully.")
    return changed

# Logs an event with a specific type and details to the MongoDB 'event_logs' collection.
def log_event(event_type, details=None):
    db = initialize_mongodb()
    utc_plus_7 = timezone(timedelta(hours=7))
    event_data = {
        "event_type": event_type,
        "timestamp": datetime.now(utc_plus_7).strftime('%Y%m%d%H%M%S'),
        "details": details
    }
    db.event_logs.insert_one(event_data)

# Configures gettext for translations based on the user's language preference.
def translate():

    language = get.get_language()

    # Configurer le chemin des fichiers de traduction
    locales_dir = os.path.join(os.path.dirname(__file__), 'locales')

    # Configurer gettext pour utiliser les traductions françaises
    lang = language  # 'en' pour anglais, 'vi' pour vietnamien, 'fr' pour français
    gettext.bindtextdomain('messages', locales_dir)
    gettext.textdomain('messages')
    language = gettext.translation('messages', locales_dir, languages=[lang])
    language.install()
    return language.gettext

# Updates a project's data in the MongoDB 'projects' collection.
# Input : Project "id" and Project dict 
def update_project(doc_id, project_data):
    db = initialize_mongodb()
    db.projects.update_one({'_id': doc_id}, {'$set': project_data})

# Updates supplier data in the MongoDB 'suppliers' collection.
# Input : supplier id and supplier dict 
def update_supplier_management(supplier_id, supplier_data):
    db = initialize_mongodb()
    db.suppliers.update_one({'_id': supplier_id}, {'$set': supplier_data})

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

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=2))
    
    title = Paragraph(f"<b>{doc_type} Document</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    headerData = [
        ["Title:", Paragraph(doc_data['title'], styles['Normal'])],
        ["Reference:", Paragraph(doc_data['reference'], styles['Normal'])],
        ["Location:", Paragraph(doc_data['location'], styles['Normal'])],
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

    requestingData = [
        ["Requesting Party Name:", Paragraph(doc_data['rp_name'], styles['Normal'])],
        ["Requesting Party Company:", Paragraph(doc_data['rp_company'], styles['Normal'])],
        ["Requesting Party Position:", Paragraph(doc_data['rp_position'], styles['Normal'])],
        ["Requesting Party Email:", Paragraph(doc_data['rp_mail'], styles['Normal'])],
        ["Requesting Party Phone:", Paragraph(doc_data['rp_phone'], styles['Normal'])],
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

    timelineData = [
        ["Request Date:", Paragraph(doc_data['requestDate'], styles['Normal'])],
        ["Request Due Date:", Paragraph(doc_data['requestDueDate'], styles['Normal'])],
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

    #otherData = [
        #["Client:", Paragraph(doc_data['client'], styles['Normal'])],
        #["Suppliers:", Paragraph("\n".join(doc_data['suppliers']), styles['Normal'])],  # Convert list to string
        #["Comments:", Paragraph(doc_data['comments'], styles['Normal'])],
    #]

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