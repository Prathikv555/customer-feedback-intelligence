"""
Test main app button functionality
"""

import streamlit as st

st.title("🧪 Main App Button Test")

# Initialize session state
if 'sidebar_question' not in st.session_state:
    st.session_state.sidebar_question = ""

def set_sentiment_question():
    st.session_state.sidebar_question = "What's the overall sentiment?"
    st.session_state.test_message = "✅ Main app: Sentiment button worked!"

def set_issues_question():
    st.session_state.sidebar_question = "What are the top issues?"
    st.session_state.test_message = "✅ Main app: Issues button worked!"

def set_improve_question():
    st.session_state.sidebar_question = "How should we improve?"
    st.session_state.test_message = "✅ Main app: Improve button worked!"

st.write("### Testing Main App Buttons")

# Quick question buttons
st.write("**Quick Questions:**")

if st.button("Sentiment?", key="main_sentiment_q", use_container_width=True, on_click=set_sentiment_question):
    pass

if st.button("Top Issues?", key="main_issues_q", use_container_width=True, on_click=set_issues_question):
    pass

if st.button("How to improve?", key="main_improve_q", use_container_width=True, on_click=set_improve_question):
    pass

# Show test message
if 'test_message' in st.session_state:
    st.success(st.session_state.test_message)
    st.write(f"Set question: {st.session_state.sidebar_question}")

# Show current state
st.write("### Current Session State")
st.write(f"sidebar_question: {st.session_state.sidebar_question}")

# Text input
question = st.text_input(
    "Current question:",
    value=st.session_state.sidebar_question,
    key="main_input"
)

st.info("If you see success message above, main app buttons are working!")
