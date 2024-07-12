from datetime import datetime, timezone
from firebase_admin import credentials, firestore, initialize_app, _apps
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO

def initialize_firebase():
    if not _apps:
        cred = credentials.Certificate('firebase_config.json')
        initialize_app(cred)

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

    otherData = [
        #["Client:", Paragraph(doc_data['client'], styles['Normal'])],
        #["Suppliers:", Paragraph("\n".join(doc_data['suppliers']), styles['Normal'])],  # Convert list to string
        #["Comments:", Paragraph(doc_data['comments'], styles['Normal'])],
    ]

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

def get_suppliers():
    db = firestore.client()
    suppliers_ref = db.collection("suppliers")
    suppliers = suppliers_ref.get()
    return [supplier.to_dict()["name"] for supplier in suppliers]

def get_rfis():
    db = firestore.client()
    rfis_ref = db.collection("rfis")
    rfis = rfis_ref.get()
    return [rfi.to_dict()["title"] for rfi in rfis]

def get_rfqs():
    db = firestore.client()
    rfqs_ref = db.collection("rfqs")
    rfqs = rfqs_ref.get()
    return [rfq.to_dict()["title"] for rfq in rfqs]

def get_clients():
    db = firestore.client()
    clients_ref = db.collection("clients")
    clients = clients_ref.get()
    return [client.to_dict()["name"] for client in clients]