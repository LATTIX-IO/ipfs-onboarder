import pytest
from fastapi.testclient import TestClient
from ipfs_onboarder.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def set_token(monkeypatch):
    monkeypatch.setenv("ONBOARDER_SECRET", "testtoken")


def test_healthz():
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_onboard_requires_token():
    res = client.post("/onboard", json={"org_name": "Acme", "owner_email": "x@x.com", "tier": "starter"})
    assert res.status_code == 401


def test_onboard_success():
    headers = {"X-Auth-Token": "testtoken"}
    payload = {"org_name": "Acme", "owner_email": "x@x.com", "tier": "starter"}
    res = client.post("/onboard", json=payload, headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["org_slug"] == "acme"
    assert body["deployment_status"] == "pending"
