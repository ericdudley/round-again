#!/usr/bin/env python3
# Setup script for Round Again database
"""
This script handles:
1. Creating the database tables
2. Adding sample data (optional)
"""

import os
import sys
import argparse
from app.models import init_db, Base

def setup_database(add_samples=False, force=False):
    """Set up the Round Again database"""
    print("Setting up Round Again database...")
    
    db_path = 'round_again.db'
    
    # Check if database already exists
    if os.path.exists(db_path) and not force:
        print(f"Database {db_path} already exists. Use --force to overwrite.")
        return False
    
    # Initialize database
    print("Creating database tables...")
    engine = init_db(db_path)
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")
    
    # Add sample data if requested
    if add_samples:
        print("Adding sample data...")
        try:
            # Import here to avoid circular imports
            from add_sample_data import add_sample_data
            add_sample_data()
        except Exception as e:
            print(f"Error adding sample data: {str(e)}")
    
    print("\n==============================================")
    print("Round Again database setup complete!")
    print("==============================================")
    print("\nYou can now run the application with:")
    print("  - Development mode: make dev")
    print("  - Production mode: make run")
    
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set up Round Again database')
    parser.add_argument('--samples', action='store_true', help='Add sample data')
    parser.add_argument('--force', action='store_true', help='Force overwrite existing database')
    
    args = parser.parse_args()
    
    if not setup_database(add_samples=args.samples, force=args.force):
        sys.exit(1)