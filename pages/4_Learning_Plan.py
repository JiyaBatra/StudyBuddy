import streamlit as st
from utils.styles import CSS

st.set_page_config(page_title="Learning Plan", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

from auth.session_manager import init_session
from database.database_operations import get_learning_plans
from utils.layout import render_app_navbar, render_app_sidebar, render_footer

init_session()
if not st.session_state.authenticated:
    st.switch_page("app.py")
render_app_sidebar("Learning Plan")
render_app_navbar("Learning Plan")

st.subheader("Personalized Learning Plan")
plans = get_learning_plans(st.session_state.user_id, 1)
if not plans:
    st.info("Complete a diagnostic assessment to create a personalized plan.")
else:
    plan = plans[0]
    c1, c2 = st.columns(2)
    c1.markdown("<div class='lw-card'><b>Strong topics</b><br>" + ("<br>".join(plan.get("strong_topics", [])) or "No strong topics recorded") + "</div>", unsafe_allow_html=True)
    c2.markdown("<div class='lw-card'><b>Topics requiring revision</b><br>" + ("<br>".join(plan.get("weak_topics", [])) or "No weak topics recorded") + "</div>", unsafe_allow_html=True)
    st.write(f"**Estimated study time:** {plan.get('estimated_time', 0)} minutes")
    for item in plan.get("topics", []):
        with st.container(border=True):
            st.markdown(f"### {item['topic']}")
            st.write(item["objective"])
            st.caption(f"{item['estimated_minutes']} minutes")
            b1, b2, b3 = st.columns(3)
            if b1.button("Start Learning", key=f"learn_{item['topic']}"):
                st.session_state.selected_topic = item["topic"]
                st.switch_page("pages/2_AI_Tutor.py")
            if b2.button("Practice Questions", key=f"practice_{item['topic']}"):
                st.session_state.selected_topic = item["topic"]
                st.switch_page("pages/5_Adaptive_Quiz.py")
            b3.button("Mark as Completed", key=f"complete_{item['topic']}")

render_footer()
