import streamlit as st
from utils.styles import CSS

st.set_page_config(page_title="Diagnostic Assessment", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

from auth.session_manager import init_session
from database.database_operations import get_profile, save_assessment, save_topic_progress
from core.assessment_engine import generate_diagnostic, evaluate
from core.learning_plan import build_learning_plan
from database.database_operations import save_learning_plan
from utils.constants import SUBJECTS
from core.llm_engine import GeminiAPIError
from utils.layout import render_app_navbar, render_app_sidebar, render_footer

init_session()
if not st.session_state.authenticated:
    st.switch_page("app.py")
render_app_sidebar("Assessments")
render_app_navbar("Diagnostic Assessment")

profile = get_profile(st.session_state.user_id)
st.subheader("Diagnostic Assessment")

if "diag_questions" not in st.session_state:
    subject = st.selectbox("Subject", SUBJECTS,
                           index=SUBJECTS.index(profile.get("preferred_subject", SUBJECTS[0])))
    topic = st.text_input("Topic", value="Foundations")
    if st.button("Generate five questions", type="primary"):
        with st.spinner("Preparing your diagnostic..."):
            try:
                questions = generate_diagnostic(subject, topic)
            except GeminiAPIError as exc:
                st.error(f"Could not generate assessment: {exc}")
            else:
                st.session_state.diag_questions = questions
                st.session_state.diag_subject = subject
                st.session_state.diag_topic = topic
                st.session_state.diag_answers = [""] * len(questions)
                st.rerun()
else:
    questions = st.session_state.diag_questions
    if "diag_index" not in st.session_state:
        st.session_state.diag_index = 0
    index = st.session_state.diag_index
    st.progress((index + 1) / len(questions))
    st.caption(f"Question {index + 1} of {len(questions)}")
    q = questions[index]
    st.markdown(f"**{q['question']}**")
    if q["type"] == "multiple_choice":
        answer = st.radio("Select one answer", q["options"],
                          index=None, key=f"diag_answer_{index}")
        if answer:
            st.session_state.diag_answers[index] = answer
    else:
        answer = st.text_input("Your answer", key=f"diag_answer_{index}",
                               value=st.session_state.diag_answers[index])
        st.session_state.diag_answers[index] = answer

    c1, c2, c3 = st.columns(3)
    with c1:
        if index > 0 and st.button("Previous"):
            st.session_state.diag_index -= 1
            st.rerun()
    with c2:
        if index < len(questions) - 1 and st.button("Next"):
            st.session_state.diag_index += 1
            st.rerun()
    with c3:
        if st.button("Submit assessment", type="primary"):
            result = evaluate(questions, st.session_state.diag_answers)
            record = {"subject": st.session_state.diag_subject,
                      "topic": st.session_state.diag_topic,
                      "questions": questions, "submitted_answers": st.session_state.diag_answers,
                      "score": result["score"], "weak_concepts": result["weak_concepts"],
                      "strong_concepts": result["strong_concepts"]}
            save_assessment({**record, "user_id": st.session_state.user_id})
            save_topic_progress(st.session_state.user_id, record["subject"], record["topic"],
                                result["score"], 1)
            plan = build_learning_plan(record["subject"], result["weak_concepts"], result["strong_concepts"])
            save_learning_plan(st.session_state.user_id, plan)
            st.session_state.assessment_result = result
            del st.session_state.diag_questions
            st.success("Assessment submitted. Your learning plan has been created.")

render_footer()
