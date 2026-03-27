import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import csv

fake = Faker()

# Define realistic feedback templates
SURVEY_TEMPLATES = [
    "The product is great but {aspect} could be improved.",
    "I'm {sentiment_word} with the {feature}. {comment}",
    "Overall rating {rating}/10. {comment}",
    "The {aspect} is {adjective}, but {issue}.",
    "Would recommend to others because {reason}. {suggestion}"
]

EMAIL_TEMPLATES = [
    "Subject: Issue with {feature}\n\nHi,\n\nI'm experiencing {problem} when using {product}. {details}\n\nThanks,\n{customer_name}",
    "Subject: Feature Request - {feature}\n\nHello,\n\nI would love to see {suggestion} implemented. {reason}\n\nBest regards,\n{customer_name}",
    "Subject: Complaint about {aspect}\n\nTo whom it may concern,\n\nI'm {sentiment_word} about {issue}. {details}\n\nSincerely,\n{customer_name}"
]

SOCIAL_MEDIA_TEMPLATES = [
    "Just tried {product} and I'm {sentiment_word}! {comment} #{hashtag}",
    "{product} is {adjective} but {issue}. #{hashtag}",
    "Customer service was {adjective}! {comment} #{hashtag}",
    "Love the new {feature}! {suggestion} #{hashtag}",
    "Having issues with {aspect}. {problem} #{hashtag}"
]

SUPPORT_TICKET_TEMPLATES = [
    "Issue Description: {problem} with {feature}\n\nSteps to reproduce: {steps}\n\nExpected behavior: {expected}\n\nActual behavior: {actual}",
    "Customer reports {issue} when using {product}. {details}\n\nTroubleshooting steps taken: {troubleshooting}",
    "Urgent: {problem} affecting {aspect}. {impact}\n\nCustomer needs resolution by {deadline}."
]

# Define categories and aspects
CATEGORIES = ['Feature Request', 'Bug Report', 'Usability', 'Performance', 'Pricing', 'Support', 'Documentation', 'Integration']
ASPECTS = ['user interface', 'performance', 'features', 'pricing', 'customer support', 'documentation', 'integration', 'reliability']
FEATURES = ['dashboard', 'reporting', 'analytics', 'export functionality', 'mobile app', 'API', 'search', 'notifications']
PRODUCTS = ['Pro Plan', 'Basic Plan', 'Enterprise Solution', 'Mobile App', 'Web Platform', 'API Service']

def generate_feedback_text(template, sentiment='neutral'):
    """Generate realistic feedback text using templates"""
    replacements = {
        'aspect': random.choice(ASPECTS),
        'feature': random.choice(FEATURES),
        'product': random.choice(PRODUCTS),
        'sentiment_word': 'very satisfied' if sentiment == 'positive' else 'frustrated' if sentiment == 'negative' else 'neutral',
        'adjective': random.choice(['excellent', 'good', 'okay', 'poor', 'terrible']),
        'rating': random.randint(1, 10),
        'comment': fake.sentence(),
        'issue': fake.sentence(),
        'suggestion': fake.sentence(),
        'reason': fake.sentence(),
        'customer_name': fake.name(),
        'problem': fake.sentence(),
        'details': fake.paragraph(),
        'hashtag': random.choice(['CustomerExperience', 'ProductFeedback', 'TechSupport', 'UserExperience']),
        'steps': '\n'.join([f"Step {i+1}: {fake.sentence()}" for i in range(3)]),
        'expected': fake.sentence(),
        'actual': fake.sentence(),
        'troubleshooting': '\n'.join([f"- {fake.sentence()}" for i in range(2)]),
        'impact': fake.sentence(),
        'deadline': fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d')
    }
    
    text = template
    for key, value in replacements.items():
        text = text.replace(f'{{{key}}}', str(value))
    
    return text

def determine_sentiment():
    """Determine sentiment with weighted distribution"""
    weights = [0.6, 0.25, 0.15]  # positive, neutral, negative
    return random.choices(['positive', 'neutral', 'negative'], weights=weights)[0]

def generate_date_range(months=6):
    """Generate dates for the last 6 months"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months*30)
    
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=random.randint(1, 3))
    
    return dates

def generate_surveys_data(num_records=500):
    """Generate survey feedback data"""
    dates = generate_date_range()
    data = []
    
    for i in range(num_records):
        date = random.choice(dates)
        sentiment = determine_sentiment()
        
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'customer_id': f"cust_{random.randint(1000, 9999)}",
            'product_id': random.choice(PRODUCTS),
            'rating': random.randint(1, 10),
            'feedback_text': generate_feedback_text(random.choice(SURVEY_TEMPLATES), sentiment),
            'sentiment': sentiment,
            'category': random.choice(CATEGORIES)
        }
        data.append(record)
    
    return pd.DataFrame(data)

def generate_emails_data(num_records=300):
    """Generate email feedback data"""
    dates = generate_date_range()
    data = []
    
    for i in range(num_records):
        date = random.choice(dates)
        sentiment = determine_sentiment()
        
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'customer_id': f"cust_{random.randint(1000, 9999)}",
            'subject': f"{'Urgent: ' if sentiment == 'negative' else ''}{random.choice(['Issue', 'Question', 'Feedback', 'Request'])} regarding {random.choice(FEATURES)}",
            'body': generate_feedback_text(random.choice(EMAIL_TEMPLATES), sentiment),
            'sentiment': sentiment,
            'category': random.choice(CATEGORIES)
        }
        data.append(record)
    
    return pd.DataFrame(data)

def generate_social_media_data(num_records=800):
    """Generate social media feedback data"""
    dates = generate_date_range()
    platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn']
    data = []
    
    for i in range(num_records):
        date = random.choice(dates)
        sentiment = determine_sentiment()
        
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'customer_id': f"cust_{random.randint(1000, 9999)}" if random.random() > 0.3 else 'anonymous',
            'platform': random.choice(platforms),
            'post_content': generate_feedback_text(random.choice(SOCIAL_MEDIA_TEMPLATES), sentiment),
            'sentiment': sentiment,
            'category': random.choice(CATEGORIES)
        }
        data.append(record)
    
    return pd.DataFrame(data)

def generate_support_tickets_data(num_records=200):
    """Generate support ticket data"""
    dates = generate_date_range()
    statuses = ['Open', 'Closed', 'In Progress', 'Pending Customer Response']
    data = []
    
    for i in range(num_records):
        date = random.choice(dates)
        sentiment = determine_sentiment()
        
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'customer_id': f"cust_{random.randint(1000, 9999)}",
            'ticket_id': f"TKT-{random.randint(10000, 99999)}",
            'issue_description': generate_feedback_text(random.choice(SUPPORT_TICKET_TEMPLATES), sentiment),
            'resolution_status': random.choice(statuses),
            'sentiment': sentiment,
            'category': random.choice(CATEGORIES)
        }
        data.append(record)
    
    return pd.DataFrame(data)

def main():
    """Main function to generate all datasets"""
    print("Generating 6 months of customer feedback data...")
    
    # Create data directory
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Generate datasets
    surveys_df = generate_surveys_data(500)
    emails_df = generate_emails_data(300)
    social_media_df = generate_social_media_data(800)
    support_tickets_df = generate_support_tickets_data(200)
    
    # Save to CSV files
    surveys_df.to_csv('data/surveys.csv', index=False)
    emails_df.to_csv('data/emails.csv', index=False)
    social_media_df.to_csv('data/social_media.csv', index=False)
    support_tickets_df.to_csv('data/support_tickets.csv', index=False)
    
    # Generate summary statistics
    print("\nDataset Summary:")
    print(f"Surveys: {len(surveys_df)} records")
    print(f"Emails: {len(emails_df)} records")
    print(f"Social Media: {len(social_media_df)} records")
    print(f"Support Tickets: {len(support_tickets_df)} records")
    print(f"Total records: {len(surveys_df) + len(emails_df) + len(social_media_df) + len(support_tickets_df)}")
    
    # Show sample data
    print("\nSample survey data:")
    print(surveys_df.head(2).to_string())
    
    print("\nData generation completed successfully!")

if __name__ == "__main__":
    main()
