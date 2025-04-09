# Setting Up the Round Again Application with Poetry

## 1. Install Poetry

If you don't have Poetry installed, install it first:

### For macOS / Linux / WSL:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### For Windows PowerShell:
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

## 3. Initialize Poetry

Initialize a new Poetry project:
```bash
poetry init
```

Follow the interactive prompts:
- Package name: `keep-in-touch`
- Version: `0.1.0`
- Description: `A simple contact management system with reminders`
- Author: Your name
- License: `MIT`
- Python version: `^3.10`
- Define dependencies interactively: `no` (we'll add them manually)

## 4. Add Dependencies

Add the required dependencies:
```bash
poetry add flask sqlalchemy apscheduler htmx-flask flask-wtf gunicorn python-dotenv jinja2 email-validator
```

Add development dependencies:
```bash
poetry add --group dev pytest pytest-flask black flake8
```

## 5. Project Setup

Create the basic directory structure:
```bash
mkdir -p app/routes app/services app/templates/emails app/static/{css,js} migrations tests
```

## 6. Create a pyproject.toml File

The Poetry initialization will have created a pyproject.toml file, but you may want to manually edit it to ensure it has the right configuration:

```toml
[tool.poetry]
name = "keep-in-touch"
version = "0.1.0"
description = "A simple contact management system with reminders"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10"
flask = "^2.3.3"
sqlalchemy = "^2.0.20"
apscheduler = "^3.10.4"
htmx-flask = "^0.1.0"
flask-wtf = "^1.1.1"
gunicorn = "^21.2.0"
python-dotenv = "^1.0.0"
jinja2 = "^3.1.2"
email-validator = "^2.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-flask = "^1.2.0"
black = "^23.7.0"
flake8 = "^6.1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 7. Create a Docker Compose File for Poetry

Replace the previous docker-compose.yml with a Poetry-compatible version:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./app:/app/app
      - ./data:/data
    environment:
      - FLASK_APP=run.py
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:////data/round_again.db
      - EMAIL_HOST=${EMAIL_HOST}
      - EMAIL_PORT=${EMAIL_PORT}
      - EMAIL_USER=${EMAIL_USER}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
      - EMAIL_FROM=${EMAIL_FROM}
      - USER_EMAIL=${USER_EMAIL}
    restart: unless-stopped
    command: poetry run gunicorn --bind 0.0.0.0:5000 run:app
```

## 8. Create a Poetry-compatible Dockerfile

```dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.6.1
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-dev

# Copy application code
COPY . /app/

# Create data directory for SQLite database
RUN mkdir -p /data
VOLUME /data

# Expose port
EXPOSE 5000

# Run the application
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

## 9. Create .env File Template

Create a `.env.example` file:

```
# Flask configuration
SECRET_KEY=your_secret_key_here
FLASK_APP=run.py
FLASK_ENV=development

# Database configuration
DATABASE_URL=sqlite:///data/round_again.db

# Email configuration
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=your_email@example.com
EMAIL_PASSWORD=your_email_password
EMAIL_FROM=noreply@keepintouch.app

# User configuration
USER_EMAIL=your_email@example.com
```

Copy this to a `.env` file and fill in your actual values:
```bash
cp .env.example .env
# Edit .env with your actual values
```

## 10. Create an Entry Point

Create a `run.py` file at the project root:

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

## 11. Development Workflow

### Start a development server:
```bash
poetry run flask run
```

### Run in a Poetry shell:
```bash
poetry shell
flask run
```

### Run tests:
```bash
poetry run pytest
```

### Format code:
```bash
poetry run black app tests
```

## 12. Docker Deployment

Build and start with Docker Compose:
```bash
docker-compose build
docker-compose up -d
```

Check logs:
```bash
docker-compose logs -f
```

Stop containers:
```bash
docker-compose down
```