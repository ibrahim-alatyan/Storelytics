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
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            sql, df = ask(question)

        # Show SQL in expander
        with st.expander("View SQL"):
            st.code(sql, language="sql")

        # Show result table
        if "error" in df.columns:
            st.error(f"Error: {df['error'][0]}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: {df['error'][0]}"
            })
        else:
            st.dataframe(df)

            # Generate and show chart
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
# Text input
# ============================================================
question = st.chat_input("Type your question...")
if question:
    process_question(question)

# ============================================================
# Voice input
# ============================================================
st.divider()
st.subheader("🎤 Voice Input")
audio = st.audio_input("Record your question")

if audio:
    with st.spinner("Transcribing..."):
        question = transcribe_audio(audio)
    st.success(f"Transcribed: {question}")
    process_question(question)



