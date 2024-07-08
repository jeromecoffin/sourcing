import streamlit as st
from utils import calculate_kpis

def show_dashboard():
    st.header("Tableau de Bord - KPIs")
    kpis = calculate_kpis()
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Nombre Total de Projets", value=kpis["total_projects"], delta="+ 1")
    col2.metric(label="Nombre Total de Fournisseurs", value=kpis["total_suppliers"], delta="-8%")
    col3.metric(label="Nombre Total de Clients", value=kpis["total_clients"], delta="0")
    col1.metric(label="Nombre Total de RFIs", value=kpis["total_rfis"])
    col2.metric(label="Nombre Total de RFQs", value=kpis["total_rfqs"])
    col3.metric(label="Temps de Réponse Moyen des RFIs (jours)", value=kpis["average_response_time_rfis"])
    col1.metric(label="Temps de Réponse Moyen des RFQs (jours)", value=kpis["average_response_time_rfqs"])
    col2.metric(label="Coût Total des Projets (en devises locales)", value=kpis["total_project_costs"])
    col3.metric(label="Performance Moyenne des Fournisseurs", value=kpis["average_supplier_performance"])
    col1.metric(label="Livraisons à Temps", value=kpis["on_time_deliveries"])
    col2.metric(label="Livraisons en Retard", value=kpis["late_deliveries"])
    col3.metric(label="Échantillons Requis", value=kpis["samples_required"])
