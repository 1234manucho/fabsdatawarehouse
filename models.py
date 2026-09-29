# models.py
"""
Fabs Data Warehouse — unified data layer.
Every entity shared across payments, biometrics, logistics, county, tenders,
companies, merchants and admin.
"""
from datetime import datetime
from decimal import Decimal

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


# ═══════════════════════════════════════════════════════════════
#  USER
# ═══════════════════════════════════════════════════════════════
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(160), unique=True, nullable=False, index=True)
    phone         = db.Column(db.String(32), index=True)
    country_code  = db.Column(db.String(8), default="+254")
    full_name     = db.Column(db.String(160), nullable=False)
    company_name  = db.Column(db.String(160))
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(32), default="merchant", index=True)
    # roles: admin, merchant, company, county, aggregator

    is_active_flag    = db.Column(db.Boolean, default=True)
    is_admin          = db.Column(db.Boolean, default=False)
    biometric_enrolled = db.Column(db.Boolean, default=False)
    biometric_template_id = db.Column(db.String(128))

    company_id    = db.Column(db.Integer, db.ForeignKey("companies.id"))
    last_login_at = db.Column(db.DateTime)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    company      = db.relationship("Company", back_populates="users", foreign_keys=[company_id])
    payouts      = db.relationship("PayoutBatch", back_populates="created_by_user",
                                   foreign_keys="PayoutBatch.created_by")
    biometric    = db.relationship("BiometricTemplate", back_populates="user",
                                   uselist=False, cascade="all, delete-orphan")

    # ── Flask-Login helpers ──
    @property
    def is_active(self):
        return bool(self.is_active_flag)

    def set_password(self, raw: str):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password_hash, raw)

    @property
    def first_name(self):
        return (self.full_name or "").split(" ")[0]

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "phone": f"{self.country_code or ''}{self.phone or ''}",
            "role": self.role,
            "is_admin": self.is_admin,
            "biometric_enrolled": self.biometric_enrolled,
        }

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


# ═══════════════════════════════════════════════════════════════
#  COMPANY
# ═══════════════════════════════════════════════════════════════
class Company(db.Model):
    __tablename__ = "companies"

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(160), nullable=False)
    slug         = db.Column(db.String(160), unique=True, index=True)
    industry     = db.Column(db.String(80))
    country      = db.Column(db.String(80), default="Kenya")
    base_currency = db.Column(db.String(3), default="KES")
    is_active    = db.Column(db.Boolean, default=True)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    users        = db.relationship("User", back_populates="company", foreign_keys="User.company_id")
    merchants    = db.relationship("Merchant", back_populates="company", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Company {self.name}>"


# ═══════════════════════════════════════════════════════════════
#  MERCHANT
# ═══════════════════════════════════════════════════════════════
class Merchant(db.Model):
    __tablename__ = "merchants"

    id               = db.Column(db.Integer, primary_key=True)
    company_id       = db.Column(db.Integer, db.ForeignKey("companies.id"), index=True)
    business_name    = db.Column(db.String(160), nullable=False)
    contact_name     = db.Column(db.String(160))
    contact_email    = db.Column(db.String(160))
    contact_phone    = db.Column(db.String(32))
    settlement_rail  = db.Column(db.String(32), default="mpesa")   # mpesa | dpo | pesapal | finserve
    settlement_acct  = db.Column(db.String(64))
    kyc_status       = db.Column(db.String(24), default="pending") # pending | verified | rejected
    is_active        = db.Column(db.Boolean, default=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship("Company", back_populates="merchants")

    def __repr__(self):
        return f"<Merchant {self.business_name}>"


# ═══════════════════════════════════════════════════════════════
#  BIOMETRIC TEMPLATE
# ═══════════════════════════════════════════════════════════════
class BiometricTemplate(db.Model):
    __tablename__ = "biometric_templates"

    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, index=True)
    method         = db.Column(db.String(24), default="fingerprint")  # fingerprint | iris | both
    template_hash  = db.Column(db.String(255), nullable=False)
    device_id      = db.Column(db.String(128))
    match_score    = db.Column(db.Float, default=0.0)
    enrolled_at    = db.Column(db.DateTime, default=datetime.utcnow)
    last_verified_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="biometric")


# ═══════════════════════════════════════════════════════════════
#  PAYOUT BATCH + RECIPIENTS
# ═══════════════════════════════════════════════════════════════
class PayoutBatch(db.Model):
    __tablename__ = "payout_batches"

    id                = db.Column(db.Integer, primary_key=True)
    reference         = db.Column(db.String(32), unique=True, index=True)
    created_by        = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    company_id        = db.Column(db.Integer, db.ForeignKey("companies.id"))

    rail              = db.Column(db.String(32), index=True)   # mpesa | dpo | pesapal | finserve
    currency          = db.Column(db.String(3), default="KES")
    total_amount      = db.Column(db.Numeric(18, 2), default=Decimal("0"))
    recipient_count   = db.Column(db.Integer, default=0)

    status            = db.Column(db.String(24), default="pending", index=True)
    # pending | biometric_verified | processing | completed | failed | partial

    external_payout_id = db.Column(db.String(128))
    biometric_verified_at = db.Column(db.DateTime)
    biometric_score   = db.Column(db.Float)

    notes             = db.Column(db.Text)
    created_at        = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    completed_at      = db.Column(db.DateTime)

    created_by_user = db.relationship("User", back_populates="payouts", foreign_keys=[created_by])
    recipients      = db.relationship("PayoutRecipient", back_populates="batch",
                                      cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PayoutBatch {self.reference} {self.status}>"


class PayoutRecipient(db.Model):
    __tablename__ = "payout_recipients"

    id         = db.Column(db.Integer, primary_key=True)
    batch_id   = db.Column(db.Integer, db.ForeignKey("payout_batches.id"), index=True)
    name       = db.Column(db.String(160))
    phone      = db.Column(db.String(32), index=True)
    amount     = db.Column(db.Numeric(18, 2), default=Decimal("0"))
    status     = db.Column(db.String(24), default="queued")   # queued | sent | failed
    external_ref = db.Column(db.String(128))
    error_msg  = db.Column(db.String(255))

    batch = db.relationship("PayoutBatch", back_populates="recipients")


# ═══════════════════════════════════════════════════════════════
#  SHIPMENT (DHL + Fleetbase)
# ═══════════════════════════════════════════════════════════════
class Shipment(db.Model):
    __tablename__ = "shipments"

    id              = db.Column(db.Integer, primary_key=True)
    payout_batch_id = db.Column(db.Integer, db.ForeignKey("payout_batches.id"), index=True)
    reference       = db.Column(db.String(48), unique=True, index=True)
    dhl_tracking    = db.Column(db.String(80), index=True)
    fleetbase_order = db.Column(db.String(80), index=True)

    carrier         = db.Column(db.String(32), default="DHL")
    service_level   = db.Column(db.String(48))
    origin          = db.Column(db.String(120))
    destination     = db.Column(db.String(120))

    status          = db.Column(db.String(32), default="created", index=True)
    # created | picked_up | in_transit | customs | out_for_delivery | delivered | failed

    cod_amount      = db.Column(db.Numeric(18, 2))
    cod_currency    = db.Column(db.String(3), default="KES")
    cod_collected   = db.Column(db.Boolean, default=False)
    cod_rail        = db.Column(db.String(24))   # mpesa | dpo

    created_at      = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════
#  COUNTY COLLECTION
# ═══════════════════════════════════════════════════════════════
class CountyCollection(db.Model):
    __tablename__ = "county_collections"

    id             = db.Column(db.Integer, primary_key=True)
    county_name    = db.Column(db.String(100), index=True)
    revenue_stream = db.Column(db.String(100), index=True)
    # parking | markets | rates | permits | waste | other

    amount         = db.Column(db.Numeric(18, 2), default=Decimal("0"))
    currency       = db.Column(db.String(3), default="KES")
    payment_method = db.Column(db.String(32))   # mpesa | dpo | pesapal | finserve
    payer_phone    = db.Column(db.String(32))
    receipt_no     = db.Column(db.String(64), unique=True, index=True)
    latitude       = db.Column(db.Float)
    longitude      = db.Column(db.Float)
    ifmis_exported = db.Column(db.Boolean, default=False)

    created_at     = db.Column(db.DateTime, default=datetime.utcnow, index=True)


# ═══════════════════════════════════════════════════════════════
#  TENDER + BID
# ═══════════════════════════════════════════════════════════════
class Tender(db.Model):
    __tablename__ = "tenders"

    id           = db.Column(db.Integer, primary_key=True)
    reference    = db.Column(db.String(32), unique=True, index=True)
    title        = db.Column(db.String(255), nullable=False)
    description  = db.Column(db.Text)
    issuer       = db.Column(db.String(160))
    category     = db.Column(db.String(80))
    value_estimate = db.Column(db.Numeric(18, 2))
    currency     = db.Column(db.String(3), default="KES")

    status       = db.Column(db.String(24), default="open", index=True)
    # open | closed | evaluating | awarded | cancelled

    deadline     = db.Column(db.DateTime)
    awarded_to   = db.Column(db.String(160))
    awarded_amount = db.Column(db.Numeric(18, 2))

    created_at   = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bids = db.relationship("Bid", back_populates="tender", cascade="all, delete-orphan")


class Bid(db.Model):
    __tablename__ = "bids"

    id          = db.Column(db.Integer, primary_key=True)
    tender_id   = db.Column(db.Integer, db.ForeignKey("tenders.id"), index=True)
    bidder_name = db.Column(db.String(160))
    bidder_email = db.Column(db.String(160))
    amount      = db.Column(db.Numeric(18, 2))
    currency    = db.Column(db.String(3), default="KES")
    score       = db.Column(db.Float, default=0.0)
    status      = db.Column(db.String(24), default="received")  # received | shortlisted | rejected | won
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    tender = db.relationship("Tender", back_populates="bids")


# ═══════════════════════════════════════════════════════════════
#  LEAD (contact form)
# ═══════════════════════════════════════════════════════════════
class Lead(db.Model):
    __tablename__ = "leads"

    id          = db.Column(db.Integer, primary_key=True)
    full_name   = db.Column(db.String(160), nullable=False)
    email       = db.Column(db.String(160), nullable=False, index=True)
    company     = db.Column(db.String(160))
    phone       = db.Column(db.String(32))
    interest    = db.Column(db.String(80))
    message     = db.Column(db.Text)
    source      = db.Column(db.String(32), default="website")
    created_at  = db.Column(db.DateTime, default=datetime.utcnow, index=True)


# ═══════════════════════════════════════════════════════════════
#  AUDIT LOG
# ═══════════════════════════════════════════════════════════════
class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    action     = db.Column(db.String(80), index=True)
    entity     = db.Column(db.String(80))
    entity_id  = db.Column(db.String(80))
    detail     = db.Column(db.Text)
    ip_address = db.Column(db.String(64))
    user_agent = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)