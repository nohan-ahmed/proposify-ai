# Proposify AI

**AI-Powered Professional Document Generation Platform**

Proposify AI is a sophisticated Django-based platform that leverages artificial intelligence to generate high-quality professional documents including business proposals, resumes, and cover letters. The platform integrates multiple AI providers and offers a credit-based system with subscription management.

## 🚀 Features

### Core Functionality
- **AI Document Generation**: Create professional proposals, resumes, and cover letters using advanced AI models
- **Multi-Provider AI Integration**: Support for OpenAI, HuggingFace, Gemini, and Anthropic models
- **User Profile Management**: Comprehensive user profiles with skills, experience, and education tracking
- **Credit-Based System**: Flexible credit system with subscription plans and payment processing
- **Asynchronous Processing**: Background job processing using Celery for scalable AI operations

### User Management
- **Custom User Authentication**: Extended Django user model with profile information
- **Social Authentication**: Google OAuth2 integration
- **Email Verification**: Secure account activation workflow
- **JWT Authentication**: Token-based API authentication

### Document Types
- **Business Proposals**: AI-generated proposals tailored to client requirements
- **Professional Resumes**: ATS-optimized resumes with quantified achievements
- **Cover Letters**: Compelling cover letters aligned with job opportunities

### Subscription & Billing
- **Flexible Plans**: Multiple subscription tiers with different credit allocations
- **Stripe Integration**: Secure payment processing
- **Usage Tracking**: Detailed billing logs and token consumption monitoring

## 🏗️ Architecture

### Technology Stack
- **Backend**: Django 5.2.7 with Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Task Queue**: Celery with Redis broker
- **Authentication**: JWT with django-allauth
- **API Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Payment Processing**: Stripe
- **AI Integration**: HuggingFace Hub, OpenAI, Gemini APIs

### Project Structure
```
proposify-ai/
├── core/                   # Core utilities and shared components
├── users/                  # User management and authentication
├── jobs/                   # Job processing and AI task management
├── credits/                # Credit system and plans
├── subsctiptions/          # Subscription and payment management
├── llm_models/             # AI model configuration and services
├── proposify_ai/           # Django project settings
└── staticfiles/            # Static assets
```

### Key Models
- **User**: Extended user model with profile information
- **Job**: Asynchronous task management for AI operations
- **Proposal**: Generated documents with metadata
- **UserCredit**: Credit balance and usage tracking
- **Plan**: Subscription plans and pricing
- **LLM**: AI model configuration and provider settings

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.13+
- Redis server
- Git

### 1. Clone Repository
```bash
git clone https://github.com/nohan-ahmed/proposify-ai.git
cd proposify-ai
```

### 2. Environment Setup
```bash
# Install dependencies and create virtual environment
uv sync

# Run commands with uv (automatically uses virtual environment)
uv run python manage.py --help
```

### 3. Environment Configuration
```bash
# Copy environment template
cp .example.env .env

# Edit .env with your configuration
nano .env
```

### 4. Required Environment Variables
```env
# Django Configuration
DJANGO_SECRET_KEY='your_django_secret_key_here'
DJANGO_DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0
FRONTEND_URL='http://127.0.0.1:8000'

# Redis Configuration
REDIS_HOST='127.0.0.1'
REDIS_PORT=6379
CELERY_BROKER_URL='redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/0'

# Email Configuration (SMTP)
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER="your_email@gmail.com"
EMAIL_HOST_PASSWORD="your_app_password"

# Payment Processing (Stripe)
STRIPE_SECRET_KEY="your_stripe_secret_key"
STRIPE_WEBHOOK_SECRET="your_stripe_webhook_secret"
STRIPE_SUCCESS_URL='http://127.0.0.1:8000/success/'
STRIPE_CANCEL_URL='http://127.0.0.1:8000/cancel/'

# AI Provider API Keys
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_TOKEN="your_huggingface_token_here"
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Database Setup
```bash
# Run migrations
uv run manage.py migrate

# Create superuser
uv run manage.py createsuperuser

# Collect static files
uv run manage.py collectstatic
```

### 6. Start Services
```bash
# Terminal 1: Start Redis server
redis-server

# Terminal 2: Start Celery worker
uv run celery -A proposify_ai worker --loglevel=info

# Terminal 3: Start Django development server
uv run manage.py runserver
# Terminal 4: Start Uvicorn for ASGI
uv run uvicorn proposify_ai.asgi:application --reload
```

## 📚 API Documentation

### Access Points
- **Swagger UI**: `http://127.0.0.1:8000/api/docs/`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc/`
- **OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/`

### Key Endpoints

#### Authentication
```
POST /api/users/register/          # User registration
GET  /api/users/verify/{uid}/{token}/  # Email verification
POST /auth/login/                  # JWT login
POST /auth/logout/                 # Logout
POST /auth/google/                 # Google OAuth2
```

#### User Management
```
GET    /api/users/skills/          # User skills CRUD
POST   /api/users/skills/
GET    /api/users/experiences/     # User experience CRUD
POST   /api/users/experiences/
GET    /api/users/educations/      # User education CRUD
POST   /api/users/educations/
```

#### Document Generation
```
GET    /api/jobs/proposals/        # List user proposals
POST   /api/jobs/proposals/        # Create new proposal
GET    /api/jobs/jobs/             # List user jobs
GET    /api/jobs/billing/          # Billing history
```

#### Credits & Subscriptions
```
GET    /api/credits/plans/         # Available plans
POST   /api/subscriptions/         # Create subscription
GET    /api/subscriptions/         # User subscriptions
```

### Authentication
All protected endpoints require JWT authentication:
```bash
# Include in request headers
Authorization: Bearer <your_jwt_token>
```

## 🔧 Configuration

### AI Model Configuration
Configure AI models through Django admin or programmatically:

```python
from llm_models.models import LLM

# Add HuggingFace model
LLM.objects.create(
    name="Llama 3.2 3B",
    provider="huggingface",
    provider_model="meta-llama/Llama-3.2-3B-Instruct",
    tokens_per_request=4000,
    max_tokens=8192,
    active=True
)
```

### Credit Plans
Create subscription plans:

```python
from credits.models import Plan

Plan.objects.create(
    name="Starter Plan",
    regular_price=9.99,
    discount_price=7.99,
    credits=100,
    description="Perfect for individuals"
)
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
uv run python manage.py test

# Run specific app tests
uv run python manage.py test users
uv run python manage.py test jobs
```

### API Testing
Use the built-in API documentation at `/api/docs/` for interactive testing, or use tools like Postman with the provided OpenAPI schema.

## 🚀 Deployment

### Production Considerations
1. **Database**: Switch to PostgreSQL for production
2. **Static Files**: Configure AWS S3 or similar for static/media files
3. **Environment**: Set `DJANGO_DEBUG=False`
4. **Security**: Update `ALLOWED_HOSTS` and configure HTTPS
5. **Scaling**: Use Gunicorn/uWSGI with nginx
6. **Monitoring**: Implement logging and error tracking

### Docker Deployment (Optional)
```dockerfile
# Example Dockerfile structure
FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen
COPY . .
CMD ["gunicorn", "proposify_ai.wsgi:application"]
```

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Ensure all tests pass: `uv run python manage.py test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Write tests for new functionality
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues
- **Redis Connection**: Ensure Redis server is running on the configured port
- **AI API Errors**: Verify API keys are correctly set in environment variables
- **Email Issues**: Check SMTP configuration and app passwords for Gmail

### Getting Help
- Check the [API documentation](http://127.0.0.1:8000/api/docs/) for endpoint details
- Review Django logs for error details
- Ensure all environment variables are properly configured

## 🔮 Roadmap

- [ ] Additional AI provider integrations (Claude, Cohere)
- [ ] Real-time document collaboration
- [ ] Advanced template customization
- [ ] Multi-language support expansion
- [ ] Mobile application development
- [ ] Enterprise features and SSO integration

---

**Built with ❤️ using Django and AI**