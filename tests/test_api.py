"""API contract tests aligned with docs/api-contract.md v2.0."""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

BACKEND_ROOT = Path(__file__).resolve().parent.parent
SEED_PATH = BACKEND_ROOT / "scripts" / "initial_seed.json"


def _seed(client: TestClient) -> dict:
    with SEED_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    import sys

    sys.path.insert(0, str(BACKEND_ROOT))
    from scripts.seed import _load, _wipe  # noqa: E402
    from app.database import SessionLocal  # noqa: E402

    db = SessionLocal()
    try:
        _wipe(db)
        _load(db, data)
    finally:
        db.close()
    return data


def test_health(client: TestClient) -> None:
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_bootstrap_empty(client: TestClient) -> None:
    r = client.get("/api/bootstrap")
    assert r.status_code == 200
    body = r.json()
    assert body["bunnies"] == []
    assert body["currentBunnyId"] == ""
    assert body["bunnyData"] == {}


def test_seed_bootstrap_matches_fixture(client: TestClient) -> None:
    seed = _seed(client)
    r = client.get("/api/bootstrap")
    assert r.status_code == 200
    body = r.json()
    assert body["currentBunnyId"] == seed["currentBunnyId"]
    assert len(body["bunnies"]) == len(seed["bunnies"])
    assert set(body["bunnyData"].keys()) == set(seed["bunnyData"].keys())
    b1 = body["bunnyData"]["b1"]
    assert len(b1["timelineEvents"]) == 8
    assert len(b1["weightRecords"]) == 14
    assert b1["bunny"]["name"] == "臭臭"


def test_current_bunny_switch(client: TestClient) -> None:
    _seed(client)
    r = client.put("/api/settings/current-bunny", json={"bunnyId": "b2"})
    assert r.status_code == 200
    assert client.get("/api/bootstrap").json()["currentBunnyId"] == "b2"
    r = client.put("/api/settings/current-bunny", json={"bunnyId": "missing"})
    assert r.status_code == 404


def test_bunny_crud(client: TestClient) -> None:
    _seed(client)
    r = client.post(
        "/api/bunnies",
        json={
            "name": "新兔",
            "breed": "垂耳兔",
            "birthDate": "2025-01-01",
            "weight": 500,
        },
    )
    assert r.status_code == 201
    bunny = r.json()
    assert bunny["name"] == "新兔"
    bunny_id = bunny["id"]

    r = client.patch(f"/api/bunnies/{bunny_id}", json={"weight": 520})
    assert r.status_code == 200
    assert r.json()["weight"] == 520

    r = client.delete(f"/api/bunnies/{bunny_id}")
    assert r.status_code == 204
    assert client.get(f"/api/bootstrap").json()["bunnyData"].get(bunny_id) is None


def test_timeline_crud(client: TestClient) -> None:
    _seed(client)
    r = client.post(
        "/api/timeline-events",
        json={
            "bunnyId": "b1",
            "date": "2025-05-26",
            "title": "测试足迹",
            "coverImage": "/assets/hero-photo.jpg",
            "description": "描述",
            "detailImages": ["/assets/hero-photo.jpg"],
            "mood": "开心",
            "color": "#F5C6C8",
        },
    )
    assert r.status_code == 201
    event = r.json()
    assert event["date"] == "2025.05.26"
    event_id = event["id"]

    r = client.patch(f"/api/timeline-events/{event_id}", json={"title": "已更新"})
    assert r.status_code == 200
    assert r.json()["title"] == "已更新"

    r = client.delete(f"/api/timeline-events/{event_id}")
    assert r.status_code == 204


def test_weight_crud(client: TestClient) -> None:
    _seed(client)
    before = len(client.get("/api/bootstrap").json()["bunnyData"]["b1"]["weightRecords"])
    r = client.post(
        "/api/weight-records",
        json={"bunnyId": "b1", "date": "2025-05", "weight": 1190},
    )
    assert r.status_code == 201
    assert r.json()["date"] == "2025-05"
    record_id = r.json()["id"]
    assert client.get("/api/bootstrap").json()["bunnyData"]["b1"]["bunny"]["weight"] == 1190

    after = len(client.get("/api/bootstrap").json()["bunnyData"]["b1"]["weightRecords"])
    assert after == before + 1

    r = client.patch(f"/api/weight-records/{record_id}", json={"weight": 1205})
    assert r.status_code == 200
    assert r.json()["weight"] == 1205
    assert client.get("/api/bootstrap").json()["bunnyData"]["b1"]["bunny"]["weight"] == 1205

    r = client.post(
        "/api/weight-records",
        json={"bunnyId": "b1", "date": "2025-05", "weight": 999},
    )
    assert r.status_code == 409

    r = client.delete(f"/api/weight-records/{record_id}")
    assert r.status_code == 204


def test_schema_v2_tables(client: TestClient) -> None:
    _seed(client)
    from sqlalchemy import inspect

    from app.database import engine

    tables = set(inspect(engine).get_table_names())
    assert tables >= {
        "bunnies",
        "timeline_events",
        "weight_records",
        "health_records",
        "photos",
        "app_settings",
    }


def test_health_record_crud(client: TestClient) -> None:
    _seed(client)
    r = client.post(
        "/api/health-records",
        json={
            "bunnyId": "b1",
            "date": "2025-05-26",
            "type": "checkup",
            "description": "体检",
            "status": "正常",
        },
    )
    assert r.status_code == 201
    assert r.json()["date"] == "2025.05.26"
    record_id = r.json()["id"]

    r = client.patch(f"/api/health-records/{record_id}", json={"status": "复查"})
    assert r.status_code == 200
    assert r.json()["status"] == "复查"

    r = client.delete(f"/api/health-records/{record_id}")
    assert r.status_code == 204


def test_photo_crud(client: TestClient) -> None:
    _seed(client)
    r = client.post(
        "/api/photos",
        json={
            "bunnyId": "b1",
            "src": "/assets/photo-1-sunbath.jpg",
            "date": "2025.05.26",
            "description": "新照片",
            "year": 2025,
            "tags": ["臭臭"],
        },
    )
    assert r.status_code == 201
    assert r.json()["date"] == "2025.05.26"
    photo_id = r.json()["id"]

    r = client.patch(f"/api/photos/{photo_id}", json={"description": "更新"})
    assert r.status_code == 200

    r = client.delete(f"/api/photos/{photo_id}")
    assert r.status_code == 204


def test_upload(client: TestClient) -> None:
    png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x01\x01\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    r = client.post(
        "/api/uploads",
        files={"file": ("test.png", BytesIO(png), "image/png")},
    )
    assert r.status_code == 200
    url = r.json()["url"]
    assert url.startswith("/uploads/") or url.startswith("http")
    if url.startswith("/uploads/"):
        assert client.get(url).status_code == 200


def test_avatar_upload(client: TestClient) -> None:
    _seed(client)
    png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x01\x01\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    r = client.post(
        "/api/bunnies/b1/avatar",
        files={"file": ("avatar.png", BytesIO(png), "image/png")},
    )
    assert r.status_code == 200
    url = r.json()["url"]
    assert url.startswith("/uploads/") or url.startswith("http")
    assert client.get("/api/bootstrap").json()["bunnyData"]["b1"]["bunny"]["avatar"] == url


def test_delete_bunny_cascades(client: TestClient) -> None:
    _seed(client)
    r = client.delete("/api/bunnies/b2")
    assert r.status_code == 204
    body = client.get("/api/bootstrap").json()
    assert "b2" not in body["bunnyData"]
    assert all(b["id"] != "b2" for b in body["bunnies"])
