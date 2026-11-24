import streamlit as st

from utils.styles import CSS

st.set_page_config(page_title="StudyBuddy", page_icon=None, layout="wide",
                   initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

from pymongo.errors import ServerSelectionTimeoutError
from requests.exceptions import RequestException
from auth.session_manager import init_session, login, logout
from auth.authentication import register, authenticate
from auth.password_manager import hash_password
from auth.password_reset import request_password_reset, reset_password
from utils.validators import valid_email, password_errors
from utils.constants import SUBJECTS, LEVELS, EXPLANATION_STYLES
from database.database_operations import get_profile, save_profile, find_user_by_id
from database.connection import create_indexes, get_database
from utils.layout import render_app_navbar, render_app_sidebar, render_footer, render_public_navbar

try:
    create_indexes(get_database())
except ServerSelectionTimeoutError:
    st.error(
        "Cannot reach MongoDB Atlas. In Atlas, confirm the cluster is running and "
        "add this machine's current public IP to Network Access. Also check that "
        "your network allows outbound connections to MongoDB on port 27017."
    )
    st.stop()
except RuntimeError as exc:
    st.error(f"MongoDB setup issue: {exc}")
    st.stop()

cookies = init_session()
reset_token = st.query_params.get("reset")
if reset_token:
    render_public_navbar("/")
    with st.container(key="auth-screen"):
        _, reset_column, _ = st.columns([1, 1.2, 1])
        with reset_column:
            with st.container(border=True, key="auth-card"):
                st.markdown("## Choose a new password")
                st.write("Reset links expire after 30 minutes and can only be used once.")
                new_password = st.text_input("New password", type="password", key="reset_new_password")
                confirm_password = st.text_input("Confirm new password", type="password",
                                                 key="reset_confirm_password")
                if st.button("Update password", type="primary", use_container_width=True):
                    errors = password_errors(new_password)
                    if new_password != confirm_password:
                        errors.append("Passwords do not match")
                    if errors:
                        for error in errors:
                            st.error(error)
                    elif reset_password(reset_token, hash_password(new_password)):
                        logout()
                        st.query_params.clear()
                        st.success("Password updated. You can now sign in.")
                    else:
                        st.error("This reset link is invalid or has expired. Request a new one.")
    render_footer()
    st.stop()
elif not st.session_state.authenticated:
    render_public_navbar()
    st.markdown("<div id='login'></div>", unsafe_allow_html=True)
    with st.container(key="auth-screen"):
        _, auth_column, _ = st.columns([1, 1.2, 1])
        with auth_column:
            with st.container(border=True, key="auth-card"):
                st.markdown("<div class='lw-auth-heading'>StudyBuddy</div>", unsafe_allow_html=True)
                st.caption("Stay signed in on this device for 30 days.")
                tabs = st.tabs(["Sign In", "Sign Up", "Forgot Password"])
                with tabs[0]:
                    email = st.text_input("Email", key="login_email")
                    password = st.text_input("Password", type="password", key="login_password")
                    if st.button("Sign In", type="primary", use_container_width=True):
                        try:
                            user = authenticate(email, password)
                            if user:
                                login(user, cookies)
                                st.rerun()
                            else:
                                st.error("Email or password is incorrect.")
                        except Exception as exc:
                            st.error(f"Unable to sign in: {exc}")
                with tabs[1]:
                    name = st.text_input("Full name", key="signup_name")
                    email = st.text_input("Email", key="signup_email")
                    password = st.text_input("Password", type="password", key="signup_password")
                    confirm = st.text_input("Confirm password", type="password", key="signup_confirm")
                    if st.button("Create account", type="primary", use_container_width=True):
                        errors = password_errors(password)
                        if not name.strip():
                            errors.append("Enter your full name")
                        if not valid_email(email):
                            errors.append("Enter a valid email")
                        if password != confirm:
                            errors.append("Passwords do not match")
                        if errors:
                            for error in errors:
                                st.error(error)
                        else:
                            try:
                                user_id = register(name.strip(), email, password)
                                user = find_user_by_id(user_id)
                                login(user, cookies)
                                st.rerun()
                            except Exception as exc:
                                st.error(str(exc))
                with tabs[2]:
                    st.write("We'll email you a secure, one-time password reset link.")
                    reset_email = st.text_input("Account email", key="reset_email")
                    if st.button("Send reset link", type="primary", use_container_width=True):
                        if not valid_email(reset_email):
                            st.error("Enter a valid email.")
                        else:
                            try:
                                request_password_reset(reset_email)
                                st.success(
                                    "If an account exists for that email, a reset link is on its way."
                                )
                            except (RequestException, RuntimeError) as exc:
                                st.error(f"Unable to send the reset email: {exc}")
else:
    render_app_sidebar()
    render_app_navbar("Student setup")
    profile = get_profile(st.session_state.user_id)
    if not profile:
        st.markdown("<div class='lw-wordmark'>StudyBuddy</div>", unsafe_allow_html=True)
        st.markdown("### Student onboarding")
        st.write("Set up your learning preferences.")
        name = st.text_input("Student name", value=st.session_state.user["full_name"])
        goal = st.text_input("Learning goal")
        subject = st.selectbox("Subject of interest", SUBJECTS)
        level = st.selectbox("Current knowledge level", LEVELS)
        style = st.selectbox("Preferred explanation style", EXPLANATION_STYLES)
        target = st.slider("Daily learning target (minutes)", 10, 120, 30)
        if st.button("Save and continue", type="primary"):
            if not goal.strip():
                st.error("Enter a learning goal")
            else:
                save_profile(st.session_state.user_id, {
                    "student_name": name.strip(), "learning_goal": goal.strip(),
                    "preferred_subject": subject, "learning_level": level,
                    "explanation_style": style, "daily_target": target
                })
                st.rerun()
    else:
        st.switch_page("pages/1_Dashboard.py")

render_footer()
