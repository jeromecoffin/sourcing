import streamlit as st
import utils
import update

# Define a custom hash function for ObjectId
def hash_objectid(obj):
    return str(obj)

# Access in create_rfi
def rfi(user_id, rfi_data):

    _ = utils.translate(user_id)

    db = utils.initialize_mongodb()
    result = db.rfis.insert_one(rfi_data)

    utils.log_event("Nouveau RFI", details=rfi_data["title"])
    st.success(_("Added New RFI"))

    update.user_rfis(user_id, result.inserted_id)
    st.cache_data.clear()

# Access in utils
def log(event_data):

    db = utils.initialize_mongodb()
    db.event_logs.insert_one(event_data)

# Access in app
def new_user(email, username, name):

    db = utils.initialize_mongodb()

    user_data = {
        "email": email,
        "username": username,
        "name": name,
        "language": "en",
        "company": "Freelance",
        "sourcing": "Garments, Accessories...",
        "lastname": "",
        "phone": "",
        "address": "",
        "experience": 1,
        "isFirstLogin": "0",
        "rfi_ids": []
    }

    db.users.insert_one(user_data)

    utils.log_event("Nouveau user", details=user_data["email"])
