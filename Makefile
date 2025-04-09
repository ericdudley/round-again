# Makefile for Round Again application

.PHONY: help setup install update clean lint format test \
	run dev docker-build docker-up docker-down docker-logs \
	db-init db-migrate email-test

# Color codes
COLOR_RESET = \033[0m
COLOR_BOLD = \033[1m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m
COLOR_CYAN = \033[36m

# Default target
.DEFAULT_GOAL := help

# Variables
POETRY = poetry
FLASK = $(POETRY) run flask
PYTEST = $(POETRY) run pytest
BLACK = $(POETRY) run black
FLAKE8 = $(POETRY) run flake8
ISORT = $(POETRY) run isort
PYTHON = $(POETRY) run python

help: ## Show this help message
	@echo ""
	@echo "$(COLOR_BOLD)Round Again Application$(COLOR_RESET)"
	@echo "$(COLOR_BOLD)------------------------$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BOLD)Available commands:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_CYAN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""

# Setup commands
setup: ## Initialize project (install poetry and dependencies)
	@echo "$(COLOR_BOLD)Setting up the project...$(COLOR_RESET)"
	@pip install poetry
	@$(POETRY) install
	@cp -n .env.example .env || true
	@echo "$(COLOR_GREEN)Setup complete. Edit .env file with your configuration.$(COLOR_RESET)"

install: ## Install dependencies
	@echo "$(COLOR_BOLD)Installing dependencies...$(COLOR_RESET)"
	@$(POETRY) install
	@echo "$(COLOR_GREEN)Dependencies installed$(COLOR_RESET)"

update: ## Update dependencies
	@echo "$(COLOR_BOLD)Updating dependencies...$(COLOR_RESET)"
	@$(POETRY) update
	@echo "$(COLOR_GREEN)Dependencies updated$(COLOR_RESET)"

clean: ## Remove temporary files and cached data
	@echo "$(COLOR_BOLD)Cleaning project...$(COLOR_RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name "*.egg" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".coverage" -exec rm -rf {} +
	@find . -type d -name "htmlcov" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "$(COLOR_GREEN)Project cleaned$(COLOR_RESET)"

# Code quality commands
lint: ## Check code style with flake8
	@echo "$(COLOR_BOLD)Linting code...$(COLOR_RESET)"
	@$(FLAKE8) app tests
	@echo "$(COLOR_GREEN)Linting complete$(COLOR_RESET)"

format: ## Format code with black and isort
	@echo "$(COLOR_BOLD)Formatting code...$(COLOR_RESET)"
	@$(ISORT) app tests
	@$(BLACK) app tests
	@echo "$(COLOR_GREEN)Formatting complete$(COLOR_RESET)"

test: ## Run tests
	@echo "$(COLOR_BOLD)Running tests...$(COLOR_RESET)"
	@$(PYTEST) -v
	@echo "$(COLOR_GREEN)Tests complete$(COLOR_RESET)"

# Development commands
run: ## Run production server
	@echo "$(COLOR_BOLD)Starting production server...$(COLOR_RESET)"
	@$(POETRY) run gunicorn --bind 0.0.0.0:5000 run:app

dev: ## Run development server with hot reloading
	@echo "$(COLOR_BOLD)Starting development server...$(COLOR_RESET)"
	@FLASK_ENV=development $(FLASK) run --host=0.0.0.0 --port=5001 --debug

shell: ## Start a Python shell with application context
	@echo "$(COLOR_BOLD)Starting Python shell with app context...$(COLOR_RESET)"
	@$(FLASK) shell

# Docker commands
docker-build: ## Build the Docker image
	@echo "$(COLOR_BOLD)Building Docker image...$(COLOR_RESET)"
	@docker-compose build
	@echo "$(COLOR_GREEN)Docker image built$(COLOR_RESET)"

docker-up: ## Start the Docker containers
	@echo "$(COLOR_BOLD)Starting Docker containers...$(COLOR_RESET)"
	@docker-compose up -d
	@echo "$(COLOR_GREEN)Docker containers started$(COLOR_RESET)"

docker-down: ## Stop the Docker containers
	@echo "$(COLOR_BOLD)Stopping Docker containers...$(COLOR_RESET)"
	@docker-compose down
	@echo "$(COLOR_GREEN)Docker containers stopped$(COLOR_RESET)"

docker-logs: ## View the Docker container logs
	@echo "$(COLOR_BOLD)Viewing Docker logs...$(COLOR_RESET)"
	@docker-compose logs -f

docker-exec: ## Access the running container
	@echo "$(COLOR_BOLD)Accessing container shell...$(COLOR_RESET)"
	@docker-compose exec web /bin/bash

# Database commands
db-init: ## Initialize the database
	@echo "$(COLOR_BOLD)Initializing database...$(COLOR_RESET)"
	@$(PYTHON) -c "from app import create_app; from app.models import init_db; init_db(create_app().config['DATABASE_URL'])"
	@echo "$(COLOR_GREEN)Database initialized$(COLOR_RESET)"

db-setup: ## Setup database with migration and optional sample data
	@echo "$(COLOR_BOLD)Setting up database...$(COLOR_RESET)"
	@$(PYTHON) setup_database.py
	@echo "$(COLOR_GREEN)Database setup complete$(COLOR_RESET)"

db-setup-samples: ## Setup database with sample data
	@echo "$(COLOR_BOLD)Setting up database with sample data...$(COLOR_RESET)"
	@$(PYTHON) setup_database.py --samples
	@echo "$(COLOR_GREEN)Database setup with samples complete$(COLOR_RESET)"

db-backup: ## Backup the SQLite database
	@echo "$(COLOR_BOLD)Backing up database...$(COLOR_RESET)"
	@mkdir -p backups
	@cp data/round_again.db backups/round_again_$(shell date +%Y%m%d%H%M%S).db
	@echo "$(COLOR_GREEN)Database backed up to backups folder$(COLOR_RESET)"

# Application commands
email-test: ## Send a test email to verify email configuration
	@echo "$(COLOR_BOLD)Sending test email...$(COLOR_RESET)"
	@$(PYTHON) -c "from app import create_app; from app.services.email_service import send_test_email; with create_app().app_context(): send_test_email('$(shell grep USER_EMAIL .env | cut -d '=' -f2)')"
	@echo "$(COLOR_GREEN)Test email sent$(COLOR_RESET)"

scheduler-test: ## Run the scheduler once to test reminder generation
	@echo "$(COLOR_BOLD)Testing scheduler...$(COLOR_RESET)"
	@$(PYTHON) -c "from app import create_app; from app.services.scheduler import SchedulerService; from sqlalchemy.orm import sessionmaker; app = create_app(); session = sessionmaker(bind=app.db_engine)(); scheduler = SchedulerService(app, app.db_engine); with app.app_context(): scheduler.send_daily_reminders()"
	@echo "$(COLOR_GREEN)Scheduler test complete$(COLOR_RESET)"