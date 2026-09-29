# blueprints/biometrics.py
from flask import Blueprint, render_template
from flask_login import login_required

biometrics_bp = Blueprint("biometrics", __name__)


@biometrics_bp.route("/")
@login_required
def index():
    return render_template("biometrics/index.html")
