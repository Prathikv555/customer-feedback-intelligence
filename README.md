# Customer Feedback Intelligence System

An AI-powered system for collecting, analyzing, and visualizing customer feedback from multiple sources.

## Features

- **Multi-source Data Collection**: Surveys, Emails, Social Media, Support Tickets
- **AI-Powered Analysis**: Sentiment analysis and automatic categorization
- **Real-time Dashboard**: Interactive visualizations and insights
- **Trend Analysis**: Identify emerging issues and patterns
- **Automated Reporting**: Generate insights automatically
- **🤖 AI Chatbot Assistant**: Ask natural language questions about your feedback data

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this repository to your local machine**

2. **Create and activate virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate sample data**:
   ```bash
   python generate_feedback_data.py
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

### For Office Deployment

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **On office laptop**:
   ```bash
   git clone <your-repo-url>
   cd customer-feedback-intelligence
   python -m venv venv
   venv\Scripts\activate  # or source venv/bin/activate on Mac/Linux
   pip install -r requirements.txt
   python generate_feedback_data.py
   python app.py
   ```

## Project Structure

```
customer-feedback-intelligence/
├── data/                          # Generated datasets
│   ├── surveys.csv
│   ├── emails.csv
│   ├── social_media.csv
│   └── support_tickets.csv
├── app.py                         # Main dashboard application
├── generate_feedback_data.py      # Data generation script
├── data_processor.py              # Data processing pipeline
├── ai_analyzer.py                 # AI analysis module
├── chatbot.py                    # 🤖 AI chatbot assistant
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── venv/                          # Virtual environment
```

## Usage

1. **Data Generation**: Run `generate_feedback_data.py` to create 6 months of sample data
2. **Dashboard**: Run `app.py` to launch the interactive dashboard
3. **Analysis**: The system automatically analyzes sentiment and categorizes feedback
4. **Insights**: View trends, patterns, and key issues in the dashboard
5. **🤖 AI Assistant**: Ask natural language questions about your data:
   - "What's the overall customer sentiment?"
   - "What are the top customer complaints?"
   - "How many bug reports did we get this month?"
   - "What features are customers requesting most?"
   - "How should we improve customer satisfaction?"

## Technology Stack

- **Data Processing**: Pandas, NumPy
- **AI/ML**: Scikit-learn, TextBlob
- **Visualization**: Plotly, Streamlit
- **Web Framework**: Streamlit
- **Data Generation**: Faker

## Sample Data

The system generates realistic sample data including:
- **500 survey responses** with ratings and comments
- **300 email communications** with various subjects and content
- **800 social media posts** from different platforms
- **200 support tickets** with issue descriptions and resolutions

All data spans 6 months with realistic temporal distribution and sentiment patterns.
