import streamlit as st
from utils.styles import CSS

st.set_page_config(page_title="Adaptive Quiz", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)

from auth.session_manager import init_session
from database.database_operations import get_profile, get_topic_progress, save_quiz, save_topic_progress
from core.adaptive_learning import next_difficulty
from core.llm_engine import GeminiAPIError, generate_json
from utils.layout import render_app_navbar, render_app_sidebar, render_footer

init_session()
if not st.session_state.authenticated:
    st.switch_page("app.py")
render_app_sidebar("Adaptive Quiz")
render_app_navbar("Adaptive Quiz")

profile = get_profile(st.session_state.user_id)
topic = st.session_state.get("selected_topic", profile.get("preferred_subject", "Foundations"))
st.subheader("Adaptive Quiz")

if "quiz_result" not in st.session_state:
    if "quiz_questions" not in st.session_state:
        subject = profile.get("preferred_subject", "General")
        difficulty = next_difficulty([])
        try:
            data = generate_json(
                f"Create 5 {difficulty.lower()} multiple-choice questions for {subject} about {topic}. "
                "Return JSON with a 'questions' array. Each item needs question, options, answer, and concept.",
                "Return only valid JSON."
            )
        except GeminiAPIError as exc:
            st.error(f"Could not generate quiz questions: {exc}")
            if st.button("Retry", type="primary"):
                st.rerun()
            render_footer()
            st.stop()
        fallback = [
            {"question": f"Which statement best describes a basic idea in {topic}?",
             "options": ["It is clearly defined", "It has no purpose", "It never changes", "It is unrelated"],
             "answer": "It is clearly defined", "concept": topic}
            for _ in range(5)
        ]
        st.session_state.quiz_questions = data["questions"][:5] if data and data.get("questions") else fallback
        st.session_state.quiz_answers = [None] * 5
        st.session_state.quiz_correct_history = []
        st.session_state.quiz_difficulty = difficulty

    questions = st.session_state.quiz_questions
    index = st.session_state.get("quiz_index", 0)
    st.progress((index + 1) / len(questions))
    st.caption(f"Difficulty: {st.session_state.quiz_difficulty}")
    q = questions[index]
    answer = st.radio(q["question"], q["options"], index=None, key=f"quiz_{index}")
    if answer:
        st.session_state.quiz_answers[index] = answer
    if st.button("Submit answer", type="primary"):
        if not answer:
            st.error("Select an answer.")
        else:
            correct = answer == q["answer"]
            st.session_state.quiz_correct_history.append(correct)
            if correct:
                st.success("Correct.")
            else:
                st.error(f"Incorrect. The correct answer is {q['answer']}.")
            if index + 1 < len(questions):
                st.session_state.quiz_index = index + 1
                st.rerun()
            else:
                correct_count = sum(st.session_state.quiz_correct_history)
                accuracy = round(correct_count / len(questions) * 100, 1)
                weak = [q["concept"] for q, a in zip(questions, st.session_state.quiz_answers) if a != q["answer"]]
                save_quiz({"user_id": st.session_state.user_id, "topic": topic,
                           "questions": questions, "answers": st.session_state.quiz_answers,
                           "correct_count": correct_count, "incorrect_count": len(questions)-correct_count,
                           "accuracy": accuracy, "difficulty": st.session_state.quiz_difficulty})
                save_topic_progress(st.session_state.user_id, profile.get("preferred_subject", "General"),
                                    topic, accuracy, 1)
                st.session_state.quiz_result = {"accuracy": accuracy, "correct": correct_count,
                                                "incorrect": len(questions)-correct_count, "weak": weak}
                st.rerun()
else:
    result = st.session_state.quiz_result
    with st.container(border=True):
        st.metric("Final score", f"{result['accuracy']}%")
        st.write(f"Correct: {result['correct']}  |  Incorrect: {result['incorrect']}")
        st.write("Concepts requiring revision: " + (", ".join(set(result["weak"])) if result["weak"] else "None recorded"))
    if st.button("Retest", type="primary"):
        for key in ["quiz_result", "quiz_questions", "quiz_answers", "quiz_correct_history",
                    "quiz_difficulty", "quiz_index"]:
            st.session_state.pop(key, None)
        st.rerun()

render_footer()
