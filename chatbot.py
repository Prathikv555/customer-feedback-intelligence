"""
AI Chatbot for Customer Feedback Intelligence System
Provides conversational interface to query feedback insights
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from typing import Dict, List, Any, Tuple
import json

class FeedbackChatbot:
    """AI-powered chatbot for customer feedback analysis"""
    
    def __init__(self, data_processor, ai_analyzer):
        self.processor = data_processor
        self.analyzer = ai_analyzer
        self.data = data_processor.processed_data
        self.insights = None
        
        # Pre-compute common insights
        if self.data is not None and not self.data.empty:
            self.insights = self.analyzer.generate_insights_summary(self.data)
    
    def get_response(self, question: str) -> str:
        """Generate response to user question"""
        question_lower = question.lower()
        
        # Greeting responses
        if any(greeting in question_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return "Hello! I'm your Customer Feedback Intelligence Assistant. I can help you analyze customer feedback data. Ask me about trends, sentiment, categories, or any insights from the data!"
        
        # Help responses
        if any(help_word in question_lower for help_word in ['help', 'what can you do', 'how can you help']):
            return """I can help you with:
📊 **Data Analysis**: Ask about sentiment trends, category distributions, or feedback volumes
🔍 **Specific Queries**: "What are the top issues?", "How is customer satisfaction?", "What are customers saying about [feature]?"
📈 **Trend Analysis**: "Are complaints increasing?", "What's the trend this month?"
🎯 **Insights**: "What are the key takeaways?", "What should we focus on?"
💡 **Recommendations**: "What should we improve?", "Where are the biggest problems?"

Try asking: "What's the overall customer sentiment?" or "What are the top customer complaints?\""""
        
        # Sentiment related questions
        if any(word in question_lower for word in ['sentiment', 'satisfaction', 'happy', 'unhappy', 'positive', 'negative']):
            return self._handle_sentiment_question(question_lower)
        
        # Trend related questions
        if any(word in question_lower for word in ['trend', 'increasing', 'decreasing', 'over time', 'monthly', 'weekly']):
            return self._handle_trend_question(question_lower)
        
        # Category related questions
        if any(word in question_lower for word in ['category', 'type', 'bug', 'feature', 'support', 'performance']):
            return self._handle_category_question(question_lower)
        
        # Volume/quantity questions
        if any(word in question_lower for word in ['how many', 'volume', 'count', 'number', 'total']):
            return self._handle_volume_question(question_lower)
        
        # Issues/problems questions
        if any(word in question_lower for word in ['issue', 'problem', 'complaint', 'concern', 'trouble']):
            return self._handle_issues_question(question_lower)
        
        # Feature/product questions
        if any(word in question_lower for word in ['feature', 'product', 'service', 'improvement']):
            return self._handle_feature_question(question_lower)
        
        # Recommendation questions
        if any(word in question_lower for word in ['recommend', 'suggest', 'improve', 'fix', 'should']):
            return self._handle_recommendation_question(question_lower)
        
        # Default response
        return """I'm not sure how to answer that specific question. Here's what I can help you with:

📊 **Ask about**: sentiment, trends, categories, volumes, issues, or recommendations
💡 **Try**: "What's the overall sentiment?" or "What are the top issues?"
📈 **Or**: "How many complaints did we get?" or "What's trending this month?"

What specific aspect of customer feedback would you like to know about?"""
    
    def _handle_sentiment_question(self, question: str) -> str:
        """Handle sentiment-related questions"""
        if not self.insights:
            return "No data available for sentiment analysis."
        
        summary = self.insights.get('summary', {})
        positive_pct = summary.get('positive_percentage', 0)
        negative_pct = summary.get('negative_percentage', 0)
        satisfaction_score = summary.get('satisfaction_score', 0)
        
        response = f"**Sentiment Analysis:**\n"
        response += f"• Positive feedback: {positive_pct}%\n"
        response += f"• Negative feedback: {negative_pct}%\n"
        response += f"• Satisfaction score: {satisfaction_score}\n\n"
        
        if 'emerging_issues' in self.insights:
            emerging = self.insights['emerging_issues']
            if 'negative_percentage' in emerging:
                response += f"**Recent Trend:** In the last {emerging.get('period_days', 7)} days, {emerging.get('negative_percentage', 0)}% of feedback was negative.\n"
        
        if negative_pct > 25:
            response += "\n⚠️ **Alert:** High negative sentiment detected. Consider immediate action."
        elif positive_pct > 70:
            response += "\n✅ **Great:** High positive sentiment! Keep up the good work."
        
        return response
    
    def _handle_trend_question(self, question: str) -> str:
        """Handle trend-related questions"""
        if self.data is None or self.data.empty:
            return "No data available for trend analysis."
        
        # Get recent vs older data comparison
        recent_date = pd.Timestamp.now() - timedelta(days=30)
        recent_data = self.data[self.data['date'] >= recent_date]
        older_data = self.data[self.data['date'] < recent_date]
        
        if recent_data.empty or older_data.empty:
            return "Insufficient data for trend analysis."
        
        recent_negative_pct = (recent_data['sentiment'] == 'negative').mean() * 100
        older_negative_pct = (older_data['sentiment'] == 'negative').mean() * 100
        
        trend = "increasing" if recent_negative_pct > older_negative_pct else "decreasing"
        change = abs(recent_negative_pct - older_negative_pct)
        
        response = f"**Trend Analysis (Last 30 Days):**\n"
        response += f"• Negative feedback is {trend} by {change:.1f}%\n"
        response += f"• Recent negative rate: {recent_negative_pct:.1f}%\n"
        response += f"• Previous negative rate: {older_negative_pct:.1f}%\n\n"
        
        if trend == "increasing":
            response += "🔴 **Action Needed:** Negative feedback is trending upward. Investigate recent issues."
        else:
            response += "🟢 **Positive:** Negative feedback is trending downward."
        
        return response
    
    def _handle_category_question(self, question: str) -> str:
        """Handle category-related questions"""
        if self.data is None or self.data.empty:
            return "No data available for category analysis."
        
        category_dist = self.data['category'].value_counts()
        total = len(self.data)
        
        response = f"**Category Distribution:**\n"
        for category, count in category_dist.head(5).items():
            pct = (count / total) * 100
            response += f"• {category}: {count} ({pct:.1f}%)\n"
        
        # Check for specific category mentions
        if 'bug' in question:
            bug_count = category_dist.get('Bug Report', 0)
            response += f"\n**Bug Reports:** {bug_count} total issues reported."
        
        if 'feature' in question:
            feature_count = category_dist.get('Feature Request', 0)
            response += f"\n**Feature Requests:** {feature_count} new features requested."
        
        return response
    
    def _handle_volume_question(self, question: str) -> str:
        """Handle volume/quantity questions"""
        if self.data is None or self.data.empty:
            return "No data available for volume analysis."
        
        total_feedback = len(self.data)
        source_dist = self.data['source'].value_counts()
        
        response = f"**Feedback Volume:**\n"
        response += f"• Total feedback: {total_feedback:,} records\n"
        response += f"• Date range: {self.data['date'].min().strftime('%Y-%m-%d')} to {self.data['date'].max().strftime('%Y-%m-%d')}\n\n"
        
        response += "**By Source:**\n"
        for source, count in source_dist.items():
            response += f"• {source}: {count}\n"
        
        # Recent volume
        recent_date = pd.Timestamp.now() - timedelta(days=7)
        recent_count = len(self.data[self.data['date'] >= recent_date])
        response += f"\n**Last 7 Days:** {recent_count} feedback items"
        
        return response
    
    def _handle_issues_question(self, question: str) -> str:
        """Handle issues/problems questions"""
        if not self.insights:
            return "No data available for issue analysis."
        
        response = "**Top Issues & Concerns:**\n"
        
        # Get negative feedback
        negative_data = self.data[self.data['sentiment'] == 'negative']
        if not negative_data.empty:
            top_negative_categories = negative_data['category'].value_counts().head(3)
            response += "**Most Complained About:**\n"
            for category, count in top_negative_categories.items():
                response += f"• {category}: {count} complaints\n"
        
        # Emerging issues
        if 'emerging_issues' in self.insights:
            emerging = self.insights['emerging_issues']
            if 'top_issues' in emerging and emerging['top_issues']:
                response += "\n**Emerging Issues:**\n"
                for issue, score in emerging['top_issues'][:5]:
                    response += f"• {issue} (severity: {score:.3f})\n"
        
        return response
    
    def _handle_feature_question(self, question: str) -> str:
        """Handle feature/product questions"""
        if self.data is None or self.data.empty:
            return "No data available for feature analysis."
        
        # Look for feature requests
        feature_requests = self.data[self.data['category'] == 'Feature Request']
        
        response = f"**Feature Analysis:**\n"
        response += f"• Total feature requests: {len(feature_requests)}\n"
        
        if not feature_requests.empty:
            # Extract common feature mentions
            all_text = ' '.join(feature_requests['clean_text'].fillna(''))
            common_words = ['dashboard', 'reporting', 'analytics', 'export', 'mobile', 'api', 'search', 'notifications']
            
            mentioned_features = []
            for word in common_words:
                if word in all_text:
                    count = all_text.count(word)
                    mentioned_features.append((word, count))
            
            if mentioned_features:
                mentioned_features.sort(key=lambda x: x[1], reverse=True)
                response += "\n**Most Requested Features:**\n"
                for feature, count in mentioned_features[:5]:
                    response += f"• {feature}: mentioned {count} times\n"
        
        return response
    
    def _handle_recommendation_question(self, question: str) -> str:
        """Handle recommendation questions"""
        if not self.insights or 'recommendations' not in self.insights:
            return "No recommendations available."
        
        recommendations = self.insights['recommendations']
        
        response = "**🎯 AI Recommendations:**\n"
        for i, rec in enumerate(recommendations, 1):
            response += f"{i}. {rec}\n"
        
        # Add additional context-based recommendations
        if self.data is not None and not self.data.empty:
            summary = self.insights.get('summary', {})
            negative_pct = summary.get('negative_percentage', 0)
            
            if negative_pct > 30:
                response += "\n**Priority Actions:**\n"
                response += "• Address top 3 complaint categories immediately\n"
                response += "• Review recent negative feedback for patterns\n"
                response += "• Consider customer outreach for affected users"
            elif negative_pct > 20:
                response += "\n**Suggested Actions:**\n"
                response += "• Monitor trending issues closely\n"
                response += "• Focus on improving most common complaint areas"
        
        return response
    
    def get_conversation_context(self) -> Dict[str, Any]:
        """Get conversation context for better responses"""
        if not self.insights:
            return {"status": "no_data"}
        
        return {
            "total_records": len(self.data) if self.data is not None else 0,
            "date_range": {
                "start": self.data['date'].min().strftime('%Y-%m-%d') if self.data is not None else None,
                "end": self.data['date'].max().strftime('%Y-%m-%d') if self.data is not None else None
            },
            "sentiment_summary": self.insights.get('summary', {}),
            "top_categories": list(self.data['category'].value_counts().head(3).index) if self.data is not None else []
        }

def main():
    """Test the chatbot"""
    print("Customer Feedback Intelligence Chatbot")
    print("Type 'quit' to exit\n")
    
    # Mock data processor and analyzer for testing
    class MockProcessor:
        def __init__(self):
            self.processed_data = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=100),
                'sentiment': np.random.choice(['positive', 'negative', 'neutral'], 100),
                'category': np.random.choice(['Bug Report', 'Feature Request', 'Support'], 100),
                'clean_text': ['sample text'] * 100
            })
    
    class MockAnalyzer:
        def generate_insights_summary(self, data):
            return {
                'summary': {
                    'positive_percentage': 60,
                    'negative_percentage': 25,
                    'satisfaction_score': 35
                },
                'recommendations': [
                    'Focus on improving customer support',
                    'Address common bug reports',
                    'Consider implementing top feature requests'
                ]
            }
    
    processor = MockProcessor()
    analyzer = MockAnalyzer()
    chatbot = FeedbackChatbot(processor, analyzer)
    
    while True:
        question = input("You: ")
        if question.lower() in ['quit', 'exit', 'bye']:
            break
        
        response = chatbot.get_response(question)
        print(f"Bot: {response}\n")

if __name__ == "__main__":
    main()
