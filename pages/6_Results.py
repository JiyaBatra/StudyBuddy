import streamlit as st
from utils.styles import CSS

st.set_page_config(page_title="Learning Results", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

from auth.session_manager import init_session
from database.database_operations import get_assessments, get_quizzes
from utils.layout import render_app_navbar, render_app_sidebar, render_footer

init_session()
if not st.session_state.authenticated:
    st.switch_page("app.py")
render_app_sidebar("Results")
render_app_navbar("Learning Results")

st.subheader("Learning Results")
assessments = get_assessments(st.session_state.user_id, 10)
quizzes = get_quizzes(st.session_state.user_id, 10)
if not assessments and not quizzes:
    st.info("No assessment or quiz results yet.")
else:
    if assessments:
        latest = assessments[0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Latest diagnostic", f"{latest.get('score', 0)}%")
        c2.metric("Strong concepts", len(latest.get("strong_concepts", [])))
        c3.metric("Concepts to revise", len(latest.get("weak_concepts", [])))
        with st.container(border=True):
            st.write("**Weak concepts:** " + (", ".join(latest.get("weak_concepts", [])) or "None recorded"))
            st.write("**Strong concepts:** " + (", ".join(latest.get("strong_concepts", [])) or "None recorded"))
    if len(assessments) >= 2:
        change = assessments[0].get("score", 0) - assessments[1].get("score", 0)
        st.metric("Diagnostic change", f"{change:+.1f} percentage points")

render_footer()
