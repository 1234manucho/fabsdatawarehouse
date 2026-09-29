# services/fleetbase.py
"""Fleetbase logistics OS client."""
from flask import current_app


def create_order(reference: str, pickup: dict, dropoff: dict):
    cfg = current_app.config
    if not cfg["FLEETBASE_API_KEY"]:
        return {"ok": False, "error": "Fleetbase not configured", "stub": True}
    # TODO: POST /v1/orders
    return {"ok": True, "stub": True, "order_id": f"FB-{reference[-6:]}"}


def get_order(order_id: str):
    if not current_app.config["FLEETBASE_API_KEY"]:
        return {"ok": False, "stub": True}
    return {"ok": True, "stub": True}