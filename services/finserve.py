# services/finserve.py
"""Finserve (Equity Bank) payments client."""
from flask import current_app


def initiate_payout(account_no: str, amount: float, reference: str):
    cfg = current_app.config
    if not cfg["FINSERVE_API_KEY"]:
        return {"ok": False, "error": "Finserve credentials not configured", "stub": True}
    # TODO: call Finserve Jenga API
    return {"ok": True, "stub": True, "reference": reference}


def check_balance(account_no: str):
    if not current_app.config["FINSERVE_API_KEY"]:
        return {"ok": False, "stub": True}
    return {"ok": True, "stub": True}