import enum
import logging
import os
from datetime import UTC, datetime, timedelta

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.time_utils import curr_time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

Base = declarative_base()


class FrequencyUnit(enum.Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class InteractionType(enum.Enum):
    CALL = "call"
    VIDEO = "video"
    EMAIL = "email"
    TEXT = "text"
    IN_PERSON = "in_person"
    OTHER = "other"


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    frequency_value = Column(Integer, nullable=False, default=1)
    frequency_unit = Column(
        Enum(FrequencyUnit), nullable=False, default=FrequencyUnit.MONTH
    )
    notes = Column(Text)
    created_at = Column(DateTime, default=curr_time)
    updated_at = Column(DateTime, default=curr_time, onupdate=curr_time)

    interactions = relationship(
        "Interaction", back_populates="contact", cascade="all, delete-orphan"
    )

    @property
    def next_due_date(self):
        """Calculate the next due date for contacting this person."""
        now = curr_time()

        if not self.interactions:
            return now

        last_interaction = max(self.interactions, key=lambda i: i.interaction_date)

        # Calculate next due date based on frequency
        if self.frequency_unit == FrequencyUnit.DAY:
            return last_interaction.interaction_date + timedelta(
                days=self.frequency_value
            )
        elif self.frequency_unit == FrequencyUnit.WEEK:
            return last_interaction.interaction_date + timedelta(
                weeks=self.frequency_value
            )
        elif self.frequency_unit == FrequencyUnit.MONTH:
            # Simple approximation for months (30 days)
            return last_interaction.interaction_date + timedelta(
                days=30 * self.frequency_value
            )
        elif self.frequency_unit == FrequencyUnit.YEAR:
            return last_interaction.interaction_date + timedelta(
                days=365 * self.frequency_value
            )

    @property
    def is_due_soon(self):
        return self.days_until_due <= 1

    @property
    def is_due(self):
        """Check if this contact is due or overdue for interaction."""
        # Cache the current time for consistent calculations
        now = curr_time()
        return self.days_until_due < 0

    @property
    def days_until_due(self):
        """Calculate days until next interaction is due (negative if overdue)."""
        # Cache the current time for consistent calculations
        now = curr_time()
        delta = self.next_due_date - now
        return delta.days


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    interaction_type = Column(Enum(InteractionType), nullable=False)
    interaction_date = Column(DateTime, nullable=False, default=curr_time)
    notes = Column(Text)

    contact = relationship("Contact", back_populates="interactions")


def init_db(db_path="round_again.db"):
    # Get absolute path
    abs_path = os.path.abspath(db_path)
    db_dir = os.path.dirname(abs_path)

    # Ensure directory exists
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Create db connection
    db_uri = f"sqlite:///{abs_path}"
    logger.info(f"Initializing database: {db_uri}")
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    return engine
