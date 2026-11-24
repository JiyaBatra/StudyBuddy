CSS = """
<style>
:root {
  color-scheme: dark;
  --white: #090A0C;
  --silver: #34383F;
  --rose: #BEC3CC;
  --pink: #E4E7EC;
  --ink: #F2F3F5;
  --silver-sheen: linear-gradient(125deg, #101114 0%, #181A1E 32%, #111316 55%, #1B1D21 78%, #101114 100%);
  --rose-sheen: linear-gradient(120deg, #A9AEB7 0%, #E8EAED 34%, #FFFFFF 48%, #D3D7DD 62%, #9DA3AC 100%);
}

html, body, [data-testid="stApp"], .stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  background: transparent !important;
  color: var(--ink) !important;
  font-family: Inter, "Plus Jakarta Sans", Arial, sans-serif;
}

html, body { background: var(--white) !important; }
[data-testid="stAppViewContainer"] { position: relative; }
[data-testid="stMain"] { position: relative; z-index: 1; }

[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(17, 19, 22, 0.94) 0%, rgba(11, 12, 14, 0.94) 100%) !important;
  border-right: 1px solid var(--silver);
  backdrop-filter: blur(16px);
}

[data-testid="stHeader"] { background: rgba(9, 10, 12, 0.55) !important; }
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"],
[data-testid="stToolbar"] { visibility: visible !important; }
[data-testid="stDeployButton"],
[data-testid="stMainMenu"] { display: none !important; }
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapseButton"] {
  display: flex !important;
  visibility: visible !important;
  width: 42px;
  height: 42px;
  margin: 8px;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--silver) !important;
  border-radius: 12px !important;
  background: var(--rose-sheen) !important;
  color: var(--white) !important;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.32);
  opacity: 1 !important;
}
[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"],
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"] {
  color: var(--white) !important;
}
.block-container { max-width: 1240px; padding: 2rem 1.5rem 3rem; }
[data-testid="stVerticalBlock"] { gap: 1.15rem; }
[data-testid="stHorizontalBlock"] { gap: 1rem; }
[data-testid="stSidebarNav"] { display: none !important; }
body:has(.st-key-auth-screen) [data-testid="stSidebar"] { display: none !important; }

.lw-video-layer {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
  background: var(--white);
}

.lw-video-layer video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: grayscale(1) brightness(0.52);
  opacity: 0.3;
}

.lw-video-shade {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(7, 8, 10, 0.52), rgba(7, 8, 10, 0.78));
}

.lw-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  min-height: 60px;
  padding: 12px 20px;
  margin-bottom: 24px;
  border: 1px solid var(--silver);
  border-radius: 16px;
  background: rgba(16, 17, 20, 0.78);
  backdrop-filter: blur(16px);
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.18);
}

.lw-navbar-brand {
  color: var(--ink) !important;
  font-size: 19px;
  font-weight: 800;
  letter-spacing: -0.5px;
  text-decoration: none !important;
}

.lw-navbar-title {
  color: var(--ink) !important;
  font-family: "Segoe Script", "Brush Script MT", "Lucida Handwriting", cursive;
  font-size: 22px;
  font-weight: 600;
}

.lw-navbar-link {
  color: var(--white) !important;
  border: 1px solid var(--rose);
  border-radius: 10px;
  padding: 8px 14px;
  text-decoration: none !important;
  background: var(--rose-sheen);
}

.st-key-lw-app-navbar {
  min-height: 60px;
  padding: 12px 20px;
  margin-bottom: 24px;
  border: 1px solid var(--silver);
  border-radius: 16px;
  background: rgba(16, 17, 20, 0.78);
  backdrop-filter: blur(16px);
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.18);
}

.st-key-lw-app-navbar [data-testid="stHorizontalBlock"] {
  align-items: center;
}

.st-key-lw-app-navbar [data-testid="stVerticalBlock"] {
  gap: 0;
}

.st-key-lw-app-navbar .stButton > button,
.st-key-lw-app-navbar .stButton > button:hover,
.st-key-lw-app-navbar .stButton > button:focus,
.st-key-lw-app-navbar .stButton > button:active {
  min-height: 42px;
  border: 1px solid var(--rose) !important;
  border-radius: 10px !important;
  background: linear-gradient(
    120deg,
    #B76E79 0%,
    #D9A079 24%,
    #F2A9BA 44%,
    #FFE1E7 50%,
    #F2A9BA 56%,
    #D88B9A 76%,
    #B76E79 100%
  ) !important;
}

.st-key-lw-app-navbar .stButton > button,
.st-key-lw-app-navbar .stButton > button * {
  color: #000000 !important;
  -webkit-text-fill-color: #000000 !important;
}

.lw-footer {
  margin-top: 56px;
  padding: 28px;
  border: 1px solid var(--silver);
  border-radius: 18px;
  background: rgba(13, 14, 17, 0.88);
  backdrop-filter: blur(16px);
  color: var(--ink) !important;
  font-size: 14px;
}

.lw-footer-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 32px;
}

.lw-footer-about { min-width: 220px; }
.lw-footer-about p { color: #A5AAB3 !important; margin: 8px 0 0; }
.lw-footer-brand {
  color: var(--ink) !important;
  font-size: 20px;
  font-weight: 800;
  text-decoration: none !important;
}

.lw-footer-links {
  display: grid;
  grid-template-columns: repeat(3, minmax(110px, 1fr));
  gap: 12px 24px;
}

.lw-footer-links a {
  color: #C6CAD1 !important;
  text-decoration: none !important;
  transition: color 160ms ease;
}

.lw-footer-links a:hover { color: #FFFFFF !important; }

.lw-footer-bottom {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-top: 26px;
  padding-top: 16px;
  border-top: 1px solid var(--silver);
  color: #858B95 !important;
  font-size: 12px;
}

[data-testid="stSidebar"] .lw-sidebar-label {
  color: var(--ink);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  margin: 20px 0 8px;
}

[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stCaption"],
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
label,
small {
  color: var(--ink) !important;
}

h1, h2, h3, h4,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
  color: var(--ink) !important;
  font-family: "Segoe Script", "Brush Script MT", "Lucida Handwriting", cursive !important;
  font-weight: 600 !important;
  letter-spacing: 0;
}

.lw-auth-heading {
  margin: 0 0 4px;
  color: var(--ink);
  text-align: center;
  font-family: "Segoe Script", "Brush Script MT", "Lucida Handwriting", cursive;
  font-size: 30px;
  font-weight: 600;
}

.lw-wordmark {
  color: var(--ink) !important;
  font-size: 21px;
  font-weight: 800;
  letter-spacing: -0.6px;
}

.lw-hero {
  background: var(--silver-sheen);
  border: 1px solid var(--silver);
  border-radius: 14px;
  padding: clamp(24px, 6vw, 56px);
}

.lw-hero h1 {
  color: var(--ink) !important;
  font-family: "Segoe Script", "Brush Script MT", "Lucida Handwriting", cursive !important;
  font-size: clamp(2rem, 7vw, 3.8rem) !important;
  line-height: 1.08 !important;
  letter-spacing: -0.045em !important;
  max-width: 100%;
  overflow-wrap: normal;
  word-break: normal;
}

.lw-card {
  background: rgba(16, 18, 21, 0.86);
  border: 1px solid var(--silver);
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.28);
  backdrop-filter: blur(12px);
}

[data-testid="stVerticalBlockBorderWrapper"] {
  border-color: var(--silver) !important;
  background: rgba(16, 18, 21, 0.78);
  border-radius: 16px !important;
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.2);
}

.lw-muted { color: var(--ink) !important; }

.st-key-auth-screen {
  min-height: calc(100vh - 9rem);
  display: flex !important;
  flex-direction: column;
  justify-content: center;
}

.st-key-auth-screen [data-testid="stHorizontalBlock"] {
  align-items: center;
  justify-content: center;
  transform: translateY(-3rem);
}

.st-key-auth-screen [data-testid="column"]:nth-child(2) > div {
  max-width: 480px;
  margin: 0 auto;
}

.lw-auth-brand {
  margin-bottom: 16px;
  text-align: center;
}

.lw-auth-title {
  margin-bottom: 22px;
  text-align: center;
}

.lw-auth-title h1 {
  font-size: clamp(2rem, 4vw, 2.7rem) !important;
  line-height: 1.08 !important;
  margin: 0 0 8px !important;
  padding: 0 !important;
}

.lw-auth-title p { margin: 0; }

.st-key-auth-card {
  background: var(--silver-sheen) !important;
  border: 1px solid var(--silver) !important;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.32);
}

.lw-tag {
  display: inline-block;
  background: var(--rose-sheen);
  color: var(--white) !important;
  border-radius: 999px;
  padding: 5px 10px;
  font-size: 12px;
  font-weight: 600;
}

.stButton > button {
  background: #15171A !important;
  border: 1px solid var(--rose) !important;
  border-radius: 10px;
  color: var(--ink) !important;
  min-height: 42px;
  transition: background 160ms ease, border-color 160ms ease, transform 160ms ease;
}

.stButton > button:hover {
  background: var(--rose-sheen) !important;
  border-color: var(--rose) !important;
  color: var(--white) !important;
  -webkit-text-fill-color: var(--white) !important;
  transform: translateY(-1px);
}

.stButton > button[kind="primary"],
.stButton > button[kind="primaryFormSubmit"] {
  background: var(--rose-sheen) !important;
  border-color: var(--rose) !important;
  color: var(--white) !important;
  -webkit-text-fill-color: var(--white) !important;
}

.stButton > button[kind="primary"] p,
.stButton > button[kind="primaryFormSubmit"] p {
  color: var(--white) !important;
}

.stTextInput [data-testid="stTextInputRootElement"] {
  background: #101215 !important;
  border: 1px solid var(--silver) !important;
  border-radius: 10px !important;
}

.stTextInput button[aria-label*="password"],
.stTextInput button[aria-label*="Password"] {
  background: var(--rose-sheen) !important;
  color: var(--white) !important;
  border-color: var(--pink) !important;
}

.stTextInput button[aria-label*="password"] svg,
.stTextInput button[aria-label*="Password"] svg {
  color: var(--white) !important;
  fill: var(--white) !important;
}

.stTextInput input,
.stTextArea textarea,
[data-baseweb="select"] > div {
  background: #101215 !important;
  border: 1px solid var(--silver) !important;
  border-radius: 10px !important;
  color: var(--ink) !important;
  -webkit-text-fill-color: var(--ink) !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder { color: #A5AAB3 !important; opacity: 1; }

.stTextInput input:focus,
.stTextArea textarea:focus,
[data-baseweb="select"] > div:focus-within {
  border-color: var(--rose) !important;
  box-shadow: 0 0 0 1px var(--rose) !important;
}

input[type="checkbox"],
input[type="radio"] { accent-color: var(--rose); }

[data-baseweb="popover"],
[data-baseweb="menu"] {
  background: #15171A !important;
  color: var(--ink) !important;
}

[data-testid="stMetric"] {
  background: rgba(18, 20, 23, 0.88) !important;
  border: 1px solid var(--silver);
  border-radius: 12px;
  padding: 14px;
}

[data-testid="stAlert"] {
  background: rgba(23, 25, 29, 0.94) !important;
  border: 1px solid var(--silver) !important;
  color: var(--ink) !important;
}

[data-testid="stSpinner"] > div {
  border-top-color: var(--rose) !important;
}

[data-testid="stTabs"] [role="tab"] {
  color: var(--ink) !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  border-bottom-color: var(--rose) !important;
}

@media (max-width: 700px) {
  .block-container { padding: 1.25rem 0.85rem 2rem; }
  .lw-footer { padding: 20px; margin-top: 36px; }
  .lw-footer-main { flex-direction: column; gap: 20px; }
  .lw-footer-links { grid-template-columns: repeat(2, minmax(110px, 1fr)); gap: 12px; }
  .lw-footer-bottom { flex-direction: column; gap: 6px; }
  [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    gap: 1rem !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"] {
    width: 100% !important;
    flex: 1 1 100% !important;
  }

  .st-key-auth-screen { min-height: auto; padding-top: 1rem; }
  .st-key-auth-screen [data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    justify-content: center;
    gap: 0 !important;
    transform: none;
  }
  .st-key-auth-screen [data-testid="column"]:not(:nth-child(2)) {
    display: none !important;
  }
  .st-key-auth-screen [data-testid="column"]:nth-child(2) {
    width: 100% !important;
    flex: 1 1 100% !important;
  }
  .st-key-auth-card { padding: 10px; }
}
</style>
"""
