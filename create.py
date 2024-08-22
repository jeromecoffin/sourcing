import streamlit as st
import utils
import update

def rfi(user_id, rfi_data):
    _ = utils.translate()
    db = utils.initialize_mongodb()
    result = db.rfis.insert_one(rfi_data)
    utils.log_event("Nouveau RFI", details=rfi_data["title"])
    st.success(_("Added New RFI"))
    update.user_rfis(user_id, result.inserted_id)
    st.cache_data.clear()

def log(event_data):
    db = utils.initialize_mongodb()
    db.event_logs.insert_one(event_data)