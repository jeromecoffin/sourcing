import nc_py_api
from json import dumps
import os
import utils

def connect():
    
    # Retrieve environment variables
    nc_user = os.getenv('NC_USER')
    nc_pass = os.getenv('NC_PASS')
    nc_url = os.getenv('NC_URL')

    # Check for missing values and raise an error if any are not provided
    if not nc_user or not nc_pass or not nc_url:
        utils.log_event("connect nextcloud", details="Missing one or more Nextcloud environment variables (NC_USER, NC_PASS, NC_URL)")
        raise EnvironmentError("Nextcloud connection credentials are not fully set.")

    try:
        # Connect to Nextcloud
        nc = nc_py_api.Nextcloud(
            nc_auth_user=nc_user,
            nc_auth_pass=nc_pass,
            nextcloud_url=nc_url,
            npa_nc_cert=False  # Assuming you're not verifying SSL certs
        )

        return nc
    
    except Exception as e:
        utils.log_event("connect nextcloud", details=e)
        raise

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

