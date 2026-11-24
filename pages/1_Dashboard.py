import streamlit as st
from utils.styles import CSS

st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

from auth.session_manager import init_session
from database.database_operations import get_profile, get_assessments, get_quizzes, get_topic_progress, get_learning_plans
from utils.layout import render_app_navbar, render_app_sidebar, render_footer

init_session()
if not st.session_state.authenticated:
    st.switch_page("app.py")
render_app_sidebar("Dashboard")
render_app_navbar("Dashboard")

profile = get_profile(st.session_state.user_id)
assessments = get_assessments(st.session_state.user_id, 5)
quizzes = get_quizzes(st.session_state.user_id, 5)
progress = get_topic_progress(st.session_state.user_id)

st.markdown(f"## Welcome, {profile.get('student_name', st.session_state.user['full_name'])}")
st.write("Your learning journey starts here." if not assessments and not quizzes else "Continue from your latest learning activity.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Diagnostic assessments", len(assessments))
c2.metric("Quiz attempts", len(quizzes))
c3.metric("Topics tracked", len(progress))
c4.metric("Daily target", f"{profile.get('daily_target', 30)} min")

left, right = st.columns([2, 1])
with left:
    with st.container(border=True):
        st.subheader("Continue Learning")
        if assessments:
            latest = assessments[0]
            st.write(f"{latest.get('subject')} - {latest.get('topic')}")
            if st.button("Open AI Tutor", type="primary"):
                st.session_state.selected_topic = latest.get("topic", profile.get("preferred_subject"))
                st.switch_page("pages/2_AI_Tutor.py")
        else:
            st.write("Take a diagnostic assessment to create your first learning plan.")
            if st.button("Start diagnostic", type="primary"):
                st.switch_page("pages/3_Assessment.py")
with right:
    with st.container(border=True):
        st.subheader("Your preferences")
        st.write(profile.get("learning_level"))
        st.write(profile.get("explanation_style"))

render_footer()
