from datetime import datetime, timezone, timedelta
from firebase_admin import credentials, firestore, initialize_app, _apps
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO
import streamlit as st
import gettext
import os

def initialize_firebase():
    if not _apps:
        firebase_config = st.secrets["firebase"]
        cred = credentials.Certificate({
            "type": firebase_config["type"],
            "project_id": firebase_config["project_id"],
            "private_key_id": firebase_config["private_key_id"],
            "private_key": firebase_config["private_key"].replace("\\n", "\n"),
            "client_email": firebase_config["client_email"],
            "client_id": firebase_config["client_id"],
            "auth_uri": firebase_config["auth_uri"],
            "token_uri": firebase_config["token_uri"],
            "auth_provider_x509_cert_url": firebase_config["auth_provider_x509_cert_url"],
            "client_x509_cert_url": firebase_config["client_x509_cert_url"],
            "universe_domain": firebase_config["universe_domain"]
        })
        initialize_app(cred)

@st.cache_data(ttl=3600)
def calculate_kpis():
    db = firestore.client()

    total_projects = db.collection("projects").get()
    total_suppliers = db.collection("suppliers").get()
    total_clients = db.collection("clients").get()
    total_rfis = db.collection("rfis").get()
    total_rfqs = db.collection("rfqs").get()

    now = datetime.now(timezone.utc)

    def get_date_safe(doc, field):
        date_str = doc.to_dict().get(field)
        if isinstance(date_str, str):
            return datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
        elif isinstance(date_str, datetime):
            return date_str
        return now

    average_response_time_rfis = sum([(now - get_date_safe(rfi, "due_date")).days for rfi in total_rfis]) / len(total_rfis) if total_rfis else 0
    average_response_time_rfqs = sum([(now - get_date_safe(rfq, "due_date")).days for rfq in total_rfqs]) / len(total_rfqs) if total_rfqs else 0

    total_project_costs = sum([rfq.to_dict().get("budget", 0) for rfq in total_rfqs])
    average_supplier_performance = sum([supplier.to_dict().get("rating", 0) for supplier in total_suppliers]) / len(total_suppliers) if total_suppliers else 0

    on_time_deliveries = len([rfq for rfq in total_rfqs if get_date_safe(rfq, "delivery_date") <= get_date_safe(rfq, "due_date")])
    late_deliveries = len(total_rfqs) - on_time_deliveries

    samples_required = len([rfi for rfi in total_rfis if rfi.to_dict().get("samples_required", False)])

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

@st.cache_data(ttl=3600)
def get_suppliers():
    db = firestore.client()
    suppliers_ref = db.collection("suppliers")
    suppliers = suppliers_ref.get()
    return [supplier.to_dict()["name"] for supplier in suppliers]

@st.cache_data(ttl=3600)
def get_rfis():
    db = firestore.client()
    rfis_ref = db.collection("rfis")
    rfis = rfis_ref.get()
    return [rfi.to_dict()["title"] for rfi in rfis]

@st.cache_data(ttl=3600)
def get_rfqs():
    db = firestore.client()
    rfqs_ref = db.collection("rfqs")
    rfqs = rfqs_ref.get()
    return [rfq.to_dict()["title"] for rfq in rfqs]

@st.cache_data(ttl=3600)
def get_clients():
    db = firestore.client()
    clients_ref = db.collection("clients")
    clients = clients_ref.get()
    return [client.to_dict()["name"] for client in clients]

def detect_and_split_comma_in_lists():
    db = firestore.client()
    suppliers_ref = db.collection("suppliers")
    docs = suppliers_ref.stream()

    for doc in docs:
        supplier_data = doc.to_dict()
        changed = False
        
        # Check and split 'category' field if it contains comma
        if 'category' in supplier_data and isinstance(supplier_data['category'], list):
            updated_categories = []
            for category in supplier_data['category']:
                if ',' in category:
                    updated_categories.extend([c.strip() for c in category.split(',')])
                    changed = True
                else:
                    updated_categories.append(category)
            if changed:
                supplier_data['category'] = updated_categories
                doc.reference.update({'category': updated_categories})
        
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
                doc.reference.update({'fields': updated_fields})

        if changed:
            print(f"Document {doc.id} updated successfully.")
    return changed

def log_event(event_type, details=None):
    utc_plus_7 = timezone(timedelta(hours=7))
    event_data = {
        "event_type": event_type,
        "timestamp": datetime.now(utc_plus_7).strftime('%Y%m%d%H%M%S'),
        "details": details
    }
    db = firestore.client()
    db.collection("event_logs").add(event_data)

def translate():

    db = firestore.client()
    agent_ref = db.collection("agents").document("user")
    agent = agent_ref.get()

    try: 
        language = agent.to_dict()["language"]
    except:
        language = 'en'

    # Configurer le chemin des fichiers de traduction
    locales_dir = os.path.join(os.path.dirname(__file__), 'locales')

    # Configurer gettext pour utiliser les traductions françaises
    lang = language  # 'en' pour anglais, 'vi' pour vietnamien, 'fr' pour français
    gettext.bindtextdomain('messages', locales_dir)
    gettext.textdomain('messages')
    language = gettext.translation('messages', locales_dir, languages=[lang])
    language.install()
    return language.gettext