# services/mpesa.py
"""M-Pesa Daraja API client — STK Push, C2B, B2C."""
from flask import current_app


def _config():
    return {
        "consumer_key": current_app.config["MPESA_CONSUMER_KEY"],
        "consumer_secret": current_app.config["MPESA_CONSUMER_SECRET"],
        "shortcode": current_app.config["MPESA_SHORTCODE"],
        "passkey": current_app.config["MPESA_PASSKEY"],
        "env": current_app.config["MPESA_ENV"],
    }


def stk_push(phone: str, amount: float, account_ref: str, description: str = "Payment"):
    """Initiate an STK push. Returns a dict — replace stub with real Daraja call."""
    cfg = _config()
    if not cfg["consumer_key"]:
        return {"ok": False, "error": "M-Pesa credentials not configured", "stub": True}
    # TODO: implement OAuth + POST /mpesa/stkpush/v1/processrequest
    return {"ok": True, "stub": True, "phone": phone, "amount": amount, "ref": account_ref}


def b2c_payout(phone: str, amount: float, remarks: str = "Payout"):
    """Send money to a phone number via B2C."""
    cfg = _config()
    if not cfg["consumer_key"]:
        return {"ok": False, "error": "M-Pesa credentials not configured", "stub": True}
    # TODO: implement OAuth + POST /mpesa/b2c/v1/paymentrequest
    return {"ok": True, "stub": True, "phone": phone, "amount": amount}


def c2b_register_urls(confirmation_url: str, validation_url: str):
    """Register C2B URLs for county / merchant collections."""
    cfg = _config()
    if not cfg["consumer_key"]:
        return {"ok": False, "error": "M-Pesa credentials not configured", "stub": True}
    # TODO: implement OAuth + POST /mpesa/c2b/v1/registerurl
    return {"ok": True, "stub": True}