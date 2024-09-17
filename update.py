import streamlit as st
import utils
from bson import ObjectId

# Define a custom hash function for ObjectId
def hash_objectid(obj):
    return str(obj)

def agent(user_id, agent_data):
    _ = utils.translate(user_id)
    db = utils.initialize_mongodb()
    db.users.update_one({"_id": user_id}, {"$set": agent_data})            
    st.success(_("Data successfully modified!"))
    st.cache_data.clear() # clear cache for language
    st.rerun()

def user_rfis(user_id, rfi_id):
    _ = utils.translate(user_id)
    db = utils.initialize_mongodb()
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    if isinstance(rfi_id, str):
        rfi_id = ObjectId(rfi_id)
    # Update the user's document to add the RFI ObjectId to rfi_ids array
    db.users.update_one(
        {"_id": user_id},
        {"$addToSet": {"rfi_ids": rfi_id}}  # $addToSet prevents duplicates
    )

def rfi(user_id, rfi_data):
    _ = utils.translate(user_id)
    db = utils.initialize_mongodb()
    db.rfis.update_one({"title": rfi_data["title"]}, {"$set": rfi_data})            
    st.success(_("Your mailbox did not respond. Copy/Past the link and share your it to the supplier!"))