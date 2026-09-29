# services/dhl.py
"""DHL Shipping Partner API client."""
from flask import current_app


def create_shipment(recipient: dict, reference: str, service: str = "express"):
    cfg = current_app.config
    if not cfg["DHL_API_KEY"]:
        return {"ok": False, "error": "DHL credentials not configured", "stub": True}
    # TODO: POST /mydhlapi/shipments
    return {
        "ok": True, "stub": True,
        "tracking": f"AWB-{reference[-8:]}",
        "service": service,
    }


def track_shipment(tracking_number: str):
    cfg = current_app.config
    if not cfg["DHL_API_KEY"]:
        return {"ok": False, "error": "DHL credentials not configured", "stub": True}
    # TODO: GET /track/shipments?trackingNumber=...
    return {
        "ok": True, "stub": True,
        "tracking": tracking_number,
        "status": "in_transit",
        "milestones": [],
    }


def cancel_shipment(tracking_number: str):
    if not current_app.config["DHL_API_KEY"]:
        return {"ok": False, "stub": True}
    return {"ok": True, "stub": True}