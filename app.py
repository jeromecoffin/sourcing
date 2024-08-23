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
import new_user

# install gettext
#msgfmt locales/en/LC_MESSAGES/messages.po -o locales/en/LC_MESSAGES/messages.mo
#msgfmt locales/fr/LC_MESSAGES/messages.po -o locales/fr/LC_MESSAGES/messages.mo
#msgfmt locales/vi/LC_MESSAGES/messages.po -o locales/vi/LC_MESSAGES/messages.mo

st.set_page_config(layout="wide")
'''hide_menu_style = """
        <style>
        div[data-testid="stToolbar"] {display: none;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)'''

# Load config.yaml for authentication
with open('cred.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

user, authentication_status, username = authenticator.login('main', fields={'Form name': 'login'})

#new = st.button("New?")

#if new:
#    user, username, authentication_status = new_user.newUser(authenticator, config)

if authentication_status:
    # Main content for logged-in users
    user_id = read.agent(username)["_id"]
    _ = utils.translate(user_id)

    authenticator.logout(_('Logout'), 'sidebar')
    st.sidebar.title("AVANTA SOURCING")
    st.sidebar.write(_("Welcome") + " " + user)

    def main():
        firstLogin = read.isFirstLogin(user_id)
        if firstLogin == "0":
            st.warning(_('Please update your settings on first login'))
            menu = [_("Settings"), _("Dashboard"), _("Create RFI"), _("Edit RFI"), _("Share RFI"), _("Support")]
        else:
            menu = [_("Dashboard"), _("Create RFI"), _("Edit RFI"), _("Share RFI"), _("Settings"), _("Support")]
        choice = st.sidebar.selectbox(_("Select an option"), menu)

        if choice == "Create RFI":
            # Initialize session state for dynamic input fields
            if "additional_fields" not in st.session_state:
                st.session_state.additional_fields = []
            create_rfi.create_rfi(user_id)
        
        elif choice == _("Edit RFI"):
            update_rfi.update_rfi(user_id)

        elif choice == _("Share RFI"):
            send_rfi.send_rfi(user_id)

        elif choice == _("Dashboard"):
            manage_rfi.show_dashboard(user_id)
            manage_rfi.list_rfis(user_id)
            manage_rfi.list_suppliers(user_id)

        elif choice == _("Settings"):
            agent_account.show_profile(user_id)
            if st.session_state["authentication_status"]:
                try:
                    if authenticator.reset_password(st.session_state["username"]):
                        st.success(_('Password modified successfully'))
                except Exception as e:
                    st.error(e)
            with open('cred.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)

    if __name__ == "__main__":
        main()

elif authentication_status == False:
    st.error('Username/password is incorrect')