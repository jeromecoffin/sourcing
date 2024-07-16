import streamlit as st
from utils import calculate_kpis
import gettext
import os
import utils

def show_dashboard():
    
    _ = utils.translate()

    st.header(_("Dashboard"))
    kpis = calculate_kpis()
    col1, col2, col3 = st.columns(3)
    col1.metric(label=_("Total Number of Projects"), value=kpis["total_projects"])
    col1.metric(label=_("Total Number of suppliers"), value=kpis["total_suppliers"])
    col2.metric(label=_("Total Number of Customers"), value=kpis["total_clients"])
    col1.metric(label=_("Total Number of RFIs"), value=kpis["total_rfis"])
    col1.metric(label=_("Total Number of RFQs"), value=kpis["total_rfqs"])
