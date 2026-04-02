"""
Dynamic Data Loader for Customer Feedback Intelligence System
Supports multiple datasets and user uploads
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import streamlit as st
from typing import Dict, List, Optional

class DynamicDataLoader:
    """Handle multiple datasets and user uploads"""
    
    def __init__(self):
        self.datasets = {}
        self.current_dataset = None
        self.load_available_datasets()
    
    def load_available_datasets(self):
        """Load all available datasets from data directory"""
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            return
        
        # Look for CSV files
        dataset_files = {
            'surveys': 'surveys.csv',
            'emails': 'emails.csv', 
            'social_media': 'social_media.csv',
            'support_tickets': 'support_tickets.csv'
        }
        
        for name, filename in dataset_files.items():
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                try:
                    self.datasets[name] = pd.read_csv(filepath)
                    print(f"Loaded {name}: {len(self.datasets[name])} records")
                except Exception as e:
                    print(f"Error loading {name}: {str(e)}")
                    self.datasets[name] = pd.DataFrame()
    
    def get_available_datasets(self) -> List[str]:
        """Get list of available dataset names"""
        return list(self.datasets.keys())
    
    def set_active_dataset(self, dataset_name: str):
        """Set the active dataset"""
        if dataset_name in self.datasets:
            self.current_dataset = dataset_name
            return True
        return False
    
    def get_current_data(self) -> pd.DataFrame:
        """Get current active dataset"""
        if self.current_dataset and self.current_dataset in self.datasets:
            return self.datasets[self.current_dataset]
        return pd.DataFrame()
    
    def get_dataset_info(self) -> Dict:
        """Get information about current dataset"""
        if not self.current_dataset:
            return {"status": "No dataset selected"}
        
        data = self.datasets[self.current_dataset]
        
        # Handle date column - convert to datetime if it's a string
        date_info = {"start": "N/A", "end": "N/A"}
        if not data.empty and 'date' in data.columns:
            try:
                # Convert to datetime if needed
                dates = pd.to_datetime(data['date'], errors='coerce')
                if not dates.isna().all():
                    date_info = {
                        "start": dates.min().strftime('%Y-%m-%d'),
                        "end": dates.max().strftime('%Y-%m-%d')
                    }
            except Exception as e:
                print(f"Date conversion error: {e}")
        
        return {
            "name": self.current_dataset,
            "records": len(data),
            "date_range": date_info,
            "sources": list(data['source'].unique()) if 'source' in data.columns else [],
            "categories": list(data['category'].unique()) if 'category' in data.columns else []
        }
    
    def combine_datasets(self, dataset_names: List[str]) -> pd.DataFrame:
        """Combine multiple datasets into one"""
        combined_data = []
        for name in dataset_names:
            if name in self.datasets:
                data = self.datasets[name].copy()
                data['dataset_source'] = name
                combined_data.append(data)
        
        if combined_data:
            return pd.concat(combined_data, ignore_index=True)
        return pd.DataFrame()
    
    def upload_dataset(self, uploaded_file, dataset_name: str) -> bool:
        """Handle user file upload"""
        try:
            # Read uploaded file
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            else:
                # Assume it's a text file that needs processing
                data = self._process_text_upload(uploaded_file)
            
            # Save to data directory
            filepath = os.path.join("data", f"{dataset_name}.csv")
            data.to_csv(filepath, index=False)
            
            # Load into memory
            self.datasets[dataset_name] = data
            self.current_dataset = dataset_name
            
            return True
            
        except Exception as e:
            st.error(f"Error uploading dataset: {str(e)}")
            return False
    
    def _process_text_upload(self, uploaded_file):
        """Process uploaded text file into feedback format"""
        try:
            # Read text content
            content = uploaded_file.read().decode('utf-8')
            lines = content.strip().split('\n')
            
            # Create structured data from text
            feedback_data = []
            for i, line in enumerate(lines):
                if line.strip():
                    feedback_data.append({
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'source': 'uploaded_text',
                        'sentiment': 'neutral',  # Default to neutral
                        'category': 'General',
                        'clean_text': line.strip(),
                        'customer_id': f'upload_user_{i+1}'
                    })
            
            return pd.DataFrame(feedback_data)
            
        except Exception as e:
            st.error(f"Error processing text file: {str(e)}")
            return pd.DataFrame()

def main():
    """Test dynamic data loader"""
    st.title("🔄 Dynamic Data Loader Test")
    
    loader = DynamicDataLoader()
    
    # Show available datasets
    st.write("### Available Datasets:")
    datasets = loader.get_available_datasets()
    if datasets:
        for dataset in datasets:
            info = loader.datasets[dataset]
            st.write(f"- **{dataset}**: {len(info)} records")
    else:
        st.warning("No datasets found. Please run generate_feedback_data.py first.")
    
    # Dataset selector
    if datasets:
        selected = st.selectbox("Select Active Dataset:", datasets)
        if selected != loader.current_dataset:
            if loader.set_active_dataset(selected):
                st.success(f"Switched to: {selected}")
                st.rerun()
    
    # File upload section
    st.write("### Upload New Dataset:")
    uploaded_file = st.file_uploader(
        "Upload CSV or text file",
        type=['csv', 'txt'],
        help="Upload your own customer feedback data"
    )
    
    if uploaded_file:
        dataset_name = st.text_input(
            "Dataset name (without extension):",
            value=f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        if st.button("Upload Dataset", type="primary"):
            if loader.upload_dataset(uploaded_file, dataset_name):
                st.success(f"Uploaded: {dataset_name}")
                st.rerun()
    
    # Show current dataset info
    if loader.current_dataset:
        info = loader.get_dataset_info()
        st.write("### Current Dataset Info:")
        st.json(info)

if __name__ == "__main__":
    main()
