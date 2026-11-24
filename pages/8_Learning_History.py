import streamlit as st
from utils.styles import CSS

st.set_page_config(page_title="Learning History", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

from auth.session_manager import init_session
from database.database_operations import get_assessments, get_quizzes, get_conversations, get_learning_plans
from utils.layout import render_app_navbar, render_app_sidebar, render_footer

init_session()
if not st.session_state.authenticated:
    st.switch_page("app.py")
render_app_sidebar("Learning History")
render_app_navbar("Learning History")

st.subheader("Learning History")
tabs = st.tabs(["Tutor conversations", "Assessments", "Quizzes", "Learning plans"])
with tabs[0]:
    conversations = get_conversations(st.session_state.user_id)
    if not conversations:
        st.info("No tutor conversations yet.")
    for conversation in conversations:
        with st.expander(conversation.get("topic", "Conversation")):
            for message in conversation.get("messages", []):
                st.markdown(f"**{message['role'].title()}:** {message['content']}")
with tabs[1]:
    assessments = get_assessments(st.session_state.user_id)
    if not assessments:
        st.info("No assessments yet.")
    for item in assessments:
        st.write(f"{item.get('topic')} - {item.get('score')}%")
with tabs[2]:
    quizzes = get_quizzes(st.session_state.user_id)
    if not quizzes:
        st.info("No quiz attempts yet.")
    for item in quizzes:
        st.write(f"{item.get('topic')} - {item.get('accuracy')}% - {item.get('difficulty')} difficulty")
with tabs[3]:
    plans = get_learning_plans(st.session_state.user_id)
    if not plans:
        st.info("No learning plans yet.")
    for item in plans:
        st.write(f"{item.get('subject')} - {item.get('estimated_time')} minutes")

render_footer()
