"""
Debug script to test chatbot button functionality with callbacks
"""

import streamlit as st

st.title("🔧 Chatbot Debug Test")

# Initialize session state
if 'sidebar_question' not in st.session_state:
    st.session_state.sidebar_question = ""

def set_sentiment_question():
    st.session_state.sidebar_question = "What's the overall sentiment?"
    st.session_state.debug_message = "✅ Sentiment button clicked!"

def set_issues_question():
    st.session_state.sidebar_question = "What are the top issues?"
    st.session_state.debug_message = "✅ Issues button clicked!"

def set_improve_question():
    st.session_state.sidebar_question = "How should we improve?"
    st.session_state.debug_message = "✅ Improve button clicked!"

st.write("### Testing Quick Question Buttons")

# Quick question buttons with callbacks
if st.button("Sentiment?", key="sentiment_q_debug", use_container_width=True, on_click=set_sentiment_question):
    pass

if st.button("Top Issues?", key="issues_q_debug", use_container_width=True, on_click=set_issues_question):
    pass

if st.button("How to improve?", key="improve_q_debug", use_container_width=True, on_click=set_improve_question):
    pass

# Show debug message
if 'debug_message' in st.session_state:
    st.write(st.session_state.debug_message)
    st.write(f"Set question: {st.session_state.sidebar_question}")

# Show current state
st.write("### Current Session State")
st.write(f"sidebar_question: {st.session_state.sidebar_question}")

# Text input
question = st.text_input(
    "Current question:",
    value=st.session_state.sidebar_question,
    key="debug_input"
)

if question != st.session_state.sidebar_question:
    st.session_state.sidebar_question = question
    st.write("✅ Question updated from text input!")

st.write("---")
st.info("If you see the checkmarks above when clicking buttons, the issue is fixed!")
