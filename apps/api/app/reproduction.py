from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from openai import OpenAI
from pydantic import BaseModel, Field

from app.core.config import settings

MAX_FILE_CHARS = 12000
MAX_TOTAL_CHARS = 48000
MAX_LOG_CHARS = 12000
MAX_UPLOAD_BYTES = 50 * 1024 * 1024
MAX_EXTRACTED_BYTES = 200 * 1024 * 1024
MAX_MEMBER_BYTES = 16 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 10000
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".next", ".data", ".ssh", ".aws", ".gnupg", ".azure", ".kube", "dist", "build", "coverage"}
SECRET_FILENAMES = {".env", ".env.local", ".env.production", ".npmrc", ".pypirc", "credentials.json"}
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


router = APIRouter()

def hy3_client() -> OpenAI:
    api_key = settings.llm_api_key
    if not api_key:
        raise HTTPException(status_code=500, detail="HY3_API_KEY is not configured")
    return OpenAI(
        api_key=api_key,
        base_url=settings.llm_base_url,
    )


def call_hy3(messages: list[dict[str, str]], temperature: float = 0.25) -> str:
    client = hy3_client()
    response = client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""


def is_sensitive_name(name: str) -> bool:
    name = name.lower()
    return name in SECRET_FILENAMES or (name.startswith(".env") and name != ".env.example") or name.endswith((".pem", ".key", ".p12", ".pfx"))


def should_include(path: Path) -> bool:
    name = path.name.lower()
    if is_sensitive_name(name):
        return False
    if name in IMPORTANT_NAMES:
        return True
    return path.suffix.lower() in IMPORTANT_SUFFIXES and path.stat().st_size <= 80_000


def read_text(path: Path) -> str:
    try:
        with path.open("rb") as file:
            content = file.read(80_000).decode("utf-8", errors="replace")
    except OSError:
        return ""
    return content[:MAX_FILE_CHARS]


def safe_extract_zip(archive: zipfile.ZipFile, target: Path) -> None:
    target_root = target.resolve()
    members = archive.infolist()
    if len(members) > MAX_ARCHIVE_MEMBERS:
        raise HTTPException(status_code=413, detail="Archive contains too many entries")
    if sum(member.file_size for member in members) > MAX_EXTRACTED_BYTES:
        raise HTTPException(status_code=413, detail="Archive is too large after extraction")
    for member in members:
        normalized = PurePosixPath(member.filename.replace("\\", "/"))
        parts = normalized.parts
        if normalized.is_absolute() or ".." in parts or (parts and parts[0].endswith(":")):
            raise HTTPException(status_code=400, detail=f"Unsafe zip path: {member.filename}")
        destination = (target / Path(*parts)).resolve()
        if target_root != destination and target_root not in destination.parents:
            raise HTTPException(status_code=400, detail=f"Unsafe zip path: {member.filename}")
        if any(part.lower() in SKIP_DIRS for part in parts) or is_sensitive_name(destination.name):
            continue
        if member.file_size > MAX_MEMBER_BYTES:
            raise HTTPException(status_code=413, detail=f"Archive member is too large: {member.filename}")
        if member.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(member) as source, destination.open("wb") as output:
            while chunk := source.read(1024 * 1024):
                output.write(chunk)


def summarize_directory(root: Path) -> str:
    files = [
        path for path in root.rglob("*")
        if path.is_file()
        and not any(part.lower() in SKIP_DIRS for part in path.relative_to(root).parts)
        and not is_sensitive_name(path.name)
    ]
    files.sort(key=lambda path: (path.name.lower() not in IMPORTANT_NAMES, str(path.relative_to(root)).lower()))
    tree = "\n".join(str(p.relative_to(root)).replace("\\", "/") for p in files[:180])
    parts = [f"# File Tree\n{tree}"]
    total = len(parts[0])

    for path in files:
        if not should_include(path):
            continue
        rel = str(path.relative_to(root)).replace("\\", "/")
        content = read_text(path)
        if not content:
            continue
        block = f"\n\n# File: {rel}\n```text\n{content}\n```"
        if total + len(block) > MAX_TOTAL_CHARS:
            continue
        parts.append(block)
        total += len(block)
    return "\n".join(parts)


def extract_zip(upload: UploadFile) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        archive_path = Path(tmp) / "project.zip"
        total = 0
        with archive_path.open("wb") as output:
            while chunk := upload.file.read(1024 * 1024):
                total += len(chunk)
                if total > MAX_UPLOAD_BYTES:
                    raise HTTPException(status_code=413, detail="Uploaded archive is too large")
                output.write(chunk)
        try:
            with zipfile.ZipFile(archive_path) as archive:
                safe_extract_zip(archive, Path(tmp) / "src")
        except zipfile.BadZipFile as exc:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid zip") from exc
        return summarize_directory(Path(tmp) / "src")


def bounded_log(value: str, limit: int = MAX_LOG_CHARS) -> str:
    text = value.strip()
    if len(text) <= limit:
        return text
    marker = "\n... [log truncated] ...\n"
    head = (limit - len(marker)) // 2
    return text[:head] + marker + text[-(limit - len(marker) - head):]


def analysis_context(project: str, error_log: str) -> str:
    log = bounded_log(error_log)
    suffix = f"\n\n# Error Log\n{log}" if log else ""
    return project.strip()[: MAX_TOTAL_CHARS - len(suffix)] + suffix


SYSTEM_PROMPT = """You are RepoPilot Hy3, a rigorous open-source project reproduction agent.
Your job is to help developers run unfamiliar repositories.
Ground conclusions in provided files and logs. If evidence is missing, say what to inspect next.
Return concise Markdown with practical commands, risks, and verification steps."""


@router.post("/analyze-text")
def analyze_text(payload: AnalyzeTextRequest) -> dict[str, Any]:
    context = analysis_context(payload.project_notes, payload.error_log)
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


@router.post("/analyze-zip")
def analyze_zip(file: UploadFile = File(...), error_log: str = Form(default="")) -> dict[str, Any]:
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Please upload a .zip file")
    project_context = extract_zip(file)
    context = analysis_context(project_context, error_log)
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
    return {"analysis": content, "context_preview": project_context[:18000]}


@router.post("/diagnose-error")
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
{bounded_log(payload.error_log, 18000)}""",
            },
        ]
    )
    return {"diagnosis": content}


@router.post("/generate-report")
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
