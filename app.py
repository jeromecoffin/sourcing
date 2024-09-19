import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import yaml
from yaml.loader import SafeLoader
import settings
import create_rfi
import utils
import read
import manage_rfi
import update_rfi
import send_rfi
import create

def main():
    # Main content for logged-in users
    user_id = read.agent(username)["_id"]
    _ = utils.translate(user_id)

    authenticator.logout(_('Logout'), 'sidebar')
    #if st.sidebar.button(label="Logout", use_container_width=True,type='primary'):
    #    authenticator.logout()
    #    st.session_state.authentication_status=None
    #    st.rerun()
    st.sidebar.title("AVANTA SOURCING RFI")
    st.sidebar.write(_("Welcome") + " " + user)
    firstLogin = read.isFirstLogin(user_id)
    if firstLogin == "0":
        st.warning(_('Please update your settings on first login'))
        menu = [_("Settings"), _("Dashboard"), _("Create RFI"), _("Send RFI"), _("Support")]
    else:
        menu = [_("Dashboard"), _("Create RFI"), _("Send RFI"), _("Settings"), _("Support")]
    choice = st.sidebar.selectbox(_("Select an option"), menu)

    if choice == _("Dashboard"):
        manage_rfi.show_dashboard(user_id)
        manage_rfi.list_rfis(user_id)
        manage_rfi.list_suppliers(user_id)

    elif choice == _("Create RFI"):
        if "additional_fields" not in st.session_state:
            st.session_state.additional_fields = []
        create_rfi.create_rfi(user_id)

    elif choice == _("Send RFI"):
        send_rfi.send_rfi(user_id)

    elif choice == _("Settings"):
        settings.show_profile(user_id)
        if st.session_state["authentication_status"]:
            try:
                if authenticator.reset_password(st.session_state["username"]):
                    st.success(_('Password modified successfully'))
            except Exception as e:
                st.error(e)
        with open('auth/cred.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    
    elif choice == _("Support"):
        url = "jerome.avanta-sourcing.com"
        st.title(_("Thank you for using Avanta Sourcing RFI Generator"))
        st.write(_("If you need any assistance, please contact : hello@avanta-sourcing.com"))
        st.subheader(_("Created by Jerome Coffin : https://www.jerome.avanta-sourcing.com"))


# install gettext
#msgfmt locales/en/LC_MESSAGES/messages.po -o locales/en/LC_MESSAGES/messages.mo
#msgfmt locales/fr/LC_MESSAGES/messages.po -o locales/fr/LC_MESSAGES/messages.mo
#msgfmt locales/vi/LC_MESSAGES/messages.po -o locales/vi/LC_MESSAGES/messages.mo

st.set_page_config(layout="wide", page_title="Avanta RFI", page_icon="🧑‍💻")

hide_menu_style = """
    <style>
    div[data-testid="stToolbar"] {display: none;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Load config.yaml for authentication
with open('auth/cred.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

col1, col2 = st.columns(2)
with col2:
    if st.session_state["authentication_status"] == None or st.session_state["authentication_status"] == False :
        st.container(height=200, border=False)
    user, authentication_status, username = authenticator.login('main', fields={'Form name': 'login'})

if authentication_status == None or authentication_status == False :
    try:
        with col1:
            logo = """
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-layers-half" viewbox="0 0 16 16">
                <path d="M8.235 1.559a.5.5 0 0 0-.47 0l-7.5 4a.5.5 0 0 0 0 .882L3.188 8 .264 9.559a.5.5 0 0 0 0 .882l7.5 4a.5.5 0 0 0 .47 0l7.5-4a.5.5 0 0 0 0-.882L12.813 8l2.922-1.559a.5.5 0 0 0 0-.882l-7.5-4zM8 9.433 1.562 6 8 2.567 14.438 6 8 9.433z"/>
            </svg>
            <span class="ms-1 fw-bolder">Avanta Sourcing</span>
            """
            st.markdown(logo, unsafe_allow_html=True)
            st.title("Welcome to Avanta-Sourcing RFI Generator!")
            st.subheader("Please login or create a new account.")
            email, username, user = authenticator.register_user(pre_authorization=False)
            if email:
                # Redirect to Stripe payment link after registration
                st.success('User registered successfully. Please complete payment to activate your account.')
                payment_link = "https://buy.stripe.com/test_00g28sfG8a4p81y6op?locale=en-GB"
                st.link_button("Complete Payment", payment_link)
                create.new_user(email, username, user)
                with open('auth/cred.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)

elif authentication_status == True :
    if __name__ == "__main__":
        try:
            main()
        except Exception as e:
            st.error(e)

st.divider()
st.write("Any Questions? hello@avanta-sourcing.com")