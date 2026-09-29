# services/pesapal.py
"""Pesapal payment gateway client."""
from flask import current_app


def submit_order(amount: float, currency: str, reference: str, callback_url: str):
    cfg = current_app.config
    if not cfg["PESAPAL_CONSUMER_KEY"]:
        return {"ok": False, "error": "Pesapal credentials not configured", "stub": True}
    # TODO: authenticate + POST /api/Transactions/SubmitOrderRequest
    return {"ok": True, "stub": True, "reference": reference}


def get_transaction_status(tracking_id: str):
    if not current_app.config["PESAPAL_CONSUMER_KEY"]:
        return {"ok": False, "stub": True}
    # TODO: POST /api/Transactions/GetTransactionStatus
    return {"ok": True, "stub": True}