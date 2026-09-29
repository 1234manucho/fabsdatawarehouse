from flask import Blueprint, redirect, url_for
from flask_login import login_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def index():
    # Admins → admin panel. Regular users → you can add a user route here later.
    return redirect(url_for("admin.index"))