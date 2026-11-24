import streamlit as st
from utils.styles import CSS

st.set_page_config(page_title="Profile", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

from auth.session_manager import init_session, logout
from auth.password_manager import hash_password
from database.database_operations import get_profile, save_profile, update_user
from utils.constants import LEVELS, EXPLANATION_STYLES, SUBJECTS
from utils.validators import password_errors
from utils.layout import render_app_navbar, render_app_sidebar, render_footer

init_session()
if not st.session_state.authenticated:
    st.switch_page("app.py")
render_app_sidebar("Profile & Settings")
render_app_navbar("Profile & Settings")

profile = get_profile(st.session_state.user_id)
st.subheader("Profile and Settings")
name = st.text_input("Student name", profile.get("student_name", st.session_state.user["full_name"]))
goal = st.text_input("Learning goal", profile.get("learning_goal", ""))
subject = st.selectbox("Preferred subject", SUBJECTS,
                       index=SUBJECTS.index(profile.get("preferred_subject", SUBJECTS[0])))
level = st.selectbox("Learning level", LEVELS,
                     index=LEVELS.index(profile.get("learning_level", "Beginner")))
style = st.selectbox("Explanation style", EXPLANATION_STYLES,
                     index=EXPLANATION_STYLES.index(profile.get("explanation_style", EXPLANATION_STYLES[0])))
target = st.slider("Daily target", 10, 120, profile.get("daily_target", 30))
if st.button("Update profile", type="primary"):
    save_profile(st.session_state.user_id, {"student_name": name, "learning_goal": goal,
                 "preferred_subject": subject, "learning_level": level,
                 "explanation_style": style, "daily_target": target})
    update_user(st.session_state.user_id, {"full_name": name})
    st.success("Profile updated.")

st.divider()
new_password = st.text_input("New password", type="password")
confirm_password = st.text_input("Confirm new password", type="password")
if st.button("Update password"):
    errors = password_errors(new_password)
    if new_password != confirm_password:
        errors.append("Passwords do not match")
    if errors:
        for error in errors:
            st.error(error)
    else:
        update_user(st.session_state.user_id, {"password_hash": hash_password(new_password)})
        st.success("Password updated.")
if st.button("Logout"):
    logout()
    st.switch_page("app.py")

render_footer()
