from pathlib import Path
import secrets

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[4]
API_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROJECT_ROOT / ".data"


def _local_encryption_key() -> str:
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    key_file = DATA_ROOT / "token.key"
    try:
        with key_file.open("x", encoding="utf-8") as handle:
            value = secrets.token_urlsafe(48)
            handle.write(value)
        try:
            key_file.chmod(0o600)
        except OSError:
            pass
        return value
    except FileExistsError:
        value = key_file.read_text(encoding="utf-8").strip()
        if not value:
            raise RuntimeError("The local token encryption key is empty")
        return value


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "RepoPilot Hy3"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    database_url: str = f"sqlite:///{(DATA_ROOT / 'repopilot.db').as_posix()}"

    github_token: str | None = None
    github_api_base_url: str = "https://api.github.com"

    llm_api_key: str | None = Field(default=None, validation_alias=AliasChoices("HY3_API_KEY", "LLM_API_KEY"))
    llm_base_url: str = Field(default="https://tokenhub.tencentmaas.com/v1", validation_alias=AliasChoices("HY3_BASE_URL", "LLM_BASE_URL"))
    llm_model: str = Field(default="hy4-flash", validation_alias=AliasChoices("HY3_MODEL", "LLM_MODEL"))
    rag_llm_enabled: bool = True
    embedding_provider: str = "deterministic"
    embedding_model: str = "deterministic-demo"
    embedding_dimensions: int = 128
    embedding_api_key: str | None = None
    embedding_base_url: str | None = None
    local_embedding_model: str = "Qwen/Qwen3-Embedding-0.6B"
    local_embedding_device: str | None = None
    qwen_embedding_model: str = "Qwen/Qwen3-Embedding-0.6B"
    dashscope_api_key: str | None = None
    dashscope_embedding_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    rerank_api_key: str | None = None
    rerank_base_url: str | None = None
    qwen_rerank_model: str = Field(default="qwen3-rerank", validation_alias=AliasChoices("RERANK_MODEL", "QWEN_RERANK_MODEL"))
    rerank_instruction: str | None = None

    milvus_enabled: bool = False
    milvus_uri: str = "http://localhost:19530"
    milvus_token: str | None = None
    milvus_collection: str = "repopilot_rag"
    rag_rerank_top_n: int = 24
    ragas_enabled: bool = True
    ragas_judge_api_key: str | None = None
    ragas_judge_base_url: str | None = None
    ragas_judge_model: str | None = None
    ragas_timeout_seconds: float = 120.0
    ragas_judge_max_tokens: int = 8192
    ragas_answer_relevancy_strictness: int = 1
    ragas_max_cases: int = 5
    ragas_context_precision_min: float = 0.75
    ragas_context_recall_min: float = 0.80
    ragas_faithfulness_min: float = 0.90
    ragas_answer_relevancy_min: float = 0.80
    ragas_agent_goal_accuracy_min: float = 0.80
    ragas_tool_call_accuracy_min: float = 0.90
    ragas_tool_call_f1_min: float = 0.90
    context_max_input_tokens: int = 24000
    context_reserved_response_tokens: int = 3000
    context_dynamic_model_window_enabled: bool = True
    context_model_window_tokens: int | None = None
    context_compact_reserved_output_tokens: int = 12000
    context_auto_compact_enabled: bool = True
    context_warning_buffer_tokens: int = 20000
    context_auto_compact_buffer_tokens: int = 13000
    context_aggressive_buffer_tokens: int = 8000
    context_manual_buffer_tokens: int = 3000
    context_max_compaction_failures: int = 3
    context_microcompact_keep_recent_messages: int = 8
    context_compact_keep_recent_messages: int = 8
    context_compact_summary_tokens: int = 1800
    context_system_ratio: float = 0.12
    context_memory_ratio: float = 0.22
    context_evidence_ratio: float = 0.34
    context_recent_ratio: float = 0.22
    context_tool_ratio: float = 0.10
    workflow_task_timeout_seconds: float = 90.0
    prompt_cache_enabled: bool = False
    prompt_cache_key: str | None = "repopilot-agent-v1"
    prompt_cache_retention: str | None = None
    repo_checkout_dir: str = str(DATA_ROOT / "repos")
    upload_dir: str = str(DATA_ROOT / "uploads")

    token_encryption_key: str = Field(default_factory=_local_encryption_key)
    demo_mode: bool = False
    github_webhook_secret: str | None = None
    feishu_feedback_webhook_url: str | None = None
    feedback_trace_base_url: str | None = None
    auto_sync_enabled: bool = False
    auto_sync_interval_seconds: int = 300
    auto_sync_limit: int = 50

    model_config = SettingsConfigDict(
        env_file=(PROJECT_ROOT / ".env", API_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


settings = Settings()
