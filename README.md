# StudyBuddy

StudyBuddy is a Python and Streamlit personalized-learning MVP with MongoDB persistence, bcrypt authentication, diagnostic assessments, a configurable LLM tutor, adaptive quizzes, mastery tracking, and progress reports.

## Setup

1. Create and activate a virtual environment:
   - `py -3.11 -m venv .venv`
   - `.venv\Scripts\activate`
2. Install dependencies:
   - `python -m pip install -r requirements.txt`
3. Copy `.env.example` to `.env`.
4. Set `MONGODB_URI` and `DATABASE_NAME`.
5. Set `GEMINI_API_KEY` and optionally `GEMINI_MODEL` to enable live Gemini responses.
6. To enable password-reset email, set `RESEND_API_KEY`, a verified `RESEND_FROM_EMAIL`, and `APP_BASE_URL`.
7. Start the app:
   - `streamlit run app.py`

## Environment

- MongoDB is required for authentication and all persistent learning data.
- The app runs in clearly labelled demo tutor and deterministic assessment mode when no LLM key is configured.
- Live AI supports Gemini. The default model is `gemini-3.5-flash-lite`; without `GEMINI_API_KEY`, the app uses demo mode.
- Sign-in cookies last for 30 days. Password-reset emails require a Resend API key and a verified sender address.
- Never commit `.env`.

## Learning flow

`Sign Up -> Onboarding -> Diagnostic Assessment -> Learning Plan -> AI Tutor -> Adaptive Quiz -> Progress`
