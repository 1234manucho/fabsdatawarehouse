# blueprints/logistics.py
from flask import Blueprint, render_template
from flask_login import login_required

logistics_bp = Blueprint("logistics", __name__)


@logistics_bp.route("/")
@login_required
def index():
    return render_template("logistics/index.html")
