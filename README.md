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

## Submission Highlights

- Concrete Hy3 scenario: open-source repository reproduction, not a generic chat UI.
- Evidence-grounded workflow: zip extraction preserves file paths and asks Hy3 to cite repository evidence.
- Full loop: analyze repository, diagnose terminal error, and generate a report for issues or PRs.
- Practical developer UX: upload, paste, copy, and demo inputs are included.
- Safer implementation details: zip paths are validated before extraction, and model-rendered Markdown is sanitized in the browser.

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

### Requirements

- Python 3.10+ with `venv` and `pip`
- Node.js 18+ with `npm`
- Network access to PyPI, npm registry, and the Hy3 API endpoint
- A Hy3-compatible API key
- Free local ports `8000` and `5173`

See [REQUIREMENTS.md](REQUIREMENTS.md) for the full dependency checklist.

### 1. Configure Hy3

Copy `.env.example` to either the repository root or `apps/api/.env`, then set your key:

```bash
HY3_API_KEY=your_key_here
HY3_BASE_URL=https://tokenhub.tencentmaas.com/v1
HY3_MODEL=hy3
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Never commit real API keys.

### 2. One-Click Startup

Run the startup script for your platform from the repository root.

Windows PowerShell:

```powershell
.\start.ps1
```

Windows Command Prompt:

```bat
start.bat
```

macOS / Linux:

```bash
chmod +x ./start.sh
./start.sh
```

The scripts install missing backend and frontend dependencies, then start:

- API: `http://127.0.0.1:8000`
- Web: `http://127.0.0.1:5173`

They do not install system dependencies such as Python or Node.js. Install those first on a new computer.

Press `Ctrl+C` in PowerShell/macOS/Linux, or close the two windows opened by `start.bat`, to stop the project.

### Manual Startup

Use these commands if you want to run the two services separately.

Backend:

```bash
cd "apps/api"
python -m venv .venv

# Windows
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# macOS / Linux
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd "apps/web"
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Open `http://127.0.0.1:5173`.

## Troubleshooting

- `HY3_API_KEY is not configured`: create `.env` from `.env.example` and replace the placeholder key.
- `Python was not found`: install Python 3.10+ and make sure `python`, `python3`, or `py` is available in your terminal.
- `Node.js package manager was not found`: install Node.js 18+ with npm, or install pnpm.
- `npm warn allow-scripts ... esbuild`: this is an npm security warning, not an install failure. If the web app starts normally, you can ignore it. If Vite later fails with an `esbuild` error, run `cd apps/web`, then `npm approve-scripts --allow-scripts-pending`, approve `esbuild`, and run the startup script again.
- Port already in use: stop the existing process on `8000` or `5173`, or edit the startup script port arguments.
- Model calls fail but `/health` works: check `HY3_API_KEY`, `HY3_BASE_URL`, and `HY3_MODEL`.

## End-to-End Demos

- Demo 1: Analyze a React/Vite project and generate a runnable reproduction plan.
- Demo 2: Diagnose a Python `ModuleNotFoundError` from a terminal log and produce a repair checklist.

See [docs/demo-1-react.md](docs/demo-1-react.md) and [docs/demo-2-python-error.md](docs/demo-2-python-error.md).

## Submission Notes

See [SUBMISSION.md](SUBMISSION.md) for the issue response draft, demo checklist, and reviewer-facing project summary.

## GitHub Project Management

Use GitHub Issues and Projects with the workflow in [.github/PROJECT_MANAGEMENT.md](.github/PROJECT_MANAGEMENT.md). Suggested labels:

- `feature`
- `bug`
- `demo`
- `docs`
- `hy3-prompt`
- `frontend`
- `backend`
