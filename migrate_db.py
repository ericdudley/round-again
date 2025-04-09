#!/usr/bin/env python3
# Script to migrate data from Keep In Touch to Round Again database

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Contact, Interaction

def migrate_data():
    """Migrate data from the old database to the new one"""
    print("Starting database migration...")
    
    # Check if old database exists
    old_db_path = 'keep_in_touch.db'
    if not os.path.exists(old_db_path):
        print(f"Old database {old_db_path} not found. No data to migrate.")
        return
    
    # Connect to old database
    old_engine = create_engine(f'sqlite:///{old_db_path}')
    OldSession = sessionmaker(bind=old_engine)
    old_session = OldSession()
    
    # Connect to new database
    new_engine = create_engine('sqlite:///round_again.db')
    NewSession = sessionmaker(bind=new_engine)
    new_session = NewSession()
    
    try:
        print("Migrating contacts...")
        # Migrate contacts first
        old_contacts = old_session.query(Contact).all()
        contacts_map = {}  # Map old IDs to new IDs
        
        for old_contact in old_contacts:
            # Create new contact with same data
            new_contact = Contact(
                name=old_contact.name,
                email=old_contact.email,
                phone=old_contact.phone,
                frequency_value=old_contact.frequency_value,
                frequency_unit=old_contact.frequency_unit,
                notes=old_contact.notes,
                created_at=old_contact.created_at,
                updated_at=old_contact.updated_at
            )
            
            new_session.add(new_contact)
            new_session.flush()  # Flush to get new ID
            
            # Map old ID to new ID
            contacts_map[old_contact.id] = new_contact.id
        
        print(f"Migrated {len(contacts_map)} contacts")
        
        # Migrate interactions
        print("Migrating interactions...")
        old_interactions = old_session.query(Interaction).all()
        interaction_count = 0
        
        for old_interaction in old_interactions:
            # Get new contact ID from map
            new_contact_id = contacts_map.get(old_interaction.contact_id)
            if new_contact_id:
                # Create new interaction with same data but new contact ID
                new_interaction = Interaction(
                    contact_id=new_contact_id,
                    interaction_type=old_interaction.interaction_type,
                    interaction_date=old_interaction.interaction_date,
                    notes=old_interaction.notes
                )
                
                new_session.add(new_interaction)
                interaction_count += 1
        
        # Commit all changes
        new_session.commit()
        print(f"Migrated {interaction_count} interactions")
        
        print("Migration completed successfully!")
        
    except Exception as e:
        new_session.rollback()
        print(f"Error during migration: {str(e)}")
    finally:
        old_session.close()
        new_session.close()

if __name__ == "__main__":
    migrate_data()