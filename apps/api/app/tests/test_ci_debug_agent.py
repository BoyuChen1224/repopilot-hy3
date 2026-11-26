import pytest

from app.services.agents.ci_debug_agent import CIDebugAgent


@pytest.mark.asyncio
async def test_ci_debug_agent_includes_failed_job_context() -> None:
    result = await CIDebugAgent().run(
        {
            "name": "backend-test",
            "status": "completed",
            "conclusion": "failure",
            "jobs": [{"name": "pytest", "conclusion": "failure", "steps": [{"name": "Run tests", "conclusion": "failure"}]}],
            "logs_text": "pytest tests/test_api.py FAILED AssertionError",
        },
        {},
    )
    assert result["failure_type"] == "test"
    assert "pytest" in result["failure_summary"]


@pytest.mark.asyncio
async def test_ci_debug_ignores_runner_permission_header_for_test_failures() -> None:
    class NoModel:
        async def chat_json(self, *_args):
            return {}

    result = await CIDebugAgent(llm=NoModel()).run(
        {
            "name": "Python checks",
            "conclusion": "failure",
            "jobs": [{"name": "unit-tests", "conclusion": "failure", "steps": []}],
            "logs_text": (
                "GITHUB_TOKEN Permissions\nContents: read\nSecret source: Actions\n"
                "FAIL: test_negative_discount_is_clamped_to_zero\n"
                "Traceback (most recent call last):\n"
                "AssertionError: 110.0 != 100.0\n"
            ),
        },
        {},
    )
    assert result["failure_type"] == "test"
    assert "AssertionError" in result["first_error"]
    assert result["is_merge_blocking"] is True


@pytest.mark.asyncio
async def test_ci_debug_still_recognizes_actual_permission_errors() -> None:
    class NoModel:
        async def chat_json(self, *_args):
            return {}

    result = await CIDebugAgent(llm=NoModel()).run(
        {"name": "publish", "conclusion": "failure", "logs_text": "PermissionError: [Errno 13] Permission denied: artifact"},
        {},
    )
    assert result["failure_type"] == "permission"
