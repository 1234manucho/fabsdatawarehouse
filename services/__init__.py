# services/__init__.py
"""External integration clients — stubs ready for real API keys."""

from . import mpesa, dpo, pesapal, finserve, dhl, payoff, fleetbase, mifos, transfi, icrms

__all__ = [
    "mpesa", "dpo", "pesapal", "finserve",
    "dhl", "payoff", "fleetbase", "mifos", "transfi", "icrms",
]