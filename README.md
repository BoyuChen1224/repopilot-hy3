# RepoPilot Hy3

RepoPilot Hy3 is an open-source project reproduction and error diagnosis assistant powered by Hy3. It helps developers understand unfamiliar repositories, produce runnable setup plans, diagnose terminal errors, and generate reproducible reports.

This project is designed for [Tencent-Hunyuan/Hy3 Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4): it demonstrates Hy3 in a concrete developer productivity scenario with an interactive frontend, backend API calls, and end-to-end demos.

## Why This Scenario

Reproducing a new repository is a common pain point: docs are incomplete, dependency versions drift, and terminal errors are noisy. RepoPilot Hy3 uses Hy3 as a development reproduction agent that reads project evidence, reasons over code and logs, and returns practical next steps with source-backed explanations.

## Hy3 Role

Hy3 is the core reasoning engine in this application. It is responsible for:

- Understanding repository structure, dependency files, framework hints, and README content.
- Generating a step-by-step reproduction plan.
- Diagnosing pasted terminal errors with likely causes and fixes.
- Producing a reproducibility report suitable for README, issue, or PR documentation.
- Keeping responses grounded in uploaded files and user-provided logs.

The app does not fine-tune or locally run a model. All intelligent analysis is performed through the Hy3 API.

## Features

- Upload a project zip or paste repository notes.
- Extract important files such as `README.md`, `package.json`, `requirements.txt`, `pyproject.toml`, `Dockerfile`, and config files.
- Generate project profile, run commands, risk points, and verification steps.
- Diagnose errors from terminal logs.
- Generate a Markdown reproduction report.
- Interactive web UI with copy-friendly results.

## Project Structure

```text
RepoPilot Hy3/
  apps/
    api/                 # FastAPI backend
    web/                 # Vite React frontend
  docs/                  # demo scripts and Hy3 role notes
  examples/              # small demo inputs
  .github/               # issue templates and project management docs
  README.md
```

## Quick Start

### 1. Configure Hy3

Create `apps/api/.env` or a root `.env` file:

```bash
HY3_API_KEY=your_key_here
HY3_BASE_URL=https://tokenhub.tencentmaas.com/v1
HY3_MODEL=hy3
```

Never commit real API keys.

### 2. Start Backend

```bash
cd "apps/api"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Start Frontend

```bash
cd "apps/web"
npm install
npm run dev
```

Open the Vite URL shown in the terminal.

## End-to-End Demos

- Demo 1: Analyze a React/Vite project and generate a runnable reproduction plan.
- Demo 2: Diagnose a Python `ModuleNotFoundError` from a terminal log and produce a repair checklist.

See [docs/demo-1-react.md](docs/demo-1-react.md) and [docs/demo-2-python-error.md](docs/demo-2-python-error.md).

## GitHub Project Management

Use GitHub Issues and Projects with the workflow in [.github/PROJECT_MANAGEMENT.md](.github/PROJECT_MANAGEMENT.md). Suggested labels:

- `feature`
- `bug`
- `demo`
- `docs`
- `hy3-prompt`
- `frontend`
- `backend`

