# Production ML Platform

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/mlplat/main.py`](src/mlplat/main.py) | HTTP handlers: `GET /healthz`, `POST /validate`, `POST /register`, `POST /promote`, `POST /drift` |
| [`src/mlplat/pipeline.py`](src/mlplat/pipeline.py) | Functions: `validate`, `register`, `promote`, `drift`, `deploy_check` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`tests/test_mlplat.py`](tests/test_mlplat.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

To serve the FastAPI application locally, install the server separately if it is not already available:

```bash
python -m pip install uvicorn
PYTHONPATH=src python -m uvicorn mlplat.main:app --reload
```

<!-- project-guide:end -->

Phase 2

Skills: validation, registry, deploy gate, drift, retrain

Data → validate → train → registry → deploy check → monitor → drift → retrain recommendation. Kubernetes apply stays false.

```bash
pip install -r requirements.txt
pytest -q
```

Laptop proof. No hosted model. Cluster apply stays false until a human approves.

## Ops plane

Workspaces, tenant isolation, job approval, and audit live under `/v1`. Production apply is refused. See `docs/ARCHITECTURE.md`.

## Documentation checks

Project architecture, interview guides, and local source links are checked automatically on pushes and pull requests. Run the same check locally:

```bash
python3 .github/scripts/validate_project_docs.py
```

See [service improvements and local run instructions](docs/UPGRADES.md).
