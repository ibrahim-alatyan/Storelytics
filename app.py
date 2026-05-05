# ============================================================
# Main Streamlit app
# ============================================================

# ============================================================
# libraries
# ============================================================
import streamlit as st
from text_to_sql import ask
from charts import generate_chart
from voice import transcribe_audio

# ============================================================
# Page config
# ============================================================
st.set_page_config(
    page_title="Superstore Chatbot",
    page_icon="🛒",
    layout="wide"
)

# ============================================================
# Sidebar - Voice Input + Clear Chat
# ============================================================
with st.sidebar:
    st.title("🎤 Voice Input")
    audio = st.audio_input("Record your question")

    if audio:
        with st.spinner("Transcribing..."):
            # Fix: send audio with correct filename so Groq knows the format
            audio_bytes = audio.read()
            import io
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "recording.wav"
            question_from_voice = transcribe_audio(audio_file)
        st.success(f"Transcribed: {question_from_voice}")
        st.session_state["voice_question"] = question_from_voice

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ============================================================
# Main area
# ============================================================
st.title("🛒 Superstore Chatbot")
st.caption("Ask anything about the data — in English or Arabic")

# ============================================================
# Chat history
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "dataframe" in message:
            st.dataframe(message["dataframe"])
        if "chart" in message:
            st.plotly_chart(message["chart"], use_container_width=True)

# ============================================================
# Process question
# ============================================================
def process_question(question: str):
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            sql, df = ask(question)

        with st.expander("View SQL"):
            st.code(sql, language="sql")

        if "error" in df.columns:
            st.error(f"Error: {df['error'][0]}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: {df['error'][0]}"
            })
        else:
            st.dataframe(df)
            fig = generate_chart(df, question)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Here are the results:",
                    "dataframe": df,
                    "chart": fig
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Here are the results:",
                    "dataframe": df
                })

# ============================================================
# Handle voice question
# ============================================================
if "voice_question" in st.session_state and st.session_state["voice_question"]:
    process_question(st.session_state["voice_question"])
    st.session_state["voice_question"] = None

# ============================================================
# Text input - always at the bottom
# ============================================================
question = st.chat_input("Type your question...")
if question:
    process_question(question)