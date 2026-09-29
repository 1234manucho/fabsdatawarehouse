# blueprints/main.py
from flask import Blueprint, render_template, request, redirect, url_for, flash

from extensions import db
from models import Lead

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/faqs")
def faqs():
    return render_template("faqs.html")


@main_bp.route("/pricing")
def pricing():
    return render_template("pricing.html")


@main_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")


@main_bp.route("/terms")
def terms():
    return render_template("terms.html")


@main_bp.route("/contact")
def contact():
    return render_template("contact.html")


@main_bp.route("/contact", methods=["POST"])
def contact_submit():
    full_name = (request.form.get("full_name") or "").strip()
    email     = (request.form.get("email") or "").strip()
    company   = (request.form.get("company") or "").strip()
    phone     = (request.form.get("phone") or "").strip()
    interest  = (request.form.get("interest") or "").strip()
    message   = (request.form.get("message") or "").strip()

    if not full_name or not email:
        flash("Name and email are required.", "error")
        return redirect(url_for("main.contact"))

    lead = Lead(
        full_name=full_name, email=email, company=company,
        phone=phone, interest=interest, message=message, source="website",
    )
    db.session.add(lead)
    db.session.commit()

    flash(f"Thanks {full_name}! We will be in touch shortly.", "success")
    return redirect(url_for("main.index") + "#contact")
