"""Sample data generators for testing and demonstration"""

import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()


def generate_resumes(n=10):
    """Generate sample resume data"""
    skills_pool = [
        'Python', 'Java', 'JavaScript', 'SQL', 'AWS', 'Azure', 'Docker',
        'Machine Learning', 'Data Science', 'React', 'Node.js', 'Django'
    ]
    
    resumes = []
    for _ in range(n):
        resume = {
            'candidate_name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'resume_text': f"""
            Experienced software engineer with {random.randint(2, 10)} years of experience.
            Skills: {', '.join(random.sample(skills_pool, random.randint(3, 7)))}
            Education: {random.choice(['Bachelor', 'Master', 'PhD'])} in Computer Science
            Previous companies: {fake.company()}, {fake.company()}
            """,
            'experience_years': random.uniform(1, 15),
            'education': random.choice(['Bachelor', 'Master', 'PhD'])
        }
        resumes.append(resume)
    
    return resumes


def generate_transactions(n=50):
    """Generate sample financial transactions"""
    transactions = []
    categories = ['salary', 'marketing', 'operations', 'technology', 'travel']
    
    for _ in range(n):
        transaction = {
            'transaction_type': random.choice(['income', 'expense']),
            'amount': random.uniform(100, 50000),
            'description': fake.sentence(),
            'date': (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
            'category': random.choice(categories)
        }
        transactions.append(transaction)
    
    return transactions


def generate_support_tickets(n=20):
    """Generate sample support tickets"""
    tickets = []
    categories = ['technical', 'billing', 'account', 'feature_request', 'general']
    priorities = ['low', 'medium', 'high', 'critical']
    
    for _ in range(n):
        ticket = {
            'customer_email': fake.email(),
            'subject': fake.sentence(),
            'description': fake.paragraph(),
            'category': random.choice(categories),
            'priority': random.choice(priorities),
            'status': random.choice(['open', 'in_progress', 'resolved', 'closed'])
        }
        tickets.append(ticket)
    
    return tickets


def generate_leads(n=30):
    """Generate sample leads"""
    leads = []
    sources = ['referral', 'organic', 'paid', 'social', 'other']
    
    for _ in range(n):
        lead = {
            'name': fake.name(),
            'email': fake.email(),
            'company': fake.company(),
            'source': random.choice(sources),
            'engagement_level': random.randint(1, 10)
        }
        leads.append(lead)
    
    return leads


def generate_customers(n=25):
    """Generate sample customers"""
    customers = []
    industries = ['Technology', 'Finance', 'Healthcare', 'Retail', 'Manufacturing']
    
    for _ in range(n):
        customer = {
            'name': fake.name(),
            'email': fake.email(),
            'company': fake.company(),
            'industry': random.choice(industries),
            'days_since_last_activity': random.randint(1, 180),
            'support_tickets': random.randint(0, 10),
            'engagement_score': random.randint(20, 100),
            'payment_failures': random.randint(0, 3),
            'avg_purchase_value': random.uniform(1000, 50000),
            'purchase_frequency': random.uniform(1, 12),
            'customer_lifespan_months': random.randint(6, 60)
        }
        customers.append(customer)
    
    return customers


if __name__ == '__main__':
    # Generate and save sample data
    import os
    
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate datasets
    datasets = {
        'resumes.json': generate_resumes(10),
        'transactions.json': generate_transactions(50),
        'support_tickets.json': generate_support_tickets(20),
        'leads.json': generate_leads(30),
        'customers.json': generate_customers(25)
    }
    
    # Save to files
    for filename, data in datasets.items():
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Generated {filename} with {len(data)} records")
    
    print("\nSample data generation complete!")
