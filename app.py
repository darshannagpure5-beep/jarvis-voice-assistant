import streamlit as st
import os
import threading
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Jarvis AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #050a0f !important;
    color: #e0f4ff;
    font-family: 'Rajdhani', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 50% 0%, #0a1628 0%, #050a0f 70%) !important;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Hero header ── */
.jarvis-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.jarvis-title {
    font-size: 4rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    background: linear-gradient(135deg, #00d4ff, #0080ff, #00d4ff);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
    margin: 0;
}
@keyframes shimmer {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}
.jarvis-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #3a7bd5;
    letter-spacing: 0.25em;
    margin-top: 0.3rem;
}

/* ── Orb ── */
.orb-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1.5rem 0;
}
.orb {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #00d4ff55, #0a1628 70%);
    border: 1.5px solid #00d4ff44;
    box-shadow: 0 0 30px #00d4ff22, 0 0 60px #0050ff11, inset 0 0 30px #00d4ff11;
    position: relative;
    transition: all 0.3s ease;
}
.orb.listening {
    box-shadow: 0 0 40px #00d4ff66, 0 0 80px #0050ff33, inset 0 0 40px #00d4ff22;
    animation: pulse 1.2s ease-in-out infinite;
    border-color: #00d4ff99;
}
.orb.thinking {
    box-shadow: 0 0 40px #ff6b0066, 0 0 80px #ff450033, inset 0 0 40px #ff6b0022;
    animation: spin-glow 1.5s linear infinite;
    border-color: #ff6b0099;
}
.orb.speaking {
    box-shadow: 0 0 40px #00ff8866, 0 0 80px #00cc6633, inset 0 0 40px #00ff8822;
    animation: pulse 0.8s ease-in-out infinite;
    border-color: #00ff8899;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.08); }
}
@keyframes spin-glow {
    0% { box-shadow: 0 0 40px #ff6b0066, 0 0 80px #ff450033; transform: rotate(0deg); }
    100% { box-shadow: 0 0 40px #ff6b00aa, 0 0 80px #ff450066; transform: rotate(360deg); }
}

/* ── Status badge ── */
.status-badge {
    text-align: center;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    color: #3a7bd5;
    margin-bottom: 1.5rem;
}
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #3a7bd5;
    margin-right: 6px;
    animation: blink 1.5s ease-in-out infinite;
}
.status-dot.active { background: #00d4ff; }
.status-dot.thinking { background: #ff6b00; animation: blink 0.6s ease-in-out infinite; }
.status-dot.speaking { background: #00ff88; }
@keyframes blink {
    0%, 100% { opacity: 1; } 50% { opacity: 0.3; }
}

/* ── Chat messages ── */
.chat-container {
    max-height: 380px;
    overflow-y: auto;
    padding: 0.5rem 0;
    scrollbar-width: thin;
    scrollbar-color: #1a3a5c #050a0f;
}
.chat-container::-webkit-scrollbar { width: 4px; }
.chat-container::-webkit-scrollbar-track { background: #050a0f; }
.chat-container::-webkit-scrollbar-thumb { background: #1a3a5c; border-radius: 2px; }

.msg-row {
    display: flex;
    margin: 0.5rem 0;
    animation: fadeUp 0.3s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
.msg-row.user { justify-content: flex-end; }
.msg-row.assistant { justify-content: flex-start; }

.bubble {
    max-width: 75%;
    padding: 0.6rem 1rem;
    border-radius: 12px;
    font-size: 0.95rem;
    line-height: 1.5;
}
.bubble.user {
    background: linear-gradient(135deg, #0a2a4a, #0d3b6e);
    border: 1px solid #1a5a9a44;
    color: #a8d8ff;
    border-bottom-right-radius: 3px;
}
.bubble.assistant {
    background: linear-gradient(135deg, #0a1f2e, #0d2840);
    border: 1px solid #00d4ff22;
    color: #d0ecff;
    border-bottom-left-radius: 3px;
}
.bubble-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    margin-bottom: 3px;
    opacity: 0.5;
}

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    border-radius: 8px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border: none;
    padding: 0.65rem 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
}
/* Primary mic button */
div[data-testid="column"]:nth-child(1) .stButton > button {
    background: linear-gradient(135deg, #003d6b, #0066bb);
    color: #00d4ff;
    box-shadow: 0 0 20px #00d4ff22;
}
div[data-testid="column"]:nth-child(1) .stButton > button:hover {
    box-shadow: 0 0 30px #00d4ff44;
    transform: translateY(-1px);
}
/* Secondary buttons */
div[data-testid="column"]:nth-child(2) .stButton > button,
div[data-testid="column"]:nth-child(3) .stButton > button {
    background: #0a1628;
    color: #5a8ab0;
    border: 1px solid #1a3a5c;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover,
div[data-testid="column"]:nth-child(3) .stButton > button:hover {
    border-color: #3a7bd5;
    color: #a0c8f0;
}

/* ── Text input ── */
.stTextInput > div > div > input {
    background: #0a1628 !important;
    border: 1px solid #1a3a5c !important;
    border-radius: 8px !important;
    color: #a8d8ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00d4ff44 !important;
    box-shadow: 0 0 0 2px #00d4ff11 !important;
}
.stTextInput label { color: #3a7bd5 !important; font-family: 'Share Tech Mono', monospace !important; font-size: 0.7rem !important; letter-spacing: 0.1em !important; }

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid #0d2840;
    margin: 1rem 0;
}

/* ── Reminder pills ── */
.reminder-pill {
    display: inline-block;
    background: #0a1f2e;
    border: 1px solid #00d4ff22;
    border-radius: 20px;
    padding: 3px 12px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: #3a9bd5;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "status" not in st.session_state:
    st.session_state.status = "idle"  # idle | listening | thinking | speaking
if "reminders" not in st.session_state:
    st.session_state.reminders = []

# ── Import backend modules ─────────────────────────────────────────────────
try:
    from llm import chat, clear_memory
    from tts import speak
    from stt import listen
    from reminders import parse_and_set_reminder, run_scheduler, set_speak
    set_speak(speak)
    if "scheduler_started" not in st.session_state:
        run_scheduler()
        st.session_state.scheduler_started = True
    backend_ok = True
except Exception as e:
    backend_ok = False
    backend_error = str(e)

# ── Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="jarvis-header">
    <p class="jarvis-title">JARVIS</p>
    <p class="jarvis-sub">JUST A RATHER VERY INTELLIGENT SYSTEM</p>
</div>
""", unsafe_allow_html=True)

if not backend_ok:
    st.error(f"⚠️ Backend error: {backend_error}")
    st.stop()

# ── Orb + status ─────────────────────────────────────────────────────────
status = st.session_state.status
orb_class = {"idle": "", "listening": "listening", "thinking": "thinking", "speaking": "speaking"}.get(status, "")
dot_class = {"listening": "active", "thinking": "thinking", "speaking": "speaking"}.get(status, "")
status_text = {"idle": "STANDBY", "listening": "LISTENING", "thinking": "PROCESSING", "speaking": "SPEAKING"}.get(status, "STANDBY")

st.markdown(f"""
<div class="orb-container">
    <div class="orb {orb_class}"></div>
</div>
<div class="status-badge">
    <span class="status-dot {dot_class}"></span>{status_text}
</div>
""", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role = msg["role"]
    label = "YOU" if role == "user" else "JARVIS"
    st.markdown(f"""
    <div class="msg-row {role}">
        <div class="bubble {role}">
            <div class="bubble-label">{label}</div>
            {msg["content"]}
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    mic_label = "🎙️  SPEAK TO JARVIS" if status == "idle" else "⏳  PROCESSING..."
    if st.button(mic_label, disabled=(status != "idle"), key="mic_btn"):
        st.session_state.status = "listening"
        st.rerun()

with col2:
    if st.button("🧹  CLEAR", key="clear_btn"):
        clear_memory()
        st.session_state.messages = []
        st.session_state.status = "idle"
        st.rerun()

with col3:
    if st.button("🔇  MUTE TTS", key="mute_btn"):
        st.session_state.tts_muted = not st.session_state.get("tts_muted", False)
        st.rerun()

# ── Text input fallback ───────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
text_input = st.text_input(
    "OR TYPE YOUR MESSAGE",
    placeholder="Type here and press Enter...",
    key="text_input",
    label_visibility="visible"
)

# ── Process voice or text ─────────────────────────────────────────────────
def process_input(user_text: str):
    """Common handler for both voice and text input."""
    if not user_text:
        return

    st.session_state.messages.append({"role": "user", "content": user_text})

    # Check reminders first
    reminder_resp = parse_and_set_reminder(user_text)
    if reminder_resp:
        st.session_state.messages.append({"role": "assistant", "content": reminder_resp})
        st.session_state.reminders.append(user_text)
        if not st.session_state.get("tts_muted"):
            speak(reminder_resp)
        st.session_state.status = "idle"
        return

    # Send to LLM
    st.session_state.status = "thinking"
    try:
        reply = chat(user_text)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.session_state.status = "speaking"
        if not st.session_state.get("tts_muted"):
            speak(reply)
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})
    finally:
        st.session_state.status = "idle"

# Handle voice flow
if status == "listening":
    with st.spinner("Listening..."):
        user_text = listen()
    if user_text:
        process_input(user_text)
    else:
        st.session_state.status = "idle"
    st.rerun()

# Handle text input
if text_input:
    process_input(text_input)
    st.rerun()

# ── Reminders panel ──────────────────────────────────────────────────────
if st.session_state.reminders:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.65rem;color:#3a7bd5;letter-spacing:0.1em;">ACTIVE REMINDERS</p>', unsafe_allow_html=True)
    for r in st.session_state.reminders:
        st.markdown(f'<span class="reminder-pill">⏰ {r}</span>', unsafe_allow_html=True)

# ── Mute indicator ────────────────────────────────────────────────────────
if st.session_state.get("tts_muted"):
    st.markdown('<p style="text-align:center;font-family:\'Share Tech Mono\',monospace;font-size:0.65rem;color:#ff6b00;letter-spacing:0.1em;margin-top:1rem;">🔇 VOICE OUTPUT MUTED</p>', unsafe_allow_html=True)
