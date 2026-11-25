import io
import zipfile
from types import SimpleNamespace

import pytest
from fastapi import BackgroundTasks, HTTPException, UploadFile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import reproduction
from app.api.routes.repos import delete_repo, import_zip_project, register_local_project
from app.core.config import settings
from app.db.models import Base
from app.services.code_analysis import _sync_checkout
from app.services.code_search import search_checkout_code
from app.schemas.repos import RepoConnectRequest


def test_analysis_reserves_space_for_error_log(monkeypatch):
    requests = []
    monkeypatch.setattr(reproduction, "call_hy3", lambda messages, **_: requests.append(messages) or "ok")
    reproduction.analyze_text(
        reproduction.AnalyzeTextRequest(project_notes="A" * 48000, error_log="ModuleNotFoundError: requests")
    )
    assert "ModuleNotFoundError: requests" in requests[0][-1]["content"]


def test_zip_analysis_retains_log_and_larger_project_preview(monkeypatch):
    requests = []
    monkeypatch.setattr(reproduction, "call_hy3", lambda messages, **_: requests.append(messages) or "ok")
    monkeypatch.setattr(reproduction, "extract_zip", lambda _: "B" * 48000)
    result = reproduction.analyze_zip(SimpleNamespace(filename="project.zip"), "error marker")
    assert "error marker" in requests[0][-1]["content"]
    assert len(result["context_preview"]) == 18000


def test_long_error_log_retains_its_beginning_and_final_exception():
    log = "Traceback\n" + "x" * 20000 + "\nModuleNotFoundError: requests"
    bounded = reproduction.bounded_log(log)
    assert bounded.startswith("Traceback")
    assert bounded.endswith("ModuleNotFoundError: requests")
    assert len(bounded) <= reproduction.MAX_LOG_CHARS


def test_archive_rejects_path_traversal(tmp_path):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("../outside.txt", "not allowed")
    buffer.seek(0)
    with zipfile.ZipFile(buffer) as archive, pytest.raises(HTTPException) as exc:
        reproduction.safe_extract_zip(archive, tmp_path / "project")
    assert exc.value.status_code == 400
    assert not (tmp_path / "outside.txt").exists()


def test_archive_skips_dependencies_and_secrets(tmp_path):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("project/README.md", "important")
        archive.writestr("project/.env", "SECRET=hidden")
        archive.writestr("project/.env.staging.json", "SECRET=also-hidden")
        archive.writestr("project/node_modules/package/index.js", "dependency")
    buffer.seek(0)
    with zipfile.ZipFile(buffer) as archive:
        reproduction.safe_extract_zip(archive, tmp_path / "project")
    summary = reproduction.summarize_directory(tmp_path / "project")
    assert "important" in summary
    assert "SECRET=hidden" not in summary
    assert "SECRET=also-hidden" not in summary
    assert "node_modules" not in summary


def test_upload_size_limit_is_enforced(monkeypatch):
    monkeypatch.setattr(reproduction, "MAX_UPLOAD_BYTES", 4)
    upload = UploadFile(file=io.BytesIO(b"12345"), filename="project.zip")
    with pytest.raises(HTTPException) as exc:
        reproduction.extract_zip(upload)
    assert exc.value.status_code == 413


@pytest.mark.asyncio
async def test_imported_archive_is_available_to_workspace_search(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "repo_checkout_dir", str(tmp_path))
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("project/README.md", "# Imported project")
        archive.writestr("project/app.py", "def imported_handler():\n    return 42\n")
    buffer.seek(0)
    upload = UploadFile(file=buffer, filename="project.zip")
    repo = await import_zip_project(BackgroundTasks(), upload, db)
    assert repo.provider == "local_archive"
    assert _sync_checkout(repo, None).is_dir()
    matches = search_checkout_code(repo.local_path, "imported_handler")
    assert matches and matches[0]["source_id"] == "app.py"


@pytest.mark.asyncio
async def test_local_directory_does_not_require_git(tmp_path):
    (tmp_path / "app.py").write_text("def local_handler():\n    return 42\n", encoding="utf-8")
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    repo = await register_local_project(RepoConnectRequest(local_path=str(tmp_path)), BackgroundTasks(), db)
    assert repo.provider == "local_directory"
    assert _sync_checkout(repo, None) == tmp_path.resolve()
    assert search_checkout_code(repo.local_path, "local_handler")


@pytest.mark.asyncio
async def test_delete_archive_removes_only_managed_copy(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "repo_checkout_dir", str(tmp_path / "managed"))
    monkeypatch.setattr("app.api.routes.repos.delete_milvus_documents", lambda **_: False)
    original = tmp_path / "original"
    original.mkdir()
    (original / "keep.txt").write_text("keep", encoding="utf-8")
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("project/README.md", "imported")
    buffer.seek(0)
    repo = await import_zip_project(BackgroundTasks(), UploadFile(file=buffer, filename="project.zip"), db)
    managed = tmp_path / "managed" / "imports" / str(repo.id)
    result = await delete_repo(repo.id, db)
    assert result["cleanup"]["removed_import"] is True
    assert not managed.exists()
    assert (original / "keep.txt").read_text(encoding="utf-8") == "keep"
