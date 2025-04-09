# app/main.py
import logging
import os
from datetime import datetime

from flask import Flask

from app.models import init_db
from app.services.scheduler_service import init_scheduler


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Load default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE_URL=os.environ.get('DATABASE_URL', 'sqlite:///round_again.db'),
        EMAIL_HOST=os.environ.get('EMAIL_HOST', 'smtp.example.com'),
        EMAIL_PORT=int(os.environ.get('EMAIL_PORT', 587)),
        EMAIL_USER=os.environ.get('EMAIL_USER', 'user@example.com'),
        EMAIL_PASSWORD=os.environ.get('EMAIL_PASSWORD', 'password'),
        EMAIL_FROM=os.environ.get('EMAIL_FROM', 'noreply@roundagain.app'),
        USER_EMAIL=os.environ.get('USER_EMAIL', 'user@example.com'),
    )
    
    # Load test config if passed in
    if test_config is not None:
        app.config.from_mapping(test_config)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize database
    db_engine = init_db(app.config['DATABASE_URL'])
    app.db_engine = db_engine
    
    # Initialize scheduler
    scheduler = init_scheduler(app, db_engine)
    app.scheduler = scheduler
    
    # Register blueprints
    from app.routes import contacts, dashboard, interactions
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(contacts.bp)
    app.register_blueprint(interactions.bp)
    
    # Make url_for('index') == url_for('dashboard.index')
    app.add_url_rule('/', endpoint='index')

    
    # datetime filter
    @app.template_filter('datetime')
    def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
        """Format datetime for display."""
        if isinstance(value, datetime):
            return value.strftime(format)
        return value

    @app.template_filter('abs')
    def abs_filter(n):
        """Jinja filter to get absolute value"""
        return abs(n)
    
    # Add global template context
    @app.context_processor
    def utility_processor():
        return {
            'abs': abs,
            'now': datetime.now()  
        }

    return app