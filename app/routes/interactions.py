import os
from datetime import datetime

import flask
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Contact, Interaction, InteractionType, init_db
from app.time_utils import curr_time

bp = Blueprint("interactions", __name__, url_prefix="/interactions")

# Create engine and session factory
engine = init_db(os.environ.get("DATABASE_URL"))
Session = sessionmaker(bind=engine)


@bp.route("/delete/<int:interaction_id>", methods=["DELETE"])
def delete(interaction_id):
    session = Session()
    try:
        interaction = session.query(Interaction).get(interaction_id)
        if not interaction:
            flash("Interaction not found!", "danger")
            return redirect(url_for("contacts.list_contacts"))

        session.delete(interaction)
        session.commit()

        flash("Interaction deleted successfully!", "success")

    except Exception as e:
        session.rollback()
        flash(f"Error deleting contact: {str(e)}", "danger")
        return redirect(url_for("contacts.list_contacts"))
    finally:
        session.close()

    return "", 200


@bp.route("/all/<int:contact_id>", methods=["GET"])
def get_interactions(contact_id):
    session = Session()
    try:
        contact = session.query(Contact).get(contact_id)
        interactions = (
            session.query(Interaction)
            .filter_by(contact_id=contact_id)
            .order_by(Interaction.interaction_date.desc())
            .all()
        )
        return render_template(
            "interaction_list.html", contact=contact, interactions=interactions
        )
    finally:
        session.close()


@bp.route("/add/<int:contact_id>", methods=["GET", "POST"])
def add_interaction(contact_id):
    """Add a new interaction for a contact."""
    session = Session()
    try:
        # Current time for consistency
        now = curr_time()

        if request.method == "POST":
            interaction_date_str = datetime.strptime(
                request.form.get("interaction_date"), "%Y-%m-%dT%H:%M"
            )

            # Process form submission
            interaction = Interaction(
                contact_id=contact_id,
                interaction_type=InteractionType(request.form.get("interaction_type")),
                interaction_date=interaction_date_str,
                notes=request.form.get("notes"),
            )

            session.add(interaction)
            session.commit()

            flash("Interaction logged successfully!", "success")

            response = flask.Response("")
            response.headers["HX-Trigger"] = "interactions"
            return response

        # Get contact for form
        contact = session.query(Contact).get(contact_id)
        if not contact:
            flash("Contact not found!", "danger")
            return redirect(url_for("contacts.list_contacts"))

        return render_template(
            "interaction_form.html",
            title="Add Interaction",
            contact=contact,
            interaction_types=InteractionType.__members__.values(),
            now=now,
        )
    except Exception as e:
        session.rollback()
        flash(f"Error logging interaction: {str(e)}", "danger")
        return redirect(url_for("contacts.detail", contact_id=contact_id))
    finally:
        session.close()


@bp.route("/new/<int:contact_id>", methods=["GET"])
def new_form(contact_id):
    """Show form to add a new interaction."""
    session = Session()
    try:
        # Current time for consistency
        now = curr_time()

        contact = session.query(Contact).get(contact_id)
        if not contact:
            flash("Contact not found!", "danger")
            return redirect(url_for("contacts.list_contacts"))

        return render_template(
            "interaction_form.html",
            title="Log Interaction",
            contact=contact,
            interaction_types=InteractionType.__members__.values(),
            now=now,
        )
    finally:
        session.close()
