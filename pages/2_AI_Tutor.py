import uuid
import streamlit as st
from utils.styles import CSS

st.set_page_config(page_title="AI Tutor", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

from auth.session_manager import init_session
from database.database_operations import get_profile, get_assessments, save_conversation, get_conversations
from core.tutor_engine import tutor_reply
from core.llm_engine import GeminiAPIError
from utils.layout import render_app_navbar, render_app_sidebar, render_footer

init_session()
if not st.session_state.authenticated:
    st.switch_page("app.py")
render_app_sidebar("AI Tutor")
render_app_navbar("AI Tutor")

profile = get_profile(st.session_state.user_id)
assessments = get_assessments(st.session_state.user_id)
mistakes = []
if assessments:
    mistakes = assessments[0].get("weak_concepts", [])

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

topic = st.session_state.get("selected_topic", profile.get("preferred_subject", "General learning"))
left, main = st.columns([1, 3])
with left:
    with st.container(border=True):
        st.subheader("Learning context")
        st.write(f"**Topic:** {topic}")
        st.write(f"**Level:** {profile.get('learning_level')}")
        st.write(f"**Style:** {profile.get('explanation_style')}")
        st.write("**Understanding:** Not yet measured" if not assessments else f"**Understanding:** {assessments[0].get('score')}% diagnostic")
        if mistakes:
            st.write("**Previous mistakes:** " + ", ".join(mistakes))
        if st.button("New conversation"):
            st.session_state.conversation_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()
with main:
    st.subheader(topic)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    prompt = st.chat_input("Ask your tutor")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            with st.spinner("Your tutor is preparing an explanation..."):
                try:
                    answer = tutor_reply(profile, topic, mistakes, prompt, st.session_state.messages)
                except GeminiAPIError as exc:
                    st.error(f"Your tutor could not respond: {exc}")
                else:
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    save_conversation(st.session_state.user_id, st.session_state.conversation_id,
                                      topic, st.session_state.messages)

render_footer()
