# RepoPilot Hy3

English | [中文](README_CN.md)

RepoPilot Hy3 is a local repository reproduction and development collaboration assistant. It analyzes project files, GitHub data, and error logs, then produces evidence-backed guidance and reports.

## Features

- Analyze ZIP archives or pasted project notes, diagnose errors, and generate Markdown reports.
- Import ZIP projects into the workspace or connect GitHub-compatible repositories for Issue, PR, and CI data.
- Use project-aware chat, workspace search, tools, Skills, and multi-agent workflows.
- Upload knowledge documents, retrieve cited evidence, manage project memory, and browse code relationships.
- Generate reports and manage multi-repository workspaces, action drafts, feedback, and audit records.
- Run RAGAS evaluations and compare results. Fixed evaluation datasets are user-provided; the automatic document smoke suite only checks that the pipeline runs.

The default setup uses React/Vite, FastAPI, and SQLite on the local machine. Generation is performed through a remote model API.

## Setup

Install Python 3.11+, Node.js 18+, npm or pnpm, and obtain a model API key. Copy `.env.example` to `.env` in the project root:

```dotenv
HY3_API_KEY=your_api_key
HY3_BASE_URL=https://tokenhub.tencentmaas.com/v1
HY3_MODEL=hy4-flash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

`HY3_MODEL` selects the generation model. Never commit `.env` or real credentials.

Run `./start.ps1` on Windows PowerShell, `start.bat` in Command Prompt, or `./start.sh` on macOS/Linux. The web app defaults to `http://127.0.0.1:5173`, API docs to `http://127.0.0.1:8000/docs`, and health to `http://127.0.0.1:8000/health`.

The home page provides a project reproduction workflow. Import a ZIP or add a local directory from the Repositories page to make files available to workspace search; local directories do not require Git and are not copied. Issue, PR, and CI synchronization require a connected remote repository.

## Retrieval services

The default SQLite setup uses keyword retrieval and deterministic demo embeddings. Vector-store status is explicitly `degraded`; this is not full semantic retrieval. For full vector retrieval, start `docker compose up -d postgres etcd minio milvus`, enable Milvus, and configure an independent OpenAI-compatible embedding service:

```dotenv
MILVUS_ENABLED=true
MILVUS_URI=http://127.0.0.1:19530
MILVUS_COLLECTION=repopilot_rag_v1
EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_BASE_URL=https://your-embedding-service.example/v1
EMBEDDING_API_KEY=your_embedding_key
EMBEDDING_MODEL=your_embedding_model
EMBEDDING_DIMENSIONS=1024
```

The service must expose `/embeddings` and return the configured dimensions. SQLite can continue to store application data; setting `DATABASE_URL` to PostgreSQL selects a separate database and does not migrate existing data automatically.

An independent reranker can be configured with `RERANK_BASE_URL`, `RERANK_API_KEY`, and `RERANK_MODEL`. It must accept `model`, `query`, `documents`, and `top_n`, and return `results` with indices and relevance scores. `RERANK_INSTRUCTION` is optional. A failed remote reranker is visibly recorded as a heuristic fallback.

Use a new Milvus collection after changing embedding models or dimensions, then reindex each existing project's knowledge base. Do not mix vector spaces.

## Evaluation and local data

The evaluation page supports RAGAS runs, traces, and comparisons. Bring your own fixed JSON suite under `docs/datas/evals/` or use the document smoke suite. A working Judge model is required for semantic scoring.

Local databases, uploaded files, imported project copies, and an automatically generated token-encryption key live under `.data/` and are ignored by Git. You can alternatively configure `TOKEN_ENCRYPTION_KEY`; keep the corresponding key when backing up the database. The local API is intended for loopback use and does not implement multi-user login.

Run `pnpm test` and `pnpm build` in `apps/web`, and `python -m pytest app/tests` in `apps/api`. Real model, GitHub, embedding, rerank, and Milvus tests require their respective credentials and services.
