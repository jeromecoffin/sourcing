from datetime import datetime, timezone
from firebase_admin import credentials, firestore, initialize_app, _apps
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 50, f"{doc_type} Document")
    p.drawString(100, height - 70, f"Title: {doc_data['title']}")
    #p.drawString(100, height - 90, f"Content: {doc_data['content']}")
    p.drawString(100, height - 110, f"Due Date: {doc_data['due_date']}")
    p.drawString(100, height - 130, f"User ID: {doc_data['user_id']}")
    #p.drawString(100, height - 150, f"Creation Date: {doc_data['creation_date']}")
    if doc_type == "RFQ":
        p.drawString(100, height - 170, f"Budget: {doc_data['budget']}")

    p.showPage()
    p.save()
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