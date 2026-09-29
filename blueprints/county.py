# blueprints/county.py
from flask import Blueprint, render_template
from flask_login import login_required

county_bp = Blueprint("county", __name__)


@county_bp.route("/")
@login_required
def index():
    return render_template("county/index.html")
