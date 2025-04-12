#!/usr/bin/env python3
# Script to initialize the Round Again database

import logging
import os

from app.models import init_db, Base
from sqlalchemy import create_engine
from dotenv import load_dotenv

def main():
    """Initialize the database with schema"""
    load_dotenv()

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    logger.info("Initializing database...")

    # Initialize the database
    engine = init_db(os.environ.get('DATABASE_URL'))

    # Create tables
    Base.metadata.create_all(engine)

    logger.info("Database initialized successfully!")
    logger.info("Tables created in round_again.db")

if __name__ == "__main__":
    main()