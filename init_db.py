#!/usr/bin/env python3
# Script to initialize the Round Again database

from app.models import init_db, Base
from sqlalchemy import create_engine

def main():
    """Initialize the database with schema"""
    print("Initializing database...")
    
    # Initialize the database
    engine = init_db('round_again.db')
    
    # Create tables
    Base.metadata.create_all(engine)
    
    print("Database initialized successfully!")
    print("Tables created in round_again.db")

if __name__ == "__main__":
    main()