from mlplat.ops import router as ops_router
from fastapi import FastAPI, HTTPException
from mlplat.pipeline import deploy_check, drift, promote, register, validate
app = FastAPI(title="Production ML Platform")
app.include_router(ops_router, prefix="/v1")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/validate")
def post_validate(body: dict):
    try:
        return validate(body.get("rows"))
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

@app.post("/register")
def post_register(body: dict):
    return register(body.get("name") or "run", body.get("metrics"))

@app.post("/promote")
def post_promote(body: dict):
    try:
        return promote(body.get("name"))
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

@app.post("/drift")
def post_drift(body: dict):
    return drift(float(body.get("train_mean", 0)), float(body.get("live_mean", 0)), float(body.get("train_std") or 1))

@app.post("/deploy/check")
def post_deploy(body: dict):
    return deploy_check(body.get("image"))
