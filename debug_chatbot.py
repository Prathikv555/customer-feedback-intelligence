"""
Debug script to test chatbot button functionality
"""

import streamlit as st

st.title("🔧 Chatbot Debug Test")

# Initialize session state
if 'sidebar_question' not in st.session_state:
    st.session_state.sidebar_question = ""

st.write("### Testing Quick Question Buttons")

# Quick question buttons
if st.button("Sentiment?", key="sentiment_q_debug", use_container_width=True):
    st.session_state.sidebar_question = "What's the overall sentiment?"
    st.write("✅ Sentiment button clicked!")
    st.write(f"Set question: {st.session_state.sidebar_question}")
    st.rerun()

if st.button("Top Issues?", key="issues_q_debug", use_container_width=True):
    st.session_state.sidebar_question = "What are the top issues?"
    st.write("✅ Issues button clicked!")
    st.write(f"Set question: {st.session_state.sidebar_question}")
    st.rerun()

if st.button("How to improve?", key="improve_q_debug", use_container_width=True):
    st.session_state.sidebar_question = "How should we improve?"
    st.write("✅ Improve button clicked!")
    st.write(f"Set question: {st.session_state.sidebar_question}")
    st.rerun()

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
