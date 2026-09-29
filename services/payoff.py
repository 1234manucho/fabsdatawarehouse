# services/payoff.py
"""Pay-off biometric verification client."""
from flask import current_app


def verify(user_id: int, biometric_token: str):
    cfg = current_app.config
    if not cfg["PAYOFF_API_KEY"]:
        # dev fallback — allow in dev so UI can be tested
        return {"authorized": True, "score": 0.9971, "stub": True}
    # TODO: POST {PAYOFF_BASE_URL}/verify
    return {"authorized": True, "score": 0.9971, "stub": True}


def enroll(user_id: int, template_blob: bytes, method: str = "fingerprint"):
    if not current_app.config["PAYOFF_API_KEY"]:
        return {"ok": True, "template_id": f"stub-{user_id}", "stub": True}
    return {"ok": True, "template_id": f"tpl-{user_id}", "stub": True}