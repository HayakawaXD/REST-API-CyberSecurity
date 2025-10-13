import json
import pytest

from codeapi import create_app, db
from codeapi.models import Vulnerability


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_vulnerabilities_empty(client):
    resp = client.get("/vulnerabilities")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == []


def test_post_vulnerability_and_get(client):
    payload = {"name": "Teste", "affected_system": "SistemaX", "severity": 7.5}
    resp = client.post("/vulnerabilities", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["name"] == "Teste"

    resp2 = client.get("/vulnerabilities")
    assert resp2.status_code == 200
    list_data = resp2.get_json()
    assert len(list_data) == 1
    assert list_data[0]["name"] == "Teste"


def test_post_missing_field(client):
    payload = {"name": "Teste2", "affected_system": "SistemaY"}
    resp = client.post("/vulnerabilities", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 400
