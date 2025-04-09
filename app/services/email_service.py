import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import current_app, render_template
import logging

logger = logging.getLogger(__name__)

def send_email(subject, to_email, html_content):
    """Send an email using the configured SMTP settings."""
    try:
        # Get email configuration from app config
        email_host = current_app.config['EMAIL_HOST']
        email_port = current_app.config['EMAIL_PORT']
        email_user = current_app.config['EMAIL_USER']
        email_password = current_app.config['EMAIL_PASSWORD']
        email_from = current_app.config['EMAIL_FROM']
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = email_from
        msg['To'] = to_email
        
        # Add HTML content
        msg.attach(MIMEText(html_content, 'html'))
        
        # Connect to SMTP server and send email
        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)
            
        logger.info(f"Email sent to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

def send_reminder_email(due_contacts):
    """Send a reminder email with a list of contacts due for communication."""
    user_email = current_app.config['USER_EMAIL']
    subject = "Keep In Touch - Your Contact Reminders"
    
    # Sort contacts by due date (most overdue first)
    sorted_contacts = sorted(due_contacts, key=lambda c: c.days_until_due)
    
    # Prepare email content
    html_content = render_template(
        'emails/daily_reminder.html',
        contacts=sorted_contacts,
        today=datetime.utcnow().date()
    )
    
    return send_email(subject, user_email, html_content)

def send_test_email(to_email):
    """Send a test email to verify email configuration."""
    subject = "Keep In Touch - Test Email"
    html_content = """
    <html>
      <body>
        <h1>Test Email</h1>
        <p>This is a test email from your Keep In Touch application.</p>
        <p>If you've received this email, your email configuration is working correctly.</p>
      </body>
    </html>
    """
    
    return send_email(subject, to_email, html_content)