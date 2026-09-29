# blueprints/dashboard.py
from flask import Blueprint, render_template
from flask_login import login_required

from models import PayoutBatch, Shipment, CountyCollection, Tender

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    stats = {
        "payout_batches": PayoutBatch.query.count(),
        "shipments_transit": Shipment.query.filter_by(status="in_transit").count(),
        "county_collections": CountyCollection.query.count(),
        "open_tenders": Tender.query.filter_by(status="open").count(),
    }
    recent_payouts = PayoutBatch.query.order_by(PayoutBatch.created_at.desc()).limit(6).all()
    return render_template("dashboard/index.html", stats=stats, recent_payouts=recent_payouts)
