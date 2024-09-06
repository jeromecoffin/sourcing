import nc_py_api
from json import dumps
import os
import streamlit as st


def connect():
    # create Nextcloud client instance class
    nc = nc_py_api.Nextcloud(
        nc_auth_user="jcoffin",
        nc_auth_pass="abc",
        nextcloud_url="http://nginx-server:81"
    )
    return nc

def capabilities():
    nc = connect()
    pretty_capabilities = dumps(nc.capabilities, indent=4, sort_keys=True)
    print(pretty_capabilities)

def list_dir(directory):
    nc = connect()
    # usual recursive traversing over directories
    for node in nc.files.listdir(directory):
        if node.is_dir:
            list_dir(node)
        else:
            print(f"{node.user_path}")

def create_file(xlsx_data, filename):
    nc = connect()
    nc_files = nc.files

    directory_path = os.path.dirname(filename) + '/'

    nc_files.makedirs(directory_path, exist_ok=True)

    byte_content = xlsx_data.read()  # Read the entire content as a byte string

    nc_files.upload(filename, byte_content)

def sharelink(file_name):
    nc = connect()
    nc_sharing = nc.files.sharing # Access the sharing functionality
    share = nc_sharing.create(
        path=file_name,  # The file you want to share
        share_type=3,      # Public link
        permissions=31     # Full permissions (edit rights)
    )
    # Step 5: Get the share link URL
    share_link_url = share.url

    # Open direclty onlyoffice
    onlyoffice_link = share_link_url.replace("/s/", "/apps/onlyoffice/s/")
    
    return onlyoffice_link
