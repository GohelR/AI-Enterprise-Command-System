"""Customer Support & CX Service - Chatbot, Sentiment Analysis, Ticket Classification"""

from typing import Dict, List, Any
from backend.app.ml.base import MLModelBase


class SentimentAnalyzer(MLModelBase):
    """Sentiment analysis for customer messages"""
    
    def __init__(self):
        super().__init__("sentiment_analyzer", "1.0.0")
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        text_lower = text.lower()
        
        # Positive words
        positive_words = ['great', 'excellent', 'amazing', 'thank', 'happy', 'satisfied', 'good', 'love', 'wonderful']
        # Negative words
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'angry', 'frustrated', 'disappointed', 'worst', 'horrible']
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = "positive"
            score = 0.6 + (min(pos_count, 5) * 0.08)
        elif neg_count > pos_count:
            sentiment = "negative"
            score = 0.4 - (min(neg_count, 5) * 0.08)
        else:
            sentiment = "neutral"
            score = 0.5
        
        return {
            'sentiment': sentiment,
            'score': round(score, 2),
            'confidence': 'high' if abs(pos_count - neg_count) >= 2 else 'medium'
        }


class TicketClassifier:
    """Classify support tickets"""
    
    CATEGORIES = {
        'technical': ['error', 'bug', 'crash', 'not working', 'broken', 'issue', 'problem'],
        'billing': ['invoice', 'payment', 'charge', 'refund', 'billing', 'subscription'],
        'account': ['login', 'password', 'account', 'access', 'authentication'],
        'feature_request': ['feature', 'request', 'add', 'enhancement', 'improve'],
        'general': []
    }
    
    @classmethod
    def classify(cls, subject: str, description: str) -> str:
        """Classify ticket into category"""
        text = (subject + " " + description).lower()
        
        for category, keywords in cls.CATEGORIES.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'general'
    
    @classmethod
    def determine_priority(cls, category: str, sentiment_score: float) -> str:
        """Determine ticket priority"""
        # High priority for negative sentiment and certain categories
        if sentiment_score < 0.3:
            return 'critical'
        elif sentiment_score < 0.5 and category in ['technical', 'billing']:
            return 'high'
        elif category == 'technical':
            return 'medium'
        else:
            return 'low'


class AIchatbot:
    """Simple rule-based chatbot"""
    
    RESPONSES = {
        'greeting': "Hello! How can I help you today?",
        'billing': "For billing questions, please provide your account number and I'll assist you.",
        'technical': "I can help with technical issues. Please describe the problem you're experiencing.",
        'goodbye': "Thank you for contacting us. Have a great day!",
        'default': "I understand your concern. Let me connect you with the right team member."
    }
    
    @classmethod
    def get_response(cls, message: str) -> str:
        """Get chatbot response"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return cls.RESPONSES['greeting']
        elif any(word in message_lower for word in ['billing', 'invoice', 'payment']):
            return cls.RESPONSES['billing']
        elif any(word in message_lower for word in ['error', 'bug', 'not working']):
            return cls.RESPONSES['technical']
        elif any(word in message_lower for word in ['bye', 'goodbye', 'thanks']):
            return cls.RESPONSES['goodbye']
        else:
            return cls.RESPONSES['default']


def analyze_support_ticket(subject: str, description: str, customer_email: str) -> Dict[str, Any]:
    """Analyze support ticket"""
    # Sentiment analysis
    sentiment_analyzer = SentimentAnalyzer()
    sentiment_result = sentiment_analyzer.analyze_sentiment(subject + " " + description)
    
    # Classify ticket
    category = TicketClassifier.classify(subject, description)
    priority = TicketClassifier.determine_priority(category, sentiment_result['score'])
    
    return {
        'category': category,
        'priority': priority,
        'sentiment': sentiment_result['sentiment'],
        'sentiment_score': sentiment_result['score']
    }


def process_chatbot_message(message: str) -> Dict[str, str]:
    """Process chatbot message"""
    response = AIchatbot.get_response(message)
    return {
        'user_message': message,
        'bot_response': response
    }
