import nc_py_api
from json import dumps

def connect():
    # create Nextcloud client instance class
    nc = nc_py_api.Nextcloud(
        nc_auth_user="Jerome",
        nc_auth_pass="GNGGujZ7FiAJH",
        nextcloud_url="http://localhost"
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

    xlsx_data.seek(0)  # Ensure we're at the start of the BytesIO stream

    byte_content = xlsx_data.read()  # Read the entire content as a byte string

    nc_files.upload(filename, byte_content)

