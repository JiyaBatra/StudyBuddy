import html
import streamlit as st

APP_PAGES = [
    ("Dashboard", "pages/1_Dashboard.py"),
    ("AI Tutor", "pages/2_AI_Tutor.py"),
    ("Assessments", "pages/3_Assessment.py"),
    ("Learning Plan", "pages/4_Learning_Plan.py"),
    ("Adaptive Quiz", "pages/5_Adaptive_Quiz.py"),
    ("Results", "pages/6_Results.py"),
    ("Progress", "pages/7_Progress.py"),
    ("Learning History", "pages/8_Learning_History.py"),
    ("Profile & Settings", "pages/9_Profile.py"),
]


def render_public_navbar(signin_href="#login"):
    st.markdown(
        "<div class='lw-navbar lw-public-navbar'>"
        "<a class='lw-navbar-brand' href='/'>StudyBuddy</a>"
        f"<a class='lw-navbar-link' href='{html.escape(signin_href, quote=True)}'>Sign In</a>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_background_video():
    st.markdown(
        "<div class='lw-video-layer' aria-hidden='true'>"
        "<video autoplay muted loop playsinline preload='metadata'>"
        "<source src='/app/static/bg-vdo.mp4' type='video/mp4'>"
        "</video><div class='lw-video-shade'></div></div>",
        unsafe_allow_html=True,
    )


def render_app_navbar(page_title):
    with st.container(key="lw-app-navbar"):
        brand, title, action = st.columns([1.2, 1.8, 0.8])
        with brand:
            st.markdown("<div class='lw-navbar-brand'>StudyBuddy</div>", unsafe_allow_html=True)
        with title:
            st.markdown(
                f"<div class='lw-navbar-title'>{html.escape(page_title)}</div>",
                unsafe_allow_html=True,
            )
        with action:
            if st.button("Log out", key="learnwise_top_logout"):
                _logout_and_redirect()


def _logout_and_redirect():
    from auth.session_manager import logout

    logout()
    st.switch_page("app.py")


def render_app_sidebar(active_page=None):
    st.sidebar.markdown("<div class='lw-wordmark'>StudyBuddy</div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div class='lw-sidebar-label'>LEARNING</div>", unsafe_allow_html=True)
    for label, page in APP_PAGES:
        if st.sidebar.button(
            label,
            type="primary" if label == active_page else "secondary",
            use_container_width=True,
            key=f"sidebar_{page.rsplit('/', 1)[-1].replace('.py', '')}",
        ):
            st.switch_page(page)
    st.sidebar.divider()
    if st.sidebar.button("Log out", use_container_width=True, key="learnwise_sidebar_logout"):
        _logout_and_redirect()


def render_footer():
    links = "".join(
        f"<a href='/{page.rsplit('/', 1)[-1].removesuffix('.py').split('_', 1)[-1]}'>"
        f"{html.escape(label)}</a>"
        for label, page in APP_PAGES
    )
    st.markdown(
        "<div class='lw-footer'>"
        "<div class='lw-footer-main'>"
        "<div class='lw-footer-about'>"
        "<a class='lw-footer-brand' href='/'>StudyBuddy</a>"
        "<p>Small steps. Stronger understanding.</p>"
        "</div>"
        f"<nav class='lw-footer-links' aria-label='Explore pages'>{links}</nav>"
        "</div>"
        "<div class='lw-footer-bottom'>"
        "<span>StudyBuddy</span><span>Made for curious minds.</span>"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )
