from types import SimpleNamespace
from uuid import uuid4

import httpx
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.routes.rag import _knowledge_base, reindex_rag
from app.core.config import settings
from app.core import config as config_module
from app.db.models import Base, Document, KnowledgeBaseConfig, Repository
from app.services.rag import embeddings, knowledge_base


def test_local_token_key_is_unique_and_persistent(tmp_path, monkeypatch):
    monkeypatch.setattr(config_module, "DATA_ROOT", tmp_path)
    first = config_module._local_encryption_key()
    assert first == config_module._local_encryption_key()
    assert len(first) >= 32


def test_remote_embedding_uses_its_own_endpoint_and_key(monkeypatch):
    calls = []

    def handle(request):
        calls.append(request)
        return httpx.Response(200, json={"data": [{"index": 0, "embedding": [0.2, 0.8]}]})

    original_client = httpx.Client
    monkeypatch.setattr(settings, "embedding_base_url", "https://embedding.example/v1")
    monkeypatch.setattr(settings, "embedding_api_key", "embedding-key")
    monkeypatch.setattr(settings, "llm_api_key", "model-key")
    monkeypatch.setattr(embeddings.httpx, "Client", lambda **_: original_client(transport=httpx.MockTransport(handle)))
    result = embeddings._embed_openai_compatible(["document"], 2, model="embedding-model")
    assert result == [[0.2, 0.8]]
    assert str(calls[0].url) == "https://embedding.example/v1/embeddings"
    assert calls[0].headers["authorization"] == "Bearer embedding-key"


@pytest.mark.asyncio
async def test_remote_rerank_uses_configured_model_and_endpoint(monkeypatch):
    calls = []

    def handle(request):
        calls.append(request)
        return httpx.Response(200, json={"results": [{"index": 1, "relevance_score": 0.9}]})

    original_client = httpx.AsyncClient
    monkeypatch.setattr(settings, "rerank_base_url", "https://rerank.example/v1/rerank")
    monkeypatch.setattr(settings, "rerank_api_key", "rerank-key")
    monkeypatch.setattr(settings, "rerank_instruction", None)
    monkeypatch.setattr(knowledge_base.httpx, "AsyncClient", lambda **_: original_client(transport=httpx.MockTransport(handle)))
    results = await knowledge_base._qwen_rerank(
        "query", [{"title": "first"}, {"title": "second"}], SimpleNamespace(rerank_model="rank-model"), 1
    )
    assert results[0]["title"] == "second"
    assert results[0]["rank_reason"] == "rank-model"
    assert str(calls[0].url) == "https://rerank.example/v1/rerank"
    assert calls[0].headers["authorization"] == "Bearer rerank-key"
    assert b'"instruct"' not in calls[0].content


@pytest.mark.asyncio
async def test_reindex_adopts_changed_embedding_contract_in_local_mode(monkeypatch):
    monkeypatch.setattr(settings, "milvus_enabled", False)
    monkeypatch.setattr(settings, "embedding_provider", "deterministic")
    monkeypatch.setattr(settings, "embedding_model", "new-space")
    monkeypatch.setattr(settings, "embedding_dimensions", 128)
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = sessionmaker(bind=engine)()
    repo = Repository(owner="local", name="sample", full_name="local/sample")
    db.add(repo)
    db.flush()
    config = KnowledgeBaseConfig(repo_id=repo.id, embedding_provider="deterministic", embedding_model="old-space", embedding_dimensions=128)
    db.add_all([config, Document(repo_id=repo.id, source_type="knowledge_file", source_id=uuid4(), title="Guide", content="Project notes", meta={})])
    db.commit()
    assert _knowledge_base(db, repo).runtime["embedding"]["requires_reindex"] is True
    result = await reindex_rag(repo.id, db)
    assert result.vector_status == "degraded"
    assert result.indexed_documents == 1
    assert config.embedding_model == "new-space"
    assert _knowledge_base(db, repo).runtime["embedding"]["requires_reindex"] is False
