# AI ChatBot with LangChain Integration

A comprehensive AI-powered ChatBot application built with Django, LangChain, and modern web technologies. This application provides intelligent conversational AI with document search, vector embeddings, subscription billing, and enterprise-ready features.

![ChatBot Interface](https://github.com/user-attachments/assets/e6861acc-d3d6-4c06-ad2b-3651bd24d794)

## 🚀 Features

### Core AI Features
- **LangChain Integration**: Advanced AI agent capabilities with memory and context awareness
- **Vector Database**: Persistent vector storage with pgvector for document embeddings
- **Document Processing**: PDF upload, text extraction, and intelligent chunking
- **Contextual Responses**: AI responses based on uploaded documents and conversation history
- **Multiple AI Models**: Support for OpenAI GPT-3.5/4 and other LLM providers

### User Management & Authentication
- **Custom User Model**: Extended Django user model with profile management
- **JWT Authentication**: Secure token-based authentication
- **Social Login**: Integration with Google, Facebook, and other providers (via django-allauth)
- **User Profiles**: Comprehensive user profile management with preferences

### Subscription & Billing
- **Prepaid Wallet System**: Mobile phone-like prepaid balance model
- **Multiple Payment Gateways**: Razorpay integration with pluggable architecture
- **Subscription Plans**: Free tier, Basic, Premium, and Enterprise plans
- **Usage Tracking**: Detailed billing based on queries, tokens, and retrieval operations
- **Auto-Recharge**: Automatic balance top-up when threshold is reached

### Content Management
- **Hierarchical Organization**: Categories → Subjects → Chapters → Documents
- **Document Upload**: PDF and text document processing
- **Content Access Control**: Free and premium content segregation
- **Learning Paths**: Structured learning progression with prerequisites

### Chat Interface
- **ChatGPT-like UI**: Modern, responsive chat interface
- **Session Management**: Multiple conversation threads
- **Message History**: Persistent chat history with search
- **Real-time Typing**: Typing indicators and real-time updates
- **Context Memory**: AI remembers user preferences and conversation context

### Admin Features
- **Comprehensive Admin Panel**: Django admin with custom interfaces
- **Content Management**: Easy content creation and organization
- **User Management**: User profiles, wallets, and subscriptions
- **Analytics Dashboard**: Usage statistics and billing reports
- **System Configuration**: LLM settings, pricing, and feature toggles

### Technical Features
- **Scalable Architecture**: Microservices-ready with Docker support
- **Background Tasks**: Celery integration for document processing
- **Caching**: Redis integration for performance optimization
- **File Storage**: S3/MinIO support for document storage
- **API First**: RESTful API with comprehensive documentation
- **Mobile Responsive**: Works seamlessly on all devices

## 🛠 Tech Stack

### Backend
- **Python 3.11+**
- **Django 4.x** - Web framework
- **Django REST Framework** - API development
- **LangChain** - AI agent orchestration
- **PostgreSQL** - Primary database
- **pgvector** - Vector similarity search
- **Redis** - Caching and task queue
- **Celery** - Background task processing

### Frontend
- **Django Templates** - Server-side rendering
- **Bootstrap 5** - UI framework
- **JavaScript/jQuery** - Interactive features
- **React** (Optional) - For SPA components

### AI/ML Stack
- **OpenAI GPT-3.5/4** - Language models
- **Sentence Transformers** - Text embeddings
- **LangChain** - AI agent framework
- **tiktoken** - Token counting

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Local development
- **Nginx** - Reverse proxy and static files
- **Gunicorn** - WSGI server

### Integrations
- **Razorpay** - Payment processing
- **AWS S3** - File storage
- **Sentry** - Error monitoring
- **GitHub Actions** - CI/CD

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 14+ with pgvector extension
- Redis
- Docker (for containerized deployment)
- OpenAI API key
- Razorpay account (for payments)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/vb5672/vb5672.github.io.git
cd vb5672.github.io
```

### 2. Environment Setup

```bash
# Copy environment file
cp backend/.env.example backend/.env

# Edit the environment file with your settings
nano backend/.env
```

### 3. Docker Deployment (Recommended)

```bash
# Start all services
docker-compose up -d

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Create sample data
docker-compose exec web python manage.py create_sample_data
```

### 4. Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Configure database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create sample data
python manage.py create_sample_data

# Run development server
python manage.py runserver
```

## 🔧 Configuration

### Environment Variables

```bash
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,localhost

# Database
DB_NAME=chatbot_ai
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# AI/LangChain
OPENAI_API_KEY=your-openai-api-key
LANGCHAIN_TRACING_V2=False

# Payment Gateway
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret

# File Storage
USE_S3=True
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket

# Billing
FREE_TIER_DAYS=30
MIN_BALANCE_THRESHOLD=10.0
COST_PER_QUERY=0.01
```

### Database Setup with pgvector

```sql
-- Connect to PostgreSQL as superuser
CREATE EXTENSION IF NOT EXISTS vector;
```

## 📚 Usage

### Accessing the Application

- **Main Interface**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/

### Default Accounts

- **Admin**: admin@chatbot.ai / admin123
- **Demo User**: demo@chatbot.ai / demo123

### Admin Panel Features

1. **User Management**: Manage users, profiles, and wallets
2. **Content Management**: Create categories, subjects, and chapters
3. **Document Upload**: Upload and process PDF documents
4. **Subscription Management**: Manage user subscriptions and billing
5. **System Configuration**: Configure AI models, pricing, and features

### API Integration

The application provides a comprehensive REST API for integration:

```python
# Example API usage
import requests

# Authentication
response = requests.post('http://localhost:8000/api/v1/auth/login/', {
    'email': 'user@example.com',
    'password': 'password'
})
token = response.json()['access']

# Send chat message
response = requests.post('http://localhost:8000/api/v1/chat/send/', {
    'message': 'Tell me about artificial intelligence'
}, headers={'Authorization': f'Bearer {token}'})
```

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django API    │    │   AI Services   │
│   (React/JS)    │◄──►│   (DRF)         │◄──►│   (LangChain)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   Redis Cache   │    │   Vector DB     │
│   (Main DB)     │    │   (Sessions)    │    │   (pgvector)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Celery        │    │   File Storage  │    │   Payment       │
│   (Tasks)       │    │   (S3/MinIO)    │    │   (Razorpay)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📦 Deployment

### Production Deployment

1. **Environment Setup**
   - Set `DEBUG=False`
   - Configure secure `SECRET_KEY`
   - Set up SSL certificates
   - Configure production database

2. **Docker Production**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

4. **Database Migration**
   ```bash
   python manage.py migrate
   ```

### Scaling Considerations

- **Database**: Use read replicas for scaling reads
- **Redis**: Use Redis Cluster for high availability
- **File Storage**: Use CDN for static/media files
- **Load Balancing**: Use Nginx or cloud load balancers
- **Monitoring**: Set up Sentry for error tracking

## 🔒 Security

- CSRF protection enabled
- SQL injection prevention
- XSS protection
- Secure password hashing
- JWT token authentication
- Rate limiting (configurable)
- Input validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Full API documentation available at `/api/docs/`
- **Issues**: Report bugs and feature requests on GitHub
- **Community**: Join our Discord server for discussions

## 🚀 Roadmap

- [ ] Advanced AI agent capabilities
- [ ] Multi-language support
- [ ] Voice chat integration
- [ ] Mobile app (React Native)
- [ ] Enterprise SSO integration
- [ ] Advanced analytics dashboard
- [ ] Custom AI model training
- [ ] Marketplace for AI agents

---

Built with ❤️ by the AI ChatBot Team