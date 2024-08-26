import streamlit as st
import yaml
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
