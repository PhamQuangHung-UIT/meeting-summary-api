from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_read_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_summarize():
    payload = {
        "title": "Team sync",
        "attendees": ["Alice", "Bob"],
        "notes": "Meeting started. Discussed the roadmap and next steps. Action items assigned to the team."
    }
    r = client.post("/summarize", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "summary" in body
    assert body["summary"] != ""
