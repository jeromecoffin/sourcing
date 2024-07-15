import streamlit as st
from utils import calculate_kpis

def show_dashboard():
    st.header("Tableau de Bord")
    kpis = calculate_kpis()
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Nombre Total de Projets", value=kpis["total_projects"])
    #col2.metric(label="Nombre de Projets en Cours", value="1", delta="+ 1")
    #col3.metric(label="Nombre de Projets Cloturés", value="1", delta="")
    col1.metric(label="Nombre Total de Fournisseurs", value=kpis["total_suppliers"])
    col2.metric(label="Nombre Total de Clients", value=kpis["total_clients"])
    col1.metric(label="Nombre Total de RFIs", value=kpis["total_rfis"])
    #col2.metric(label="Nombre de RFIs Envoyés", value="50")
    col1.metric(label="Nombre Total de RFQs", value=kpis["total_rfqs"])
    #col2.metric(label="Nombre de RFQs Envoyés", value="20")
