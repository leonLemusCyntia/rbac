from pathlib import Path
import pytest
import requests_mock

from .app import app


@pytest.yield_fixture(scope='function')
def client():
    app.config["TESTING"] = True

    with app.app_context():
        yield app.test_client()  # tests run here

def test_home(client):
    response = client.get("/", content_type="html/text")
    assert response.status_code == 200

def test_payments_with_auth(client, requests_mock):
    requests_mock.get("http://rbac:3000/rbac-auth")
    response = client.get("/payments", content_type="html/text", query_string={"user_id": "user_id"})
    assert response.status_code == 200

def test_payments_without_auth(client, requests_mock):
    requests_mock.get("http://rbac:3000/rbac-auth", status_code=403)
    response = client.get("/payments", content_type="html/text", query_string={"user_id": "user_id"})
    assert response.status_code == 403

