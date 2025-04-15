import os
from datetime import datetime
from logging import getLogger

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Contact, FrequencyUnit, Interaction, InteractionType, init_db
from app.time_utils import curr_time

# Create a logger
logger = getLogger(__name__)

bp = Blueprint("contacts", __name__, url_prefix="/contacts")

# Create engine and session factory
engine = init_db(os.environ.get("DATABASE_URL"))
Session = sessionmaker(bind=engine)


@bp.route("/")
def list_contacts():
    """List all contacts."""
    session = Session()
    try:
        filter_type = request.args.get("filter", "all")

        # Cached time for consistent calculations
        now = curr_time()

        if filter_type == "due":
            # Filter for due contacts
            contacts = [
                contact
                for contact in session.query(Contact).all()
                if contact.is_due_soon
            ]
        elif filter_type == "overdue":
            # Filter for overdue contacts (same as due for now)
            contacts = [
                contact for contact in session.query(Contact).all() if contact.is_due
            ]
        else:
            # Show all contacts
            contacts = session.query(Contact).all()

        # Pass the current time to the template for consistent display
        return render_template(
            "contact_list.html",
            title="All Contacts",
            contacts=contacts,
            filter=filter_type,
            now=now,
        )
    finally:
        session.close()


@bp.route("/new", methods=["GET"])
def new_form():
    """Show form to add a new contact."""
    frequency_units = FrequencyUnit.__members__.values()
    return render_template("contact_form.html", frequency_units=frequency_units)


@bp.route("/create", methods=["POST"])
def create():
    """Create a new contact."""
    session = Session()
    try:
        new_contact = Contact(
            name=request.form.get("name"),
            email=request.form.get("email"),
            phone=request.form.get("phone"),
            frequency_value=int(request.form.get("frequency_value")),
            frequency_unit=FrequencyUnit(request.form.get("frequency_unit")),
            notes=request.form.get("notes"),
        )

        session.add(new_contact)
        session.commit()

        flash("Contact added successfully!", "success")
        return redirect(url_for("contacts.list_contacts"))
    except Exception as e:
        session.rollback()
        flash(f"Error adding contact: {str(e)}", "danger")
        return redirect(url_for("contacts.new_form"))
    finally:
        session.close()


@bp.route("/<int:contact_id>/detail", methods=["GET"])
def detail(contact_id):
    """Show contact details."""
    session = Session()
    try:
        # Current time for consistency
        now = curr_time()

        contact = session.query(Contact).get(contact_id)
        if not contact:
            flash("Contact not found!", "danger")
            return redirect(url_for("contacts.list_contacts"))

        # Get interactions for this contact
        interactions = (
            session.query(Interaction)
            .filter_by(contact_id=contact_id)
            .order_by(Interaction.interaction_date.desc())
            .all()
        )

        return render_template(
            "contact_detail.html", contact=contact, interactions=interactions, now=now
        )
    finally:
        session.close()


@bp.route("/<int:contact_id>/edit", methods=["GET"])
def edit_form(contact_id):
    """Show form to edit a contact."""
    session = Session()
    try:
        contact = session.query(Contact).get(contact_id)
        if not contact:
            flash("Contact not found!", "danger")
            return redirect(url_for("contacts.list_contacts"))

        frequency_units = FrequencyUnit.__members__.values()
        return render_template(
            "contact_form.html", contact=contact, frequency_units=frequency_units
        )
    finally:
        session.close()


@bp.route("/<int:contact_id>/update", methods=["POST"])
def update(contact_id):
    """Update a contact."""
    session = Session()
    try:
        contact = session.query(Contact).get(contact_id)
        if not contact:
            flash("Contact not found!", "danger")
            return redirect(url_for("contacts.list_contacts"))

        # Update contact fields
        contact.name = request.form.get("name")
        contact.email = request.form.get("email")
        contact.phone = request.form.get("phone")
        contact.frequency_value = int(request.form.get("frequency_value"))
        contact.frequency_unit = FrequencyUnit(request.form.get("frequency_unit"))
        contact.notes = request.form.get("notes")

        session.commit()
        flash("Contact updated successfully!", "success")
        return redirect(url_for("contacts.detail_page", contact_id=contact_id))
    except Exception as e:
        session.rollback()
        flash(f"Error updating contact: {str(e)}", "danger")
        return redirect(url_for("contacts.edit_form", contact_id=contact_id))
    finally:
        session.close()


@bp.route("/<int:contact_id>/delete", methods=["DELETE"])
def delete(contact_id):
    """Delete a contact."""
    session = Session()
    try:
        contact = session.query(Contact).get(contact_id)
        if not contact:
            flash("Contact not found!", "danger")
            return redirect(url_for("contacts.list_contacts"))

        session.delete(contact)
        session.commit()

        flash("Contact deleted successfully!", "success")

        # For HTMX, return updated contact list
        contacts = session.query(Contact).all()
        return render_template("contact_list.html", contacts=contacts, filter="all")
    except Exception as e:
        session.rollback()
        flash(f"Error deleting contact: {str(e)}", "danger")
        return redirect(url_for("contacts.detail", contact_id=contact_id))
    finally:
        session.close()


@bp.route("/<int:contact_id>/interactions/new", methods=["GET"])
def new_interaction_form(contact_id):
    """Show form to add a new interaction."""
    session = Session()
    try:
        contact = session.query(Contact).get(contact_id)
        if not contact:
            flash("Contact not found!", "danger")
            return redirect(url_for("contacts.list_contacts"))

        interaction_types = InteractionType.__members__.values()
        return render_template(
            "interaction_form.html",
            contact=contact,
            interaction_types=interaction_types,
        )
    finally:
        session.close()


@bp.route("/<int:contact_id>", methods=["GET"])
def detail_page(contact_id):
    """Show form to add a new interaction."""
    session = Session()
    try:
        contact = session.query(Contact).get(contact_id)
        if not contact:
            flash("Contact not found!", "danger")
            return redirect(url_for("contacts.list_contacts"))

        interaction_types = InteractionType.__members__.values()
        return render_template(
            "pages/contact_detail_page.html",
            contact=contact,
            interaction_types=interaction_types,
        )
    finally:
        session.close()
