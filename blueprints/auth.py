# blueprints/auth.py
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db, limiter
from models import User, AuditLog

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return render_template("auth/login.html"), 401

        if not user.is_active:
            flash("This account has been suspended.", "error")
            return render_template("auth/login.html"), 403

        login_user(user, remember=remember)
        user.last_login_at = datetime.utcnow()
        db.session.add(AuditLog(
            user_id=user.id,
            action="login",
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string[:255] if request.user_agent else None,
        ))
        db.session.commit()

        flash(f"Welcome back, {user.first_name}!", "success")
        next_url = request.args.get("next") or url_for("dashboard.index")
        return redirect(next_url)

    return render_template("auth/login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        full_name    = (request.form.get("full_name") or "").strip()
        company_name = (request.form.get("company_name") or "").strip()
        email        = (request.form.get("email") or "").strip().lower()
        country_code = (request.form.get("country_code") or "+254").strip()
        phone        = (request.form.get("phone") or "").strip()
        password     = request.form.get("password") or ""
        confirm      = request.form.get("confirm_password") or ""
        role         = (request.form.get("role") or "merchant").strip()

        errors = []
        if not full_name:
            errors.append("Full name is required.")
        if not email or "@" not in email:
            errors.append("A valid email is required.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if User.query.filter_by(email=email).first():
            errors.append("An account with that email already exists.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("auth/signup.html"), 400

        user = User(
            email=email,
            full_name=full_name,
            company_name=company_name,
            country_code=country_code,
            phone=phone,
            role=role,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f"Welcome to Fabs Data Warehouse, {user.first_name}!", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("auth/signup.html")


@auth_bp.route("/logout")
@login_required
def logout():
    user_id = current_user.id
    logout_user()
    db.session.add(AuditLog(user_id=user_id, action="logout", ip_address=request.remote_addr))
    db.session.commit()
    flash("You have been signed out.", "info")
    return redirect(url_for("main.index"))