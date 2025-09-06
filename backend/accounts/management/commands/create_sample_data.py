"""
Management command to create sample data for the AI ChatBot application.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import UserProfile, Wallet, Subscription
from content.models import Category, Subject, Chapter
from chat.models import ChatSession, Message
from datetime import datetime, timedelta
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for the AI ChatBot application'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample categories
        tech_category = Category.objects.get_or_create(
            name='Technology',
            defaults={
                'slug': 'technology',
                'description': 'Programming, AI, and technology topics',
                'icon': 'fas fa-laptop-code',
                'color': '#007bff',
                'order': 1
            }
        )[0]
        
        business_category = Category.objects.get_or_create(
            name='Business',
            defaults={
                'slug': 'business',
                'description': 'Business, entrepreneurship, and management',
                'icon': 'fas fa-briefcase',
                'color': '#28a745',
                'order': 2
            }
        )[0]
        
        # Create sample subjects
        python_subject = Subject.objects.get_or_create(
            category=tech_category,
            name='Python Programming',
            defaults={
                'slug': 'python-programming',
                'description': 'Learn Python programming from basics to advanced',
                'difficulty_level': 'BEGINNER',
                'estimated_hours': 40,
                'order': 1
            }
        )[0]
        
        ai_subject = Subject.objects.get_or_create(
            category=tech_category,
            name='Artificial Intelligence',
            defaults={
                'slug': 'artificial-intelligence',
                'description': 'Machine Learning, Deep Learning, and AI concepts',
                'difficulty_level': 'INTERMEDIATE',
                'estimated_hours': 60,
                'order': 2
            }
        )[0]
        
        # Create sample chapters
        Chapter.objects.get_or_create(
            subject=python_subject,
            title='Python Basics',
            defaults={
                'slug': 'python-basics',
                'description': 'Variables, data types, and basic operations',
                'content': 'This chapter covers the fundamentals of Python programming...',
                'is_free': True,
                'estimated_minutes': 45,
                'order': 1
            }
        )
        
        Chapter.objects.get_or_create(
            subject=python_subject,
            title='Object-Oriented Programming',
            defaults={
                'slug': 'oop',
                'description': 'Classes, objects, inheritance, and polymorphism',
                'content': 'Learn about object-oriented programming concepts in Python...',
                'is_free': False,
                'estimated_minutes': 60,
                'order': 2
            }
        )
        
        Chapter.objects.get_or_create(
            subject=ai_subject,
            title='Introduction to Machine Learning',
            defaults={
                'slug': 'intro-ml',
                'description': 'Fundamentals of machine learning algorithms',
                'content': 'Machine learning is a subset of artificial intelligence...',
                'is_free': True,
                'estimated_minutes': 50,
                'order': 1
            }
        )
        
        # Create sample users with profiles and wallets
        demo_user = User.objects.get_or_create(
            email='demo@chatbot.ai',
            defaults={
                'username': 'demo_user',
                'first_name': 'Demo',
                'last_name': 'User',
                'is_verified': True
            }
        )[0]
        
        # Set password for demo user
        demo_user.set_password('demo123')
        demo_user.save()
        
        # Create user profile
        UserProfile.objects.get_or_create(
            user=demo_user,
            defaults={
                'bio': 'Demo user for testing the AI ChatBot application',
                'company': 'ChatBot Inc.',
                'location': 'San Francisco, CA'
            }
        )
        
        # Create wallet with some balance
        wallet = Wallet.objects.get_or_create(
            user=demo_user,
            defaults={
                'balance': Decimal('25.00'),
                'low_balance_threshold': Decimal('5.00')
            }
        )[0]
        
        # Create sample subscription
        Subscription.objects.get_or_create(
            user=demo_user,
            plan_type='BASIC',
            defaults={
                'monthly_cost': Decimal('9.99'),
                'query_limit': 1000,
                'token_limit': 100000,
                'start_date': datetime.now(),
                'end_date': datetime.now() + timedelta(days=30),
                'status': 'ACTIVE'
            }
        )
        
        # Create sample chat session
        chat_session = ChatSession.objects.get_or_create(
            user=demo_user,
            title='Getting Started with AI',
            defaults={
                'description': 'Learning about AI and ChatBot features',
                'subject': ai_subject,
                'is_active': True
            }
        )[0]
        
        # Create sample messages
        Message.objects.get_or_create(
            session=chat_session,
            message_type='USER',
            content='Hello! Can you tell me about artificial intelligence?',
            defaults={
                'token_count': 12,
                'character_count': 52
            }
        )
        
        Message.objects.get_or_create(
            session=chat_session,
            message_type='ASSISTANT',
            content='Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines that can perform tasks that typically require human intelligence. This includes learning, reasoning, problem-solving, perception, and language understanding.',
            defaults={
                'token_count': 45,
                'character_count': 280,
                'model_used': 'gpt-3.5-turbo',
                'response_time': 1.2,
                'cost': Decimal('0.001')
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write(f'Demo user: demo@chatbot.ai / password: demo123')
        self.stdout.write(f'Admin user: admin@chatbot.ai / password: admin123')