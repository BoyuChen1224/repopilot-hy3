from __future__ import annotations

import os
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()
load_dotenv(Path(__file__).resolve().parents[3] / ".env")

MAX_FILE_CHARS = 12000
MAX_TOTAL_CHARS = 48000
IMPORTANT_NAMES = {
    "readme.md",
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "poetry.lock",
    "pdm.lock",
    "dockerfile",
    "docker-compose.yml",
    "vite.config.ts",
    "vite.config.js",
    "next.config.js",
    "tsconfig.json",
    "main.py",
    "app.py",
}
IMPORTANT_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".md", ".json", ".toml", ".yaml", ".yml"}


class AnalyzeTextRequest(BaseModel):
    project_notes: str = Field(default="", description="README, file tree, or project notes pasted by the user")
    error_log: str = Field(default="", description="Optional terminal error log")


class DiagnoseRequest(BaseModel):
    project_context: str = ""
    error_log: str


class ReportRequest(BaseModel):
    analysis: str
    diagnosis: str = ""


app = FastAPI(title="RepoPilot Hy3 API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def hy3_client() -> OpenAI:
    api_key = os.getenv("HY3_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="HY3_API_KEY is not configured")
    return OpenAI(
        api_key=api_key,
        base_url=os.getenv("HY3_BASE_URL", "https://tokenhub.tencentmaas.com/v1"),
    )


def call_hy3(messages: list[dict[str, str]], temperature: float = 0.25) -> str:
    client = hy3_client()
    response = client.chat.completions.create(
        model=os.getenv("HY3_MODEL", "hy3"),
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""


def should_include(path: Path) -> bool:
    name = path.name.lower()
    if name in IMPORTANT_NAMES:
        return True
    return path.suffix.lower() in IMPORTANT_SUFFIXES and path.stat().st_size <= 80_000


def read_text(path: Path) -> str:
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    return content[:MAX_FILE_CHARS]


def summarize_directory(root: Path) -> str:
    parts: list[str] = []
    total = 0
    files = [p for p in root.rglob("*") if p.is_file()]
    tree = "\n".join(str(p.relative_to(root)).replace("\\", "/") for p in files[:180])
    parts.append(f"# File Tree\n{tree}")

    for path in files:
        if not should_include(path):
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        content = read_text(path)
        if not content:
            continue
        block = f"\n\n# File: {rel}\n```text\n{content}\n```"
        if total + len(block) > MAX_TOTAL_CHARS:
            break
        parts.append(block)
        total += len(block)
    return "\n".join(parts)


def extract_zip(upload: UploadFile) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        archive_path = Path(tmp) / "project.zip"
        archive_path.write_bytes(upload.file.read())
        try:
            with zipfile.ZipFile(archive_path) as archive:
                archive.extractall(Path(tmp) / "src")
        except zipfile.BadZipFile as exc:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid zip") from exc
        return summarize_directory(Path(tmp) / "src")


SYSTEM_PROMPT = """You are RepoPilot Hy3, a rigorous open-source project reproduction agent.
Your job is to help developers run unfamiliar repositories.
Ground conclusions in provided files and logs. If evidence is missing, say what to inspect next.
Return concise Markdown with practical commands, risks, and verification steps."""


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze-text")
def analyze_text(payload: AnalyzeTextRequest) -> dict[str, Any]:
    context = payload.project_notes.strip()
    if payload.error_log.strip():
        context += f"\n\n# Error Log\n{payload.error_log.strip()}"
    if not context:
        raise HTTPException(status_code=400, detail="project_notes or error_log is required")
    content = call_hy3(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""Analyze this project context and produce:
1. Project profile
2. Detected stack and evidence
3. Reproduction checklist
4. Likely run commands
5. Risk points
6. Verification plan

Project context:
{context[:MAX_TOTAL_CHARS]}""",
            },
        ]
    )
    return {"analysis": content}


@app.post("/analyze-zip")
def analyze_zip(file: UploadFile = File(...), error_log: str = Form(default="")) -> dict[str, Any]:
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Please upload a .zip file")
    context = extract_zip(file)
    if error_log.strip():
        context += f"\n\n# Error Log\n{error_log.strip()}"
    content = call_hy3(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""Use the extracted repository evidence to create a reproduction plan.
Include file-backed evidence for each major claim.

Repository evidence:
{context[:MAX_TOTAL_CHARS]}""",
            },
        ]
    )
    return {"analysis": content, "context_preview": context[:8000]}


@app.post("/diagnose-error")
def diagnose_error(payload: DiagnoseRequest) -> dict[str, Any]:
    if not payload.error_log.strip():
        raise HTTPException(status_code=400, detail="error_log is required")
    content = call_hy3(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""Diagnose this terminal error for a repository reproduction workflow.
Return likely root causes, evidence, commands to try, code/config changes to inspect, and a short prevention note.

Project context:
{payload.project_context[:18000]}

Error log:
{payload.error_log[:18000]}""",
            },
        ]
    )
    return {"diagnosis": content}


@app.post("/generate-report")
def generate_report(payload: ReportRequest) -> dict[str, Any]:
    content = call_hy3(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""Turn the following analysis into a polished Markdown reproduction report.
Use sections: Environment, Project Summary, Setup Steps, Run Steps, Error Diagnosis, Verification, Open Questions.

Analysis:
{payload.analysis}

Diagnosis:
{payload.diagnosis}""",
            },
        ],
        temperature=0.2,
    )
    return {"report": content}

