"""
Simple and reliable chatbot implementation
"""

import streamlit as st
from data_processor import DataProcessor
from ai_analyzer import AIAnalyzer
from chatbot import FeedbackChatbot

st.title("🤖 Simple Chatbot Test")

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = ""

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Load data and initialize chatbot
@st.cache_data
def load_data():
    processor = DataProcessor()
    processor.load_data()
    data = processor.preprocess_data()
    analyzer = AIAnalyzer()
    insights = analyzer.generate_insights_summary(data)
    chatbot = FeedbackChatbot(processor, analyzer)
    return data, chatbot

data, chatbot = load_data()

st.write("### 💬 Simple Chat Interface")

# Question input
question = st.text_input(
    "Ask about your data:",
    placeholder="e.g., What's overall sentiment?",
    value=st.session_state.current_question
)

# Quick question buttons
st.write("**Quick Questions:**")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Sentiment", use_container_width=True):
        st.session_state.current_question = "What's the overall customer sentiment?"

with col2:
    if st.button("Issues", use_container_width=True):
        st.session_state.current_question = "What are the top customer issues?"

with col3:
    if st.button("Improve", use_container_width=True):
        st.session_state.current_question = "How should we improve customer satisfaction?"

# Ask button
if st.button("Ask Question", type="primary"):
    if question:
        with st.spinner("Thinking..."):
            response = chatbot.get_response(question)
            st.session_state.chat_history.append((question, response))
            st.session_state.current_question = ""
            st.rerun()

# Display current question
if st.session_state.current_question:
    st.info(f"**Current Question:** {st.session_state.current_question}")

# Display response
if st.session_state.chat_history:
    latest_q, latest_a = st.session_state.chat_history[-1]
    st.success(f"**Latest Answer:** {latest_a}")

# Chat history
if st.session_state.chat_history:
    st.write("### 📜 Chat History")
    for i, (q, a) in enumerate(st.session_state.chat_history[-5:]):
        st.write(f"{i+1}. **Q:** {q}")
        st.write(f"   **A:** {a}")
        st.write("---")

if st.button("Clear History"):
    st.session_state.chat_history = []
    st.session_state.current_question = ""
    st.rerun()
