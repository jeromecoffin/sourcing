import streamlit as st
from utils import calculate_kpis

def show_dashboard():
    st.header("Tableau de Bord - KPIs")
    kpis = calculate_kpis()

    st.metric(label="Nombre Total de Projets", value=kpis["total_projects"])
    st.metric(label="Nombre Total de Fournisseurs", value=kpis["total_suppliers"])
    st.metric(label="Nombre Total de Clients", value=kpis["total_clients"])
    st.metric(label="Nombre Total de RFIs", value=kpis["total_rfis"])
    st.metric(label="Nombre Total de RFQs", value=kpis["total_rfqs"])
    st.metric(label="Temps de Réponse Moyen des RFIs (jours)", value=kpis["average_response_time_rfis"])
    st.metric(label="Temps de Réponse Moyen des RFQs (jours)", value=kpis["average_response_time_rfqs"])
    st.metric(label="Coût Total des Projets (en devises locales)", value=kpis["total_project_costs"])
    st.metric(label="Performance Moyenne des Fournisseurs", value=kpis["average_supplier_performance"])
    st.metric(label="Livraisons à Temps", value=kpis["on_time_deliveries"])
    st.metric(label="Livraisons en Retard", value=kpis["late_deliveries"])
    st.metric(label="Échantillons Requis", value=kpis["samples_required"])
