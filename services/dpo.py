# services/dpo.py
"""DPO Group payments client."""
from flask import current_app


def create_token(amount: float, currency: str, reference: str):
    cfg = current_app.config
    if not cfg["DPO_COMPANY_TOKEN"]:
        return {"ok": False, "error": "DPO credentials not configured", "stub": True}
    # TODO: call /API/v6/createToken
    return {"ok": True, "stub": True, "reference": reference}


def verify_token(token: str):
    if not current_app.config["DPO_COMPANY_TOKEN"]:
        return {"ok": False, "stub": True}
    # TODO: call /API/v6/verifyToken
    return {"ok": True, "stub": True}


def refund(transaction_token: str, amount: float):
    if not current_app.config["DPO_COMPANY_TOKEN"]:
        return {"ok": False, "stub": True}
    # TODO: call /API/v6/refund
    return {"ok": True, "stub": True}