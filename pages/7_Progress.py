import streamlit as st
from utils.styles import CSS

st.set_page_config(page_title="Progress", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

import pandas as pd
import plotly.express as px
from auth.session_manager import init_session
from database.database_operations import get_topic_progress, get_assessments, get_quizzes
from utils.layout import render_app_navbar, render_app_sidebar, render_footer

init_session()
if not st.session_state.authenticated:
    st.switch_page("app.py")
render_app_sidebar("Progress")
render_app_navbar("Progress")

st.subheader("Learning Progress")
progress = get_topic_progress(st.session_state.user_id)
assessments = get_assessments(st.session_state.user_id)
quizzes = get_quizzes(st.session_state.user_id)
if not progress and not assessments and not quizzes:
    st.info("No learning activity has been recorded yet.")
else:
    if assessments:
        df = pd.DataFrame([{"Attempt": i+1, "Score": a["score"]} for i, a in enumerate(reversed(assessments))])
        st.plotly_chart(px.line(df, x="Attempt", y="Score", title="Diagnostic improvement", markers=True,
                                template="plotly_dark", color_discrete_sequence=["#D3D7DD"]),
                        use_container_width=True)
    if quizzes:
        df = pd.DataFrame([{"Attempt": i+1, "Accuracy": q["accuracy"]} for i, q in enumerate(reversed(quizzes))])
        st.plotly_chart(px.bar(df, x="Attempt", y="Accuracy", title="Quiz accuracy",
                               template="plotly_dark", color_discrete_sequence=["#BEC3CC"]),
                        use_container_width=True)
    if progress:
        df = pd.DataFrame([{"Topic": p["topic"], "Mastery": p["mastery_score"],
                            "Status": p["mastery_status"]} for p in progress])
        st.plotly_chart(px.bar(df, x="Topic", y="Mastery", color="Status",
                               title="Topic mastery", range_y=[0, 100],
                               template="plotly_dark",
                               color_discrete_sequence=["#E4E7EC", "#A9AEB7", "#747B86"]),
                        use_container_width=True)

render_footer()
