from uuid import UUID

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.routes import action_drafts
from app.db.models import ActionDraft, Base, Issue, Repository, User
from app.db.session import get_db


def test_label_confirmation_serializes_results_and_preserves_existing_records(monkeypatch):
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    db = sessions()
    repo = Repository(owner="owner", name="test", full_name="owner/test")
    user = User(name="owner", role="owner")
    db.add_all([repo, user])
    db.flush()
    issue = Issue(repo_id=repo.id, number=1, title="Boundary test", state="open")
    db.add(issue)
    db.commit()
    repo_id, issue_id = str(repo.id), str(issue.id)
    db.close()

    calls = []

    async def fake_execute(_db, draft, _repo):
        calls.append(draft.id)
        return [{"name": "repopilot-tested"}]

    monkeypatch.setattr(action_drafts, "_execute_github_draft", fake_execute)
    app = FastAPI()
    app.include_router(action_drafts.router, prefix="/api/action-drafts")

    def override_db():
        session = sessions()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as client:
        created = client.post(
            "/api/action-drafts",
            json={
                "repo_id": repo_id,
                "draft_type": "add_labels",
                "target_type": "issue",
                "target_id": issue_id,
                "title": "repopilot-tested",
                "content": "Test label",
            },
        )
        assert created.status_code == 200
        draft_id = created.json()["id"]
        assert created.json()["status"] == "pending_confirmation"

        confirmed = client.post(f"/api/action-drafts/{draft_id}/confirm")
        assert confirmed.status_code == 200
        assert confirmed.json()["draft"]["status"] == "executed"
        assert confirmed.json()["draft"]["execution_result"] == {"result": [{"name": "repopilot-tested"}]}
        assert confirmed.json()["audit_id"]
        assert client.post(f"/api/action-drafts/{draft_id}/confirm").status_code == 400
        assert len(calls) == 1

        db = sessions()
        db.get(ActionDraft, UUID(draft_id)).execution_result = [{"name": "older-label"}]
        db.commit()
        db.close()
        existing = client.get(f"/api/action-drafts/{draft_id}")
        assert existing.status_code == 200
        assert existing.json()["execution_result"] == {"result": [{"name": "older-label"}]}
        assert client.get("/api/action-drafts").status_code == 200

    engine.dispose()
