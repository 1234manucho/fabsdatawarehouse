# services/transfi.py
"""TransFi multi-currency payout client."""
from flask import current_app


def payout(recipients: list, currency: str):
    cfg = current_app.config
    if not cfg["TRANSFI_API_KEY"]:
        return {"ok": False, "error": "TransFi not configured", "stub": True}
    # TODO: POST /v2/payouts
    return {"ok": True, "stub": True, "payout_id": "TRF-STUB-0001"}


def get_payout(payout_id: str):
    if not current_app.config["TRANSFI_API_KEY"]:
        return {"ok": False, "stub": True}
    return {"ok": True, "stub": True}