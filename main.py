import streamlit as st
import langchain_helper as lch
import textwrap
from langchain.memory import ConversationBufferMemory
import re

# --- Page title ---
st.title("🎥 YouTube Assistant")

# --- Memory and session state ---
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", input_key="question")

if "db" not in st.session_state:
    st.session_state.db = None

# --- Sidebar: Chat Form and Clear Button ---
with st.sidebar:
    st.markdown("### 🧠 Ask About Any YouTube Video")

# These go OUTSIDE sidebar to avoid `submit` being lost
with st.form(key="query_form"):
    youtube_url = st.text_input("YouTube Video URL", max_chars=100)
    query = st.text_area("Ask a question about the video", max_chars=500, key="query")
    submit = st.form_submit_button("Submit")

with st.sidebar:
    if st.button("🧹 Clear Chat"):
        st.session_state.memory.clear()
        st.session_state.db = None
        st.rerun()

# --- Video Preview ---
def get_youtube_thumbnail(url):
    video_id_match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if video_id_match:
        video_id = video_id_match.group(1)
        return f"https://img.youtube.com/vi/{video_id}/0.jpg"
    return None

if youtube_url:
    thumb = get_youtube_thumbnail(youtube_url)
    if thumb:
        st.image(thumb, width=480)

# --- Query Response ---
if submit and youtube_url and query:
    with st.spinner("Loading video transcript and generating answer..."):
        if st.session_state.db is None:
            st.session_state.db = lch.create_vector_db_from_youtube_url(youtube_url)

        response, docs = lch.get_response_from_query(
            db=st.session_state.db, 
            query=query, 
            memory=st.session_state.memory
        )

    st.subheader("💬 Assistant's Answer")
    st.text(textwrap.fill(response, width=80))

# --- Chat History ---
if st.session_state.memory.buffer:
    st.markdown("### 💬 Chat History")
    chat_history = st.session_state.memory.buffer.split("\n")
    for line in chat_history:
        if line.strip().startswith("Human:"):
            st.markdown(f"🧑‍💬 **You:** {line.replace('Human:', '').strip()}")
        elif line.strip().startswith("AI:"):
            st.markdown(f"🤖 **Assistant:** {line.replace('AI:', '').strip()}")

# --- Quiz Generator ---
if youtube_url and st.button("🧪 Generate Quiz"):
    with st.spinner("Creating quiz from the video transcript..."):
        quiz = lch.generate_quiz_questions(st.session_state.db)
    st.subheader("📝 Quiz Questions")
    st.text_area("Quiz", quiz, height=300)
