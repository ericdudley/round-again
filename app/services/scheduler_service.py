from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import sessionmaker
from app.models import Contact, Interaction
from .email_service import send_reminder_email
import logging

logger = logging.getLogger(__name__)

class SchedulerService:
    def __init__(self, app, db_engine):
        self.app = app
        self.Session = sessionmaker(bind=db_engine)
        self.scheduler = BackgroundScheduler()
        
        # Add jobs
        self.scheduler.add_job(
            self.send_daily_reminders, 
            'cron', 
            hour=7, 
            minute=0,
            id='daily_reminders'
        )
    
    def start(self):
        """Start the scheduler."""
        self.scheduler.start()
        logger.info("Scheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler shut down")
    
    def send_daily_reminders(self):
        """Send daily reminder emails for contacts due soon."""
        logger.info("Running daily reminder job")
        
        with self.Session() as session:
            # Get all contacts
            contacts = session.query(Contact).all()
            
            # Filter for contacts due today or tomorrow
            due_contacts = []
            for contact in contacts:
                days_until_due = contact.days_until_due
                if -5 <= days_until_due <= 1:  # Include slightly overdue contacts
                    due_contacts.append(contact)
            
            if due_contacts:
                logger.info(f"Found {len(due_contacts)} contacts due for communication")
                # Send email with the list of contacts due
                with self.app.app_context():
                    send_reminder_email(due_contacts)
            else:
                logger.info("No contacts due for communication today")

def init_scheduler(app, db_engine):
    """Initialize and start the scheduler."""
    scheduler_service = SchedulerService(app, db_engine)
    scheduler_service.start()
    
    # Register shutdown handler
    @app.teardown_appcontext
    def shutdown_scheduler(exception=None):
        scheduler_service.shutdown()
    
    return scheduler_service