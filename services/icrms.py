# services/icrms.py
"""County revenue (ICRMS-style) collection client."""
from flask import current_app


def record_collection(county: str, stream: str, amount: float, phone: str, receipt: str):
    cfg = current_app.config
    if not cfg["ICRMS_API_KEY"]:
        return {"ok": True, "stub": True, "receipt": receipt}
    # TODO: POST {ICRMS_BASE_URL}/collections
    return {"ok": True, "stub": True, "receipt": receipt}


def export_ifmis(county: str, period: str):
    if not current_app.config["ICRMS_API_KEY"]:
        return {"ok": False, "stub": True}
    return {"ok": True, "stub": True}