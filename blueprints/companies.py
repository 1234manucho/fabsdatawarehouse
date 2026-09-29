# blueprints/companies.py
from flask import Blueprint, render_template
from flask_login import login_required

companies_bp = Blueprint("companies", __name__)


@companies_bp.route("/")
@login_required
def index():
    return render_template("companies/index.html")
