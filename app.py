import streamlit as st
from firebase_admin import credentials, firestore, initialize_app
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import onboarding
import agent_account
import supplier_management
import rfi_rfq_management
import kpi_dashboard
import project_management
from utils import initialize_firebase
import utils

# install gettext
#msgfmt locales/en/LC_MESSAGES/messages.po -o locales/en/LC_MESSAGES/messages.mo
#msgfmt locales/fr/LC_MESSAGES/messages.po -o locales/fr/LC_MESSAGES/messages.mo
#msgfmt locales/vi/LC_MESSAGES/messages.po -o locales/vi/LC_MESSAGES/messages.mo

# Initialize Firebase
initialize_firebase()

st.set_page_config(layout="wide")

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

user, authentication_status, username = authenticator.login('main', fields = {'Form name': 'login'})
_ = utils.translate()
if authentication_status:

    authenticator.logout(_('Logout'), 'sidebar')
    st.sidebar.title(f"{_('Welcome')} {user}")

    def main():
        
        menu = [_("Dashboard"), _("Onboarding"), _("Project Management"), _("Suppliers Management"), _("RFI/RFQ"), _("Account")]
        choice = st.sidebar.selectbox(_("Select an option"), menu)

        if choice == _("Dashboard"):
            kpi_dashboard.show_dashboard()
            st.divider()
            with st.form("kpi_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder=_("More KPI, other details..."))
                submit = st.form_submit_button(_("Submit"))
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success(_("Thanks for feedback!"))
        elif choice == _("Onboarding"):
            onboarding.show_onboarding()
            st.divider()
            with st.form("onboarding_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder=_("More customer data..."))
                submit = st.form_submit_button(_("Submit"))
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success(_("Thanks for feedback!"))
        elif choice == _("Project Management"):
            project_management.manage_projects()
            st.divider()
            with st.form("projets_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder=_("Add field xxx ; More RFIs..."))
                submit = st.form_submit_button(_("Submit"))
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success(_("Thanks for feedback!"))
        elif choice == _("Suppliers Management"):
            supplier_management.manage_suppliers()
            st.divider()
            with st.form("suppliers_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder=_("More/less fields if the new client form ; display other details in the list..."))
                submit = st.form_submit_button(_("Submit"))
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success(_("Thanks for feedback!"))
        elif choice == "RFI/RFQ":
            rfi_rfq_management.manage_rfi_rfq()
            st.divider()
            with st.form("documents_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder=_("Modify fields for RFI/RFQ..."))
                submit = st.form_submit_button(_("Submit"))
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success(_("Thanks for feedback!"))
        elif choice == _("Account"):
            agent_account.show_profile()
            if st.session_state["authentication_status"]:
                try:
                    if authenticator.reset_password(st.session_state["username"]):
                        st.success(_('Password modified successfully'))
                except Exception as e:
                    st.error(e)
            with open('cred.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.divider()
            with st.form("documents_feedback_form", clear_on_submit=True):
                feedback = st.text_area("feedback", placeholder=_("Data to generate invoices..."))
                submit = st.form_submit_button(_("Submit"))
                if submit:
                    user_feedback = {
                        "module": choice,
                        "feedback": feedback,
                    }
                    db = firestore.client()
                    db.collection("feedbacks").add(user_feedback)
                    st.success(_("Thanks for feedback!"))



    if __name__ == "__main__":
        main()

elif authentication_status == False:
    st.error(_('Username/password is incorrect'))
elif authentication_status == None:
    st.warning(_('Please enter your username and password'))
