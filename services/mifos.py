# services/mifos.py
"""Mifos / Fineract core banking client."""
from flask import current_app


def bulk_payout(recipients: list, currency: str = "KES"):
    cfg = current_app.config
    if not cfg["MIFOS_TOKEN"]:
        return {"ok": False, "error": "Mifos not configured", "stub": True}
    # TODO: POST to Mifos Payment Hub
    return {"ok": True, "stub": True, "payout_id": "MIFOS-STUB-0001"}


def get_client(client_id: int):
    if not current_app.config["MIFOS_TOKEN"]:
        return {"ok": False, "stub": True}
    return {"ok": True, "stub": True}