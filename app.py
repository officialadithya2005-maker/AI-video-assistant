import streamlit as st
from dotenv import load_dotenv
from utilities.audioprocessor import process_input
from core.transcriber import transcribe_all
from core.summarise import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ------------------------------------------------------------------
# Page Config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="AI Video Intelligence Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Custom CSS
# ------------------------------------------------------------------
st.markdown("""
<style>
    /* ---------- Global text defaults ---------- */
    html, body, [class*="css"] {
        color: #e5e7eb !important;
    }

    .main {
        background-color: #0e1117;
    }
    .stApp {
        background: linear-gradient(180deg, #0e1117 0%, #131722 100%);
    }

    /* ---------- Headings & body text everywhere ---------- */
    h1, h2, h3, h4, h5, h6 {
        color: #f9fafb !important;
    }
    p, span, li, label, div {
        color: #e5e7eb;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #e5e7eb !important;
    }

    /* ---------- Title ---------- */
    .title-container {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }
    .title-container h1 {
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0;
    }
    .title-container p {
        color: #d1d5db !important;
        font-size: 1rem;
        margin-top: 0.2rem;
    }

    /* ---------- Cards ---------- */
    .card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        color: #f3f4f6;
    }
    .card h2, .card h3, .card h4 {
        color: #f9fafb !important;
    }
    .card p, .card span, .card li {
        color: #e5e7eb !important;
    }

    .badge {
        display: inline-block;
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: #ffffff !important;
        padding: 0.25rem 0.9rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    /* ---------- Buttons ---------- */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: #ffffff !important;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
    }
    .stButton>button p {
        color: #ffffff !important;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: #131722;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }
    section[data-testid="stSidebar"] h3 {
        color: #f9fafb !important;
    }
    /* Radio button labels */
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stRadio p {
        color: #e5e7eb !important;
    }
    /* Text input / selectbox labels */
    section[data-testid="stSidebar"] label,
    .stTextInput label,
    .stSelectbox label {
        color: #d1d5db !important;
        font-weight: 600;
    }
    /* Text input field text */
    .stTextInput input {
        color: #f9fafb !important;
        background-color: rgba(255,255,255,0.06) !important;
    }
    .stTextInput input::placeholder {
        color: #9ca3af !important;
        opacity: 1;
    }
    /* Selectbox field text */
    .stSelectbox div[data-baseweb="select"] * {
        color: #f9fafb !important;
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] button {
        color: #9ca3af !important;
    }
    .stTabs [data-baseweb="tab-list"] button p {
        color: inherit !important;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #a855f7 !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] p {
        color: #a855f7 !important;
    }

    /* ---------- Chat bubbles ---------- */
    .chat-bubble-user {
        background: linear-gradient(90deg, #6366f1, #7c3aed);
        color: #ffffff !important;
        padding: 0.7rem 1rem;
        border-radius: 14px 14px 2px 14px;
        margin: 0.4rem 0;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-bubble-assistant {
        background: rgba(255,255,255,0.08);
        color: #f3f4f6 !important;
        padding: 0.7rem 1rem;
        border-radius: 14px 14px 14px 2px;
        margin: 0.4rem 0;
        max-width: 80%;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* ---------- Expander ---------- */
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] p {
        color: #e5e7eb !important;
    }

    /* ---------- Text area (transcript) ---------- */
    .stTextArea textarea {
        color: #f3f4f6 !important;
        background-color: rgba(255,255,255,0.04) !important;
    }

    /* ---------- Checkbox labels (action items) ---------- */
    .stCheckbox label p, .stCheckbox label span {
        color: #e5e7eb !important;
    }

    /* ---------- Progress / status text ---------- */
    .stProgress p, div[data-testid="stMarkdownContainer"] p {
        color: #e5e7eb !important;
    }

    /* ---------- Alerts (error/success) keep readable ---------- */
    div[data-testid="stAlert"] p {
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Session State Init
# ------------------------------------------------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.markdown("""
<div class="title-container">
    <h1>🎬 AI Video Intelligence Assistant</h1>
    <p>Turn any video into a searchable, summarized knowledge base</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Sidebar — Input Controls
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    input_mode = st.radio("Source Type", ["YouTube URL", "Local File Path"], horizontal=False)

    if input_mode == "YouTube URL":
        source = st.text_input("📺 YouTube URL", placeholder="https://youtube.com/watch?v=...")
    else:
        source = st.text_input("📁 Local File Path", placeholder="/path/to/video.mp4")

    language = st.selectbox("🌐 Language", ["english", "hinglish"], index=0)

    st.markdown("---")
    run_btn = st.button("🚀 Process Video", use_container_width=True)

    st.markdown("---")
    st.markdown("### 🧠 Pipeline Stages")
    st.markdown("""
    1. Audio extraction & chunking
    2. Speech-to-text transcription
    3. Summarization
    4. Action item extraction
    5. Key decision detection
    6. RAG index build
    """)

    if st.session_state.result:
        st.markdown("---")
        if st.button("🗑️ Clear Session", use_container_width=True):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.rerun()

# ------------------------------------------------------------------
# Run Pipeline
# ------------------------------------------------------------------
if run_btn:
    if not source:
        st.error("⚠️ Please enter a YouTube URL or file path first.")
    else:
        with st.spinner("🔄 Processing video — this may take a few minutes..."):
            progress = st.progress(0, text="Extracting audio...")
            try:
                chunks = process_input(source)
                progress.progress(20, text="Transcribing...")

                transcript = transcribe_all(chunks, language)
                progress.progress(45, text="Generating title & summary...")

                title = generate_title(transcript)
                summary = summarize(transcript)
                progress.progress(65, text="Extracting action items & decisions...")

                action_items = extract_action_items(transcript)
                decisions = extract_key_decisions(transcript)
                questions = extract_questions(transcript)
                progress.progress(85, text="Building RAG index...")

                rag_chain = build_rag_chain(transcript)
                progress.progress(100, text="Done!")

                st.session_state.result = {
                    "title": title,
                    "transcript": transcript,
                    "summary": summary,
                    "action_items": action_items,
                    "key_decisions": decisions,
                    "open_questions": questions,
                    "rag_chain": rag_chain,
                }
                st.session_state.chat_history = []
                st.success("✅ Video processed successfully!")
            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")

# ------------------------------------------------------------------
# Results Display
# ------------------------------------------------------------------
result = st.session_state.result

if result:
    st.markdown(f"""
    <div class="card">
        <span class="badge">🎯 Processed</span>
        <h2 style="margin-top:0.3rem;">{result['title']}</h2>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📋 Summary", "✅ Action Items", "🔑 Decisions", "❓ Questions", "📝 Transcript", "💬 Chat"])

    # --- Summary Tab ---
    with tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📋 Summary")
        st.write(result["summary"])
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Action Items Tab ---
    with tabs[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### ✅ Action Items")
        items = result["action_items"]
        if isinstance(items, (list, tuple)):
            for i, item in enumerate(items, 1):
                st.checkbox(f"{item}", key=f"action_{i}")
        else:
            st.write(items)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Decisions Tab ---
    with tabs[2]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 🔑 Key Decisions")
        decisions = result["key_decisions"]
        if isinstance(decisions, (list, tuple)):
            for d in decisions:
                st.markdown(f"- 🔹 {d}")
        else:
            st.write(decisions)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Questions Tab ---
    with tabs[3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### ❓ Open Questions")
        questions = result["open_questions"]
        if isinstance(questions, (list, tuple)):
            for q in questions:
                st.markdown(f"- ❔ {q}")
        else:
            st.write(questions)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Transcript Tab ---
    with tabs[4]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 📝 Full Transcript")
        with st.expander("Click to expand full transcript", expanded=False):
            st.text_area("Transcript", result["transcript"], height=400, label_visibility="collapsed")
        st.download_button(
            "⬇️ Download Transcript",
            data=result["transcript"],
            file_name=f"{result['title']}_transcript.txt",
            mime="text/plain",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Chat Tab ---
    with tabs[5]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 💬 Chat with Your Video")

        chat_container = st.container()
        with chat_container:
            for role, msg in st.session_state.chat_history:
                if role == "user":
                    st.markdown(f'<div class="chat-bubble-user">{msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bubble-assistant">🤖 {msg}</div>', unsafe_allow_html=True)

        question = st.chat_input("Ask something about this video...")
        if question:
            st.session_state.chat_history.append(("user", question))
            with st.spinner("Thinking..."):
                try:
                    answer = ask_question(result["rag_chain"], question)
                except Exception as e:
                    answer = f"⚠️ Error: {e}"
            st.session_state.chat_history.append(("assistant", answer))
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="card" style="text-align:center; padding: 3rem 1rem;">
        <h3 style="color:#d1d5db;">👋 Get started</h3>
        <p style="color:#9ca3af;">Enter a YouTube URL or local file path in the sidebar and click <b>Process Video</b> to begin.</p>
    </div>
    """, unsafe_allow_html=True)