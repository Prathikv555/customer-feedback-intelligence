"""
Simple test script to verify chatbot functionality
"""

import streamlit as st
from data_processor import DataProcessor
from ai_analyzer import AIAnalyzer
from chatbot import FeedbackChatbot

# Test the chatbot independently
st.title("🤖 Chatbot Test")

# Load and process data
processor = DataProcessor()
processor.load_data()
data = processor.preprocess_data()

if not data.empty:
    st.error("No data found. Please run generate_feedback_data.py first")
else:
    # Initialize analyzer and chatbot
    analyzer = AIAnalyzer()
    insights = analyzer.generate_insights_summary(data)
    chatbot = FeedbackChatbot(processor, analyzer)
    
    st.success("Chatbot initialized successfully!")
    
    # Test questions
    test_questions = [
        "What's the overall sentiment?",
        "What are the top issues?",
        "How should we improve?"
    ]
    
    for question in test_questions:
        st.write(f"**Question:** {question}")
        response = chatbot.get_response(question)
        st.write(f"**Answer:** {response}")
        st.write("---")

st.info("If you see responses above, the chatbot is working correctly!")
