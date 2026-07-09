# RepoPilot Hy3 Submission Notes

## Issue Response Draft

RepoPilot Hy3 demonstrates Hy3 in a concrete developer productivity scenario: reproducing unfamiliar open-source repositories and diagnosing setup errors.

The application provides a FastAPI backend and a React frontend. Users can upload a project zip or paste project notes, then Hy3 generates a repository profile, setup checklist, likely run commands, risk points, and verification steps. If a terminal error is provided, Hy3 diagnoses likely root causes and produces actionable repair steps. Finally, the app can turn the analysis into a Markdown reproduction report for README, Issue, or PR workflows.

## Why This Shows Hy3 Well

- Hy3 handles mixed evidence: README text, dependency files, config files, file trees, and terminal logs.
- The task needs reasoning, not only summarization: Hy3 must infer stack, runtime, commands, risks, and fixes.
- The output is directly useful to developers and can be validated with demo repositories.
- The product is an end-to-end workflow rather than a single prompt.

## Demo Checklist

1. Start the backend with `uvicorn app.main:app --reload --port 8000`.
2. Start the frontend with `npm run dev`.
3. Upload `examples/demo-react-app.zip`.
4. Click `Analyze` and show stack detection, run commands, risks, and verification steps.
5. Paste the Python error log from `docs/demo-2-python-error.md`.
6. Click `Diagnose` and show the root cause and fix commands.
7. Click `Report` and show the Markdown reproduction report.

## Reviewer Notes

- API keys are loaded from environment variables and are not committed.
- Zip uploads are extracted with path validation to prevent unsafe archive paths.
- Model-rendered Markdown is sanitized before display in the browser.
- The repository includes English and Chinese README files, docs, sample inputs, and GitHub project-management templates.
