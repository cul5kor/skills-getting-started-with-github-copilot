import os
import sys
from fastapi.testclient import TestClient

# Ensure `src` is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import app

client = TestClient(app)


def test_root_redirects_to_static():
    resp = client.get("/", allow_redirects=False)
    assert resp.status_code in (301, 302, 307)
    assert "/static/index.html" in resp.headers.get("location", "")


def test_get_activities_contains_known_activity():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data


def test_signup_success_and_duplicate():
    activity = "Math Club"
    email = "pytest_user@example.com"

    # first signup should succeed
    resp1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp1.status_code == 200
    assert "Signed up" in resp1.json().get("message", "")

    # second signup with same email should fail (duplicate)
    resp2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp2.status_code == 400


def test_signup_nonexistent_activity_returns_404():
    resp = client.post("/activities/NoSuchActivity/signup", params={"email": "x@x.com"})
    assert resp.status_code == 404
