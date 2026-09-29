from functools import wraps
from flask import (
    Blueprint, render_template, redirect, url_for,
    request, flash, abort,
)
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import or_

from extensions import db
from models import User


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not getattr(current_user, "is_admin", False):
            abort(403)
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route("/")
@admin_required
def index():
    stats = {
        "total_users":     User.query.count(),
        "active_users":    User.query.filter_by(is_active_flag=True).count(),
        "admin_users":     User.query.filter_by(is_admin=True).count(),
        "total_payouts":   0,   # wire to your Payout model when ready
        "pending_tenders": 0,
    }
    recent_users = (
        User.query
        .order_by(User.created_at.desc().nullslast())
        .limit(10)
        .all()
    )
    return render_template("admin/index.html", stats=stats, recent_users=recent_users)


@admin_bp.route("/users")
@admin_required
def users():
    q = request.args.get("q", "").strip()
    query = User.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(User.email.ilike(like),
                                 User.full_name.ilike(like),
                                 User.company_name.ilike(like)))
    all_users = query.order_by(User.created_at.desc().nullslast()).all()
    return render_template("admin/users.html", users=all_users, q=q)


@admin_bp.route("/users/new", methods=["GET", "POST"])
@admin_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@admin_required
def user_form(user_id=None):
    user = User.query.get(user_id) if user_id else None
    if user_id and not user:
        abort(404)

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if not email:
            flash("Email is required.", "error")
            return render_template("admin/user_form.html", user=user)

        # uniqueness check
        clash = User.query.filter(User.email == email)
        if user:
            clash = clash.filter(User.id != user.id)
        if clash.first():
            flash("A user with that email already exists.", "error")
            return render_template("admin/user_form.html", user=user)

        if user is None:
            user = User(email=email)
            db.session.add(user)
        else:
            user.email = email

        user.full_name      = request.form.get("full_name", "").strip() or None
        user.company_name   = request.form.get("company_name", "").strip() or None
        user.role           = request.form.get("role", "user")
        user.is_admin       = (user.role == "admin")
        user.is_active_flag = bool(request.form.get("is_active_flag"))

        pw = request.form.get("password", "").strip()
        if pw:
            user.password_hash = generate_password_hash(pw)
        elif user.id is None:
            flash("Password is required for a new user.", "error")
            return render_template("admin/user_form.html", user=user)

        db.session.commit()
        flash(f"{'Updated' if user_id else 'Created'} {user.email}.", "success")
        return redirect(url_for("admin.users"))

    return render_template("admin/user_form.html", user=user)


@admin_bp.route("/users/<int:user_id>/toggle", methods=["POST"])
@admin_required
def user_toggle(user_id):
    u = User.query.get_or_404(user_id)
    if u.id == current_user.id:
        flash("You cannot deactivate your own account.", "error")
        return redirect(url_for("admin.users"))
    u.is_active_flag = not u.is_active_flag
    db.session.commit()
    flash(f"{'Activated' if u.is_active_flag else 'Deactivated'} {u.email}.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/transactions")
@admin_required
def transactions():
    return render_template("admin/transactions.html", transactions=[])


@admin_bp.route("/settings")
@admin_required
def settings():
    return render_template("admin/settings.html")