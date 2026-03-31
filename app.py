"""
Customer Feedback Intelligence Dashboard
Main application for visualizing customer feedback insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from data_processor import DataProcessor
from ai_analyzer import AIAnalyzer
from chatbot import FeedbackChatbot

# Set page config
st.set_page_config(
    page_title="Customer Feedback Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_data():
    """Load and process data with caching"""
    processor = DataProcessor()
    processor.load_data()
    processed_data = processor.preprocess_data()
    return processor, processed_data

@st.cache_data
def get_ai_insights(_data):
    """Get AI insights with caching"""
    analyzer = AIAnalyzer()
    insights = analyzer.generate_insights_summary(_data)
    return insights, analyzer

def create_sentiment_gauge(sentiment_dist):
    """Create sentiment gauge chart"""
    total = sum(sentiment_dist.values())
    positive_pct = (sentiment_dist.get('positive', 0) / total * 100) if total > 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = positive_pct,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Positive Sentiment %"},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_temporal_trend_chart(data, period='month'):
    """Create temporal trend chart"""
    if period == 'month':
        trend_data = data.groupby(['month', 'sentiment']).size().unstack(fill_value=0)
        trend_data.index = trend_data.index.astype(str)
    else:
        trend_data = data.groupby(['week', 'sentiment']).size().unstack(fill_value=0)
        trend_data.index = trend_data.index.astype(str)
    
    fig = go.Figure()
    
    colors = {'positive': '#2E8B57', 'negative': '#DC143C', 'neutral': '#4682B4'}
    
    for sentiment in ['positive', 'negative', 'neutral']:
        if sentiment in trend_data.columns:
            fig.add_trace(go.Scatter(
                x=trend_data.index,
                y=trend_data[sentiment],
                mode='lines+markers',
                name=sentiment.capitalize(),
                line=dict(color=colors[sentiment], width=3),
                marker=dict(size=8)
            ))
    
    fig.update_layout(
        title=f"Sentiment Trends by {period.capitalize()}",
        xaxis_title=f"{period.capitalize()}",
        yaxis_title="Number of Feedback",
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_category_distribution_chart(category_dist):
    """Create category distribution chart"""
    fig = go.Figure(data=[
        go.Bar(
            x=list(category_dist.keys()),
            y=list(category_dist.values()),
            marker_color='lightblue',
            text=list(category_dist.values()),
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Feedback by Category",
        xaxis_title="Category",
        yaxis_title="Count",
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig

def create_source_pie_chart(source_dist):
    """Create source distribution pie chart"""
    fig = go.Figure(data=[
        go.Pie(
            labels=list(source_dist.keys()),
            values=list(source_dist.values()),
            hole=0.3,
            marker_colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']
        )
    ])
    
    fig.update_layout(
        title="Feedback Sources",
        height=400
    )
    
    return fig

def create_word_cloud_data(key_phrases):
    """Create word cloud data"""
    if not key_phrases:
        return pd.DataFrame({'word': [], 'size': []})
    
    words = [phrase[0] for phrase in key_phrases[:20]]
    sizes = [phrase[1] * 100 for phrase in key_phrases[:20]]
    
    return pd.DataFrame({'word': words, 'size': sizes})

def main():
    """Main application"""
    # Header
    st.markdown('<h1 class="main-header">📊 Customer Feedback Intelligence Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Dashboard Controls")
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    # Time period filter
    time_period = st.sidebar.selectbox(
        "Select Time Period",
        ["Last 30 Days", "Last 3 Months", "Last 6 Months", "All Time"],
        index=2
    )
    
    # AI Chatbot in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 AI Assistant")
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Initialize question in session state
    if 'sidebar_question' not in st.session_state:
        st.session_state.sidebar_question = ""
    
    # Quick question buttons (outside expander for better interaction)
    st.sidebar.markdown("**Quick Questions:**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.sidebar.button("Sentiment?", key="sentiment_q", use_container_width=True):
            st.session_state.sidebar_question = "What's the overall sentiment?"
    
    with col2:
        if st.sidebar.button("Top Issues?", key="issues_q", use_container_width=True):
            st.session_state.sidebar_question = "What are the top issues?"
    
    if st.sidebar.button("How to improve?", key="improve_q", use_container_width=True):
        st.session_state.sidebar_question = "How should we improve?"
    
    # Chat interface in expander
    with st.sidebar.expander("💬 Ask Your Question", expanded=False):
        # Get current question from session state
        current_question = st.session_state.sidebar_question
        
        user_question = st.text_input(
            "Type your question...",
            placeholder="e.g., What's the sentiment?",
            value=current_question,
            key="sidebar_question_input"
        )
        
        # Update session state if user changes input
        if user_question != current_question:
            st.session_state.sidebar_question = user_question
        
        ask_button = st.button("Ask", type="primary", key="sidebar_ask")
        
        # Process question
        if ask_button and st.session_state.sidebar_question:
            with st.spinner("Thinking..."):
                try:
                    # Initialize chatbot if not already done
                    if 'chatbot' not in st.session_state:
                        st.session_state.chatbot = FeedbackChatbot(processor, analyzer)
                    
                    response = st.session_state.chatbot.get_response(st.session_state.sidebar_question)
                    
                    # Add to chat history
                    st.session_state.chat_history.append((st.session_state.sidebar_question, response))
                    
                    # Display latest response
                    st.markdown("**Latest Response:**")
                    st.markdown(response)
                    
                    # Clear the question
                    st.session_state.sidebar_question = ""
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Show recent chat history
        if st.session_state.chat_history:
            st.markdown("**Recent Questions:**")
            for i, (q, a) in enumerate(st.session_state.chat_history[-3:]):  # Show last 3
                with st.expander(f"Q{i+1}: {q[:30]}..."):
                    st.markdown(f"**Q:** {q}")
                    st.markdown(f"**A:** {a}")
        
        if st.button("Clear Chat", key="clear_chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.sidebar_question = ""
            st.rerun()
    
    # Load data
    with st.spinner("Loading and processing data..."):
        try:
            processor, data = load_and_process_data()
            
            if data.empty:
                st.error("No data found. Please run the data generation script first.")
                st.info("Run: `python generate_feedback_data.py`")
                return
            
            # Filter by time period
            if time_period == "Last 30 Days":
                cutoff_date = datetime.now() - timedelta(days=30)
                data = data[data['date'] >= cutoff_date]
            elif time_period == "Last 3 Months":
                cutoff_date = datetime.now() - timedelta(days=90)
                data = data[data['date'] >= cutoff_date]
            elif time_period == "Last 6 Months":
                cutoff_date = datetime.now() - timedelta(days=180)
                data = data[data['date'] >= cutoff_date]
            
            # Get AI insights
            insights, analyzer = get_ai_insights(data)
            
            # Initialize chatbot in session state
            if 'chatbot' not in st.session_state:
                st.session_state.chatbot = FeedbackChatbot(processor, analyzer)
            
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return
    
    # Key Metrics
    st.markdown("## 📈 Key Metrics")
    metrics = processor.get_key_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Feedback",
            f"{metrics.get('total_records', 0):,}",
            delta="Records"
        )
    
    with col2:
        st.metric(
            "Satisfaction Score",
            f"{metrics.get('satisfaction_score', 0)}%",
            delta="Positive - Negative"
        )
    
    with col3:
        st.metric(
            "Avg Response Length",
            f"{metrics.get('avg_response_length', 0)} chars",
            delta="Characters"
        )
    
    with col4:
        st.metric(
            "Most Active Day",
            metrics.get('most_active_day', 'N/A'),
            delta="Day of Week"
        )
    
    # Charts Row 1
    st.markdown("## 📊 Sentiment Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        sentiment_dist = processor.get_sentiment_distribution()
        fig_gauge = create_sentiment_gauge(sentiment_dist)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Sentiment distribution bar chart
        fig_sentiment = go.Figure(data=[
            go.Bar(
                x=list(sentiment_dist.keys()),
                y=list(sentiment_dist.values()),
                marker_color=['lightgreen', 'lightgray', 'lightcoral']
            )
        ])
        fig_sentiment.update_layout(
            title="Sentiment Distribution",
            xaxis_title="Sentiment",
            yaxis_title="Count",
            height=300
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # Temporal Trends
    st.markdown("## 📈 Temporal Trends")
    period = st.selectbox("Select Period", ["month", "week"], key="trend_period")
    fig_trend = create_temporal_trend_chart(data, period)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Category and Source Analysis
    st.markdown("## 📂 Category & Source Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        category_dist = processor.get_category_distribution()
        fig_category = create_category_distribution_chart(category_dist)
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        source_dist = processor.get_source_distribution()
        fig_source = create_source_pie_chart(source_dist)
        st.plotly_chart(fig_source, use_container_width=True)
    
    # AI Insights
    st.markdown("## 🤖 AI-Powered Insights")
    
    # Summary insights
    if 'summary' in insights:
        summary = insights['summary']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Positive %", f"{summary.get('positive_percentage', 0)}%")
        
        with col2:
            st.metric("Negative %", f"{summary.get('negative_percentage', 0)}%")
        
        with col3:
            st.metric("Satisfaction", f"{summary.get('satisfaction_score', 0)}")
    
    # Emerging Issues Alert
    if 'emerging_issues' in insights:
        emerging = insights['emerging_issues']
        if 'alert_level' in emerging:
            alert_color = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(emerging['alert_level'], '⚪')
            
            st.markdown(f"### {alert_color} Emerging Issues Alert")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Negative Feedback", f"{emerging.get('negative_percentage', 0)}%")
            
            with col2:
                st.metric("Period", f"Last {emerging.get('period_days', 0)} days")
            
            with col3:
                st.metric("Alert Level", emerging.get('alert_level', 'unknown').upper())
    
    # Key Phrases
    if 'key_phrases' in insights and insights['key_phrases']:
        st.markdown("### 🔑 Key Topics Mentioned")
        
        # Create word cloud style display
        phrases_df = create_word_cloud_data(insights['key_phrases'])
        
        if not phrases_df.empty:
            # Display as a table with sizing
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Display top phrases
                top_phrases = insights['key_phrases'][:10]
                for i, (phrase, score) in enumerate(top_phrases, 1):
                    st.write(f"{i}. **{phrase}** (Score: {score:.3f})")
            
            with col2:
                # Simple bar chart of top phrases
                top_5_phrases = insights['key_phrases'][:5]
                phrases = [p[0] for p in top_5_phrases]
                scores = [p[1] for p in top_5_phrases]
                
                fig_phrases = go.Figure(data=[
                    go.Bar(y=phrases, x=scores, orientation='h')
                ])
                fig_phrases.update_layout(
                    title="Top 5 Key Phrases",
                    height=300,
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig_phrases, use_container_width=True)
    
    # Recommendations
    if 'recommendations' in insights:
        st.markdown("### 💡 Recommendations")
        
        for i, recommendation in enumerate(insights['recommendations'], 1):
            st.markdown(f"""
            <div class="insight-box">
                <strong>{i}.</strong> {recommendation}
            </div>
            """, unsafe_allow_html=True)
    
    # Topics Analysis
    if 'topics' in insights and insights['topics']:
        st.markdown("### 📚 Topic Analysis")
        
        topics = insights['topics']
        for topic_id, words in topics.items():
            with st.expander(f"Topic {topic_id + 1}"):
                st.write(", ".join(words))
    
    # Data Table
    st.markdown("## 📋 Recent Feedback Data")
    
    # Sample data display
    sample_size = st.slider("Show sample records", 10, 100, 20)
    sample_data = data.head(sample_size)
    
    # Select columns to display
    display_columns = ['date', 'source', 'sentiment', 'category', 'clean_text']
    available_columns = [col for col in display_columns if col in sample_data.columns]
    
    if available_columns:
        st.dataframe(
            sample_data[available_columns],
            use_container_width=True,
            hide_index=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Customer Feedback Intelligence System | Real-time Analysis & Insights"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
