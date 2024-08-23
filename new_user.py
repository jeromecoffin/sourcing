import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import yaml
from yaml.loader import SafeLoader
import agent_account
import create_rfi
import utils
import read
import manage_rfi
import update_rfi
import send_rfi
import create


def newUser(authenticator, config):
    authentication_status = False
    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
    if email_of_registered_user:

        # Add the new user to the credentials
        config['credentials']['usernames'][username_of_registered_user] = {
            'email': email_of_registered_user,
            'name': name_of_registered_user,
            'role': 'user', # Default role
            'password': config['credentials']['usernames'][username_of_registered_user]['password']
        }

        # Save the new credentials back to the YAML file
        with open('cred.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        
        create.new_user(email_of_registered_user, username_of_registered_user, name_of_registered_user)
        st.success('User registered successfully')
        authentication_status = True
        return name_of_registered_user, username_of_registered_user, authentication_status
    return name_of_registered_user, username_of_registered_user, authentication_status
