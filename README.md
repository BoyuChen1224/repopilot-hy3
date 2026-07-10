<div align="center">

[中文](README_CN.md) | English

# RepoPilot Hy3

**A Hy3-powered repository reproduction and error diagnosis assistant.**

Turn repository evidence and terminal logs into runnable setup plans, actionable diagnoses, and reusable Markdown reports.

</div>

---

## Table of Contents

- [Overview](#overview)
- [Issue #4 Checklist](#issue-4-checklist)
- [How Hy3 Powers RepoPilot](#how-hy3-powers-repopilot)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quickstart](#quickstart)
- [End-to-End Demos](#end-to-end-demos)
- [Backend API](#backend-api)
- [Troubleshooting](#troubleshooting)
- [CodeBuddy Collaboration](#codebuddy-collaboration)
- [Security Notes](#security-notes)
- [Related Documentation](#related-documentation)

---

## Overview

Reproducing an unfamiliar repository is rarely just a matter of running one command. Documentation may be incomplete, dependency versions drift, entry points are unclear, and terminal output is often too noisy to diagnose quickly.

RepoPilot Hy3 turns that workflow into an interactive developer tool. Upload a project zip or paste repository notes, add an optional error log, and let Hy3 produce:

- A project profile grounded in repository files.
- Detected frameworks, runtimes, package managers, and entry points.
- A step-by-step reproduction checklist with likely run commands.
- Root-cause hypotheses and repair steps for terminal errors.
- A copy-ready Markdown reproduction report for a README, Issue, or PR.

This project was created for [Tencent-Hunyuan/Hy3 Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4), which asks participants to build an end-to-end application powered by the Hy3 API in a concrete real-world scenario.

## Issue #4 Checklist

| Issue requirement | Status in this repository | Evidence |
| --- | --- | --- |
| Use the Hy3 API without training, fine-tuning, or local inference | Complete | The FastAPI backend calls a configurable Hy3-compatible OpenAI API |
| Provide at least one interactive frontend | Complete | Bilingual React/Vite web interface with upload, text input, actions, tabs, and copy controls |
| Run at least two end-to-end demo flows | Complete | React/Vite reproduction and Python error diagnosis demos are documented below |
| Attach a video or GIF no longer than two minutes | Complete | Two 1080p walkthroughs are available under [Demo videos](#demo-videos); each is under one minute |
| Make project source available and explain Hy3's role | Documented | Repository source is public and Hy3 responsibilities are described below; this README makes no license claim |
| Record CodeBuddy-assisted work | Documented | Collaboration areas are listed in [CodeBuddy Collaboration](#codebuddy-collaboration) |

## How Hy3 Powers RepoPilot

Hy3 is the reasoning engine of RepoPilot, not a local dependency or a generic chat widget. The application uses Hy3 to:

- Understand README content, dependency manifests, configuration files, file trees, and terminal logs.
- Infer the project stack and produce evidence-backed setup instructions.
- Diagnose installation and runtime errors with likely causes, commands, and verification steps.
- Convert prior analysis and diagnosis into a structured Markdown reproduction report.

```text
Developer input
    -> React web UI
    -> FastAPI evidence extraction and prompt construction
    -> Hy3 API
    -> sanitized, copyable Markdown
```

All model intelligence is accessed through the configured API endpoint. RepoPilot Hy3 performs **no model training, fine-tuning, local inference, or local model deployment**.

For uploaded archives, the backend validates zip paths before extraction, selects relevant text files, and bounds the submitted context. The frontend sanitizes model-generated Markdown before rendering it.

## Features

- Upload a project `.zip` or paste a README, file tree, configuration, and setup notes.
- Extract high-value evidence from files such as `README.md`, `package.json`, `requirements.txt`, `pyproject.toml`, `Dockerfile`, and framework configs.
- Generate project profiles, likely commands, risks, and verification plans.
- Diagnose pasted terminal errors and stack traces.
- Generate reusable Markdown reproduction reports.
- Switch the web interface between English and Chinese.
- Copy analysis, diagnosis, and report results directly from the UI.

## Project Structure

```text
RepoPilot Hy3/
├── apps/
│   ├── api/                  # FastAPI backend and Hy3 API integration
│   └── web/                  # React/Vite interactive frontend
├── docs/                     # Demo guides and Hy3 role notes
├── examples/                 # Bundled demo inputs
├── video/                    # Demo 1 and Demo 2 walkthrough videos
├── .env.example              # Hy3 API configuration template
├── start.ps1                 # One-click startup for PowerShell
├── start.bat                 # One-click startup for Command Prompt
├── start.sh                  # One-click startup for macOS/Linux
├── README.md                 # English documentation
└── README_CN.md              # Chinese documentation
```

## Quickstart

### Requirements

- Python 3.10+ with `venv` and `pip`.
- Node.js 18+ with `npm` (or `pnpm`).
- Network access to the Python and JavaScript package registries and the configured Hy3 API endpoint.
- A Hy3-compatible API key.
- Free local ports `8000` and `5173`.

See [REQUIREMENTS.md](REQUIREMENTS.md) for the complete environment checklist and platform-specific notes.

### 1. Clone and configure

```bash
git clone https://github.com/BoyuChen1224/repopilot-hy3.git
cd repopilot-hy3
```

Copy the environment template:

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

```bat
:: Windows Command Prompt
copy .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

Edit `.env` and replace the API-key placeholder:

```dotenv
HY3_API_KEY=your_hy3_api_key
HY3_BASE_URL=https://tokenhub.tencentmaas.com/v1
HY3_MODEL=hy3
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Never commit a real API key. The backend also accepts `apps/api/.env` if you prefer service-local configuration.

### 2. Start both services

Run one command from the repository root.

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

The startup script creates the backend virtual environment when needed, installs project dependencies, and starts both services:

| Service | URL |
| --- | --- |
| Web interface | `http://127.0.0.1:5173` |
| Backend API | `http://127.0.0.1:8000` |
| Interactive API docs | `http://127.0.0.1:8000/docs` |
| Health check | `http://127.0.0.1:8000/health` |

The API root `/` is not a web page and may return `404`; open the web interface or API docs instead.

### 3. Verify the deployment

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Then open `http://127.0.0.1:5173` and run [Demo 1](#demo-1-reactvite-project-reproduction).

### Manual startup

Use separate terminals when you need to inspect each service independently.

Backend:

```bash
cd apps/api
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
cd apps/web
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

## End-to-End Demos

### Demo 1: React/Vite project reproduction

**Input:** [`examples/demo-react-app.zip`](examples/demo-react-app.zip)

**Flow:**

1. Open the web interface.
2. Upload `examples/demo-react-app.zip`.
3. Select **Analyze** to generate an evidence-backed reproduction plan.
4. Review the Analysis tab, then select **Report**.

**Expected output:** Hy3 identifies Vite and React from repository evidence, recommends Node.js/npm commands, highlights risks such as runtime-version mismatch or a missing lockfile, provides verification steps, and produces a reusable Markdown report.

Detailed guide: [docs/demo-1-react.md](docs/demo-1-react.md)

### Demo 2: Python error diagnosis

**Input:** Paste the project context from [`examples/demo-python-error/README.md`](examples/demo-python-error/README.md) and the `ModuleNotFoundError` log from [`docs/demo-2-python-error.md`](docs/demo-2-python-error.md).

**Flow:**

1. Paste the project context into **Project notes or README**.
2. Paste the terminal log into **Error log**.
3. Select **Analyze**, then **Diagnose**.
4. Review the likely cause and repair steps, then select **Report**.

**Expected output:** Hy3 identifies the missing `requests` dependency, grounds the diagnosis in `requirements.txt`, recommends a virtual environment and `pip install -r requirements.txt`, and verifies the repair with `python main.py`.

Detailed guide: [docs/demo-2-python-error.md](docs/demo-2-python-error.md)

### Demo videos

| Demo | Video | Duration | Resolution |
| --- | --- | --- | --- |
| React/Vite project reproduction | [Watch Demo 1](video/Demo_1.mp4) | 00:47 | 1920×1080 |
| Python error diagnosis | [Watch Demo 2](video/Demo_2.mp4) | 00:59 | 1920×1080 |

Both walkthroughs are shorter than the two-minute limit in Issue #4. If the browser does not play an MP4 inline, open the linked file from its GitHub file page.

## Backend API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Verify that the backend is running |
| `POST` | `/analyze-text` | Analyze pasted project notes and an optional error log |
| `POST` | `/analyze-zip` | Extract and analyze an uploaded project zip |
| `POST` | `/diagnose-error` | Diagnose a terminal error using project context |
| `POST` | `/generate-report` | Convert analysis and diagnosis into a Markdown report |

Open `http://127.0.0.1:8000/docs` for request schemas and an interactive API client.

## Troubleshooting

- **`HY3_API_KEY is not configured`:** create `.env` from `.env.example` and replace the placeholder with a valid key.
- **Python was not found:** install Python 3.10+ and ensure `python`, `python3`, or `py` is available in your terminal.
- **Node.js package manager was not found:** install Node.js 18+ with npm, or install pnpm.
- **Port already in use:** stop the process using `8000` or `5173`, or pass different ports to the startup script where supported.
- **The API health check works but model calls fail:** verify `HY3_API_KEY`, `HY3_BASE_URL`, and `HY3_MODEL`.
- **npm warns about an unapproved `esbuild` install script:** if Vite does not start, run `npm approve-scripts --allow-scripts-pending` under `apps/web`, approve `esbuild`, and retry.

More details: [REQUIREMENTS.md](REQUIREMENTS.md)

## CodeBuddy Collaboration

CodeBuddy-assisted development covered the following project areas:

- FastAPI endpoints and the Hy3-compatible API integration.
- React/Vite interactive frontend, bilingual UI copy, result tabs, and copy actions.
- Repository zip evidence extraction and archive-path validation.
- Prompt design for analysis, diagnosis, and report generation.
- Cross-platform one-click startup scripts and environment handling.
- Demo inputs, issue-facing notes, troubleshooting guidance, and bilingual README organization.

The final project behavior and documentation were reviewed against the checked-in source and the Issue #4 requirements.

## Security Notes

- Keep real API keys only in `.env` or your process environment; do not commit them.
- Zip member paths are validated before extraction to prevent archive path traversal.
- Uploaded repository context is size-limited before it is sent to the configured API.
- Model-generated Markdown is sanitized with DOMPurify before browser rendering.
- Review generated commands before running them in an unfamiliar environment.

## Related Documentation

- [Environment requirements](REQUIREMENTS.md)
- [Hy3 role and prompting principles](docs/hy3-role.md)
- [Demo 1 guide](docs/demo-1-react.md)
- [Demo 2 guide](docs/demo-2-python-error.md)
- [Issue #4](https://github.com/Tencent-Hunyuan/Hy3/issues/4)
- [Tencent-Hunyuan/Hy3](https://github.com/Tencent-Hunyuan/Hy3)
