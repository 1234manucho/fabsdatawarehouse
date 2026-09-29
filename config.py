# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)


class Config:
    # ── Core ──
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    DEBUG = False
    TESTING = False

    # ── Database ──
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{os.path.join(INSTANCE_DIR, 'fabs.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # ── Sessions ──
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"

    # ── CSRF ──
    WTF_CSRF_TIME_LIMIT = None

    # ── Rate limiting ──
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "300 per hour")

    # ── Module flags ──
    ENABLE_PAYMENTS   = os.getenv("ENABLE_PAYMENTS", "true").lower() == "true"
    ENABLE_BIOMETRICS = os.getenv("ENABLE_BIOMETRICS", "true").lower() == "true"
    ENABLE_LOGISTICS  = os.getenv("ENABLE_LOGISTICS", "true").lower() == "true"
    ENABLE_COUNTY     = os.getenv("ENABLE_COUNTY", "true").lower() == "true"
    ENABLE_TENDERS    = os.getenv("ENABLE_TENDERS", "true").lower() == "true"
    ENABLE_PETROLEUM  = os.getenv("ENABLE_PETROLEUM", "false").lower() == "true"

    # ── Integrations ──
    MIFOS_BASE_URL    = os.getenv("MIFOS_BASE_URL", "")
    MIFOS_TENANT      = os.getenv("MIFOS_TENANT", "default")
    MIFOS_TOKEN       = os.getenv("MIFOS_TOKEN", "")

    TRANSFI_API_KEY   = os.getenv("TRANSFI_API_KEY", "")
    TRANSFI_BASE_URL  = os.getenv("TRANSFI_BASE_URL", "https://api.transfi.com/v2")

    PAYOFF_BASE_URL   = os.getenv("PAYOFF_BASE_URL", "http://localhost:8081")
    PAYOFF_API_KEY    = os.getenv("PAYOFF_API_KEY", "")

    FLEETBASE_BASE_URL = os.getenv("FLEETBASE_BASE_URL", "http://localhost:8000")
    FLEETBASE_API_KEY  = os.getenv("FLEETBASE_API_KEY", "")

    DHL_API_KEY       = os.getenv("DHL_API_KEY", "")
    DHL_API_SECRET    = os.getenv("DHL_API_SECRET", "")
    DHL_BASE_URL      = os.getenv("DHL_BASE_URL", "https://api-eu.dhl.com")

    MPESA_CONSUMER_KEY    = os.getenv("MPESA_CONSUMER_KEY", "")
    MPESA_CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET", "")
    MPESA_SHORTCODE       = os.getenv("MPESA_SHORTCODE", "174379")
    MPESA_PASSKEY         = os.getenv("MPESA_PASSKEY", "")
    MPESA_ENV             = os.getenv("MPESA_ENV", "sandbox")

    DPO_COMPANY_TOKEN = os.getenv("DPO_COMPANY_TOKEN", "")
    DPO_API_KEY       = os.getenv("DPO_API_KEY", "")
    DPO_ENV           = os.getenv("DPO_ENV", "sandbox")

    PESAPAL_CONSUMER_KEY    = os.getenv("PESAPAL_CONSUMER_KEY", "")
    PESAPAL_CONSUMER_SECRET = os.getenv("PESAPAL_CONSUMER_SECRET", "")
    PESAPAL_ENV             = os.getenv("PESAPAL_ENV", "sandbox")

    FINSERVE_API_KEY    = os.getenv("FINSERVE_API_KEY", "")
    FINSERVE_API_SECRET = os.getenv("FINSERVE_API_SECRET", "")
    FINSERVE_ENV        = os.getenv("FINSERVE_ENV", "sandbox")

    ICRMS_BASE_URL = os.getenv("ICRMS_BASE_URL", "")
    ICRMS_API_KEY  = os.getenv("ICRMS_API_KEY", "")

    OFFICIAL_LOGISTICS_PARTNER = "DHL"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}