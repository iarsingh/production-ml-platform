from fastapi.testclient import TestClient
from mlplat.main import app
client = TestClient(app)

def test_pipeline_gates():
    rows = [{"label": i % 2} for i in range(10)]
    assert client.post("/validate", json={"rows": rows}).json()["ok"] is True
    client.post("/register", json={"name": "v2", "metrics": {"auc": 0.9}})
    assert client.post("/promote", json={"name": "v2"}).json()["applied"] is False
    assert client.post("/drift", json={"train_mean": 0, "live_mean": 5, "train_std": 1}).json()["retrain"] is True
    assert client.post("/deploy/check", json={"image": "ml:latest"}).json()["passed"] is False
    assert client.post("/validate", json={"rows": [1,2]}).status_code == 422
