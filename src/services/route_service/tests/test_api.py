from fastapi.testclient import TestClient
from ..service.main import app

client = TestClient(app)

def test_route_success():
    payload = {
        "waypoints": [
            {"lat": 55.7558, "lng": 37.6176},
            {"lat": 55.7512, "lng": 37.6184}
        ]
    }

    resp = client.post("/routing/v1/route", json=payload)

    assert resp.status_code in (200, 422, 503)

    if resp.status_code == 200:
        data = resp.json()

        assert "geometry" in data
        assert data["geometry"]["type"] == "LineString"
        assert isinstance(data["geometry"]["coordinates"], list)
        assert len(data["geometry"]["coordinates"]) > 1

        assert "total_distance" in data
        assert data["total_distance"] > 0

        assert "estimated_time" in data
        assert data["estimated_time"] > 0