#!/usr/bin/env python3
# Script to add sample data to Round Again database

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Contact, Interaction, FrequencyUnit, InteractionType

def add_sample_data():
    """Add sample data to the database"""
    print("Adding sample data to database...")
    
    # Connect to database
    engine = create_engine('sqlite:///round_again.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Create sample contacts
        contacts = [
            Contact(
                name="John Smith",
                email="john.smith@example.com",
                phone="555-123-4567",
                frequency_value=2,
                frequency_unit=FrequencyUnit.WEEK,
                notes="College friend from computer science"
            ),
            Contact(
                name="Emily Johnson",
                email="emily.j@example.com",
                phone="555-987-6543",
                frequency_value=1,
                frequency_unit=FrequencyUnit.MONTH,
                notes="Former colleague from ABC Corp"
            ),
            Contact(
                name="Michael Chen",
                email="mchen@example.com",
                phone="555-555-1212",
                frequency_value=3,
                frequency_unit=FrequencyUnit.MONTH,
                notes="Met at industry conference"
            ),
            Contact(
                name="Sarah Williams",
                email="swilliams@example.com",
                phone="555-789-0123",
                frequency_value=6,
                frequency_unit=FrequencyUnit.MONTH,
                notes="Mentor from graduate school"
            ),
            Contact(
                name="David Rodriguez",
                email="drodriguez@example.com",
                phone="555-246-8101",
                frequency_value=1,
                frequency_unit=FrequencyUnit.WEEK,
                notes="Close friend from hometown"
            )
        ]
        
        # Add contacts to database
        for contact in contacts:
            session.add(contact)
        
        # Flush to get contact IDs
        session.flush()
        
        # Create interactions for contacts
        now = datetime.utcnow()
        
        # John Smith interactions (one overdue)
        session.add(Interaction(
            contact_id=contacts[0].id,
            interaction_type=InteractionType.CALL,
            interaction_date=now - timedelta(days=20),
            notes="Caught up about new job"
        ))
        
        # Emily Johnson interactions (due soon)
        session.add(Interaction(
            contact_id=contacts[1].id,
            interaction_type=InteractionType.VIDEO,
            interaction_date=now - timedelta(days=25),
            notes="Virtual coffee chat"
        ))
        
        # Michael Chen interactions (recent)
        session.add(Interaction(
            contact_id=contacts[2].id,
            interaction_type=InteractionType.EMAIL,
            interaction_date=now - timedelta(days=5),
            notes="Sent article about industry trends"
        ))
        session.add(Interaction(
            contact_id=contacts[2].id,
            interaction_type=InteractionType.CALL,
            interaction_date=now - timedelta(days=90),
            notes="Birthday call"
        ))
        
        # Sarah Williams interactions (overdue)
        session.add(Interaction(
            contact_id=contacts[3].id,
            interaction_type=InteractionType.IN_PERSON,
            interaction_date=now - timedelta(days=200),
            notes="Met for lunch downtown"
        ))
        
        # David Rodriguez interactions (multiple)
        session.add(Interaction(
            contact_id=contacts[4].id,
            interaction_type=InteractionType.TEXT,
            interaction_date=now - timedelta(days=2),
            notes="Quick check-in"
        ))
        session.add(Interaction(
            contact_id=contacts[4].id,
            interaction_type=InteractionType.CALL,
            interaction_date=now - timedelta(days=10),
            notes="Long conversation about future plans"
        ))
        session.add(Interaction(
            contact_id=contacts[4].id,
            interaction_type=InteractionType.IN_PERSON,
            interaction_date=now - timedelta(days=30),
            notes="Met for dinner"
        ))
        
        # Commit all changes
        session.commit()
        print("Sample data added successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"Error adding sample data: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    add_sample_data()