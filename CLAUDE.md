# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Run Commands
- Install dependencies: `make setup` or `poetry install`
- Run development server: `make dev` or `poetry run flask run --debug`
- Run production server: `make run` or `poetry run gunicorn run:app`
- Run tests: `make test` or `poetry run pytest -v`
- Run single test: `poetry run pytest tests/path_to_test.py::test_name -v`
- Format code: `make format` or `poetry run black app tests`
- Lint code: `make lint` or `poetry run flake8 app tests`

## Code Style Guidelines
- **Formatting**: Black with 88-character line length
- **Linting**: Flake8 for code quality checks
- **Imports**: Group standard library, then third-party, then local imports
- **Typing**: Use Python type hints for function parameters and return values
- **Naming**: Use snake_case for variables/functions, PascalCase for classes, UPPER_CASE for constants
- **Error Handling**: Use specific exceptions, handle errors gracefully with proper logging
- **Documentation**: Use docstrings for classes and functions
- **Database**: SQLAlchemy ORM with declarative models
- **Routes**: Organized into Flask blueprints
- **Environment Variables**: Use python-dotenv and .env file (never commit real secrets)