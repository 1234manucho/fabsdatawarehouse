# tests/test_app.py
import pytest

from app import create_app
from extensions import db


@pytest.fixture
def client():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        with app.test_client() as c:
            yield c
        db.session.remove()
        db.drop_all()


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["status"] in ("ok", "degraded")


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"FABS" in r.data


def test_about(client):
    r = client.get("/about")
    assert r.status_code == 200


def test_faqs(client):
    r = client.get("/faqs")
    assert r.status_code == 200


def test_pricing(client):
    r = client.get("/pricing")
    assert r.status_code == 200


def test_login_page(client):
    r = client.get("/auth/login")
    assert r.status_code == 200


def test_signup_page(client):
    r = client.get("/auth/signup")
    assert r.status_code == 200


def test_dashboard_requires_login(client):
    r = client.get("/dashboard/", follow_redirects=False)
    assert r.status_code == 302


def test_404(client):
    r = client.get("/this-does-not-exist")
    assert r.status_code == 404