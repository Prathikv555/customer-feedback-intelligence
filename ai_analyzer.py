"""
AI Analysis Module for Customer Feedback Intelligence System
Handles sentiment analysis, categorization, and trend detection
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter
import re
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class AIAnalyzer:
    """AI-powered feedback analysis"""
    
    def __init__(self):
        self.sentiment_model = None
        self.category_model = None
        self.vectorizer = None
        self.topic_model = None
        self.feature_names = None
        
    def analyze_sentiment_textblob(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using TextBlob"""
        if pd.isna(text) or text == "":
            return {"polarity": 0, "subjectivity": 0, "sentiment": "neutral"}
        
        blob = TextBlob(str(text))
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Categorize sentiment
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "sentiment": sentiment,
            "confidence": abs(polarity)
        }
    
    def categorize_feedback_rule_based(self, text: str) -> str:
        """Categorize feedback using rule-based approach"""
        if pd.isna(text) or text == "":
            return "General"
        
        text = str(text).lower()
        
        # Define category keywords
        categories = {
            'Feature Request': ['request', 'feature', 'add', 'implement', 'would like', 'suggest', 'enhancement'],
            'Bug Report': ['bug', 'error', 'issue', 'problem', 'broken', 'not working', 'crash', 'fail'],
            'Usability': ['difficult', 'confusing', 'hard to use', 'user interface', 'ui', 'ux', 'navigation'],
            'Performance': ['slow', 'lag', 'performance', 'speed', 'fast', 'optimize', 'loading'],
            'Pricing': ['price', 'cost', 'expensive', 'cheap', 'affordable', 'subscription', 'billing'],
            'Support': ['support', 'help', 'customer service', 'assistance', 'response', 'ticket'],
            'Documentation': ['documentation', 'guide', 'manual', 'tutorial', 'instructions', 'help docs'],
            'Integration': ['integration', 'api', 'connect', 'sync', 'third party', 'compatibility']
        }
        
        # Score each category
        category_scores = {}
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in text)
            category_scores[category] = score
        
        # Return category with highest score, or General if no matches
        if max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get)
        else:
            return "General"
    
    def extract_key_phrases(self, texts: List[str], top_n: int = 20) -> List[Tuple[str, float]]:
        """Extract key phrases using TF-IDF"""
        if not texts:
            return []
        
        # Clean texts
        clean_texts = [str(text).lower() if not pd.isna(text) else "" for text in texts]
        
        # TF-IDF Vectorization
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(clean_texts)
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get average TF-IDF scores
            mean_scores = np.mean(tfidf_matrix.toarray(), axis=0)
            
            # Get top phrases
            top_indices = np.argsort(mean_scores)[::-1][:top_n]
            top_phrases = [(feature_names[i], mean_scores[i]) for i in top_indices]
            
            return top_phrases
        except:
            return []
    
    def discover_topics(self, texts: List[str], n_topics: int = 5) -> Dict[int, List[str]]:
        """Discover topics using Latent Dirichlet Allocation"""
        if not texts:
            return {}
        
        # Clean texts
        clean_texts = [str(text).lower() if not pd.isna(text) else "" for text in texts]
        
        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(clean_texts)
            
            # LDA
            self.topic_model = LatentDirichletAllocation(
                n_components=n_topics,
                random_state=42,
                max_iter=10
            )
            
            lda_matrix = self.topic_model.fit_transform(tfidf_matrix)
            feature_names = vectorizer.get_feature_names_out()
            
            # Extract topics
            topics = {}
            for topic_idx, topic in enumerate(self.topic_model.components_):
                top_words_idx = topic.argsort()[-10:][::-1]
                top_words = [feature_names[i] for i in top_words_idx]
                topics[topic_idx] = top_words
            
            return topics
        except:
            return {}
    
    def detect_emerging_issues(self, df: pd.DataFrame, days: int = 7) -> Dict[str, Any]:
        """Detect emerging issues from recent data"""
        if df.empty:
            return {}
        
        # Filter recent data
        recent_date = pd.Timestamp.now() - pd.Timedelta(days=days)
        recent_df = df[df['date'] >= recent_date]
        
        if recent_df.empty:
            return {}
        
        # Get negative feedback from recent period
        negative_recent = recent_df[recent_df['sentiment'] == 'negative']
        
        if negative_recent.empty:
            return {"message": "No negative feedback in recent period"}
        
        # Extract key issues
        key_phrases = self.extract_key_phrases(negative_recent['clean_text'].tolist(), top_n=10)
        
        # Get top categories with negative sentiment
        negative_categories = negative_recent['category'].value_counts().head(5)
        
        # Calculate trend (increase in negative feedback)
        total_recent = len(recent_df)
        negative_recent_count = len(negative_recent)
        negative_percentage = (negative_recent_count / total_recent * 100) if total_recent > 0 else 0
        
        return {
            "period_days": days,
            "total_feedback": total_recent,
            "negative_feedback": negative_recent_count,
            "negative_percentage": round(negative_percentage, 2),
            "top_issues": key_phrases,
            "affected_categories": negative_categories.to_dict(),
            "alert_level": "high" if negative_percentage > 30 else "medium" if negative_percentage > 20 else "low"
        }
    
    def generate_insights_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive insights summary"""
        if df.empty:
            return {}
        
        # Overall sentiment analysis
        sentiment_dist = df['sentiment'].value_counts().to_dict()
        total_feedback = len(df)
        
        # Key metrics
        positive_pct = (sentiment_dist.get('positive', 0) / total_feedback * 100) if total_feedback > 0 else 0
        negative_pct = (sentiment_dist.get('negative', 0) / total_feedback * 100) if total_feedback > 0 else 0
        
        # Top categories
        top_categories = df['category'].value_counts().head(5)
        
        # Key phrases across all feedback
        key_phrases = self.extract_key_phrases(df['clean_text'].tolist(), top_n=15)
        
        # Emerging issues
        emerging_issues = self.detect_emerging_issues(df)
        
        # Topics
        topics = self.discover_topics(df['clean_text'].tolist())
        
        return {
            "summary": {
                "total_feedback": total_feedback,
                "sentiment_distribution": sentiment_dist,
                "positive_percentage": round(positive_pct, 2),
                "negative_percentage": round(negative_pct, 2),
                "satisfaction_score": round(positive_pct - negative_pct, 2)
            },
            "top_categories": top_categories.to_dict(),
            "key_phrases": key_phrases,
            "emerging_issues": emerging_issues,
            "topics": topics,
            "recommendations": self._generate_recommendations(sentiment_dist, top_categories, emerging_issues)
        }
    
    def _generate_recommendations(self, sentiment_dist: Dict, categories: pd.Series, emerging_issues: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Based on sentiment
        total = sum(sentiment_dist.values())
        negative_pct = (sentiment_dist.get('negative', 0) / total * 100) if total > 0 else 0
        
        if negative_pct > 25:
            recommendations.append("High negative feedback detected. Prioritize addressing customer concerns.")
        
        # Based on top categories
        if not categories.empty:
            top_category = categories.index[0]
            if top_category == 'Bug Report':
                recommendations.append("Focus on bug fixes and quality assurance.")
            elif top_category == 'Feature Request':
                recommendations.append("Consider implementing most requested features.")
            elif top_category == 'Support':
                recommendations.append("Improve customer support response times and quality.")
        
        # Based on emerging issues
        if 'alert_level' in emerging_issues and emerging_issues['alert_level'] == 'high':
            recommendations.append("URGENT: Address emerging issues immediately to prevent customer churn.")
        
        if not recommendations:
            recommendations.append("Overall feedback is positive. Continue monitoring for trends.")
        
        return recommendations
    
    def analyze_text_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analyze a batch of texts for sentiment and category"""
        results = []
        
        for text in texts:
            sentiment_result = self.analyze_sentiment_textblob(text)
            category = self.categorize_feedback_rule_based(text)
            
            results.append({
                "sentiment": sentiment_result["sentiment"],
                "sentiment_score": sentiment_result["polarity"],
                "category": category,
                "confidence": sentiment_result["confidence"]
            })
        
        return results

def main():
    """Test the AI analyzer"""
    # Create sample data
    sample_texts = [
        "The product is great but the user interface could be improved.",
        "I'm experiencing a bug when trying to export data.",
        "Customer support was very helpful and responsive.",
        "The pricing is too expensive for small businesses.",
        "Would love to see a dark mode feature added."
    ]
    
    analyzer = AIAnalyzer()
    
    print("=== Sample Analysis ===")
    for i, text in enumerate(sample_texts):
        result = analyzer.analyze_text_batch([text])[0]
        print(f"Text: {text}")
        print(f"Sentiment: {result['sentiment']} (Score: {result['sentiment_score']:.2f})")
        print(f"Category: {result['category']}")
        print()

if __name__ == "__main__":
    main()
