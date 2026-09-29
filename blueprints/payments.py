# blueprints/payments.py
from flask import Blueprint, render_template
from flask_login import login_required

payments_bp = Blueprint("payments", __name__)


@payments_bp.route("/")
@login_required
def index():
    return render_template("payments/index.html")
