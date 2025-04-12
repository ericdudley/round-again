FROM python:3.13-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.7.1
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV DATABASE_URL="sqlite:////data/db.sqlite3"
ENV NODE_VERSION=20.x

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install NodeJS and npm
RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION} | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy package.json and install npm dependencies first
COPY package.json tailwind.config.js /app/
RUN npm install

# Copy CSS input file and build CSS
COPY app/static/css/input.css /app/app/static/css/
RUN npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/styles.css --minify

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry
RUN poetry config virtualenvs.create false
# Install dependencies (using updated flag instead of deprecated --no-dev)
RUN poetry install --no-interaction --no-ansi --only main

# Copy application code
COPY . /app/

# Create data directory for SQLite database
RUN mkdir -p /data
VOLUME /data

# Expose port
EXPOSE 5000

# Run the application
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "run:app"]