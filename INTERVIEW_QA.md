# production-ml-platform — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does production-ml-platform address, and what can you demonstrate?

Data → validate → train → registry → deploy check → monitor → drift → retrain recommendation. Kubernetes apply stays false.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/mlplat/main.py`](src/mlplat/main.py): Implementation or supporting configuration.
- [`src/mlplat/pipeline.py`](src/mlplat/pipeline.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`tests/test_mlplat.py`](tests/test_mlplat.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `validate` and explain the decision it makes?

The main walkthrough here is `validate(rows)` in [`src/mlplat/pipeline.py`](src/mlplat/pipeline.py#L4).

```python
def validate(rows):
    if not isinstance(rows, list) or len(rows) < 8:
        raise ValueError("need at least 8 rows")
    if any("label" not in row for row in rows):
        raise ValueError("label required")
    return {"ok": True, "rows": len(rows)}
```

The implementation calls `ValueError`, `any`, `isinstance`, `len`. In an interview, trace those calls in execution order using a fixture input.

## 4. What responsibility does `promote` have?

`promote(name)` is defined in [`src/mlplat/pipeline.py`](src/mlplat/pipeline.py#L15).

Its return expressions include:

- `{'champion': name, 'applied': False}`

It uses `ValueError`. This is the code path I would compare against the caller to explain responsibility boundaries.

## 5. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `HTTPException(422, str(exc))` in [`src/mlplat/main.py`](src/mlplat/main.py#L14).
- `HTTPException(422, str(exc))` in [`src/mlplat/main.py`](src/mlplat/main.py#L25).
- `ValueError('need at least 8 rows')` in [`src/mlplat/pipeline.py`](src/mlplat/pipeline.py#L6).
- `ValueError('label required')` in [`src/mlplat/pipeline.py`](src/mlplat/pipeline.py#L8).
- `ValueError('unknown model')` in [`src/mlplat/pipeline.py`](src/mlplat/pipeline.py#L17).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 6. Which test would you use to demonstrate correctness?

[`tests/test_mlplat.py`](tests/test_mlplat.py#L5) contains `test_pipeline_gates`:

```python
def test_pipeline_gates():
    rows = [{"label": i % 2} for i in range(10)]
    assert client.post("/validate", json={"rows": rows}).json()["ok"] is True
    client.post("/register", json={"name": "v2", "metrics": {"auc": 0.9}})
    assert client.post("/promote", json={"name": "v2"}).json()["applied"] is False
    assert client.post("/drift", json={"train_mean": 0, "live_mean": 5, "train_std": 1}).json()["retrain"] is True
    assert client.post("/deploy/check", json={"image": "ml:latest"}).json()["passed"] is False
    assert client.post("/validate", json={"rows": [1,2]}).status_code == 422
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 7. What HTTP interface does the code expose?

- `GET /healthz` → `healthz` in [`src/mlplat/main.py`](src/mlplat/main.py#L6).
- `POST /validate` → `post_validate` in [`src/mlplat/main.py`](src/mlplat/main.py#L10).
- `POST /register` → `post_register` in [`src/mlplat/main.py`](src/mlplat/main.py#L17).
- `POST /promote` → `post_promote` in [`src/mlplat/main.py`](src/mlplat/main.py#L21).
- `POST /drift` → `post_drift` in [`src/mlplat/main.py`](src/mlplat/main.py#L28).
- `POST /deploy/check` → `post_deploy` in [`src/mlplat/main.py`](src/mlplat/main.py#L32).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 8. Where does state live, and what happens with multiple workers?

Module-level containers include `REGISTRY` in [`src/mlplat/pipeline.py`](src/mlplat/pipeline.py).

These containers belong to a Python process. Inspect which are constant fixtures and which are mutated. Mutable process state needs an explicit shared-storage or synchronization strategy before multiple workers can provide consistent behavior.

## 9. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 10. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 11. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 12. What is the input-to-output contract of `validate`?

In [`src/mlplat/pipeline.py`](src/mlplat/pipeline.py#L4), `validate(rows)` receives the inputs. The function computes these intermediate values:

The implementation delegates or iterates directly; trace the calls in the source walkthrough.

Its result is defined by:

- `{'ok': True, 'rows': len(rows)}`

## 13. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/mlplat/pipeline.py`](src/mlplat/pipeline.py#L4) branches on:

- `not isinstance(rows, list) or len(rows) < 8`
- `any(('label' not in row for row in rows))`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
