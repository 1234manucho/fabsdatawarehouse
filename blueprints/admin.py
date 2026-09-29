# blueprints/admin.py
from functools import wraps

from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from models import User, PayoutBatch, Shipment, CountyCollection

admin_bp = Blueprint("admin", __name__)


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
        "users": User.query.count(),
        "payouts": PayoutBatch.query.count(),
        "shipments": Shipment.query.count(),
        "collections": CountyCollection.query.count(),
    }
    recent_users = User.query.order_by(User.created_at.desc()).limit(6).all()
    return render_template("admin/index.html", active="dashboard",
                           stats=stats, recent_users=recent_users)


@admin_bp.route("/analytics")
@admin_required
def analytics():
    return render_template("admin/index.html", active="analytics")


@admin_bp.route("/users")
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).limit(50).all()
    return render_template("admin/users.html", active="users", users=all_users)


@admin_bp.route("/transactions")
@admin_required
def transactions():
    return render_template("admin/transactions.html", active="transactions")


@admin_bp.route("/payouts")
@admin_required
def payouts():
    return render_template("admin/transactions.html", active="payouts")


@admin_bp.route("/biometrics")
@admin_required
def biometrics():
    return render_template("admin/index.html", active="biometrics")


@admin_bp.route("/logistics")
@admin_required
def logistics():
    return render_template("admin/index.html", active="logistics")


@admin_bp.route("/merchants")
@admin_required
def merchants():
    return render_template("admin/users.html", active="merchants")


@admin_bp.route("/settings")
@admin_required
def settings():
    return render_template("admin/settings.html", active="settings")


@admin_bp.route("/reports")
@admin_required
def reports():
    return render_template("admin/index.html", active="reports")
