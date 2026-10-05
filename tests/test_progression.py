from mlplat.progression import mlops

def test_mlops_stages_and_no_apply():
    rows = [{"x": 1, "label": 0} for _ in range(8)]
    out = mlops(rows, live_mean=1)
    assert "retraining" in out["stages"]
    assert out["applied"] is False

