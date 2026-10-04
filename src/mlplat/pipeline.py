REGISTRY = {"champion": {"version": "1", "metrics": {"auc": 0.81}}}
DRIFT_Z = 2.0

def validate(rows):
    if not isinstance(rows, list) or len(rows) < 8:
        raise ValueError("need at least 8 rows")
    if any("label" not in row for row in rows):
        raise ValueError("label required")
    return {"ok": True, "rows": len(rows)}

def register(name, metrics):
    REGISTRY[name] = {"version": str(len(REGISTRY)+1), "metrics": metrics or {}}
    return REGISTRY[name]

def promote(name):
    if name not in REGISTRY:
        raise ValueError("unknown model")
    REGISTRY["champion"] = REGISTRY[name]
    return {"champion": name, "applied": False}

def drift(train_mean, live_mean, train_std=1.0):
    z = abs(live_mean - train_mean) / (train_std or 1)
    return {"z": round(z, 4), "drift": z >= DRIFT_Z, "retrain": z >= DRIFT_Z}

def deploy_check(image):
    failed = []
    if str(image).endswith(":latest") or image == "latest":
        failed.append("latest")
    return {"passed": not failed, "failed": failed, "applied": False}
