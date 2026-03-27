"""
Data Processing Pipeline for Customer Feedback Intelligence System
Handles data loading, cleaning, and preprocessing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from typing import Dict, List, Tuple

class DataProcessor:
    """Main data processing class"""
    
    def __init__(self):
        self.data = {}
        self.processed_data = None
        
    def load_data(self, data_path: str = "data/") -> Dict[str, pd.DataFrame]:
        """Load all CSV data files"""
        file_paths = {
            'surveys': f"{data_path}surveys.csv",
            'emails': f"{data_path}emails.csv",
            'social_media': f"{data_path}social_media.csv",
            'support_tickets': f"{data_path}support_tickets.csv"
        }
        
        for source, path in file_paths.items():
            try:
                self.data[source] = pd.read_csv(path)
                self.data[source]['source'] = source
                print(f"Loaded {len(self.data[source])} records from {source}")
            except FileNotFoundError:
                print(f"Warning: {path} not found")
                self.data[source] = pd.DataFrame()
        
        return self.data
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text data"""
        if pd.isna(text):
            return ""
        
        # Convert to string and lowercase
        text = str(text).lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def preprocess_data(self) -> pd.DataFrame:
        """Preprocess all data sources"""
        all_data = []
        
        for source, df in self.data.items():
            if df.empty:
                continue
                
            # Create a copy to avoid modifying original
            processed_df = df.copy()
            
            # Clean text fields
            if source == 'surveys':
                processed_df['clean_text'] = processed_df['feedback_text'].apply(self.clean_text)
            elif source == 'emails':
                processed_df['clean_text'] = (processed_df['subject'] + ' ' + processed_df['body']).apply(self.clean_text)
            elif source == 'social_media':
                processed_df['clean_text'] = processed_df['post_content'].apply(self.clean_text)
            elif source == 'support_tickets':
                processed_df['clean_text'] = processed_df['issue_description'].apply(self.clean_text)
            
            # Convert date column
            processed_df['date'] = pd.to_datetime(processed_df['date'])
            
            # Add additional features
            processed_df['text_length'] = processed_df['clean_text'].str.len()
            processed_df['word_count'] = processed_df['clean_text'].str.split().str.len()
            
            all_data.append(processed_df)
        
        # Combine all data
        if all_data:
            self.processed_data = pd.concat(all_data, ignore_index=True)
            
            # Sort by date
            self.processed_data = self.processed_data.sort_values('date')
            
            # Add temporal features
            self.processed_data['month'] = self.processed_data['date'].dt.to_period('M')
            self.processed_data['week'] = self.processed_data['date'].dt.to_period('W')
            self.processed_data['day_of_week'] = self.processed_data['date'].dt.day_name()
            
            print(f"Processed {len(self.processed_data)} total records")
            return self.processed_data
        else:
            print("No data to process")
            return pd.DataFrame()
    
    def get_sentiment_distribution(self) -> Dict[str, int]:
        """Get sentiment distribution across all data"""
        if self.processed_data is None:
            return {}
        
        return self.processed_data['sentiment'].value_counts().to_dict()
    
    def get_category_distribution(self) -> Dict[str, int]:
        """Get category distribution across all data"""
        if self.processed_data is None:
            return {}
        
        return self.processed_data['category'].value_counts().to_dict()
    
    def get_source_distribution(self) -> Dict[str, int]:
        """Get distribution by data source"""
        if self.processed_data is None:
            return {}
        
        return self.processed_data['source'].value_counts().to_dict()
    
    def get_temporal_trends(self, period: str = 'month') -> pd.DataFrame:
        """Get temporal trends for sentiment analysis"""
        if self.processed_data is None:
            return pd.DataFrame()
        
        if period == 'month':
            trends = self.processed_data.groupby(['month', 'sentiment']).size().unstack(fill_value=0)
        elif period == 'week':
            trends = self.processed_data.groupby(['week', 'sentiment']).size().unstack(fill_value=0)
        else:
            trends = self.processed_data.groupby(['date', 'sentiment']).size().unstack(fill_value=0)
        
        return trends
    
    def get_top_categories_by_sentiment(self, sentiment: str, top_n: int = 10) -> pd.Series:
        """Get top categories for a specific sentiment"""
        if self.processed_data is None:
            return pd.Series()
        
        filtered = self.processed_data[self.processed_data['sentiment'] == sentiment]
        return filtered['category'].value_counts().head(top_n)
    
    def get_key_metrics(self) -> Dict:
        """Get key metrics for dashboard"""
        if self.processed_data is None:
            return {}
        
        total_records = len(self.processed_data)
        sentiment_dist = self.get_sentiment_distribution()
        
        # Calculate satisfaction score (positive - negative) / total
        positive = sentiment_dist.get('positive', 0)
        negative = sentiment_dist.get('negative', 0)
        satisfaction_score = ((positive - negative) / total_records * 100) if total_records > 0 else 0
        
        # Average response length
        avg_response_length = self.processed_data['text_length'].mean()
        
        # Most active day
        most_active_day = self.processed_data['day_of_week'].mode().iloc[0] if not self.processed_data['day_of_week'].mode().empty else 'N/A'
        
        return {
            'total_records': total_records,
            'satisfaction_score': round(satisfaction_score, 2),
            'avg_response_length': round(avg_response_length, 2),
            'most_active_day': most_active_day,
            'sentiment_distribution': sentiment_dist,
            'date_range': {
                'start': self.processed_data['date'].min().strftime('%Y-%m-%d'),
                'end': self.processed_data['date'].max().strftime('%Y-%m-%d')
            }
        }
    
    def export_processed_data(self, output_path: str = "data/processed_feedback.csv"):
        """Export processed data to CSV"""
        if self.processed_data is not None:
            self.processed_data.to_csv(output_path, index=False)
            print(f"Processed data exported to {output_path}")
        else:
            print("No processed data to export")

def main():
    """Test the data processor"""
    processor = DataProcessor()
    
    # Load data
    processor.load_data()
    
    # Preprocess
    processed_data = processor.preprocess_data()
    
    # Show some insights
    if not processed_data.empty:
        print("\n=== Key Metrics ===")
        metrics = processor.get_key_metrics()
        for key, value in metrics.items():
            print(f"{key}: {value}")
        
        print("\n=== Sentiment Distribution ===")
        print(processor.get_sentiment_distribution())
        
        print("\n=== Category Distribution ===")
        print(processor.get_category_distribution())
        
        print("\n=== Source Distribution ===")
        print(processor.get_source_distribution())

if __name__ == "__main__":
    main()
