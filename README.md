# ColdGuard Backend

ColdGuard — IoT Temperature Monitoring System
Django Backend API

---

## Requirements

- Python 3.12+
- Redis
- Git

---

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/asaadaskar/Coldguard-Backend.git
cd Coldguard-Backend
```

### 2. Create Virtual Environment

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements-dev.txt
```

### 4. Environment Variables
```bash
cp .env.example .env
```
Edit `.env` with your values:

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Start Redis
**Mac:**
```bash
brew services start redis
```
**Windows:**
```bash
# Download Redis from https://redis.io/download
redis-server
```

### 7. Start Django Server
```bash
python manage.py runserver
```

### 8. Start Celery Worker
```bash
celery -A coldguard worker --loglevel=info
```

### 9. Start Celery Beat
```bash
celery -A coldguard beat --loglevel=info
```

---

## Documentation

```bash
cd docs
make html
open build/html/index.html
```

---

## Git Workflow

### Branches
Git:   KAN-{nummer}-{beschreibung}
PR:    KAN-{nummer}: {beschreibung}

### Commits
[KAN-{nummer}]: {message}

Example:
[KAN-36]: add GitHub Actions CI pipeline

### Install Git Hooks
```bash
./setup.sh
```

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/temperature/ | Receive temperature from ESP32 |

---

## Test API

```bash
curl -X POST http://127.0.0.1:8000/api/temperature/ \
  -H "Content-Type: application/json" \
  -H "X-Device-Key: coldguard-device-001" \
  -d '{"temperature": 9.5, "status": "ALARM_HIGH"}'
```

---

## Project Structure
Coldguard-Backend/
├── coldguard/          ← Django project
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
├── temperature/        ← Temperature app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── notifications.py
│   ├── constants.py
│   └── tasks.py
├── docs/               ← Sphinx documentation
├── .github/
│   └── workflows/
│       └── ci.yml      ← GitHub Actions
├── requirements.txt
├── requirements-dev.txt
└── manage.py

---

## Built With

- [Django](https://djangoproject.com) — Web Framework
- [Django REST Framework](https://django-rest-framework.org) — API
- [Celery](https://celeryproject.org) — Task Queue
- [Redis](https://redis.io) — Message Broker
- [Sphinx](https://sphinx-doc.org) — Documentation